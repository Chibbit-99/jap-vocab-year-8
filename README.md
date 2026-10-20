# Year 8 Japanese · Study companion

A self-contained study app for the vocabulary, kanji and grammar in this repository. It is a single
`index.html` (no build step, no dependencies) that fetches the three JSON files next to it.

## Use it

**GitHub Pages:** open the published site — `index.html` sits at the repository root, so
*Settings → Pages → Deploy from a branch → `main` / `(root)`* is all that is needed.

**Locally:** browsers block `fetch()` on `file://` pages, so serve the folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

`index.html`, `vocab.json`, `kanji.json` and `structures.json` must stay in the same folder.

## What it does

- **Browse** all 480 vocabulary pairs (searchable, with Japanese text-to-speech), 68 kanji
  (readings, words they appear in, sources and notes) and 76 grammar patterns (examples, variants
  and formation notes).
- **Study** with multiple-choice quizzes or flip-and-grade flashcards, filtered by deck, by
  smart review, new cards, tricky cards or everything.
- **Smart review** schedules cards at 1, 2, 4 and 7-day intervals; a missed card comes back
  tomorrow. Due cards are prioritised, then new material fills the session.
- **Track progress** — mastery, quiz accuracy, daily reviews and streaks are stored in
  `localStorage` on the device. Nothing is sent anywhere.
- Light/dark theme, keyboard shortcuts, and a responsive layout for phones.

The JSON files are the source of truth and are not modified by the app.
