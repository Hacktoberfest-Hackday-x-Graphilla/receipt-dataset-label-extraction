# Receipt Dataset & Label Extraction

> **Project status: Initial scaffold**
> No OCR, computer vision, AI extraction, dataset processing, or annotation tooling exists yet. Everything below is planned or proposed.

## Purpose

A dataset-oriented project focused on **collecting receipt images** and preparing **structured labels** that can later be used for OCR, document understanding, computer vision, and AI information extraction.

Good extraction models need clean, well-labeled receipt data — that dataset is the deliverable of this repository first; pipelines come later.

## What receipt data is being collected

- Photographs and scans of receipts (grocery, restaurant, retail, fuel, utility…)
- Each image paired with a human-verified label set
- Provenance and quality metadata for every item

## Intended dataset fields (planned)

| Field | Example |
|---|---|
| `merchant` | "Store Name" |
| `date` | `2026-09-12` |
| `total` | `1250.00` |
| `subtotal` | `1157.14` |
| `tax` | `92.86` |
| `currency` | `NPR` |
| `receipt_number` | `INV-0042` |
| `items` | list of {description, quantity, unit_price, amount} |

Field definitions live in `docs/label-schema.md` (proposed).

## Data / annotation workflow (proposed)

```text
collect → dataset/images/raw/ → preprocess (planned) → annotate
→ dataset/annotations/raw/ → validate → dataset/annotations/validated/
→ dataset/metadata/ index
```

Human validation is a required stage — raw annotations are never treated as ground truth. Details: `ANNOTATION_GUIDELINES.md` and `docs/annotation-process.md`.

## Potential future OCR & AI extraction (not built)

- OCR over receipt images
- Field extraction models (merchant/date/total/items)
- Evaluation harness comparing model output to validated labels
- Error analysis by receipt type, quality, and layout

## Privacy considerations

- **Redact or avoid** personal data: card numbers, names, addresses, phone numbers, loyalty IDs.
- Prefer receipts you have the right to share; note restrictions in metadata.
- Do not submit receipts containing another person's sensitive information.

## Hack Day contribution paths

See [`PROJECT.md`](PROJECT.md) for beginner / intermediate / advanced ideas — both data contributors and developers are welcome.

## Current status: initial scaffold only

- ✅ Structure and guidelines documentation
- ❌ No dataset collected yet
- ❌ No OCR/CV/AI/annotation tooling

## Repository layout

```text
dataset/images/       raw + processed images (empty)
dataset/annotations/  raw, validated, schemas (empty)
dataset/metadata/     dataset index (empty)
docs/                 annotation process, label schema, quality
examples/             example records (planned)
src/                  preprocessing/annotation/extraction/evaluation (planned)
tests/                tests for future tooling
.github/              issue templates and CI (planned)
```
