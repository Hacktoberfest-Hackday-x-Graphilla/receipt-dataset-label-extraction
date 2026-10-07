# PROJECT — Receipt Dataset & Label Extraction

> **Project status: Initial scaffold.** This is the shared plan; nothing is implemented yet.

## Vision

Build a **clean, human-verified, privacy-safe receipt dataset** with structured labels — a foundation that future OCR and AI extraction pipelines can be trained and evaluated against.

## Goals

1. Collect receipt images from willing, legitimate sources.
2. Annotate them with a consistent label schema.
3. Validate annotations so `dataset/annotations/validated/` is trustworthy ground truth.
4. Later: build extraction pipelines and measure them against that ground truth.

## Non-goals (for now)

- No OCR, CV, ML, or annotation tooling at scaffold stage.
- No real personal data in the repository.
- No automatic scraping of private data.

## Proposed roadmap

| Phase | Description | Status |
|---|---|---|
| 0 | Repository scaffold and guidelines | ✅ Done |
| 1 | Finalize label schema | Planned |
| 2 | First small batch of privacy-checked images + labels | Planned |
| 3 | Validation process + reviewer checklist | Planned |
| 4 | Preprocessing pipeline | To be implemented |
| 5 | Baseline OCR/extraction + evaluation harness | Future |

## Hack Day Contribution Ideas

> Ideas only — none of these are implemented.

### Beginner
- Submit a few privacy-checked receipt images following `DATA_GUIDELINES.md`.
- Annotate one image against the draft schema and report confusing fields in an issue.
- Improve documentation: clarity, examples, typo fixes.
- Help draft the label schema field definitions in `docs/label-schema.md`.

### Intermediate
- Define the annotation JSON schema in `dataset/annotations/schemas/`.
- Write a validation checklist (required fields, ranges, date formats) in `docs/dataset-quality.md`.
- Propose a preprocessing spec: deskew, denoise, resize, redaction.
- Design an inter-annotator agreement process for double annotation.

### Advanced
- Build the image preprocessing pipeline with tests (`src/preprocessing/`).
- Create an evaluation harness comparing extracted fields to validated labels (`src/evaluation/`).
- Research OCR/extraction approaches suited to thermal-print and crumpled receipts.
- Design the dataset versioning and release process (splits, licenses, changelogs).

## Related documents

- [`DATA_GUIDELINES.md`](DATA_GUIDELINES.md) — what images are accepted
- [`ANNOTATION_GUIDELINES.md`](ANNOTATION_GUIDELINES.md) — how to label
- [`docs/`](docs/) — annotation process, label schema, dataset quality
