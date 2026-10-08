# Receipt Dataset & Label Extraction

Collect **receipt images** and the **labels** extracted from them (merchant, date, total, items…) as an open, human-verified dataset. A future OCR / AI extraction model can be trained and tested against it.

**Status: just started.** The label suggester works; the dataset is what contributors build.

## Try it

```bash
pip install -r requirements.txt
```

Then copy `.env.example` to `.env` and put your Google AI Studio API key in `GEMINI_API_KEY`. `.env` is gitignored, so the key never leaves your machine.

Drop receipt files (PDF, JPG, PNG, WEBP) into `dataset/receipts/` and run:

```bash
python -m src.extraction.suggest_labels
```

For every receipt the script writes one `<name>.label.json` **next to it** — the label fields suggested by a Gemma model. Receipts that already have a suggestion are skipped, so re-running is safe.

How each receipt is read:

- **JPG / PNG / WEBP** → the image is sent to the model and read by vision.
- **PDF with a text layer** → the text is sent to the model.
- **Scanned PDF (image only, e.g. a phone photo)** → the page images are sent to the model and read by vision. No local OCR / Tesseract needed.

## The suggested label for one receipt

| Field | Meaning |
|---|---|
| `merchant` | store / business name |
| `date` | ISO date (`YYYY-MM-DD`) |
| `currency` | 3-letter code (NPR, USD, INR…) |
| `subtotal` / `tax` / `total` | amounts (plain numbers) |
| `receipt_number` | printed bill / receipt / invoice number |
| `receipt_type` | grocery, restaurant, retail, fuel, utility, travel, other |
| `language` | main language of the receipt (en, ne, hi…) |
| `items` | list of `{description, quantity, unit_price, amount}` |

Unreadable or missing values are `null` — never invented. See [`examples/example-label.json`](examples/example-label.json).

**Machine suggestions are not data yet.** Review each `.label.json`, fix it if needed, then move it into `dataset/labels/` so it counts. The dataset is the human-verified labels, not the suggestions.

## Contribute — 3 steps, no coding

1. Open the **Issues** tab.
2. Pick any issue labelled `beginner` or `good first issue`.
3. Comment **"I'll take this"** and follow the lines in the issue — a comment is enough.

Ideas: submit a privacy-checked receipt photo, review a suggested label, or improve the docs. Stuck? Post in **Discussions** — no question is dumb.

## Data rules (keep it honest)

- **Real receipts only** — you can stand behind every label you contribute.
- **No personal data** — redact or avoid card numbers, names, addresses, phone numbers, loyalty IDs. Never submit someone else's sensitive information.
- **No fabrication** — never invent values. Unreadable field? Write `null`.
- **Rights** — only share material you have the right to redistribute.

## Layout

```text
dataset/receipts/      drop receipt files here (gitignored)
dataset/labels/        human-verified labels (the dataset — contribute here)
examples/              example label (clearly marked EXAMPLE)
src/extraction/        the label suggester script
tests/                 tests
.env.example           template for your local, gitignored .env
```

## License

Code: [MIT](LICENSE). Contributed data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).