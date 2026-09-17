"""Print HTML pages to PDF through headless Microsoft Edge.

    python tools/print_pdf.py guides/field-guide.html events/*/report.html

Each PDF is written beside its page. Pages print with their own @page size
and backgrounds, and no browser header or footer. If anything is wider than
the paper (the steward's log tally table, for one), the page is scaled down
just enough to fit, the way the print dialog's fit-to-width does. A page whose
CSS asks for `size: landscape` is measured at landscape width.

Needs Edge and the `websocket-client` package.
"""
import base64
import json
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9333
# CSS px of printable width on US Letter: portrait 8.5in, landscape 11in, less margins
PORTRAIT_PX, LANDSCAPE_PX = 739, 989


class DevTools:
    def __init__(self, url):
        self.ws = websocket.create_connection(url, timeout=60, suppress_origin=True)
        self.n = 0

    def call(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg["result"]


def main():
    pages = [Path(p).resolve() for p in sys.argv[1:]]
    if not pages:
        sys.exit(__doc__)
    profile = tempfile.mkdtemp(prefix="civicmill-print-")
    edge = subprocess.Popen(
        [EDGE, "--headless=new", "--disable-gpu", f"--remote-debugging-port={PORT}",
         f"--user-data-dir={profile}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        target = None
        for _ in range(100):
            try:
                targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
                target = next(t for t in targets if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.2)
        if target is None:
            sys.exit("could not reach headless Edge")
        dt = DevTools(target["webSocketDebuggerUrl"])
        dt.call("Page.enable")
        dt.call("Emulation.setEmulatedMedia", media="print")
        for page in pages:
            landscape = bool(re.search(r"size\s*:\s*landscape", page.read_text(encoding="utf-8")))
            width = LANDSCAPE_PX if landscape else PORTRAIT_PX
            dt.call("Emulation.setDeviceMetricsOverride", width=width, height=900,
                    deviceScaleFactor=1, mobile=False)
            dt.call("Page.navigate", url=page.as_uri())
            time.sleep(3.5)          # load, web fonts, and any fit-the-title script
            view, content = dt.call("Runtime.evaluate", returnByValue=True, expression="""(() => {
                let widest = document.documentElement.scrollWidth;
                document.querySelectorAll('table, pre').forEach(e => widest = Math.max(widest, e.scrollWidth));
                return [document.documentElement.clientWidth, widest];
            })()""")["result"]["value"]
            scale = 1.0 if content <= view + 1 else round(max(0.5, view / content) - 0.005, 3)
            pdf = dt.call("Page.printToPDF", printBackground=True, preferCSSPageSize=True,
                          displayHeaderFooter=False, scale=scale)
            out = page.with_suffix(".pdf")
            out.write_bytes(base64.b64decode(pdf["data"]))
            print(f"wrote {out.name}  (scale {scale})")
        dt.ws.close()
    finally:
        edge.terminate()


if __name__ == "__main__":
    main()
