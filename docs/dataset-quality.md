# Dataset Quality

> **Project status: Initial scaffold.** No dataset exists yet — this page defines the *planned* quality standards.

## Quality dimensions

| Dimension | Meaning | How it will be measured (planned) |
|---|---|---|
| **Completeness** | Required fields filled or explicitly null | Automated field checks |
| **Accuracy** | Labels match the image | Human review, sampled audits |
| **Consistency** | Same conventions across annotators | Inter-annotator agreement |
| **Legibility** | Image is readable | Intake checklist |
| **Privacy** | No personal data present | Privacy checklist + review |
| **Diversity** | Range of receipt types, layouts, quality | Metadata statistics |

## Planned checks (to be implemented)

- Schema validation: types, required fields, amount arithmetic (`subtotal + tax ≈ total` where present)
- Uniqueness: no duplicate images or `receipt_id`s
- Privacy flag: `privacy_checked = true` for every entry
- Split hygiene: no receipt appears in more than one dataset split (future)

## Review policy (proposed)

- 100% review for the first batches while the schema stabilizes.
- Later: full review for new contributions + sampled audits of older ones.
- Rejected items are corrected and resubmitted, never quietly deleted.

## Versioning (future)

- Dataset releases tagged (e.g. `v0.1`) with a changelog.
- Every release reports: image count, validation coverage, field fill rates.

## Reporting

Quality statistics will eventually live in `dataset/metadata/`. Until then, raise gaps as issues labelled `quality`.
