
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

from pdf_service import (
    extract_text_from_pdf,
    extract_structured_pdf
)

from report_classifier import classify_report
from biomarker_service import analyze_biomarkers
from analysis_service import analyze_report
from imaging_service import analyze_imaging_report
from gemini_ocr_service import extract_pdf_with_gemini
from translation_service import normalize_language, SUPPORTED_LANGUAGES


app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Health Report Interpreter backend is running"
    })


@app.route("/upload", methods=["POST"])
def upload_report():

    if "file" not in request.files:
        return jsonify({"error": "No PDF file was uploaded."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file was selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are supported."}), 400

    filename = secure_filename(file.filename)

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(file_path)

    try:
        # Normalize language: accept both ISO codes ("hi") and
        # legacy full names ("Hindi"). Defaults to "en".
        raw_language = request.form.get("language", "en").strip() or "en"
        lang = normalize_language(raw_language)

        # Map ISO code to English name for Gemini prompt
        LANGUAGE_DISPLAY_NAMES = {
            "en": "English", "hi": "Hindi", "te": "Telugu",
            "ta": "Tamil", "kn": "Kannada", "ml": "Malayalam",
            "mr": "Marathi", "bn": "Bengali",
        }
        response_language = LANGUAGE_DISPLAY_NAMES.get(lang, "English")

        gemini_extraction = None
        try:
            gemini_extraction = extract_pdf_with_gemini(
                file_path,
                response_language=response_language
            )
        except Exception as error:
            if hasattr(error, "errors"):
                error_details = "; ".join(
                    "{}: {}".format(
                        ".".join(str(part) for part in item.get("loc", [])),
                        item.get("msg", "invalid value")
                    )
                    for item in error.errors()
                )
            else:
                error_details = str(error)[:500]
            print(
                "Gemini OCR failed; using local extraction:",
                type(error).__name__,
                error_details
            )

        if gemini_extraction:
            gemini_report_type = gemini_extraction["report_type"]
            has_incomplete_output = (
                (gemini_report_type == "laboratory"
                 and not gemini_extraction["biomarkers"])
                or (gemini_report_type == "imaging"
                    and len(gemini_extraction["text"]) < 40)
                or (gemini_report_type == "general"
                    and len(gemini_extraction["text"]) < 120)
            )
            if has_incomplete_output:
                print(
                    "Gemini OCR output was incomplete; using local extraction."
                )
                gemini_extraction = None

        extracted_text = (
            gemini_extraction["text"]
            if gemini_extraction and gemini_extraction["text"]
            else extract_text_from_pdf(file_path)
        )
        ocr_source = "Gemini" if gemini_extraction else "Tesseract"

        if not extracted_text.strip():
            return jsonify({
                "error": "Could not extract readable content from this PDF."
            }), 400

        if gemini_extraction:
            structured_page_count = gemini_extraction["page_count"]
            structured_pdf = None
        else:
            structured_pdf = extract_structured_pdf(file_path)
            structured_page_count = len(structured_pdf.get("pages", []))

        report_type = (
            gemini_extraction["report_type"]
            if gemini_extraction
            else classify_report(extracted_text)
        )

        # Separate analysis paths for laboratory and imaging reports.
        if report_type == "imaging":
            report_analysis = analyze_imaging_report(extracted_text, lang=lang)

        else:
            biomarkers = []

            if report_type == "laboratory":
                biomarkers = (
                    gemini_extraction["biomarkers"]
                    if gemini_extraction
                    else analyze_biomarkers(structured_pdf)
                )

            report_analysis = analyze_report(biomarkers, lang=lang)
            report_analysis["report_type"] = report_type
            report_analysis["findings"] = []

        if gemini_extraction and gemini_extraction.get("overall_impression"):
            report_analysis["impression"] = gemini_extraction["overall_impression"]

        # Debug output
        print("\n" + "=" * 60)
        print("REPORT")
        print("=" * 60)
        print("Filename:", filename)
        print("OCR SOURCE:", ocr_source)
        print("REPORT TYPE:", report_type)
        print("LANGUAGE:", lang)
        print("TEXT LENGTH:", len(extracted_text))
        print("STRUCTURED PAGES:", structured_page_count)
        print("BIOMARKERS FOUND:", len(report_analysis.get("biomarkers", [])))
        print("IMAGING FINDINGS:", len(report_analysis.get("findings", [])))
        print("PATTERNS FOUND:", len(report_analysis.get("patterns", [])))
        print("KNOWLEDGE ITEMS:", len(report_analysis.get("knowledge", [])))
        print("DOCTOR QUESTIONS:", len(report_analysis.get("doctor_questions", [])))

        for finding in report_analysis.get("findings", []):
            print(
                "FINDING:",
                finding.get("organ"),
                "|",
                finding.get("description")
            )

        for biomarker in report_analysis.get("biomarkers", []):
            print(
                "BIOMARKER:",
                biomarker.get("name"),
                "|",
                biomarker.get("value"),
                biomarker.get("unit"),
                "|",
                biomarker.get("status")
            )

        print("=" * 60 + "\n")

        return jsonify({
            "message": "Report processed successfully",
            "filename": filename,
            "status": "document_processed",
            "language": lang,
            "analysis": {
                "report_type": report_type,
                "biomarkers": report_analysis.get("biomarkers", []),
                "findings": report_analysis.get("findings", []),
                "patterns": report_analysis.get("patterns", []),
                "impression": report_analysis.get("impression", ""),
                "concern_level": report_analysis.get("concern_level", {}),
                "knowledge": report_analysis.get("knowledge", []),
                "doctor_questions": report_analysis.get("doctor_questions", [])
            }
        })

    except Exception as error:
        print("ERROR WHILE PROCESSING REPORT:", error)

        return jsonify({
            "error": "An error occurred while processing the medical report.",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
