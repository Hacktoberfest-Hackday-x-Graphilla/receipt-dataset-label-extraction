# Data Guidelines

> **Project status: Initial scaffold.** These are the *proposed* rules for contributing receipt images. No dataset exists yet.

## Principles

1. **Consent & legality** — only submit receipts you are allowed to share (your own, or explicitly permitted).
2. **Privacy** — no personal/sensitive data visible in the image.
3. **Originality** — submit the image as-is; note any preprocessing already applied.
4. **Provenance** — record where each image came from.

## Directory stages

| Directory | Purpose |
|---|---|
| `dataset/images/raw/` | Original receipt images, unmodified |
| `dataset/images/processed/` | Derived versions (deskewed, resized, redacted) — *future* |
| `dataset/metadata/` | Index describing every image |

## Privacy checklist (before submitting an image)

- [ ] No full card numbers or bank details
- [ ] No personal names, phone numbers, or addresses (yours or others')
- [ ] No loyalty/ID barcodes tied to a person
- [ ] No handwritten signatures

If any appear, **redact the image first** (solid, non-reversible redaction) or do not submit it.

## Proposed naming convention

```text
{yyyy-mm-dd}_{merchant-slug}_{seq}.{ext}
```

Example: `2026-09-12_example-store_001.jpg`

Exact conventions will be finalized in `docs/dataset-quality.md`.

## Proposed per-image metadata

- `id`, `file_path`, `source` (how obtained), `receipt_type` (grocery/restaurant/…)
- `language`, `currency`
- `license_notes`, `contributed_by`, `added_at`
- `privacy_checked` (must be `true`)

## Quality expectations

- Receipt fully in frame and legible
- Reasonable resolution (no blurry, unreadable text)
- Duplicates avoided — check `dataset/metadata/` first

## Not accepted

- Images of other people's sensitive data
- Fabricated or AI-generated receipts presented as real
- Screenshots containing payment credentials
