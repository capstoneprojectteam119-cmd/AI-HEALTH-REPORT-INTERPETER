
import re
from translation_service import (
    get_concern_translation,
    get_organ_translation,
    IMAGING_KNOWLEDGE,
    IMAGING_QUESTIONS,
    NO_IMPRESSION_TEXT,
    normalize_language,
)


def clean_text(text):
    text = str(text or "")
    text = text.replace("\x0c", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_ocr_text(text):
    text = clean_text(text)

    # Remove common OCR artifacts at the beginning.
    text = re.sub(
        r"^\s*(?:fe|f\s*e)\s*\.?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text


def extract_impression(text):
    text = normalize_ocr_text(text)

    # Locate the radiologist's conclusion.
    patterns = [
        r"SONOGRAPHICALLY\s*[-:]\s*(.*)",
        r"IMPRESSION\s*[:\-]?\s*(.*)",
        r"CONCLUSION\s*[:\-]?\s*(.*)"
    ]

    impression = ""

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:
            impression = match.group(1)
            break

    if not impression:
        return ""

    # Remove common report footers.
    impression = re.split(
        r"THANKS\s+FOR\s+REFERRAL|"
        r"REGARDS|"
        r"REPORT\s+ENDS|"
        r"END\s+OF\s+REPORT",
        impression,
        flags=re.IGNORECASE
    )[0]

    impression = clean_text(impression)

    # Remove trailing OCR marks.
    impression = re.sub(r"[\s*|]+$", "", impression)

    return impression.strip(" :-;.")


def split_impression_items(impression):
    if not impression:
        return []

    # Split numbered findings such as:
    # 1. Finding one 2. Finding two
    parts = re.split(
        r"(?<!\d)\s*(?:\d+[\.\)]|[ivx]+[\.\)])\s*",
        impression,
        flags=re.IGNORECASE
    )

    items = []

    for part in parts:
        part = clean_text(part)
        part = part.strip(" .;:*|-")

        if len(part) > 8:
            items.append(part)

    if not items:
        items = [impression]

    return items


def identify_organ(description):
    text = description.lower()

    if "ureter" in text or "hydroureter" in text:
        return "Left kidney and ureter" if "left" in text else "Ureter"

    if "kidney" in text or "renal" in text:
        if "right" in text:
            return "Right kidney"
        if "left" in text:
            return "Left kidney"
        return "Kidneys"

    if "gall bladder" in text or "gallbladder" in text:
        return "Gall bladder"

    if "liver" in text:
        return "Liver"

    if "pancreas" in text:
        return "Pancreas"

    if "spleen" in text:
        return "Spleen"

    if "urinary bladder" in text or "bladder" in text:
        return "Urinary bladder"

    if "uterus" in text:
        return "Uterus"

    if "ovary" in text or "ovaries" in text:
        return "Ovaries"

    return "Imaging finding"


def extract_important_findings(impression):
    items = split_impression_items(impression)
    findings = []

    for item in items:
        item_lower = item.lower()

        important_terms = [
            "calculus",
            "calculi",
            "stone",
            "microlith",
            "hydronephrosis",
            "hydroureter",
            "lesion",
            "mass",
            "cyst",
            "thickening",
            "dilatation",
            "dilation",
            "obstruction",
            "fluid",
            "nodule"
        ]

        if not any(term in item_lower for term in important_terms):
            continue

        findings.append({
            "organ": identify_organ(item),
            "description": item
        })

    return findings


def build_imaging_knowledge(impression, findings, lang="en"):
    text = (
        impression + " " +
        " ".join(item["description"] for item in findings)
    ).lower()

    knowledge = []
    lang_knowledge = IMAGING_KNOWLEDGE.get(lang, IMAGING_KNOWLEDGE["en"])

    if any(term in text for term in [
        "calculus", "calculi", "stone", "microlith"
    ]):
        k_item = lang_knowledge.get("stones", IMAGING_KNOWLEDGE["en"]["stones"])
        knowledge.append({
            "title": k_item["title"],
            "content": k_item["content"],
            "source": "General medical knowledge",
            "related_biomarker": "Imaging finding"
        })

    if any(term in text for term in [
        "hydroureteronephrosis", "hydronephrosis"
    ]):
        k_item = lang_knowledge.get("dilation", IMAGING_KNOWLEDGE["en"]["dilation"])
        knowledge.append({
            "title": k_item["title"],
            "content": k_item["content"],
            "source": "General medical knowledge",
            "related_biomarker": "Imaging finding"
        })

    return knowledge


def generate_imaging_questions(impression, lang="en"):
    text = impression.lower()
    questions = []
    q_dict = IMAGING_QUESTIONS.get(lang, IMAGING_QUESTIONS["en"])

    if any(term in text for term in [
        "calculus", "calculi", "stone", "microlith"
    ]):
        questions.extend([
            q_dict["stone_significance"],
            q_dict["urine_flow"],
            q_dict["followup_imaging"],
        ])

    if any(term in text for term in [
        "hydroureteronephrosis", "hydronephrosis"
    ]):
        questions.append(q_dict["dilation_cause"])

    questions.append(q_dict["urgent_symptoms"])

    return questions[:5]


def analyze_imaging_report(extracted_text, lang="en"):
    lang = normalize_language(lang)
    impression = extract_impression(extracted_text)

    raw_findings = extract_important_findings(impression)

    # Localize organ names in findings
    findings = []
    for item in raw_findings:
        findings.append({
            "organ": get_organ_translation(item["organ"], lang),
            "description": item["description"]
        })

    if impression:
        simple_impression = impression
    else:
        simple_impression = NO_IMPRESSION_TEXT.get(lang, NO_IMPRESSION_TEXT["en"])

    knowledge = build_imaging_knowledge(
        impression,
        findings,
        lang=lang
    )

    questions = generate_imaging_questions(impression, lang=lang)

    text = impression.lower()

    has_stone_or_dilation = any(
        term in text
        for term in [
            "calculus",
            "calculi",
            "stone",
            "microlith",
            "hydroureteronephrosis",
            "hydronephrosis"
        ]
    )

    if has_stone_or_dilation:
        concern_trans = get_concern_translation("imaging_follow_up", lang)
        concern_level = {
            "level": "follow_up",
            "label": concern_trans.get("label", "Medical follow-up recommended"),
            "description": concern_trans.get("description", "The imaging report describes urinary stones and/or urinary tract dilation.")
        }
    else:
        concern_trans = get_concern_translation("imaging_review", lang)
        concern_level = {
            "level": "review",
            "label": concern_trans.get("label", "Clinical review recommended"),
            "description": concern_trans.get("description", "Imaging findings should be interpreted with symptoms, medical history and clinical examination.")
        }

    return {
        "report_type": "imaging",
        "biomarkers": [],
        "findings": findings,
        "patterns": [],
        "impression": simple_impression,
        "concern_level": concern_level,
        "knowledge": knowledge,
        "doctor_questions": questions
    }
