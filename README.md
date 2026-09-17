# CivicMill

The Saturday Board: a noticeboard, a lot of coloured sticky notes, and a real
decision from the Wisconsin State Capitol put to passers-by at the Dane County
Farmers' Market in Madison. A project of [Sortition USA](https://sortitionusa.org/).

**Website:** https://cjforman.github.io/CivicMill/

## What is here

| Folder | What it holds |
|---|---|
| [`CivicMillBoard.html`](CivicMillBoard.html) | The board tool. Turns a photograph of a finished board into data you can score and share. |
| [`guides/`](guides/) | How to run a board: the field guide, the steward's guide, and the steward's log (tally sheets). Each as a printable HTML page and a PDF. |
| [`dockets/`](dockets/) | The questions. [`madison/madison-docket.md`](dockets/madison/madison-docket.md) lists the issue cards; each background brief is published in its event folder after the board has been run. |
| [`events/`](events/) | One folder per board run, named `YYYY-MM-DD-place-issue`: the report, the background brief, the board data (`board.json` opens in the tool), and photographs. |
| [`assets/`](assets/) | Sortition USA logos. |
| [`tools/`](tools/) | `build_page.py`, which turns a report, brief or docket from Markdown into its printable HTML page. |

Markdown is the source of truth for every report, brief and docket. After
editing one, rebuild its page from the repository root (Python 3, standard
library only):

```bash
python tools/build_page.py events/2026-09-05-madison-foxconn/report.md
```

The guides are hand-written HTML with a Markdown copy beside them; keep the
two in step.

### Adding an event

1. Create `events/YYYY-MM-DD-place-issue/` with `report.md`, `brief.md`,
   `board.json`, and `photos/`. Remove location data from photographs and blur
   anything a passer-by wrote on a sign-up sheet before committing.
2. Build the pages with `tools/build_page.py`, and print each to PDF.
3. In the docket, mark the issue as run and link its report and brief.
4. Add the event to [`index.html`](index.html).

## The board tool

[`CivicMillBoard.html`](CivicMillBoard.html) is a single HTML file: no server,
no account, nothing to install. Open it in a browser, or use it online at
https://cjforman.github.io/CivicMill/CivicMillBoard.html.

### What it records

- **Notes** on two rows: the Wall of Why (what is wrong) and Solutions (what to
  do about it).
- **Stacks.** A note placed on top of another is agreement, so each note
  records how many sheets were piled on that spot.
- **Colonies.** Related notes filed side by side. These are worked out from
  where the notes sit; you can also name them.
- **Votes against**, marks of approval, readings you could not make out, and a
  comment on any note.

### How the score works

The winner is not simply the tallest stack. Each note scores its own stack
plus the stacks immediately to its left and right, and nothing counts across
a gap between colonies. An idea in the middle of a busy colony therefore
outscores the same idea standing alone. A tall stack with nothing beside it
does not win.

This favours ideas that hold up when they are rephrased: if the people around
an idea were reaching for the same thing in different words, it is robust.

### Using it

1. **Open** a saved board, or **Load photo board** to see an example from the
   Dane County Farmers' Market in Madison.
2. Drag notes to where they sat. Double-click to edit text. Shift-click several
   notes and press **Group** to name a colony.
3. Press **Compute scores from layout**. Each note shows its score; the winner
   is marked in red.
4. **Save** writes the board to a `.json` file. In Chrome and Edge it keeps
   saving to that file as you work, and reopens it next time.
5. **Export CSV** for analysis, or **Share…** for a single HTML file with your
   board built in.

**Trace photo** puts a photograph of the real board behind the canvas so you
can place notes accurately.

## Licence

The board tool and `tools/` are MIT-licensed ([LICENSE](LICENSE)). The guides,
dockets, reports, photographs and board data are CC BY 4.0
([LICENSE-docs.md](LICENSE-docs.md)). The Sortition USA logos are not covered
by either.
