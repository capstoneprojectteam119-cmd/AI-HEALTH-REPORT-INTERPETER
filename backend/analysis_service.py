import json
import os
import re

from translation_service import (
    get_status_label,
    get_status_explanation,
    get_concern_translation,
    get_impression_phrases,
    get_doctor_question_templates,
    get_pattern_translation,
    get_knowledge_translation,
    normalize_language,
)


# =========================================================
# LOAD MEDICAL KNOWLEDGE BASE
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KNOWLEDGE_FILE = os.path.join(
    BASE_DIR,
    "knowledge_base",
    "medical_knowledge.json"
)


def load_knowledge_base():
    try:
        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception as error:
        print("Knowledge base error:", error)
        return []


KNOWLEDGE_BASE = load_knowledge_base()


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):
    if not text:
        return ""

    text = str(text).lower()

    text = text.replace("μ", "u")
    text = text.replace("µ", "u")

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# BIOMARKER ALIASES
# =========================================================

BIOMARKER_ALIASES = {

    "c reactive protein": [
        "c reactive protein",
        "c reactive protein",
        "c-reactive protein",
        "crp"
    ],

    "rdw": [
        "rdw",
        "rdw cv",
        "rdw sd",
        "red cell distribution width"
    ],

    "hemoglobin": [
        "hemoglobin",
        "haemoglobin",
        "hb",
        "hgb"
    ],

    "rbc": [
        "rbc",
        "red blood cell",
        "red blood cells",
        "red blood cell count"
    ],

    "wbc": [
        "wbc",
        "white blood cell",
        "white blood cells",
        "white blood count",
        "total leucocyte count",
        "total leukocyte count",
        "tlc"
    ],

    "neutrophils": [
        "neutrophil",
        "neutrophils",
        "neut"
    ],

    "lymphocytes": [
        "lymphocyte",
        "lymphocytes",
        "lymph"
    ],

    "monocytes": [
        "monocyte",
        "monocytes",
        "mono"
    ],

    "eosinophils": [
        "eosinophil",
        "eosinophils",
        "eos"
    ],

    "basophils": [
        "basophil",
        "basophils",
        "baso"
    ],

    "mcv": [
        "mcv",
        "mean corpuscular volume"
    ],

    "mch": [
        "mch",
        "mean corpuscular hemoglobin",
        "mean corpuscular haemoglobin"
    ],

    "mchc": [
        "mchc",
        "mean corpuscular hemoglobin concentration",
        "mean corpuscular haemoglobin concentration"
    ],

    "glucose": [
        "glucose",
        "blood glucose",
        "blood sugar",
        "fasting glucose",
        "fasting plasma glucose",
        "fasting blood sugar",
        "fbs"
    ],

    "hba1c": [
        "hba1c",
        "hb a1c",
        "a1c",
        "glycated hemoglobin",
        "glycated haemoglobin",
        "glycosylated hemoglobin",
        "glycosylated haemoglobin"
    ],

    "hdl": [
        "hdl",
        "hdl cholesterol",
        "high density lipoprotein"
    ],

    "ldl": [
        "ldl",
        "ldl cholesterol",
        "low density lipoprotein"
    ],

    "total cholesterol": [
        "total cholesterol",
        "cholesterol total"
    ],

    "triglycerides": [
        "triglycerides",
        "triglyceride"
    ],

    "bilirubin": [
        "bilirubin",
        "total bilirubin",
        "direct bilirubin",
        "indirect bilirubin"
    ],

    "creatinine": [
        "creatinine",
        "serum creatinine"
    ],

    "urea": [
        "urea",
        "blood urea",
        "serum urea",
        "bun",
        "blood urea nitrogen"
    ],

    "platelets": [
        "platelet",
        "platelets",
        "platelet count"
    ],

    "t3": [
        "t3",
        "total t3",
        "t3 total",
        "triiodothyronine"
    ],

    "t4": [
        "t4",
        "total t4",
        "t4 total",
        "thyroxine"
    ],

    "tsh": [
        "tsh",
        "thyroid stimulating hormone"
    ],

    "sodium": [
        "sodium",
        "na"
    ],

    "potassium": [
        "potassium",
        "k"
    ],

    "chloride": [
        "chloride",
        "chlorides",
        "cl"
    ],

    "uric acid": [
        "uric acid"
    ],

    "alkaline phosphatase": [
        "alkaline phosphatase",
        "alp"
    ],

    "ast": [
        "ast",
        "sgot",
        "sgot ast",
        "aspartate aminotransferase"
    ],

    "alt": [
        "alt",
        "sgpt",
        "sgpt alt",
        "alanine aminotransferase"
    ],

    "gamma glutamyl transferase": [
        "gamma glutamyl transferase",
        "gamma glutamyl transpeptidase",
        "ggt",
        "ggtp"
    ],

    "ferritin": [
        "ferritin",
        "serum ferritin"
    ],

    "iron": [
        "iron",
        "serum iron"
    ],

    "vitamin d": [
        "vitamin d",
        "25 oh vitamin d",
        "25 hydroxy vitamin d",
        "25 oh d"
    ],

    "vitamin b12": [
        "vitamin b12",
        "b12",
        "cobalamin"
    ],

    "folate": [
        "folate",
        "folic acid"
    ],

    "calcium": [
        "calcium",
        "serum calcium"
    ],

    "albumin": [
        "albumin",
        "serum albumin"
    ],

    "total protein": [
        "total protein",
        "serum total protein"
    ],

    "ige": [
        "ige",
        "immunoglobulin e",
        "immunoglobulin e total"
    ]
}


# =========================================================
# FIND CANONICAL BIOMARKER NAME
# =========================================================

def identify_biomarker(name):

    normalized_name = normalize_text(name)

    if not normalized_name:
        return None

    # Exact match first
    for canonical_name, aliases in BIOMARKER_ALIASES.items():

        for alias in aliases:

            if normalized_name == normalize_text(alias):
                return canonical_name

    # Longest matching alias
    matches = []

    for canonical_name, aliases in BIOMARKER_ALIASES.items():

        for alias in aliases:

            normalized_alias = normalize_text(alias)

            if (
                normalized_alias
                and normalized_alias in normalized_name
            ):
                matches.append(
                    (
                        len(normalized_alias),
                        canonical_name
                    )
                )

    if matches:
        matches.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return matches[0][1]

    return None


# =========================================================
# FIND KNOWLEDGE TOPIC
# =========================================================

def get_topic_aliases(canonical_name):

    topic_aliases = {

        "glucose": [
            "glucose",
            "blood glucose",
            "blood sugar"
        ],

        "hba1c": [
            "hba1c",
            "a1c",
            "glycated hemoglobin",
            "glycated haemoglobin"
        ],

        "hdl": [
            "hdl",
            "cholesterol"
        ],

        "ldl": [
            "ldl",
            "cholesterol"
        ],

        "total cholesterol": [
            "cholesterol"
        ],

        "triglycerides": [
            "triglycerides",
            "cholesterol"
        ],

        "rdw": [
            "rdw",
            "red blood cell"
        ],

        "bilirubin": [
            "bilirubin"
        ],

        "creatinine": [
            "kidney",
            "creatinine"
        ],

        "urea": [
            "urea",
            "kidney"
        ],

        "wbc": [
            "white blood cell",
            "white blood cells",
            "wbc"
        ],

        "platelets": [
            "platelet",
            "platelets"
        ],

        "t3": [
            "thyroid",
            "t3",
            "t4"
        ],

        "t4": [
            "thyroid",
            "t3",
            "t4"
        ],

        "tsh": [
            "thyroid",
            "tsh"
        ],

        "ast": [
            "liver",
            "ast",
            "sgot"
        ],

        "alt": [
            "liver",
            "alt",
            "sgpt"
        ],

        "alkaline phosphatase": [
            "liver",
            "alkaline phosphatase"
        ],

        "gamma glutamyl transferase": [
            "liver",
            "gamma glutamyl transferase",
            "ggt"
        ]
    }

    return topic_aliases.get(
        canonical_name,
        [canonical_name]
    )


# =========================================================
# RAG RETRIEVAL
# =========================================================

def retrieve_knowledge(biomarker):

    name = biomarker.get(
        "name",
        ""
    )

    canonical_name = identify_biomarker(
        name
    )

    normalized_name = normalize_text(
        name
    )

    if not canonical_name:

        return None


    best_match = None
    best_score = 0


    for item in KNOWLEDGE_BASE:

        score = 0

        topic = normalize_text(
            item.get(
                "topic",
                ""
            )
        )

        title = normalize_text(
            item.get(
                "title",
                ""
            )
        )

        keywords = [
            normalize_text(keyword)
            for keyword in item.get(
                "keywords",
                []
            )
        ]


        # -------------------------------------------------
        # EXACT TOPIC MATCH
        # -------------------------------------------------

        if topic == canonical_name:
            score += 100


        # -------------------------------------------------
        # EXACT KEYWORD MATCH
        # -------------------------------------------------

        for keyword in keywords:

            if keyword == canonical_name:
                score += 80

            elif keyword == normalized_name:
                score += 70


        # -------------------------------------------------
        # TITLE MATCH
        # -------------------------------------------------

        if canonical_name in title:
            score += 50


        # -------------------------------------------------
        # TOPIC ALIAS MATCH
        # -------------------------------------------------

        for alias in get_topic_aliases(
            canonical_name
        ):

            alias = normalize_text(alias)

            if not alias:
                continue

            if alias == topic:
                score += 40

            elif alias in keywords:
                score += 30

            elif alias in title:
                score += 20


        if score > best_score:

            best_score = score
            best_match = item


    if best_match and best_score >= 30:

        return best_match


    return None


# =========================================================
# FALLBACK KNOWLEDGE
# =========================================================

def generate_fallback_knowledge(
    biomarker
):

    name = biomarker.get(
        "name",
        "this medical result"
    )

    status = biomarker.get(
        "status",
        "unknown"
    )


    if status == "high":

        explanation = (
            f"{name} is above the reference range "
            "provided by the laboratory. The meaning "
            "of an elevated result depends on what "
            "the test measures and should be interpreted "
            "alongside the other findings and clinical "
            "context."
        )

    elif status == "low":

        explanation = (
            f"{name} is below the reference range "
            "provided by the laboratory. The meaning "
            "of a low result depends on what the test "
            "measures and should be interpreted alongside "
            "the other findings and clinical context."
        )

    else:

        explanation = (
            f"{name} is within the reference range "
            "provided by the laboratory. Reference "
            "ranges are used as one part of interpreting "
            "laboratory results."
        )


    return {

        "title":
            f"Understanding {name}",

        "content":
            explanation,

        "source":
            "General medical knowledge",

        "matched":
            False
    }


# =========================================================
# GET BIOMARKER KNOWLEDGE
# =========================================================

def get_biomarker_knowledge(
    biomarker
):

    knowledge = retrieve_knowledge(
        biomarker
    )


    if knowledge:

        return {

            "title":
                knowledge.get(
                    "title",
                    f"Understanding "
                    f"{biomarker.get('name', '')}"
                ),

            "content":
                knowledge.get(
                    "content",
                    ""
                ),

            "source":
                knowledge.get(
                    "source",
                    "Medical knowledge base"
                ),

            "matched":
                True
        }


    return generate_fallback_knowledge(
        biomarker
    )


# =========================================================
# ANALYZE BIOMARKER
# =========================================================

def analyze_biomarker(
    biomarker,
    lang="en"
):

    name = biomarker.get(
        "name",
        "Unknown biomarker"
    )

    status = biomarker.get(
        "status",
        "unknown"
    )


    knowledge = get_biomarker_knowledge(
        biomarker
    )

    # Localize knowledge if translated entry exists
    if knowledge and lang != "en":
        # Check topic or matched id
        retrieved = retrieve_knowledge(biomarker)
        if retrieved and retrieved.get("id"):
            translated_k = get_knowledge_translation(retrieved["id"], lang)
            if translated_k:
                knowledge = {
                    **knowledge,
                    "title": translated_k.get("title", knowledge["title"]),
                    "content": translated_k.get("content", knowledge["content"]),
                }

    if biomarker.get("status_explanation") and lang == "en":
        status_explanation = biomarker["status_explanation"]
    else:
        status_explanation = get_status_explanation(name, status, lang)

    status_label = biomarker.get("status_label") or get_status_label(status, lang)

    return {

        **biomarker,

        "status_label":
            status_label,

        "status_explanation":
            status_explanation,

        "knowledge":
            knowledge
    }


# =========================================================
# ABNORMAL RESULTS
# =========================================================

def get_abnormal_biomarkers(
    biomarkers
):

    return [

        biomarker

        for biomarker in biomarkers

        if biomarker.get(
            "status"
        ) in [
            "high",
            "low"
        ]
    ]


# =========================================================
# OVERALL IMPRESSION
# =========================================================

def generate_overall_impression(biomarkers, lang="en"):
    """
    Generate a report-level summary of extracted biomarker statuses.

    This is a rule-based summary of reference-range flags. It is not
    a medical diagnosis or a clinical risk assessment.
    """
    phrases = get_impression_phrases(lang)

    if not biomarkers:
        return phrases.get(
            "no_biomarkers",
            "No laboratory biomarkers were confidently identified from this report."
        )

    normal = []
    abnormal = []
    unclassified = []

    for biomarker in biomarkers:
        name = biomarker.get("name", "Unknown biomarker")
        status = str(biomarker.get("status", "unknown")).lower().strip()

        if status == "normal":
            normal.append(name)
        elif status in ("high", "low"):
            abnormal.append(name)
        else:
            unclassified.append(name)

    parts = [
        phrases["identified"].format(
            total=len(biomarkers),
            normal=len(normal),
            abnormal=len(abnormal),
            unclassified=len(unclassified),
        )
    ]

    if abnormal:
        if len(abnormal) == 1:
            names_text = abnormal[0]
        elif len(abnormal) == 2:
            names_text = f"{abnormal[0]} and {abnormal[1]}" if lang == "en" else f"{abnormal[0]}, {abnormal[1]}"
        else:
            names_text = ", ".join(abnormal[:-1]) + f", and {abnormal[-1]}" if lang == "en" else ", ".join(abnormal)

        parts.append(
            phrases["outside_include"].format(names=names_text)
        )
    else:
        parts.append(
            phrases["none_flagged"]
        )

    if unclassified:
        shown_names = unclassified[:5]
        unknown_text = ", ".join(shown_names)

        if len(unclassified) > 5:
            unknown_text += f", and {len(unclassified) - 5} more"

        parts.append(
            phrases["unknown_status"].format(names=unknown_text)
        )

    if abnormal:
        parts.append(phrases["abnormal_note"])
    elif unclassified:
        parts.append(phrases["unknown_note"])
    else:
        parts.append(phrases["all_normal_note"])

    return " ".join(parts)


# =========================================================
# PATTERN DETECTION
# =========================================================
def detect_patterns(
    biomarkers
):

    patterns = []


    # -----------------------------------------------------
    # GLUCOSE
    # -----------------------------------------------------

    if any(

        identify_biomarker(
            item.get("name", "")
        ) == "glucose"

        and item.get("status") == "high"

        for item in biomarkers
    ):

        patterns.append({

            "name":
                "Elevated glucose",

            "description":
                (
                    "The glucose result is above the "
                    "reference range provided in the "
                    "report. Glucose results are generally "
                    "interpreted together with other "
                    "measurements and clinical context."
                )
        })


    # -----------------------------------------------------
    # LIPIDS
    # -----------------------------------------------------

    low_hdl = any(

        identify_biomarker(
            item.get("name", "")
        ) == "hdl"

        and item.get("status") == "low"

        for item in biomarkers
    )


    high_ldl = any(

        identify_biomarker(
            item.get("name", "")
        ) == "ldl"

        and item.get("status") == "high"

        for item in biomarkers
    )


    if low_hdl and high_ldl:

        patterns.append({

            "name":
                "Lipid profile pattern",

            "description":
                (
                    "The report shows both a low HDL "
                    "result and an elevated LDL result. "
                    "These lipid measurements are commonly "
                    "considered together."
                )
        })

    elif low_hdl:

        patterns.append({

            "name":
                "Low HDL",

            "description":
                (
                    "HDL is below the reference range "
                    "provided in the report and is "
                    "interpreted together with the rest "
                    "of the lipid profile."
                )
        })

    elif high_ldl:

        patterns.append({

            "name":
                "Elevated LDL",

            "description":
                (
                    "LDL is above the reference range "
                    "provided in the report and is "
                    "interpreted together with the rest "
                    "of the lipid profile."
                )
        })


    # -----------------------------------------------------
    # RDW
    # -----------------------------------------------------

    if any(

        identify_biomarker(
            item.get("name", "")
        ) == "rdw"

        and item.get("status") == "high"

        for item in biomarkers
    ):

        patterns.append({

            "name":
                "Elevated RDW",

            "description":
                (
                    "RDW is above the reference range. "
                    "It describes variation in red blood "
                    "cell size and is interpreted alongside "
                    "other blood-count measurements."
                )
        })


    # -----------------------------------------------------
    # CRP
    # -----------------------------------------------------

    if any(

        identify_biomarker(
            item.get("name", "")
        ) == "c reactive protein"

        and item.get("status") == "high"

        for item in biomarkers
    ):

        patterns.append({

            "name":
                "Elevated C-reactive protein",

            "description":
                (
                    "C-reactive protein is above the "
                    "reference range provided in the "
                    "report. CRP can increase with "
                    "inflammation, but the result is "
                    "non-specific and needs clinical context."
                )
        })


    # -----------------------------------------------------
    # BILIRUBIN
    # -----------------------------------------------------

    if any(

        identify_biomarker(
            item.get("name", "")
        ) == "bilirubin"

        and item.get("status") == "high"

        for item in biomarkers
    ):

        patterns.append({

            "name":
                "Elevated bilirubin",

            "description":
                (
                    "One or more bilirubin measurements "
                    "are above the provided reference "
                    "range. Bilirubin is interpreted "
                    "together with other relevant results."
                )
        })


    # -----------------------------------------------------
    # WBC
    # -----------------------------------------------------

    if any(

        identify_biomarker(
            item.get("name", "")
        ) == "wbc"

        and item.get("status") == "high"

        for item in biomarkers
    ):

        patterns.append({

            "name":
                "Elevated white blood cell count",

            "description":
                (
                    "The white blood cell count is above "
                    "the reference range provided in the report."
                )
        })


    elif any(

        identify_biomarker(
            item.get("name", "")
        ) == "wbc"

        and item.get("status") == "low"

        for item in biomarkers
    ):

        patterns.append({

            "name":
                "Low white blood cell count",

            "description":
                (
                    "The white blood cell count is below "
                    "the reference range provided in the report."
                )
        })


    # -----------------------------------------------------
    # PLATELETS
    # -----------------------------------------------------

    if any(

        identify_biomarker(
            item.get("name", "")
        ) == "platelets"

        and item.get("status") == "high"

        for item in biomarkers
    ):

        patterns.append({

            "name":
                "Elevated platelet count",

            "description":
                (
                    "The platelet count is above the "
                    "reference range provided in the report."
                )
        })


    elif any(

        identify_biomarker(
            item.get("name", "")
        ) == "platelets"

        and item.get("status") == "low"

        for item in biomarkers
    ):

        patterns.append({

            "name":
                "Low platelet count",

            "description":
                (
                    "The platelet count is below the "
                    "reference range provided in the report."
                )
        })


    return patterns


# =========================================================
# CONCERN LEVEL
# =========================================================

def determine_concern_level(
    biomarkers,
    patterns,
    lang="en"
):

    abnormal = get_abnormal_biomarkers(
        biomarkers
    )


    if not abnormal:
        trans = get_concern_translation("low", lang)
        return {
            "level": "low",
            "label": trans.get("label", "Low concern"),
            "description": trans.get("description", "No analyzed laboratory results were outside their provided reference ranges.")
        }


    if len(abnormal) >= 4:
        trans = get_concern_translation("follow_up_many", lang)
        return {
            "level": "follow_up",
            "label": trans.get("label", "Medical follow-up recommended"),
            "description": trans.get("description", "Several results are outside their provided reference ranges.")
        }


    trans = get_concern_translation("follow_up_few", lang)
    return {
        "level": "follow_up",
        "label": trans.get("label", "Medical follow-up recommended"),
        "description": trans.get("description", "One or more results are outside their provided reference ranges.")
    }


# =========================================================
# DOCTOR QUESTIONS
# =========================================================

def generate_doctor_questions(
    biomarkers,
    patterns,
    lang="en"
):

    abnormal = get_abnormal_biomarkers(
        biomarkers
    )

    templates = get_doctor_question_templates(lang)
    questions = []


    for biomarker in abnormal[:4]:

        name = biomarker.get(
            "name",
            "this result"
        )

        status = biomarker.get(
            "status",
            "abnormal"
        )


        if status == "high":
            questions.append(templates["high"].format(name=name))
        else:
            questions.append(templates["low"].format(name=name))


    if patterns:
        questions.append(templates["patterns_together"])


    questions.append(templates["repeat_monitor"])
    questions.append(templates["additional_testing"])


    unique_questions = []

    for question in questions:

        if question not in unique_questions:

            unique_questions.append(
                question
            )


    return unique_questions[:6]


# =========================================================
# RAG KNOWLEDGE ANALYSIS
# =========================================================

def generate_knowledge_analysis(
    analyzed_biomarkers,
    patterns
):

    knowledge_items = []

    seen = set()


    # -----------------------------------------------------
    # PRIORITY 1:
    # ABNORMAL RESULTS WITH MATCHED KNOWLEDGE
    # -----------------------------------------------------

    for biomarker in analyzed_biomarkers:

        status = biomarker.get(
            "status"
        )

        knowledge = biomarker.get(
            "knowledge"
        )

        if status not in [
            "high",
            "low"
        ]:

            continue


        if not knowledge:
            continue


        if not knowledge.get(
            "matched",
            False
        ):

            continue


        name = biomarker.get(
            "name",
            ""
        )


        key = normalize_text(
            name
        )


        if key in seen:
            continue


        knowledge_items.append({

            "title":
                knowledge.get(
                    "title",
                    f"Understanding {name}"
                ),

            "content":
                knowledge.get(
                    "content",
                    ""
                ),

            "source":
                knowledge.get(
                    "source",
                    "Medical knowledge base"
                ),

            "related_biomarker":
                name
        })


        seen.add(key)


    # -----------------------------------------------------
    # PRIORITY 2:
    # ABNORMAL RESULTS WITHOUT KNOWLEDGE MATCH
    #
    # This gives unfamiliar biomarkers a fallback,
    # but does not flood the section with normal results.
    # -----------------------------------------------------

    for biomarker in analyzed_biomarkers:

        status = biomarker.get(
            "status"
        )

        knowledge = biomarker.get(
            "knowledge"
        )

        if status not in [
            "high",
            "low"
        ]:

            continue


        if not knowledge:
            continue


        name = biomarker.get(
            "name",
            ""
        )


        key = normalize_text(
            name
        )


        if key in seen:
            continue


        knowledge_items.append({

            "title":
                knowledge.get(
                    "title",
                    f"Understanding {name}"
                ),

            "content":
                knowledge.get(
                    "content",
                    ""
                ),

            "source":
                knowledge.get(
                    "source",
                    "General medical knowledge"
                ),

            "related_biomarker":
                name
        })


        seen.add(key)


    # -----------------------------------------------------
    # PRIORITY 3:
    # IMPORTANT DETECTED PATTERNS
    #
    # Add a pattern only if it is not already represented
    # by the biomarker explanation.
    # -----------------------------------------------------

    pattern_knowledge = {

        "elevated glucose":
            (
                "An elevated glucose result can have "
                "different explanations. Glucose is "
                "interpreted using the laboratory reference "
                "range together with related glucose tests "
                "and clinical context."
            ),

        "lipid profile pattern":
            (
                "HDL and LDL are components of the lipid "
                "profile and are commonly interpreted "
                "together with total cholesterol, "
                "triglycerides and other cardiovascular "
                "risk factors."
            ),

        "elevated rdw":
            (
                "An elevated RDW means there is greater "
                "variation in red blood cell size. It is "
                "generally interpreted alongside other "
                "red blood cell measurements."
            ),

        "elevated c reactive protein":
            (
                "An elevated C-reactive protein result "
                "can occur with inflammation, but CRP is "
                "non-specific and does not by itself "
                "identify the cause."
            ),

        "elevated bilirubin":
            (
                "Elevated bilirubin results are interpreted "
                "together with other bilirubin measurements, "
                "liver-related tests and clinical information."
            )
    }


    for pattern in patterns:

        pattern_name = normalize_text(
            pattern.get(
                "name",
                ""
            )
        )


        if pattern_name not in pattern_knowledge:
            continue


        pattern_key = (
            "pattern:"
            + pattern_name
        )


        if pattern_key in seen:
            continue


        knowledge_items.append({

            "title":
                pattern.get(
                    "name",
                    "Detected pattern"
                ),

            "content":
                pattern_knowledge[
                    pattern_name
                ],

            "source":
                "Medical knowledge base",

            "related_biomarker":
                "Detected pattern"
        })


        seen.add(pattern_key)


    # -----------------------------------------------------
    # LIMIT RAG RESULTS
    # -----------------------------------------------------

    return knowledge_items[:8]
# =========================================================
# MAIN REPORT ANALYSIS
# =========================================================

def analyze_report(
    biomarkers,
    lang="en"
):

    if biomarkers is None:
        biomarkers = []

    lang = normalize_language(lang)

    analyzed_biomarkers = []

    for biomarker in biomarkers:

        analyzed_biomarkers.append(
            analyze_biomarker(
                biomarker,
                lang=lang
            )
        )

    raw_patterns = detect_patterns(
        analyzed_biomarkers
    )

    # Localize patterns
    patterns = []
    for pattern in raw_patterns:
        p_name = pattern.get("name", "")
        p_trans = get_pattern_translation(p_name, lang)
        patterns.append({
            "name": p_trans.get("name", p_name),
            "description": p_trans.get("description", pattern.get("description", ""))
        })

    concern_level = determine_concern_level(
        analyzed_biomarkers,
        patterns,
        lang=lang
    )

    impression = generate_overall_impression(
        analyzed_biomarkers,
        lang=lang
    )

    knowledge = generate_knowledge_analysis(
        analyzed_biomarkers,
        raw_patterns
    )

    doctor_questions = generate_doctor_questions(
        analyzed_biomarkers,
        patterns,
        lang=lang
    )

    return {

        "biomarkers":
            analyzed_biomarkers,

        "patterns":
            patterns,

        "impression":
            impression,

        "concern_level":
            concern_level,

        "knowledge":
            knowledge,

        "doctor_questions":
            doctor_questions
    }
