# Year 8 Japanese · Study app

A single, self-contained `index.html` (no build step, no dependencies) that fetches `vocab.json`,
`kanji.json` and `structures.json` and turns them into a study app.

## Use it

**GitHub Pages:** `index.html` sits at the repository root, so *Settings → Pages → Deploy from a
branch → `main` / `(root)`* is all that is needed.

**Locally:** browsers block `fetch()` on `file://` pages, so serve the folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Keep `index.html`, `vocab.json`, `kanji.json` and `structures.json` together.

## What it does

- **Browse** 480 vocabulary pairs (search, Japanese text-to-speech), 68 kanji (on/kun readings, the
  words each appears in, notes and sources) and 76 grammar patterns (examples, variants, formation
  notes).
- **Study** any deck with multiple-choice quizzes or flashcards, filtered to due + new cards, new
  cards, tricky cards or everything.
- **Sentence mode** builds real sentences by filling grammar patterns with vocabulary of the right
  type — adjectives with the nouns they suit, foods with eating/ordering patterns, places with
  existence patterns, numbers with prices and ages. Each answer shows the full sentence, its
  English meaning and the grammar rule it practises.
- **Scheduled review**: correct answers move a word up at 1, 2, 4 then 7-day intervals; a missed
  card returns tomorrow. Progress, accuracy and streaks are saved in `localStorage` only.
- Keyboard shortcuts (number keys, Enter, Space, arrows), light/dark theme, phone-friendly layout.

## Vocabulary metadata

`vocab.json` keeps every original `{"English": "日本語"}` pair untouched. Entries also carry a few
`$`-prefixed study keys used by sentence mode:

```json
{ "Cat": "ねこ", "$type": "animal" },
{ "Australia": "オーストラリア", "$type": "country", "$nat": "Australian" },
{ "Piano": "ピアノ", "$type": "instrument", "$play": "ひきます" },
{ "Three hundred": "さんびゃく", "$type": "number", "$num": 300 }
```

| key | meaning |
| --- | --- |
| `$type` | semantic class: `animal`, `person`, `family`, `food`, `drink`, `place`, `activity`, `sport`, `instrument`, `song`, `thing`, `adj_i`, `adj_na`, `colour_noun`, `colour_adj`, `verb`, `preference`, `country`, `language`, `day`, `day_relative`, `time`, `number`, `age`, `counter_people`, `event`, `locality`, `money_unit`, `question` |
| `$en` | optional natural English used inside sentences |
| `$nat` | demonym for countries (“Australian”) |
| `$play` | which verb an instrument takes (ひきます / ふきます / たたきます) |
| `$num` | numeric value for numbers, prices and ages |

Entries that are set phrases, particles or classroom language (86 of them) have no `$type` and are
simply left out of generated sentences.

The tagging is reproducible — edit `tools/add_vocab_metadata.py`, then run:

```bash
python3 tools/add_vocab_metadata.py
```

The script rewrites `vocab.json` in a stable format and asserts the English/Japanese pairs are
unchanged before writing.
