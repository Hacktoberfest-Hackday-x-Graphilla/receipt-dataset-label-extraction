# Contributing

Thank you for helping build a high-quality receipt dataset! This repository is an **initial scaffold** — read the guidelines before contributing.

**Never contributed before? No coding needed** — collecting and labeling receipts is data work anyone can do. There's a plain-language guide in [`docs/how-to-contribute.md`](docs/how-to-contribute.md) — you can do almost everything from the GitHub website.

## Two contribution tracks

1. **Data contributors** — collect, classify, annotate, and validate receipt data.
2. **Developers** — eventually build preprocessing, OCR/extraction, and evaluation pipelines.

Both tracks are described in [`PROJECT.md`](PROJECT.md).

## Ground rules

1. **Privacy first.** Never submit receipts with visible personal data (card numbers, names, addresses). Redact before submitting. See `DATA_GUIDELINES.md`.
2. **No fabricated labels.** Labels must reflect what is actually on the image. If unreadable, mark it `unreadable` — never guess.
3. **Validate before trusting.** Raw annotations go through the validation stage; do not move files into `validated/` yourself unless you are a reviewer following `ANNOTATION_GUIDELINES.md`.
4. **No stub code.** Code lands only when it works with tests; no placeholder scripts.
5. **No secrets.** Never commit API keys or tokens.

## Workflow

1. Fork and branch from `main`.
2. Follow `DATA_GUIDELINES.md` (images) or `ANNOTATION_GUIDELINES.md` (labels).
3. Open a pull request describing the source and count of contributions.
4. A reviewer checks privacy, quality, and format before merge.

## Commit message style

Conventional Commits: `data:`, `docs:`, `feat:`, `chore:`.

## Reporting issues

Use templates in `.github/ISSUE_TEMPLATE/`. Suggested labels: `data`, `annotation`, `tooling`, `docs`.

## Conduct

Be respectful and constructive. Prepared for Hacktoberfest Hack Day Bhairahawa 2026 × Graphilla Technology.
