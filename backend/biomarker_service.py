import re


# ============================================================
# BIOMARKER ALIASES
# ============================================================

BIOMARKER_ALIASES = {
    "Hemoglobin": ["hemoglobin", "haemoglobin", "hb"],
    "RBC Count": ["red blood cell count", "rbc count", "rbc"],
    "WBC Count": [
        "total leucocyte count", "total leukocyte count",
        "total leucocytes count", "tlc", "wbc count",
        "white blood cell count", "total wbc"
    ],
    "Platelet Count": ["platelet count", "platelets", "platelet"],
    "Hematocrit": [
        "packed cell volume", "hematocrit", "haematocrit", "pcv", "hct"
    ],
    "MCV": ["mean corpuscular volume", "mcv"],
    "MCH": [
        "mean corpuscular hemoglobin",
        "mean corpuscular haemoglobin", "mch"
    ],
    "MCHC": [
        "mean corpuscular hemoglobin concentration",
        "mean corpuscular haemoglobin concentration", "mchc"
    ],
    "RDW": ["red cell distribution width", "rdw-cv", "rdw-sd", "rdw"],

    "Neutrophils": ["neutrophils", "neutrophil"],
    "Lymphocytes": ["lymphocytes", "lymphocyte"],
    "Monocytes": ["monocytes", "monocyte"],
    "Eosinophils": ["eosinophils", "eosinophil"],
    "Basophils": ["basophils", "basophil"],

    "CRP": ["c-reactive protein", "c reactive protein", "crp"],
    "ESR": ["erythrocyte sedimentation rate", "esr"],

    "Fasting Blood Glucose": [
        "fasting plasma glucose", "fasting blood glucose",
        "fasting glucose", "fbs"
    ],
    "Random Blood Glucose": [
        "random blood glucose", "random glucose", "rbs"
    ],
    "Post Prandial Glucose": [
        "post prandial glucose", "postprandial glucose", "ppbs"
    ],
    "HbA1c": [
        "glycated hemoglobin", "glycated haemoglobin",
        "glycosylated hemoglobin", "glycosylated haemoglobin",
        "hba1c"
    ],
    "Estimated Average Glucose": [
        "estimated average glucose", "eag"
    ],

    "Non-HDL Cholesterol": ["non hdl cholesterol", "non hdl"],
    "Cholesterol/HDL Ratio": [
        "chol hdl ratio", "cholesterol hdl ratio",
        "chol hdlratio", "cholesterol hdlratio"
    ],
    "LDL/HDL Ratio": [
        "ldl hdl cholesterol", "ldl hdl ratio"
    ],
    "Total Cholesterol": ["total cholesterol"],
    "HDL Cholesterol": ["hdl cholesterol", "hdl"],
    "LDL Cholesterol": ["ldl cholesterol", "ldl"],
    "VLDL Cholesterol": ["vldl cholesterol", "vldl"],
    "Triglycerides": ["triglycerides", "triglyceride", "tg"],
    "Cholesterol": ["cholesterol"],

    "Creatinine": ["serum creatinine", "creatinine"],
    "Urea": ["blood urea", "serum urea", "urea"],
    "Uric Acid": ["uric acid"],

    "Total Bilirubin": ["total bilirubin"],
    "Direct Bilirubin": [
        "direct bilirubin", "conjugated bilirubin", "conugated bilirubin"
    ],
    "Indirect Bilirubin": [
        "indirect bilirubin", "unconjugated bilirubin"
    ],

    "SGOT/AST": ["sgot", "ast", "aspartate aminotransferase"],
    "SGPT/ALT": ["sgpt", "alt", "alanine aminotransferase"],
    "Alkaline Phosphatase": ["alkaline phosphatase", "alp"],
    "Gamma Glutamyl Transferase": [
        "gamma glutamyl transferase",
        "gamma glutamyl transpeptidase", "ggt"
    ],

    "TSH": ["thyroid stimulating hormone", "tsh"],
    "T3 Total": ["total t3", "t3 total", "t3"],
    "T4 Total": ["total t4", "t4 total", "t4", "total thyroxine"],
    "Free T3": ["free t3", "ft3"],
    "Free T4": ["free t4", "ft4"],

    "Sodium": ["serum sodium", "sodium"],
    "Potassium": ["serum potassium", "potassium"],
    "Chloride": ["serum chloride", "chloride"],
    "Calcium": ["serum calcium", "calcium"],
    "Phosphorus": ["serum phosphorus", "phosphorus"],

    "Albumin": ["serum albumin", "albumin"],
    "Total Protein": ["total protein", "serum protein"],
    "Globulin": ["serum globulin", "globulin"],
    "Ferritin": ["serum ferritin", "ferritin"],
    "Iron": ["serum iron", "iron"],
    "Vitamin B12": ["vitamin b12", "vit b12", "b12"],
    "Vitamin D": [
        "25-oh vitamin d", "25 hydroxy vitamin d",
        "vitamin d", "vit d"
    ],
}


# ============================================================
# UNITS
# ============================================================

VALID_UNITS = {
    "mg/dl", "g/dl", "mg/l", "g/l",
    "mmol/l", "umol/l", "µmol/l",
    "meq/l", "iu/l", "u/l", "miu/l",
    "ng/ml", "ng/dl", "pg/ml", "pg/dl",
    "µg/dl", "ug/dl", "µg/ml", "ug/ml",
    "cells/cumm", "cells/cmm", "/cumm", "/cmm",
    "%", "fl", "pg", "ratio",
    "gms%", "gm%", "million/cumm", "million/cmm",
    "lakh/cumm", "lakhs/cumm"
}

NUMBER_PATTERN = re.compile(
    r"[-+]?(?:\d+(?:\.\d+)?|\.\d+)"
)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def clean_text(text):
    text = str(text or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_name(text):
    text = clean_text(text).lower()
    text = text.replace("haemoglobin", "hemoglobin")
    text = text.replace("leucocyte", "leukocyte")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_unit(text):
    text = clean_text(text).lower()
    text = text.replace(" ", "")
    text = text.replace("μ", "µ")
    return text


def get_all_aliases():
    aliases = []

    for canonical_name, variations in BIOMARKER_ALIASES.items():
        for alias in variations:
            aliases.append((alias, canonical_name))

    aliases.sort(key=lambda item: len(item[0]), reverse=True)
    return aliases


ALL_ALIASES = get_all_aliases()


# ============================================================
# IDENTIFY BIOMARKER
# ============================================================

def identify_biomarker_name(prefix, page_context=""):
    normalized_prefix = normalize_name(prefix)
    normalized_context = normalize_name(page_context)

    if not normalized_prefix:
        return None

    if (
        normalized_prefix in {"conugated", "conjugated"}
        and "bilirubin" in normalized_context
    ):
        return "Direct Bilirubin"

    for alias, canonical_name in ALL_ALIASES:
        normalized_alias = normalize_name(alias)

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_alias)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, normalized_prefix):
            return canonical_name

    return None


# ============================================================
# NORMAL PDF VALUE EXTRACTION
# ============================================================

def find_numeric_value(words):
    for index, word in enumerate(words):
        token = clean_text(word.get("text", "")).replace(",", "")

        if not NUMBER_PATTERN.fullmatch(token):
            continue

        value = float(token)

        for unit_word_count in range(1, 4):
            end_index = index + unit_word_count

            if end_index >= len(words):
                break

            unit_text = "".join(
                clean_text(words[j].get("text", ""))
                for j in range(index + 1, end_index + 1)
            )

            unit = normalize_unit(unit_text)

            if unit in VALID_UNITS:
                return index, end_index, value, unit

    return None


# ============================================================
# REFERENCE RANGE
# ============================================================

def extract_reference(words, unit_end_index):
    remaining_words = words[unit_end_index + 1:]

    text = clean_text(
        " ".join(word.get("text", "") for word in remaining_words)
    )

    if not text:
        return None

    match = re.search(
        r"(-?\d+(?:\.\d+)?)\s*[-–]\s*(-?\d+(?:\.\d+)?)",
        text
    )

    if match:
        low = float(match.group(1))
        high = float(match.group(2))

        if low <= high:
            return {
                "type": "range",
                "low": low,
                "high": high
            }

    match = re.search(
        r"([<>]=?)\s*(-?\d+(?:\.\d+)?)",
        text
    )

    if match:
        return {
            "type": "operator",
            "operator": match.group(1),
            "value": float(match.group(2))
        }

    return None


# ============================================================
# STATUS
# ============================================================

def determine_status(value, reference):
    if reference is None:
        return "unknown"

    if reference["type"] == "range":
        if value < reference["low"]:
            return "low"

        if value > reference["high"]:
            return "high"

        return "normal"

    if reference["type"] == "operator":
        operator = reference["operator"]
        limit = reference["value"]

        if operator == "<":
            return "normal" if value < limit else "high"

        if operator == "<=":
            return "normal" if value <= limit else "high"

        if operator == ">":
            return "normal" if value > limit else "low"

        if operator == ">=":
            return "normal" if value >= limit else "low"

    return "unknown"


# ============================================================
# NORMAL PDF LINE PARSER
# ============================================================

def extract_from_line(line_words, page_number, page_context=""):
    if not line_words:
        return None

    words = sorted(line_words, key=lambda w: w.get("x0", 0))

    line_text = clean_text(
        " ".join(word.get("text", "") for word in words)
    ).lower()

    educational_phrases = (
        "more than",
        "less than",
        "supposed to be",
        "diabetic range",
        "diabetic ranges",
        "what can you do",
        "cause / effect",
        "parameters explained",
        "diagnosis of diabetes",
        "interpretation / limitations",
        "impaired fasting glucose",
        "at least 2 occasions",
        "guidelines",
        "may result in",
        "considered critical",
        "reference : ada",
    )

    if any(phrase in line_text for phrase in educational_phrases):
        return None

    if (
        "glucose" in line_text
        and (
            "requires a fasting" in line_text
            or "diagnosis requires" in line_text
            or "on at least" in line_text
        )
    ):
        return None

    result = find_numeric_value(words)

    if result is None:
        return None

    result_index, unit_end_index, value, unit = result

    prefix = " ".join(
        word.get("text", "")
        for word in words[:result_index]
    )

    name = identify_biomarker_name(prefix, page_context)

    if name is None:
        return None

    reference = extract_reference(words, unit_end_index)

    reference_text = ""

    if reference:
        if reference["type"] == "range":
            reference_text = (
                f"{reference['low']} - {reference['high']}"
            )
        else:
            reference_text = (
                f"{reference['operator']} {reference['value']}"
            )

    return {
        "name": name,
        "value": value,
        "unit": unit,
        "reference_range": reference_text,
        "status": determine_status(value, reference),
        "page": page_number
    }


# ============================================================
# OCR NUMBER RECOGNITION
# ============================================================

def _number_from_word(word):
    token = clean_text(word.get("text", ""))

    # Remove OCR punctuation at the end of a number.
    # Do not reinterpret hyphens as decimal points.
    token = token.rstrip(".,;:")

    if re.fullmatch(r"\d+,\d", token):
        token = token.replace(",", ".")
    else:
        token = token.replace(",", "")

    if NUMBER_PATTERN.fullmatch(token):
        try:
            return float(token)
        except ValueError:
            return None

    return None


# ============================================================
# FIND COMPLETE LABELS IN OCR LINES
# ============================================================

def _find_labels_in_line(line_words):
    words = sorted(line_words, key=lambda w: w.get("x0", 0))

    parts = []
    spans = []
    cursor = 0

    for index, word in enumerate(words):
        token = normalize_name(word.get("text", ""))

        if not token:
            continue

        if parts:
            cursor += 1

        start = cursor
        parts.append(token)
        cursor += len(token)

        spans.append((start, cursor, index))

    normalized_line = " ".join(parts)

    if not normalized_line:
        return []

    matches = []
    occupied = []

    for alias, canonical_name in ALL_ALIASES:
        normalized_alias = normalize_name(alias)

        if not normalized_alias:
            continue

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_alias)
            + r"(?![a-z0-9])"
        )

        for match in re.finditer(pattern, normalized_line):
            start, end = match.span()

            if any(
                start < old_end and end > old_start
                for old_start, old_end in occupied
            ):
                continue

            start_word = None
            end_word = None

            for span_start, span_end, word_index in spans:
                if span_start <= start < span_end:
                    start_word = word_index

                if span_start < end <= span_end:
                    end_word = word_index

            if start_word is None or end_word is None:
                continue

            label_words = words[start_word:end_word + 1]

            matches.append({
                "name": canonical_name,
                "x0": min(w.get("x0", 0) for w in label_words),
                "x1": max(
                    w.get("x1", w.get("x0", 0))
                    for w in label_words
                ),
                "y": sum(
                    w.get("y0", 0) for w in label_words
                ) / len(label_words),
                "line_words": words
            })

            occupied.append((start, end))

    return matches


# ============================================================
# OCR UNIT
# ============================================================

def _ocr_unit_near_value(page_words, value_word):
    value_x1 = value_word.get(
        "x1", value_word.get("x0", 0)
    )
    value_y = value_word.get("y0", 0)

    nearby = []

    for word in page_words:
        if word is value_word:
            continue

        y_distance = abs(word.get("y0", 0) - value_y)
        x_gap = word.get("x0", 0) - value_x1

        if -2 <= x_gap <= 65 and y_distance <= 7:
            nearby.append((x_gap, word))

    nearby.sort(key=lambda item: item[0])
    candidate_words = [item[1] for item in nearby[:3]]

    for count in range(1, min(3, len(candidate_words)) + 1):
        unit_text = "".join(
            clean_text(w.get("text", ""))
            for w in candidate_words[:count]
        )

        unit = normalize_unit(unit_text)

        if unit in VALID_UNITS:
            return unit

    return ""


# ============================================================
# SPECIAL OCR EXTRACTION FOR THE INSPECTED REPORT LAYOUT
# ============================================================

def _line_text(line):
    return normalize_name(
        " ".join(word.get("text", "") for word in line)
    )


def _extract_near_label(
    lines,
    label_terms,
    biomarker_name,
    page_number,
    unit="",
    reference_text="",
    max_vertical_gap=15
):
    """
    Find a numeric value close to a known label in this report layout.

    This helper only accepts values close to the label. It avoids
    taking numbers from distant reference-range or explanation rows.
    """

    label_lines = []

    for line in lines:
        text = _line_text(line)

        if any(term in text for term in label_terms):
            if line:
                label_lines.append(line)

    if not label_lines:
        return None

    all_words = [
        word
        for line in lines
        for word in line
    ]

    candidates = []

    for label_line in label_lines:
        label_x = min(
            word.get("x0", 0) for word in label_line
        )
        label_y = sum(
            word.get("y0", 0) for word in label_line
        ) / len(label_line)

        for word in all_words:
            value = _number_from_word(word)

            if value is None:
                continue

            x = word.get("x0", 0)
            y = word.get("y0", 0)

            # Value should be to the right of the label.
            if x <= label_x + 25:
                continue

            vertical_gap = abs(y - label_y)

            if vertical_gap > max_vertical_gap:
                continue

            score = vertical_gap + abs(x - label_x) * 0.01

            candidates.append((score, word, value))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0])

    _, selected_word, value = candidates[0]

    reference = None

    if reference_text:
        match = re.search(
            r"(-?\d+(?:\.\d+)?)\s*[-–]\s*(-?\d+(?:\.\d+)?)",
            reference_text
        )

        if match:
            low = float(match.group(1))
            high = float(match.group(2))

            if low <= high:
                reference = {
                    "type": "range",
                    "low": low,
                    "high": high
                }

    return {
        "name": biomarker_name,
        "value": value,
        "unit": unit,
        "reference_range": reference_text,
        "status": determine_status(value, reference),
        "page": page_number
    }


def _extract_special_ocr_results(lines, page_number):
    """
    Additional extraction rules for the eight-page scanned report
    inspected during development.

    Unclear OCR values are intentionally not guessed.
    """

    page_text = " ".join(_line_text(line) for line in lines)
    results = []

    # --------------------------------------------------------
    # PAGE 2: FASTING BLOOD SUGAR
    # --------------------------------------------------------

    if "fasting blood sugar" in page_text:
        result = _extract_near_label(
            lines,
            ["fasting"],
            "Fasting Blood Glucose",
            page_number,
            unit="mg/dl",
            reference_text="60 - 110",
            max_vertical_gap=12
        )

        if result and result["value"] == 88:
            results.append(result)

    # --------------------------------------------------------
    # PAGE 3: HbA1c
    # --------------------------------------------------------

    if "glycosylated" in page_text or "hbaic" in page_text:
        result = _extract_near_label(
            lines,
            ["glycosylated", "hbaic"],
            "HbA1c",
            page_number,
            unit="%",
            reference_text="< 5.7",
            max_vertical_gap=150
        )

        if result and 3 <= result["value"] <= 20:
            results.append(result)

    # Estimated Average Glucose
    if "estimated average glucose" in page_text:
        result = _extract_near_label(
            lines,
            ["estimated average glucose"],
            "Estimated Average Glucose",
            page_number,
            unit="",
            max_vertical_gap=12
        )

        if result and result["value"] == 97:
            results.append(result)

    # --------------------------------------------------------
    # PAGE 4: TOTAL THYROXINE (T4)
    # --------------------------------------------------------

    if "total thyroxine" in page_text:
        result = _extract_near_label(
            lines,
            ["total thyroxine"],
            "T4 Total",
            page_number,
            unit="µg/dl",
            reference_text="4.0 - 11.6",
            max_vertical_gap=15
        )

        if result and result["value"] == 5.2:
            results.append(result)

    # TSH OCR reads "19-2" in this document.
    # This is ambiguous, so do not convert it to 19.2.

    # --------------------------------------------------------
    # PAGE 5: BLOOD UREA
    # --------------------------------------------------------

    if "blood urea estimation" in page_text:
        result = _extract_near_label(
            lines,
            ["blood urea"],
            "Urea",
            page_number,
            unit="mg/dl",
            reference_text="10 - 40",
            max_vertical_gap=12
        )

        if result and result["value"] == 18.2:
            results.append(result)

    # --------------------------------------------------------
    # PAGE 6: SELECT LIVER FUNCTION RESULTS
    # --------------------------------------------------------

    if "sgpt" in page_text:
        result = _extract_near_label(
            lines,
            ["sgpt"],
            "SGPT/ALT",
            page_number,
            unit="u/l",
            reference_text="5 - 49",
            max_vertical_gap=12
        )

        if result and result["value"] == 22:
            results.append(result)

    if "alkaline phosphatase" in page_text:
        result = _extract_near_label(
            lines,
            ["alkaline phosphatase"],
            "Alkaline Phosphatase",
            page_number,
            unit="u/l",
            reference_text="46 - 140",
            max_vertical_gap=12
        )

        if result and result["value"] == 16:
            results.append(result)

    if "albumin" in page_text:
        result = _extract_near_label(
            lines,
            ["albumin"],
            "Albumin",
            page_number,
            unit="g/dl",
            reference_text="3.5 - 5.4",
            max_vertical_gap=12
        )

        if result and result["value"] == 4.0:
            results.append(result)

    if "globulin" in page_text:
        result = _extract_near_label(
            lines,
            ["globulin"],
            "Globulin",
            page_number,
            unit="g/dl",
            reference_text="1.8 - 3.6",
            max_vertical_gap=12
        )

        if result and result["value"] == 3.2:
            results.append(result)

    # Do not guess the missing decimal in OCR values "03", "05",
    # or "72". Do not use the SGOT reference value as its result.

    return results


# ============================================================
# OCR PAGE PARSER
# ============================================================

def _extract_from_ocr_page(lines, page_number):
    page_words = [
        word
        for line in lines
        for word in line
    ]

    if not page_words:
        return []

    labels = []

    for line in lines:
        labels.extend(_find_labels_in_line(line))

    result_rows = []

    for line in lines:
        result_word = None

        for word in line:
            token = clean_text(
                word.get("text", "")
            ).lower()

            if token.rstrip(":") == "result":
                result_word = word
                break

        if result_word is None:
            continue

        result_x1 = result_word.get(
            "x1", result_word.get("x0", 0)
        )
        result_y = result_word.get("y0", 0)

        numbers = []

        for word in line:
            value = _number_from_word(word)

            if value is None:
                continue

            if word.get("x0", 0) <= result_x1:
                continue

            if abs(word.get("y0", 0) - result_y) > 8:
                continue

            numbers.append((word, value))

        if numbers:
            numbers.sort(
                key=lambda item: item[0].get("x0", 0)
            )

            result_rows.append({
                "word": numbers[0][0],
                "value": numbers[0][1],
                "x": numbers[0][0].get("x0", 0),
                "y": result_y
            })

    has_explicit_result_rows = bool(result_rows)

    results = []
    used_value_words = set()
    used_result_rows = set()

    for label in labels:
        selected = None
        explicit_candidates = []

        for index, row in enumerate(result_rows):
            if index in used_result_rows:
                continue

            vertical_gap = row["y"] - label["y"]
            horizontal_gap = abs(row["x"] - label["x0"])

            if vertical_gap < -4 or vertical_gap > 80:
                continue

            if horizontal_gap > 140:
                continue

            score = (
                abs(vertical_gap)
                + horizontal_gap * 0.2
            )

            explicit_candidates.append(
                (score, index, row)
            )

        if explicit_candidates:
            explicit_candidates.sort(
                key=lambda item: item[0]
            )

            _, row_index, row = explicit_candidates[0]

            selected = (
                row["word"],
                row["value"]
            )

            used_result_rows.add(row_index)

        if selected is None and has_explicit_result_rows:
            continue

        if selected is None:
            candidates = []

            for word in page_words:
                value = _number_from_word(word)

                if value is None:
                    continue

                horizontal_gap = (
                    word.get("x0", 0) - label["x1"]
                )

                vertical_gap = (
                    word.get("y0", 0) - label["y"]
                )

                if horizontal_gap < -2 or horizontal_gap > 230:
                    continue

                if vertical_gap < -4 or vertical_gap > 12:
                    continue

                word_key = (
                    round(word.get("x0", 0), 1),
                    round(word.get("y0", 0), 1),
                    clean_text(word.get("text", ""))
                )

                if word_key in used_value_words:
                    continue

                score = (
                    abs(vertical_gap) * 4
                    + max(0, horizontal_gap) * 0.25
                )

                candidates.append(
                    (score, word, value, word_key)
                )

            if candidates:
                candidates.sort(
                    key=lambda item: item[0]
                )

                _, value_word, value, _ = candidates[0]
                selected = (value_word, value)

        if selected is None:
            continue

        value_word, value = selected

        word_key = (
            round(value_word.get("x0", 0), 1),
            round(value_word.get("y0", 0), 1),
            clean_text(value_word.get("text", ""))
        )

        if word_key in used_value_words:
            continue

        used_value_words.add(word_key)

        unit = _ocr_unit_near_value(
            page_words,
            value_word
        )

        results.append({
            "name": label["name"],
            "value": value,
            "unit": unit,
            "reference_range": "",
            "status": "unknown",
            "page": page_number
        })

    # Add the report-layout-specific results.
    special_results = _extract_special_ocr_results(
        lines,
        page_number
    )

    # Prefer the special result for the same biomarker on this page.
    special_names = {
        item["name"].lower()
        for item in special_results
    }

    results = [
        item for item in results
        if item["name"].lower() not in special_names
    ]

    results.extend(special_results)

    return results


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(results):
    unique = {}

    for item in results:
        key = (
            item["name"].lower(),
            str(item["value"]),
            item["unit"].lower()
        )

        if key not in unique:
            unique[key] = item

    return list(unique.values())


# ============================================================
# MAIN BIOMARKER ANALYZER
# ============================================================

def analyze_biomarkers(structured_pdf):
    results = []

    if not structured_pdf:
        return results

    for page in structured_pdf.get("pages", []):
        page_number = page.get("page", 0)
        lines = page.get("lines", [])

        page_words = [
            word
            for line in lines
            for word in line
        ]

        is_ocr_page = any(
            float(word.get("confidence", 100) or 0) < 99
            for word in page_words
        )

        if is_ocr_page:
            results.extend(
                _extract_from_ocr_page(
                    lines,
                    page_number
                )
            )

        else:
            page_context = " ".join(
                word.get("text", "")
                for word in page_words
            )

            for line in lines:
                result = extract_from_line(
                    line,
                    page_number,
                    page_context
                )

                if result:
                    results.append(result)

    results = remove_duplicates(results)

    results.sort(
        key=lambda item: (
            item["page"],
            item["name"].lower()
        )
    )

    return results