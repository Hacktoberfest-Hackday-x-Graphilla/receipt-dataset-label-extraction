# Annotation Guidelines

> **Project status: Initial scaffold.** These are *proposed* annotation rules. The formal schema is still being drafted in `docs/label-schema.md`.

## Golden rule

**Label what you see, not what you assume.** If a field is unreadable, missing, or ambiguous, use the designated "unreadable"/`null` value — never guess.

## Proposed workflow (future)

1. Pick an unlabeled image from `dataset/images/raw/`.
2. Fill the label fields for that image (see below).
3. Save the annotation to `dataset/annotations/raw/`.
4. A **different** reviewer validates it → `dataset/annotations/validated/`.

Raw annotations are never treated as ground truth.

## Field-by-field guidance (draft)

| Field | Rule |
|---|---|
| `merchant` | Exact printed name; transliterate only if unreadable script |
| `date` | ISO `YYYY-MM-DD`; if only partial (no year), mark partial |
| `total` | The **final** amount paid — not subtotal |
| `subtotal` | Pre-tax amount; `null` if not printed |
| `tax` | Sum of tax lines; list separately if multiple rates |
| `currency` | Infer from symbol/context only if unambiguous |
| `receipt_number` | As printed; `null` if absent |
| `items` | One entry per printed line item: description, qty, unit price, amount |

## Edge cases to flag (not fudge)

- Discounts, tips, service charges
- Multi-tax receipts (VAT + other)
- Handwritten additions
- Cropped or partially visible receipts
- Non-standard layouts (thermal roll, two-column)

## Validation criteria (draft)

A reviewer accepts an annotation when:

- [ ] All required fields present (or explicitly `null`/`unreadable`)
- [ ] `total` = printed final amount
- [ ] Numbers match the image exactly
- [ ] No invented content
- [ ] Image passes the privacy checklist in `DATA_GUIDELINES.md`

## Anti-bias notes

- Annotate independently before comparing with others on hard cases.
- Record disagreement rather than silently overwriting.
- A future inter-annotator agreement process is proposed in `docs/dataset-quality.md`.
