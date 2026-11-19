"""Gemini OCR and structured extraction for scanned PDFs."""

import os
from datetime import datetime
from pathlib import Path
from typing import Literal

import fitz
from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
LOG_FILE = Path(__file__).resolve().parent.parent / "logs.txt"


class ExtractedBiomarker(BaseModel):
    name: str = Field(description="Test name as printed in the report")
    value: float | None = Field(description="Reported numeric result, or null if unreadable")
    unit: str = Field(description="Unit printed beside result, or empty string")
    reference_range: str = Field(description="Applicable printed range/category, or empty string")
    page: int | None = Field(description="One-based PDF page number")
    status: Literal["low", "normal", "high", "unknown"] = Field(
        description="Classification against only the applicable range printed in this report"
    )
    status_label: str = Field(
        description="Localized display label for the status in the requested language"
    )
    status_explanation: str = Field(
        description="Short plain-language explanation of the classification, including why unknown"
    )


class GeminiPDFExtraction(BaseModel):
    report_type: Literal["laboratory", "imaging", "general"]
    relevant_text: str = Field(
        description="For imaging, concise findings and impression; for general, a short relevant summary"
    )
    overall_impression: str = Field(
        description="A concise, plain-language summary of the report in the requested language"
    )
    biomarkers: list[ExtractedBiomarker]


EXTRACTION_PROMPT = """Read this PDF and extract only the useful information; do not transcribe every page.

Classify it as laboratory, imaging, or general.
Write overall_impression as a brief, plain-language summary of the report's main findings.

For every laboratory result, return its printed test name, numeric value, unit, printed reference
range or category, one-based page number, status, and a short understandable explanation. Match the
result and range from the same row, using the page layout. Use a demographic-specific printed range
when applicable. Compare only against this report's printed ranges/categories, including written
limits such as less than, greater than, and up to, and comma-formatted numbers. For category-based
ranges, explain which printed category contains the value. Classify as low, normal, high, or unknown.
If unknown, explain exactly what information is missing or unreadable. Never invent a range, use
general medical reference ranges, or diagnose. Do not mistake numbers in ranges for results. Use null
for unreadable numeric values and empty strings for unreadable units/ranges. Preserve printed units.

For imaging, return no biomarkers; put only findings and impression in relevant_text. For general,
return no biomarkers and a short relevant summary in relevant_text. Keep relevant_text empty for labs.
"""


def _is_scanned_pdf(file_path):
    with fitz.open(file_path) as document:
        return any(len(page.get_text("text").strip()) < 50 for page in document)


def _normalize_biomarkers(items):
    biomarkers = []
    for item in items:
        name = str(item.get("name") or "").strip()
        value = item.get("value")
        if not name or value is None:
            continue
        try:
            value = float(value)
        except (TypeError, ValueError):
            continue
        biomarkers.append({
            "name": name,
            "value": value,
            "unit": str(item.get("unit") or "").strip(),
            "reference_range": str(item.get("reference_range") or "").strip(),
            "status": item.get("status", "unknown"),
            "status_label": str(item.get("status_label") or "").strip(),
            "status_explanation": str(item.get("status_explanation") or "").strip(),
            "page": item.get("page"),
        })
    return biomarkers


def _append_gemini_log(label, content):
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    with LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(f"\n{'=' * 80}\n[{timestamp}] {label}\n")
        log_file.write(str(content).rstrip())
        log_file.write("\n")


def extract_pdf_with_gemini(file_path, response_language="English"):
    """Return Gemini extraction for scanned PDFs, or None when Gemini is not configured."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or not _is_scanned_pdf(file_path):
        return None

    from google import genai
    from google.genai import types

    with fitz.open(file_path) as document:
        page_count = len(document)
    with open(file_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    client = genai.Client(api_key=api_key)
    language_prompt = (
        f"\n\nWrite overall_impression, status_explanation, and any explanatory "
        f"relevant_text in {response_language}. Keep test names, measured values, "
        "units, and reference ranges exactly as printed. Translate status_label too; keep status values "
        "as the English tokens low, normal, high, or unknown."
    )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[EXTRACTION_PROMPT + language_prompt,
                  types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GeminiPDFExtraction,
            temperature=0,
        ),
    )
    if not response.text:
        raise ValueError("Gemini returned an empty response")

    # Log the exact structured response for each run, including OCR and classification.
    _append_gemini_log("GEMINI RAW RESPONSE", response.text)
    extracted = GeminiPDFExtraction.model_validate_json(response.text)
    biomarkers = _normalize_biomarkers(
        [item.model_dump() for item in extracted.biomarkers]
    )
    relevant_text = extracted.relevant_text.strip()

    if extracted.report_type == "laboratory":
        if not biomarkers:
            raise ValueError("Gemini found no readable numeric laboratory results")
        document_text = "Laboratory report\n" + "\n".join(
            f"{item['name']}: {item['value']} {item['unit']}"
            for item in biomarkers
        )
    else:
        document_text = relevant_text
        if not document_text:
            raise ValueError("Gemini could not read relevant text from this scanned PDF")

    return {
        "text": document_text,
        "overall_impression": extracted.overall_impression.strip(),
        "report_type": extracted.report_type,
        "biomarkers": biomarkers,
        "page_count": page_count,
    }
