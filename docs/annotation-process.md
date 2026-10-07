# Annotation Process

> **Project status: Initial scaffold.** This is the proposed end-to-end process; no annotation has started and no tooling exists.

## Overview

```text
image (raw)  →  annotate  →  annotation (raw)  →  review  →  annotation (validated)
                                                        ↘ rejected → back to annotate
```

## Stages

### 1. Intake
- Image passes the privacy + quality checklist in `DATA_GUIDELINES.md`.
- Metadata entry created in `dataset/metadata/`.

### 2. Annotation
- An annotator fills every field in the draft schema (`docs/label-schema.md`).
- Unreadable/absent values use `null` / `unreadable` — never guessed.
- Saved to `dataset/annotations/raw/`.

### 3. Validation (review)
- A second person checks against `ANNOTATION_GUIDELINES.md`.
- Pass → `dataset/annotations/validated/`.
- Fail → returned with notes; fix and resubmit.

### 4. Agreement (future, proposed)
- For a sample of items, double-annotate independently and measure agreement.
- Disagreements are documented, not averaged away.

## Roles

| Role | Responsibility |
|---|---|
| Contributor | Supplies privacy-checked images |
| Annotator | Fills labels |
| Reviewer | Validates labels; moves to `validated/` |
| Maintainer | Resolves schema questions, releases versions |

## Open questions

- Annotation format (JSON per image vs. JSONL per batch)?
- Tooling: manual text files first, tool-assisted later?
- Minimum review coverage (100% vs. sampled)?

## To be implemented

Annotation templates, validation checks, and any tooling will be added under `src/annotation/` in a future phase.
