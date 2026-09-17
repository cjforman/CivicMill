# CivicMill — house rules

CivicMill is a Sortition USA project: the **Saturday Board**, a public
deliberation stall at the Dane County Farmers' Market in Madison. Visitors say
what worries them about a real decision the Wisconsin Capitol has already
taken, post a first idea, file it beside the ideas most like it, and trim the
ones that would make other people's problems worse. At the end of the day the
board's answer is compared with what the Capitol did.

This repository is public, and so is its website (GitHub Pages,
https://cjforman.github.io/CivicMill/). Treat every commit as publication.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Landing page. Every guide, docket and event is listed here. |
| `CivicMillBoard.html` | The board tool: one self-contained HTML file, no build, no dependencies. Its URL is shared, so it never moves. |
| `guides/` | Field guide, steward's guide, steward's log. Hand-written HTML with a Markdown copy beside it, plus a PDF. |
| `dockets/<city>/` | The questions. The public docket shows **issue cards only**. |
| `events/YYYY-MM-DD-place-issue/` | One board run: `report.md`, `brief.md`, `board.json` (opens in the tool), `board-raw-transcription.json`, `photos/`, and the built `.html`/`.pdf`. |
| `assets/` | Sortition USA logos. Not covered by the CC licence. |
| `tools/build_page.py` | Markdown → printable HTML for reports, briefs and dockets (stdlib only). |
| `tools/print_pdf.py` | HTML → PDF through headless Edge, fitting wide tables to the page. |

Licences: code (`CivicMillBoard.html`, `tools/`) is MIT; guides, dockets,
events, photographs and data are CC BY 4.0 (`LICENSE-docs.md`). `.nojekyll`
must stay, or Pages renders `report.md` over `report.html`.

## Sources of truth

- **Reports, briefs, dockets:** the `.md` is the source. Never hand-edit the
  built `.html`. After any edit, rebuild with
  `python tools/build_page.py <file.md> ...` from the repo root, then reprint
  the PDF with `python tools/print_pdf.py <file.html> ...`.
- **Guides:** the `.html` is hand-written. Change the `.md` and `.html`
  together, then reprint the PDF.
- **The board tool:** scores come from the board document, never from reading
  the DOM back. Any change to scoring must leave saved `board.json` files
  opening and scoring unchanged.

## Rules about content

1. **How the method is described.** The method's origin is described only
   as: *"a method we devised using our general knowledge of deliberative
   processes and common sense."* Do not add theory, formal models, or
   explanations of why the rules produce good answers beyond the
   plain-language "Why the odd rules?" section of the field guide. If a draft
   seems to need more, ask the owner.
2. **Nothing before its Saturday.** The public docket shows the issue card
   only. An issue's background brief (what the Capitol did, who held power,
   what happened since) is published in its event folder **after** that
   issue has been run, never before, because visitors may read the site
   first. Never publish expected outcomes or which issues are "controls".
   The owner supplies each brief. Don't write one from memory.
3. **Photographs.** Publish crops of the board only. Before committing, strip
   all metadata (EXIF/XMP) and blur anything a passer-by wrote, such as the
   mailing-list sign-up sheet. No identifiable visitors or bystanders.
4. **Board data is a record.** Transcriptions describe what was on the board.
   Don't tidy, reword or regroup notes in `board-raw-transcription.json`.
   Make judgement calls in `board.json` and say so in the report.
5. **The owner's prose is the owner's.** Reports are written by the owner in
   plain spoken language. Fix what you're asked to fix. Don't rewrite voice,
   add methodology, or use "it's not X, it's Y" constructions.

## Adding an event

1. `events/YYYY-MM-DD-place-issue/` with `report.md`, `board.json`,
   `board-raw-transcription.json`, `photos/` (cleaned as above), and
   `brief.md` once the owner releases it.
2. Build the HTML and print the PDFs.
3. In the docket, mark the issue **Run** and link its report and brief.
4. Add the event to `index.html` under "Boards we have run".
5. Check that every local link resolves before committing.

## Working practice

- **Never work in the desktop app's preview pane.** It serves files as `data:`
  URLs: localStorage, the File System Access API and
  `alert`/`confirm`/`prompt` are disabled, and it reloads on every edit (which
  once destroyed the owner's board layout). Open pages in a real browser.
- **No feature may depend on a browser dialog.** A suppressed `confirm()`
  returns false and silently kills the button. Use in-page UI.
- **Check visibility with computed style,** not the `hidden` property.
- **Don't redesign what wasn't asked.** A question about how something works
  is a question, not a request to change it. Read the guides before touching
  a rule or the scoring.
- iPhone photos carry an EXIF rotation. Apply it before cropping.
- Pages must work at phone width (16 px gutters, no sideways scroll) and print
  cleanly.
- Commit or push only when the owner asks. Pushing publishes the website.
