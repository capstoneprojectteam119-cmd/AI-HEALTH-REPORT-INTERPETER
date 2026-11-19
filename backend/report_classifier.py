import re


def classify_report(text):
    """
    Classify a medical report based on its overall structure
    and medical terminology.

    Returns:
        laboratory
        imaging
        general
    """

    text_lower = text.lower()

    # -----------------------------------------
    # Laboratory indicators
    # -----------------------------------------

    laboratory_terms = [
        "hemoglobin",
        "haemoglobin",
        "rbc",
        "wbc",
        "mcv",
        "mch",
        "mchc",
        "rdw",
        "platelet",
        "neutrophils",
        "lymphocytes",
        "monocytes",
        "eosinophils",
        "basophils",
        "serum",
        "plasma",
        "reference range",
        "reference interval",
        "laboratory",
        "mg/dl",
        "g/dl",
        "mmol/l",
        "iu/l",
        "u/l"
    ]

    # -----------------------------------------
    # Imaging indicators
    # -----------------------------------------

    imaging_terms = [
        "ultrasound",
        "sonography",
        "sonographic",
        "x-ray",
        "xray",
        "radiograph",
        "radiology",
        "radiologist",
        "ct scan",
        "computed tomography",
        "mri",
        "magnetic resonance",
        "echotexture",
        "hypoechoic",
        "hyperechoic",
        "lesion",
        "nodule",
        "mass",
        "impression",
        "kidney",
        "liver",
        "gall bladder",
        "gallbladder",
        "pancreas",
        "spleen",
        "uterus",
        "ovary"
    ]

    # -----------------------------------------
    # Count evidence
    # -----------------------------------------

    laboratory_score = sum(
        1
        for term in laboratory_terms
        if term in text_lower
    )

    imaging_score = sum(
        1
        for term in imaging_terms
        if term in text_lower
    )

    # -----------------------------------------
    # Determine report type
    # -----------------------------------------

    if laboratory_score >= 3 and laboratory_score > imaging_score:
        return "laboratory"

    if imaging_score >= 3 and imaging_score > laboratory_score:
        return "imaging"

    return "general"