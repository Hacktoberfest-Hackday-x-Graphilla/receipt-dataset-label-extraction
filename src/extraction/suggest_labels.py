"""suggest_labels.py - Read receipts and suggest label fields for them.

Run it with no arguments (from the repo root):

    python -m src.extraction.suggest_labels

It reads every receipt in the receipts folder (default dataset/receipts/),
asks a Google AI Studio model (Gemma, served by the Gemini Developer API)
to read each one and extract the label fields, then writes one JSON label
file next to each receipt (<name>.label.json).

These are MACHINE SUGGESTIONS, not ground truth - a human must review each
one before it counts as data (see the README). Receipts that already have a
suggestion are skipped on later runs, so re-running is safe.

How a receipt is read:
  - JPG / PNG / WEBP  -> the image is sent to the model and read by vision.
  - PDF with a text layer -> the text is sent to the model.
  - PDF without a text layer (a phone scan) -> the page images are sent to
    the model and read by vision. No local OCR / Tesseract needed.

Setup (once):
    1. pip install -r requirements.txt
    2. Copy .env.example to .env and put your API key in GEMINI_API_KEY.
       .env is gitignored - the key never leaves your machine.
"""

import json
import os
import re
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # the key can also be exported in the shell instead
    pass

REPO_ROOT = Path(__file__).resolve().parents[2]
RECEIPTS_FOLDER = Path(
    os.environ.get("RECEIPTS_FOLDER", str(REPO_ROOT / "dataset" / "receipts"))
)
MODEL = os.environ.get("GEMINI_MODEL", "gemma-4-26b-a4b-it")

LABEL_SUFFIX = ".label.json"
PDF_SUFFIX = ".pdf"
IMAGE_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}

TEXT_MIN_NONSPACE = 30  # below this a PDF text layer counts as empty
MAX_TEXT_CHARS = 60000
VISION_DPI = 200
VISION_MAX_PAGES = 3
MAX_RENDER_PIXELS = 30_000_000

PROMPT = """You read a receipt or invoice and return ONE label as valid JSON, with no text before or after it.

JSON shape:
{
  "merchant": "store or business name, or null",
  "date": "ISO date (YYYY-MM-DD), or null if unreadable",
  "currency": "3-letter currency code (NPR, USD, INR, ...), or null",
  "subtotal": number, or null,
  "tax": number, or null,
  "total": number, or null,
  "receipt_number": "printed bill / receipt / invoice number, or null",
  "receipt_type": "grocery, restaurant, retail, fuel, utility, travel, other, or null",
  "language": "main language of the receipt (en, ne, hi, ...), or null",
  "items": [
    {"description": "item name", "quantity": number, "unit_price": number, "amount": number}
  ]
}

Rules:
- Set a field to null ONLY when it is not on the receipt. Never invent values.
- Amounts are plain numbers: no currency symbols, no commas.
- items may be an empty list when the line items are not legible."""


# ---------------------------------------------------------------------------
# Model reply -> dict
# ---------------------------------------------------------------------------
def parse_model_json(raw: str) -> dict:
    """Turn the model reply into one label dict."""
    text = (raw or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("model reply contained no JSON object")
        data = json.loads(match.group(0))
    if isinstance(data, list):  # tolerate a single-element wrapper array
        if len(data) == 1:
            data = data[0]
    if not isinstance(data, dict):
        raise ValueError("model reply is not a JSON object")
    return data


# ---------------------------------------------------------------------------
# Clean + validate the label
# ---------------------------------------------------------------------------
def _text(raw: dict, key: str, max_len: int = 200):
    value = str(raw.get(key) or "").strip()
    return value[:max_len] or None


def _iso_date(value):
    value = str(value or "").strip()
    return value if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) else None


def _currency(value):
    value = str(value or "").strip().upper()
    return value if re.fullmatch(r"[A-Z]{3}", value) else None


def _number(value):
    if value is None:
        return None
    try:
        number = float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None
    if number != number or number in (float("inf"), float("-inf")):
        return None  # reject NaN / infinity
    return round(number, 2)


def _items(value) -> list:
    if not isinstance(value, list):
        return []
    out = []
    for item in value[:50]:
        if not isinstance(item, dict):
            continue
        description = str(item.get("description") or "").strip()[:120]
        out.append({
            "description": description or None,
            "quantity": _number(item.get("quantity")),
            "unit_price": _number(item.get("unit_price")),
            "amount": _number(item.get("amount")),
        })
    return out


def clean_record(raw: dict) -> dict:
    """Normalize one model label into the shape stored next to a receipt."""
    return {
        "merchant": _text(raw, "merchant"),
        "date": _iso_date(raw.get("date")),
        "currency": _currency(raw.get("currency")),
        "subtotal": _number(raw.get("subtotal")),
        "tax": _number(raw.get("tax")),
        "total": _number(raw.get("total")),
        "receipt_number": _text(raw, "receipt_number", max_len=60),
        "receipt_type": _text(raw, "receipt_type", max_len=30),
        "language": _text(raw, "language", max_len=10),
        "items": _items(raw.get("items")),
    }


def receipt_id_from(path: Path) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    return slug or "receipt"


# ---------------------------------------------------------------------------
# Read the receipt
# ---------------------------------------------------------------------------
def pdf_text_or_none(path: Path) -> str:
    """Return a PDF's text layer, or '' when there is no usable text layer."""
    import pymupdf as fitz

    doc = fitz.open(path)
    try:
        text = "\n".join(page.get_text("text") for page in doc)
        if len(re.sub(r"\s", "", text)) >= TEXT_MIN_NONSPACE:
            return text
        return ""
    finally:
        doc.close()


def render_pdf_pages(path: Path) -> list:
    """Render the first pages of a scanned PDF as PNG bytes for the model."""
    import pymupdf as fitz

    doc = fitz.open(path)
    try:
        pages = []
        for page in list(doc)[:VISION_MAX_PAGES]:
            width = max(page.rect.width, 1) * (VISION_DPI / 72)
            height = max(page.rect.height, 1) * (VISION_DPI / 72)
            matrix = fitz.Matrix(VISION_DPI / 72, VISION_DPI / 72)
            if width * height > MAX_RENDER_PIXELS:  # keep huge pages within limits
                scale = (MAX_RENDER_PIXELS / (width * height)) ** 0.5
                matrix = fitz.Matrix(VISION_DPI / 72 * scale, VISION_DPI / 72 * scale)
            pix = page.get_pixmap(matrix=matrix)
            pages.append((pix.tobytes("png"), "image/png"))
        return pages
    finally:
        doc.close()


# ---------------------------------------------------------------------------
# Ask the model (Google AI Studio / Gemini Developer API)
# ---------------------------------------------------------------------------
def _client():
    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit(
            "GEMINI_API_KEY not found - copy .env.example to .env, add your key, and re-run."
        )
    from google import genai

    return genai.Client()  # reads GEMINI_API_KEY from the environment


def ask_model_text(text: str):
    client = _client()
    response = client.models.generate_content(
        model=MODEL,
        contents=[PROMPT, "Receipt text:\n" + text[:MAX_TEXT_CHARS]],
    )
    return clean_record(parse_model_json(response.text))


def ask_model_vision(pages: list):
    from google.genai import types

    client = _client()
    parts = [
        types.Part.from_bytes(data=data, mime_type=mime) for data, mime in pages
    ]
    response = client.models.generate_content(
        model=MODEL,
        contents=[*parts, PROMPT],
    )
    return clean_record(parse_model_json(response.text))


def extract_one(path: Path):
    """Return the cleaned label for one receipt."""
    if path.suffix.lower() == PDF_SUFFIX:
        text = pdf_text_or_none(path)
        if text:
            return ask_model_text(text)
        pages = render_pdf_pages(path)
        if not pages:
            raise ValueError("pdf has no readable text and could not be rendered")
        return ask_model_vision(pages)

    mime = IMAGE_MIME.get(path.suffix.lower())
    if not mime:
        raise ValueError(f"unsupported receipt file type: {path.suffix}")
    return ask_model_vision([(path.read_bytes(), mime)])


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------
def label_path_for(path: Path) -> Path:
    return path.with_suffix(path.suffix + LABEL_SUFFIX)


def write_label(path: Path, record: dict, ok: bool = True, error: str = "") -> None:
    """Write the suggestion JSON next to the receipt."""
    out = {
        "receipt_id": receipt_id_from(path),
        "image": str(path),
        **record,
        "suggested_by_model": MODEL,
        "reviewed": False,
        "notes": (
            "Machine-suggested labels - review before this counts as dataset data."
        ),
    }
    if not ok:
        out["notes"] = f"FAILED to extract labels: {error}"
    label_path_for(path).write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    if not RECEIPTS_FOLDER.is_dir():
        print(f"Receipts folder not found: {RECEIPTS_FOLDER}")
        print(f"Create it ({RECEIPTS_FOLDER}) and drop receipt files inside.")
        return 1

    files = sorted(
        p for p in RECEIPTS_FOLDER.iterdir()
        if p.is_file()
        and (p.suffix.lower() in IMAGE_MIME or p.suffix.lower() == PDF_SUFFIX)
    )
    if not files:
        print(f"No receipts in {RECEIPTS_FOLDER} yet - add a PDF, JPG, PNG or WEBP and re-run.")
        return 0

    print(f"Receipts folder : {RECEIPTS_FOLDER}")
    print(f"Model           : {MODEL}")
    print(f"Receipts        : {len(files)}")
    print("----------------------------------------------")

    suggested = skipped = failed = 0
    for path in files:
        if label_path_for(path).exists():
            print(f"  skip  {path.name} (already suggested)")
            skipped += 1
            continue
        try:
            record = extract_one(path)
        except SystemExit:
            raise
        except Exception as err:  # keep going to the next receipt
            failed += 1
            write_label(path, {}, ok=False, error=str(err))
            print(f"  fail  {path.name}: {err}")
            continue
        write_label(path, record)
        suggested += 1
        print(f"  done  {path.name} -> {label_path_for(path).name}")

    print("----------------------------------------------")
    print(f"{suggested} new suggestion(s), {skipped} skipped, {failed} failed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())