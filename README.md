# CivicMill

Tools for running and reading public deliberation boards: a noticeboard, a lot
of coloured sticky notes, and a question put to passers-by.

## CivicMill Board

[`CivicMillBoard.html`](CivicMillBoard.html) turns a photograph of a finished
board into data you can score and share. It is a single HTML file: no server,
no account, nothing to install. Open it in a browser.

**Use it online:** https://cjforman.github.io/CivicMill/

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

---

Developed by [Sortition USA](https://sortitionusa.org/).
