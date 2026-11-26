import os
import logging
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load backend secrets explicitly from backend/.env
backend_env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(backend_env_path)

from auth import require_auth
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
from supabase_service import (
    save_report,
    get_user_reports,
    get_report_by_id,
    delete_report,
)

# Configure server logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("health_interpreter_api")

app = Flask(__name__)

# Parse comma-separated authorized origins from CLERK_AUTHORIZED_PARTIES
raw_azp = os.getenv("CLERK_AUTHORIZED_PARTIES", "http://localhost:5173")
authorized_origins = [
    origin.strip() for origin in raw_azp.split(",") if origin.strip()
] or ["http://localhost:5173"]

# Restrict CORS to authorized frontend origins with explicit headers
CORS(
    app,
    resources={r"/*": {"origins": authorized_origins}},
    allow_headers=["Authorization", "Content-Type"],
    methods=["GET", "POST", "OPTIONS"],
    supports_credentials=True
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET"])
def home():
    """
    Public backend health check endpoint.
    """
    return jsonify({
        "status": "healthy",
        "message": "AI Health Report Interpreter backend is running"
    })


@app.route("/upload", methods=["POST"])
@require_auth
def upload_report():
    """
    Protected PDF upload and clinical analysis endpoint.
    Requires a valid Clerk session token.
    """
    if "file" not in request.files:
        return jsonify({"error": "No PDF file was uploaded."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file was selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are supported."}), 400

    filename = secure_filename(file.filename)

    # Use verified Clerk user ID for isolated storage path when available
    user_id = getattr(g, "user_id", None)
    if user_id:
        user_folder = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(user_id))
        os.makedirs(user_folder, exist_ok=True)
        file_path = os.path.join(user_folder, filename)
    else:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

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
            logger.warning(
                "Gemini OCR fallback triggered. Reason: %s",
                type(error).__name__
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
                logger.info(
                    "Gemini OCR output incomplete; falling back to local extraction."
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
            biomarkers = (
                gemini_extraction["biomarkers"]
                if gemini_extraction and gemini_extraction.get("biomarkers")
                else analyze_biomarkers(structured_pdf) if structured_pdf else []
            )

            report_analysis = analyze_report(biomarkers, lang=lang)
            report_analysis["report_type"] = report_type
            report_analysis["findings"] = []

        if gemini_extraction and gemini_extraction.get("overall_impression"):
            report_analysis["impression"] = gemini_extraction["overall_impression"]

        # Server-side diagnostic metrics without logging report contents or tokens
        logger.info(
            "Report processed successfully for user %s | file=%s | ocr=%s | type=%s | lang=%s | biomarkers=%d | findings=%d",
            user_id or "anonymous",
            filename,
            ocr_source,
            report_type,
            lang,
            len(report_analysis.get("biomarkers", [])),
            len(report_analysis.get("findings", []))
        )

        analysis_payload = {
            "report_type": report_type,
            "biomarkers": report_analysis.get("biomarkers", []),
            "findings": report_analysis.get("findings", []),
            "patterns": report_analysis.get("patterns", []),
            "impression": report_analysis.get("impression", ""),
            "concern_level": report_analysis.get("concern_level", {}),
            "knowledge": report_analysis.get("knowledge", []),
            "doctor_questions": report_analysis.get("doctor_questions", []),
        }

        saved_record = None
        if user_id:
            try:
                saved_record = save_report(
                    user_id=user_id,
                    filename=filename,
                    report_type=report_type,
                    language=lang,
                    ocr_source=ocr_source,
                    analysis=analysis_payload,
                )
            except Exception as db_error:
                logger.warning(
                    "Failed to save report to Supabase: %s",
                    type(db_error).__name__,
                )

        return jsonify({
            "message": "Report processed successfully",
            "report_id": saved_record["id"] if saved_record else None,
            "filename": filename,
            "status": "document_processed",
            "language": lang,
            "analysis": analysis_payload,
        })

    except Exception as error:
        logger.error(
            "Server processing error: %s: %s",
            type(error).__name__,
            str(error)
        )
        return jsonify({
            "error": "An error occurred while processing the medical report.",
            "message": "Unable to complete report analysis at this time."
        }), 500


@app.route("/reports", methods=["GET"])
@require_auth
def list_reports():
    """Return saved report history for the authenticated Clerk user."""
    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Authenticated user ID not found."}), 401

    try:
        limit = min(int(request.args.get("limit", 20)), 100)
    except ValueError:
        limit = 20

    try:
        reports = get_user_reports(user_id=user_id, limit=limit)
        return jsonify({"reports": reports})
    except Exception as error:
        logger.error("Failed to fetch reports: %s", type(error).__name__)
        return jsonify({"error": "Unable to fetch report history."}), 500


@app.route("/reports/<report_id>", methods=["GET"])
@require_auth
def get_report(report_id):
    """Return a single saved report owned by the authenticated Clerk user."""
    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Authenticated user ID not found."}), 401

    try:
        report = get_report_by_id(user_id=user_id, report_id=report_id)
        if not report:
            return jsonify({"error": "Report not found."}), 404
        return jsonify({"report": report})
    except Exception as error:
        logger.error("Failed to fetch report %s: %s", report_id, type(error).__name__)
        return jsonify({"error": "Unable to fetch report."}), 500


@app.route("/reports/<report_id>", methods=["DELETE"])
@require_auth
def remove_report(report_id):
    """Delete a saved report owned by the authenticated Clerk user."""
    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Authenticated user ID not found."}), 401

    try:
        deleted = delete_report(user_id=user_id, report_id=report_id)
        if not deleted:
            return jsonify({"error": "Report not found."}), 404
        return jsonify({"message": "Report deleted successfully."})
    except Exception as error:
        logger.error("Failed to delete report %s: %s", report_id, type(error).__name__)
        return jsonify({"error": "Unable to delete report."}), 500


@app.route("/ask", methods=["POST"])
@require_auth
def ask_about_report():
    """Interactive AI Assistant endpoint to answer questions about the analyzed report."""
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    analysis = data.get("analysis") or {}
    lang = normalize_language((data.get("language") or "en").strip() or "en")

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY is not configured."}), 503

    LANGUAGE_DISPLAY_NAMES = {
        "en": "English", "hi": "Hindi", "te": "Telugu",
        "ta": "Tamil", "kn": "Kannada", "ml": "Malayalam",
        "mr": "Marathi", "bn": "Bengali",
    }
    response_language = LANGUAGE_DISPLAY_NAMES.get(lang, "English")

    try:
        from google import genai
        from gemini_ocr_service import MODEL_NAME
        import json

        client = genai.Client(api_key=api_key)
        prompt = (
            f"You are a helpful, empathetic clinical AI assistant. "
            f"Answer the user's question about their medical report in {response_language} using simple, clear language. "
            f"Do not diagnose; recommend consulting a doctor for medical decisions.\n\n"
            f"Report Analysis:\n{json.dumps(analysis, ensure_ascii=False)[:6000]}\n\n"
            f"User Question: {question}"
        )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        answer = (response.text or "").strip()
        if not answer:
            return jsonify({"error": "No response generated."}), 502
        return jsonify({"answer": answer})
    except Exception as error:
        logger.error("AI Assistant error: %s: %s", type(error).__name__, str(error))
        return jsonify({"error": "Unable to answer right now. Please try again."}), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
