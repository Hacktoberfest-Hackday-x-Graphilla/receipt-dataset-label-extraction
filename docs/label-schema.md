# Label Schema

> **Project status: Initial scaffold.** The schema below is **draft/proposed** and will be finalized in `dataset/annotations/schemas/`. It is not yet enforced by any tooling.

## Draft: one annotation record per receipt image

```json
{
  "receipt_id": "2026-09-12_example-store_001",
  "image": "dataset/images/raw/2026-09-12_example-store_001.jpg",
  "merchant": "EXAMPLE STORE",
  "date": "2026-09-12",
  "currency": "NPR",
  "subtotal": 1157.14,
  "tax": 92.86,
  "total": 1250.00,
  "receipt_number": "INV-0042",
  "items": [
    {
      "description": "EXAMPLE ITEM",
      "quantity": 2,
      "unit_price": 578.57,
      "amount": 1157.14
    }
  ],
  "receipt_type": "grocery",
  "language": "ne",
  "annotation": { "status": "draft", "annotated_by": "", "reviewed_by": "" }
}
```

*Illustrative example only — not a real receipt, not an enforced schema.*

## Field types (draft)

| Field | Type | Required | Notes |
|---|---|---|---|
| `receipt_id` | string | yes | Matches naming convention |
| `merchant` | string | yes | Printed name; `null` if unreadable |
| `date` | date (ISO) or `partial_date` | yes | Never invent missing parts |
| `currency` | string (ISO 4217) | yes | Only if unambiguous |
| `subtotal` | number \| null | no | `null` if not printed |
| `tax` | number \| null | no | |
| `total` | number \| null | yes | Final amount paid |
| `receipt_number` | string \| null | no | |
| `items` | array | no | May be empty if unreadable |
| `status` | `draft` \| `validated` \| `rejected` | yes | Validation state |

## Decisions still to make

- Handling of multiple taxes, tips, discounts
- Rounding/precision rules for amounts
- Whether line items are required for validation
- Versioning of the schema (schema `version` field)

Track decisions as issues labelled `schema`.
