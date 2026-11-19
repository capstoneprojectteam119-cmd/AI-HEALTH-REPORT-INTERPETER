"""
Backend translation service for the AI Health Report Interpreter.

Provides localised versions of all user-facing text that the
local analysis pipeline generates (impressions, patterns, concern
levels, doctor questions, knowledge explanations, status labels).

Design decisions
────────────────
• Fixed analysis strings are stored as pre-written dictionaries
  — no external API is needed for these.
• Gemini OCR already translates its own output when configured.
• Biomarker numerical values, units and reference ranges are
  NEVER modified.
• English canonical biomarker identifiers are always preserved
  internally.
"""

# =========================================================
# SUPPORTED LANGUAGES
# =========================================================

SUPPORTED_LANGUAGES = {"en", "hi", "te", "ta", "kn", "ml", "mr", "bn"}

# Map legacy full-name values to ISO codes (backward compat)
LANGUAGE_NAME_MAP = {
    "english": "en",
    "hindi": "hi",
    "telugu": "te",
    "tamil": "ta",
    "kannada": "kn",
    "malayalam": "ml",
    "marathi": "mr",
    "bengali": "bn",
}


def normalize_language(raw):
    """Return a valid ISO language code, defaulting to 'en'."""
    if not raw:
        return "en"
    code = str(raw).strip().lower()
    if code in SUPPORTED_LANGUAGES:
        return code
    mapped = LANGUAGE_NAME_MAP.get(code)
    return mapped if mapped else "en"


# =========================================================
# STATUS LABELS
# =========================================================

STATUS_LABELS = {
    "en": {"high": "High", "low": "Low", "normal": "Normal", "unknown": "Unknown"},
    "hi": {"high": "अधिक", "low": "कम", "normal": "सामान्य", "unknown": "अज्ञात"},
    "te": {"high": "ఎక్కువ", "low": "తక్కువ", "normal": "సాధారణం", "unknown": "తెలియదు"},
    "ta": {"high": "அதிகம்", "low": "குறைவு", "normal": "இயல்பானது", "unknown": "தெரியவில்லை"},
    "kn": {"high": "ಹೆಚ್ಚು", "low": "ಕಡಿಮೆ", "normal": "ಸಾಮಾನ್ಯ", "unknown": "ತಿಳಿದಿಲ್ಲ"},
    "ml": {"high": "ഉയർന്നത്", "low": "കുറഞ്ഞത്", "normal": "സാധാരണം", "unknown": "അജ്ഞാതം"},
    "mr": {"high": "जास्त", "low": "कमी", "normal": "सामान्य", "unknown": "अज्ञात"},
    "bn": {"high": "বেশি", "low": "কম", "normal": "স্বাভাবিক", "unknown": "অজানা"},
}


def get_status_label(status, lang):
    """Return localised status label text."""
    labels = STATUS_LABELS.get(lang, STATUS_LABELS["en"])
    return labels.get(status, labels.get("unknown", "Unknown"))


# =========================================================
# CONCERN LEVEL LABELS & DESCRIPTIONS
# =========================================================

CONCERN_TRANSLATIONS = {
    "en": {
        "low": {
            "label": "Low concern",
            "description": "No analyzed laboratory results were outside their provided reference ranges.",
        },
        "follow_up_many": {
            "label": "Medical follow-up recommended",
            "description": (
                "Several results are outside their provided reference ranges. "
                "The findings should be reviewed with a healthcare professional, "
                "especially when considered together."
            ),
        },
        "follow_up_few": {
            "label": "Medical follow-up recommended",
            "description": (
                "One or more results are outside their provided reference ranges. "
                "These findings may have different causes and should be interpreted "
                "in clinical context."
            ),
        },
        "imaging_follow_up": {
            "label": "Medical follow-up recommended",
            "description": (
                "The imaging report describes urinary stones and/or urinary tract "
                "dilation. Please discuss these findings with a healthcare "
                "professional for assessment and appropriate follow-up."
            ),
        },
        "imaging_review": {
            "label": "Clinical review recommended",
            "description": (
                "Imaging findings should be interpreted with symptoms, medical "
                "history and clinical examination."
            ),
        },
    },
    "hi": {
        "low": {
            "label": "कम चिंता",
            "description": "विश्लेषित प्रयोगशाला परिणामों में से कोई भी उनकी संदर्भ सीमा से बाहर नहीं था।",
        },
        "follow_up_many": {
            "label": "चिकित्सा अनुवर्ती अनुशंसित",
            "description": (
                "कई परिणाम उनकी संदर्भ सीमा से बाहर हैं। "
                "इन निष्कर्षों की एक स्वास्थ्य पेशेवर के साथ समीक्षा की जानी चाहिए, "
                "विशेष रूप से जब इन्हें एक साथ देखा जाए।"
            ),
        },
        "follow_up_few": {
            "label": "चिकित्सा अनुवर्ती अनुशंसित",
            "description": (
                "एक या अधिक परिणाम उनकी संदर्भ सीमा से बाहर हैं। "
                "इन निष्कर्षों के विभिन्न कारण हो सकते हैं और इनकी "
                "नैदानिक संदर्भ में व्याख्या की जानी चाहिए।"
            ),
        },
        "imaging_follow_up": {
            "label": "चिकित्सा अनुवर्ती अनुशंसित",
            "description": (
                "इमेजिंग रिपोर्ट में मूत्र पथरी और/या मूत्र पथ फैलाव का वर्णन है। "
                "कृपया इन निष्कर्षों पर मूल्यांकन और उचित अनुवर्ती के लिए "
                "स्वास्थ्य पेशेवर से चर्चा करें।"
            ),
        },
        "imaging_review": {
            "label": "नैदानिक समीक्षा अनुशंसित",
            "description": (
                "इमेजिंग निष्कर्षों की व्याख्या लक्षणों, चिकित्सा इतिहास "
                "और नैदानिक परीक्षण के साथ की जानी चाहिए।"
            ),
        },
    },
    "te": {
        "low": {
            "label": "తక్కువ ఆందోళన",
            "description": "విశ్లేషించిన ప్రయోగశాల ఫలితాలు ఏవీ వాటి సూచన పరిధి బయట లేవు.",
        },
        "follow_up_many": {
            "label": "వైద్య ఫాలో-అప్ సిఫార్సు",
            "description": (
                "అనేక ఫలితాలు వాటి సూచన పరిధి బయట ఉన్నాయి. "
                "ఈ ఫలితాలను ఆరోగ్య నిపుణులతో సమీక్షించాలి, "
                "ముఖ్యంగా వాటిని కలిపి పరిగణించినప్పుడు."
            ),
        },
        "follow_up_few": {
            "label": "వైద్య ఫాలో-అప్ సిఫార్సు",
            "description": (
                "ఒకటి లేదా అంతకంటే ఎక్కువ ఫలితాలు వాటి సూచన పరిధి బయట ఉన్నాయి. "
                "ఈ ఫలితాలకు వివిధ కారణాలు ఉండవచ్చు మరియు వాటిని "
                "వైద్య సందర్భంలో అర్థం చేసుకోవాలి."
            ),
        },
        "imaging_follow_up": {
            "label": "వైద్య ఫాలో-అప్ సిఫార్సు",
            "description": (
                "ఇమేజింగ్ నివేదిక మూత్ర రాళ్లు మరియు/లేదా మూత్ర నాళం విస్తరణను వివరిస్తుంది. "
                "దయచేసి ఈ ఫలితాలను ఆరోగ్య నిపుణులతో చర్చించండి."
            ),
        },
        "imaging_review": {
            "label": "వైద్య సమీక్ష సిఫార్సు",
            "description": (
                "ఇమేజింగ్ ఫలితాలను లక్షణాలు, వైద్య చరిత్ర "
                "మరియు వైద్య పరీక్షతో అర్థం చేసుకోవాలి."
            ),
        },
    },
    "ta": {
        "low": {
            "label": "குறைந்த கவலை",
            "description": "பகுப்பாய்வு செய்யப்பட்ட ஆய்வக முடிவுகள் எதுவும் குறிப்பு வரம்பிற்கு வெளியே இல்லை.",
        },
        "follow_up_many": {
            "label": "மருத்துவ பின்தொடர்வு பரிந்துரைக்கப்படுகிறது",
            "description": (
                "பல முடிவுகள் குறிப்பு வரம்பிற்கு வெளியே உள்ளன. "
                "இந்த கண்டுபிடிப்புகளை சுகாதார நிபுணருடன் மதிப்பாய்வு செய்ய வேண்டும், "
                "குறிப்பாக ஒன்றாகக் கருதும்போது."
            ),
        },
        "follow_up_few": {
            "label": "மருத்துவ பின்தொடர்வு பரிந்துரைக்கப்படுகிறது",
            "description": (
                "ஒன்று அல்லது அதற்கு மேற்பட்ட முடிவுகள் குறிப்பு வரம்பிற்கு வெளியே உள்ளன. "
                "இந்த கண்டுபிடிப்புகளுக்கு வெவ்வேறு காரணங்கள் இருக்கலாம், "
                "மருத்துவ சூழலில் விளக்கப்பட வேண்டும்."
            ),
        },
        "imaging_follow_up": {
            "label": "மருத்துவ பின்தொடர்வு பரிந்துரைக்கப்படுகிறது",
            "description": (
                "இமேஜிங் அறிக்கை சிறுநீர் கற்கள் மற்றும்/அல்லது சிறுநீர் பாதை விரிவாக்கத்தை விவரிக்கிறது. "
                "தயவுசெய்து இந்த கண்டுபிடிப்புகளை சுகாதார நிபுணருடன் விவாதிக்கவும்."
            ),
        },
        "imaging_review": {
            "label": "மருத்துவ மதிப்பாய்வு பரிந்துரைக்கப்படுகிறது",
            "description": (
                "இமேஜிங் கண்டுபிடிப்புகளை அறிகுறிகள், மருத்துவ வரலாறு "
                "மற்றும் மருத்துவ பரிசோதனையுடன் விளக்க வேண்டும்."
            ),
        },
    },
    "kn": {
        "low": {
            "label": "ಕಡಿಮೆ ಆತಂಕ",
            "description": "ವಿಶ್ಲೇಷಿಸಿದ ಪ್ರಯೋಗಾಲಯ ಫಲಿತಾಂಶಗಳು ಯಾವುದೂ ಅವುಗಳ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಯ ಹೊರಗೆ ಇರಲಿಲ್ಲ.",
        },
        "follow_up_many": {
            "label": "ವೈದ್ಯಕೀಯ ಅನುಸರಣೆ ಶಿಫಾರಸು",
            "description": (
                "ಹಲವಾರು ಫಲಿತಾಂಶಗಳು ಅವುಗಳ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಯ ಹೊರಗಿವೆ. "
                "ಈ ಫಲಿತಾಂಶಗಳನ್ನು ಆರೋಗ್ಯ ವೃತ್ತಿಪರರೊಂದಿಗೆ ಪರಿಶೀಲಿಸಬೇಕು."
            ),
        },
        "follow_up_few": {
            "label": "ವೈದ್ಯಕೀಯ ಅನುಸರಣೆ ಶಿಫಾರಸು",
            "description": (
                "ಒಂದು ಅಥವಾ ಹೆಚ್ಚಿನ ಫಲಿತಾಂಶಗಳು ಅವುಗಳ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಯ ಹೊರಗಿವೆ. "
                "ಈ ಫಲಿತಾಂಶಗಳಿಗೆ ವಿವಿಧ ಕಾರಣಗಳಿರಬಹುದು ಮತ್ತು ವೈದ್ಯಕೀಯ ಸಂದರ್ಭದಲ್ಲಿ ಅರ್ಥೈಸಬೇಕು."
            ),
        },
        "imaging_follow_up": {
            "label": "ವೈದ್ಯಕೀಯ ಅನುಸರಣೆ ಶಿಫಾರಸು",
            "description": (
                "ಇಮೇಜಿಂಗ್ ವರದಿಯಲ್ಲಿ ಮೂತ್ರನಾಳದ ಕಲ್ಲುಗಳು ಮತ್ತು/ಅಥವಾ ಮೂತ್ರನಾಳ ಹಿಗ್ಗುವಿಕೆಯ ವಿವರಣೆಯಿದೆ. "
                "ದಯವಿಟ್ಟು ಈ ಫಲಿತಾಂಶಗಳನ್ನು ಆರೋಗ್ಯ ವೃತ್ತಿಪರರೊಂದಿಗೆ ಚರ್ಚಿಸಿ."
            ),
        },
        "imaging_review": {
            "label": "ವೈದ್ಯಕೀಯ ಪರಿಶೀಲನೆ ಶಿಫಾರಸು",
            "description": (
                "ಇಮೇಜಿಂಗ್ ಫಲಿತಾಂಶಗಳನ್ನು ರೋಗಲಕ್ಷಣಗಳು, ವೈದ್ಯಕೀಯ ಇತಿಹಾಸ "
                "ಮತ್ತು ವೈದ್ಯಕೀಯ ಪರೀಕ್ಷೆಯೊಂದಿಗೆ ಅರ್ಥೈಸಬೇಕು."
            ),
        },
    },
    "ml": {
        "low": {
            "label": "കുറഞ്ഞ ആശങ്ക",
            "description": "വിശകലനം ചെയ്ത ലാബ് ഫലങ്ങൾ ഒന്നും അവയുടെ റഫറൻസ് ശ്രേണിക്ക് പുറത്തല്ല.",
        },
        "follow_up_many": {
            "label": "മെഡിക്കൽ ഫോളോ-അപ്പ് ശുപാർശ",
            "description": (
                "നിരവധി ഫലങ്ങൾ അവയുടെ റഫറൻസ് ശ്രേണിക്ക് പുറത്താണ്. "
                "ഈ കണ്ടെത്തലുകൾ ആരോഗ്യ പ്രൊഫഷണലുമായി അവലോകനം ചെയ്യണം."
            ),
        },
        "follow_up_few": {
            "label": "മെഡിക്കൽ ഫോളോ-അപ്പ് ശുപാർശ",
            "description": (
                "ഒന്നോ അതിലധികമോ ഫലങ്ങൾ അവയുടെ റഫറൻസ് ശ്രേണിക്ക് പുറത്താണ്. "
                "ഈ കണ്ടെത്തലുകൾക്ക് വ്യത്യസ്ത കാരണങ്ങൾ ഉണ്ടാകാം, "
                "ക്ലിനിക്കൽ സന്ദർഭത്തിൽ വ്യാഖ്യാനിക്കണം."
            ),
        },
        "imaging_follow_up": {
            "label": "മെഡിക്കൽ ഫോളോ-അപ്പ് ശുപാർശ",
            "description": (
                "ഇമേജിംഗ് റിപ്പോർട്ടിൽ മൂത്രാശയ കല്ലുകളും/അല്ലെങ്കിൽ മൂത്രനാള വികാസവും വിവരിച്ചിരിക്കുന്നു. "
                "ദയവായി ഈ കണ്ടെത്തലുകൾ ആരോഗ്യ പ്രൊഫഷണലുമായി ചർച്ച ചെയ്യുക."
            ),
        },
        "imaging_review": {
            "label": "ക്ലിനിക്കൽ അവലോകനം ശുപാർശ",
            "description": (
                "ഇമേജിംഗ് കണ്ടെത്തലുകൾ ലക്ഷണങ്ങൾ, മെഡിക്കൽ ചരിത്രം, "
                "ക്ലിനിക്കൽ പരിശോധന എന്നിവ ഉപയോഗിച്ച് വ്യാഖ്യാനിക്കണം."
            ),
        },
    },
    "mr": {
        "low": {
            "label": "कमी चिंता",
            "description": "विश्लेषित प्रयोगशाळा निकालांपैकी कोणताही त्यांच्या संदर्भ श्रेणीबाहेर नव्हता.",
        },
        "follow_up_many": {
            "label": "वैद्यकीय पाठपुरावा अनुशंसित",
            "description": (
                "अनेक निकाल त्यांच्या संदर्भ श्रेणीबाहेर आहेत. "
                "या निष्कर्षांचे आरोग्य व्यावसायिकांसोबत पुनरावलोकन करावे."
            ),
        },
        "follow_up_few": {
            "label": "वैद्यकीय पाठपुरावा अनुशंसित",
            "description": (
                "एक किंवा अधिक निकाल त्यांच्या संदर्भ श्रेणीबाहेर आहेत. "
                "या निष्कर्षांची विविध कारणे असू शकतात आणि नैदानिक संदर्भात अर्थ लावावा."
            ),
        },
        "imaging_follow_up": {
            "label": "वैद्यकीय पाठपुरावा अनुशंसित",
            "description": (
                "इमेजिंग अहवालात मूत्र खडे आणि/किंवा मूत्रमार्ग विस्ताराचे वर्णन आहे. "
                "कृपया या निष्कर्षांबद्दल आरोग्य व्यावसायिकांशी चर्चा करा."
            ),
        },
        "imaging_review": {
            "label": "नैदानिक पुनरावलोकन अनुशंसित",
            "description": (
                "इमेजिंग निष्कर्षांचा अर्थ लक्षणे, वैद्यकीय इतिहास "
                "आणि नैदानिक तपासणीसह लावावा."
            ),
        },
    },
    "bn": {
        "low": {
            "label": "কম উদ্বেগ",
            "description": "বিশ্লেষিত ল্যাব ফলাফলের কোনোটিই তাদের রেফারেন্স রেঞ্জের বাইরে ছিল না।",
        },
        "follow_up_many": {
            "label": "চিকিৎসা ফলো-আপ প্রস্তাবিত",
            "description": (
                "বেশ কিছু ফলাফল তাদের রেফারেন্স রেঞ্জের বাইরে। "
                "এই ফলাফলগুলি একজন স্বাস্থ্য পেশাদারের সাথে পর্যালোচনা করা উচিত।"
            ),
        },
        "follow_up_few": {
            "label": "চিকিৎসা ফলো-আপ প্রস্তাবিত",
            "description": (
                "এক বা একাধিক ফলাফল তাদের রেফারেন্স রেঞ্জের বাইরে। "
                "এই ফলাফলগুলির বিভিন্ন কারণ থাকতে পারে এবং "
                "ক্লিনিক্যাল প্রেক্ষাপটে ব্যাখ্যা করা উচিত।"
            ),
        },
        "imaging_follow_up": {
            "label": "চিকিৎসা ফলো-আপ প্রস্তাবিত",
            "description": (
                "ইমেজিং রিপোর্টে মূত্রনালীর পাথর এবং/অথবা মূত্রনালীর প্রসারণের বর্ণনা আছে। "
                "অনুগ্রহ করে এই ফলাফলগুলি একজন স্বাস্থ্য পেশাদারের সাথে আলোচনা করুন।"
            ),
        },
        "imaging_review": {
            "label": "ক্লিনিক্যাল পর্যালোচনা প্রস্তাবিত",
            "description": (
                "ইমেজিং ফলাফলগুলি উপসর্গ, চিকিৎসা ইতিহাস "
                "এবং ক্লিনিক্যাল পরীক্ষার সাথে ব্যাখ্যা করা উচিত।"
            ),
        },
    },
}


def get_concern_translation(concern_key, lang):
    """Return localised concern label+description dict."""
    lang_dict = CONCERN_TRANSLATIONS.get(lang, CONCERN_TRANSLATIONS["en"])
    return lang_dict.get(concern_key, CONCERN_TRANSLATIONS["en"].get(concern_key, {}))


# =========================================================
# REPORT-TYPE DISPLAY LABELS
# =========================================================

REPORT_TYPE_LABELS = {
    "en": {"laboratory": "Laboratory", "imaging": "Imaging", "general": "General"},
    "hi": {"laboratory": "प्रयोगशाला", "imaging": "इमेजिंग", "general": "सामान्य"},
    "te": {"laboratory": "ప్రయోగశాల", "imaging": "ఇమేజింగ్", "general": "సాధారణ"},
    "ta": {"laboratory": "ஆய்வகம்", "imaging": "இமேஜிங்", "general": "பொதுவான"},
    "kn": {"laboratory": "ಪ್ರಯೋಗಾಲಯ", "imaging": "ಇಮೇಜಿಂಗ್", "general": "ಸಾಮಾನ್ಯ"},
    "ml": {"laboratory": "ലാബ്", "imaging": "ഇമേജിംഗ്", "general": "പൊതുവായ"},
    "mr": {"laboratory": "प्रयोगशाळा", "imaging": "इमेजिंग", "general": "सामान्य"},
    "bn": {"laboratory": "ল্যাব", "imaging": "ইমেজিং", "general": "সাধারণ"},
}


# =========================================================
# BIOMARKER STATUS EXPLANATION TEMPLATES
# =========================================================

STATUS_EXPLANATION_TEMPLATES = {
    "en": {
        "high": "{name} is above the reference range provided in the report.",
        "low": "{name} is below the reference range provided in the report.",
        "normal": "{name} is within the reference range provided in the report.",
        "unknown": "The result for {name} could not be confidently classified using the available reference information.",
    },
    "hi": {
        "high": "{name} रिपोर्ट में दी गई संदर्भ सीमा से ऊपर है।",
        "low": "{name} रिपोर्ट में दी गई संदर्भ सीमा से नीचे है।",
        "normal": "{name} रिपोर्ट में दी गई संदर्भ सीमा के भीतर है।",
        "unknown": "{name} के परिणाम को उपलब्ध संदर्भ जानकारी से विश्वसनीय रूप से वर्गीकृत नहीं किया जा सका।",
    },
    "te": {
        "high": "{name} నివేదికలో అందించిన సూచన పరిధి కంటే ఎక్కువగా ఉంది.",
        "low": "{name} నివేదికలో అందించిన సూచన పరిధి కంటే తక్కువగా ఉంది.",
        "normal": "{name} నివేదికలో అందించిన సూచన పరిధిలో ఉంది.",
        "unknown": "{name} ఫలితాన్ని అందుబాటులో ఉన్న సూచన సమాచారంతో విశ్వసనీయంగా వర్గీకరించలేకపోయింది.",
    },
    "ta": {
        "high": "{name} அறிக்கையில் வழங்கப்பட்ட குறிப்பு வரம்பை விட அதிகமாக உள்ளது.",
        "low": "{name} அறிக்கையில் வழங்கப்பட்ட குறிப்பு வரம்பை விட குறைவாக உள்ளது.",
        "normal": "{name} அறிக்கையில் வழங்கப்பட்ட குறிப்பு வரம்பிற்குள் உள்ளது.",
        "unknown": "{name} முடிவை கிடைக்கும் குறிப்பு தகவலைக் கொண்டு நம்பகமாக வகைப்படுத்த முடியவில்லை.",
    },
    "kn": {
        "high": "{name} ವರದಿಯಲ್ಲಿ ನೀಡಲಾದ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಹೆಚ್ಚಿದೆ.",
        "low": "{name} ವರದಿಯಲ್ಲಿ ನೀಡಲಾದ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಕಡಿಮೆಯಾಗಿದೆ.",
        "normal": "{name} ವರದಿಯಲ್ಲಿ ನೀಡಲಾದ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಯೊಳಗಿದೆ.",
        "unknown": "{name} ಫಲಿತಾಂಶವನ್ನು ಲಭ್ಯವಿರುವ ಉಲ್ಲೇಖ ಮಾಹಿತಿಯಿಂದ ವಿಶ್ವಾಸಾರ್ಹವಾಗಿ ವರ್ಗೀಕರಿಸಲಾಗಲಿಲ್ಲ.",
    },
    "ml": {
        "high": "{name} റിപ്പോർട്ടിൽ നൽകിയ റഫറൻസ് ശ്രേണിയേക്കാൾ ഉയർന്നതാണ്.",
        "low": "{name} റിപ്പോർട്ടിൽ നൽകിയ റഫറൻസ് ശ്രേണിയേക്കാൾ കുറവാണ്.",
        "normal": "{name} റിപ്പോർട്ടിൽ നൽകിയ റഫറൻസ് ശ്രേണിക്കുള്ളിലാണ്.",
        "unknown": "{name} ഫലം ലഭ്യമായ റഫറൻസ് വിവരങ്ങൾ ഉപയോഗിച്ച് വിശ്വസനീയമായി വർഗ്ഗീകരിക്കാൻ കഴിഞ്ഞില്ല.",
    },
    "mr": {
        "high": "{name} अहवालात दिलेल्या संदर्भ श्रेणीपेक्षा जास्त आहे.",
        "low": "{name} अहवालात दिलेल्या संदर्भ श्रेणीपेक्षा कमी आहे.",
        "normal": "{name} अहवालात दिलेल्या संदर्भ श्रेणीत आहे.",
        "unknown": "{name} चा निकाल उपलब्ध संदर्भ माहितीवरून विश्वासार्हपणे वर्गीकृत करता आला नाही.",
    },
    "bn": {
        "high": "{name} রিপোর্টে দেওয়া রেফারেন্স রেঞ্জের উপরে আছে।",
        "low": "{name} রিপোর্টে দেওয়া রেফারেন্স রেঞ্জের নিচে আছে।",
        "normal": "{name} রিপোর্টে দেওয়া রেফারেন্স রেঞ্জের মধ্যে আছে।",
        "unknown": "{name}-এর ফলাফল উপলব্ধ রেফারেন্স তথ্য দিয়ে নির্ভরযোগ্যভাবে শ্রেণীবদ্ধ করা যায়নি।",
    },
}


def get_status_explanation(name, status, lang):
    """Return localised status explanation for a biomarker."""
    templates = STATUS_EXPLANATION_TEMPLATES.get(lang, STATUS_EXPLANATION_TEMPLATES["en"])
    template = templates.get(status, templates.get("unknown", "{name}"))
    return template.format(name=name)


# =========================================================
# OVERALL IMPRESSION HELPER PHRASES
# =========================================================

IMPRESSION_PHRASES = {
    "en": {
        "identified": "The system identified {total} biomarker result(s): {normal} within the provided reference ranges, {abnormal} outside those ranges, and {unclassified} that could not be confidently classified.",
        "outside_include": "Results outside the supplied ranges include: {names}.",
        "none_flagged": "No analyzed biomarker result was flagged as high or low.",
        "unknown_status": "The system could not determine a status for {names}. Check whether the report provides a usable reference range and whether the extracted value and unit are correct.",
        "abnormal_note": "These flags reflect the reference ranges printed in the report. They should be interpreted with the complete report and relevant clinical context, and discussed with a healthcare professional when appropriate.",
        "unknown_note": "Because some results could not be classified, this summary does not establish that all results are normal.",
        "all_normal_note": "No analyzed result was flagged outside the ranges printed in the report. This does not rule out every possible health issue.",
        "no_biomarkers": "No laboratory biomarkers were confidently identified from this report. Check the extracted report text or review the original document.",
    },
    "hi": {
        "identified": "सिस्टम ने {total} बायोमार्कर परिणाम(ओं) की पहचान की: {normal} दी गई संदर्भ सीमा के भीतर, {abnormal} उन सीमाओं से बाहर, और {unclassified} जिन्हें विश्वसनीय रूप से वर्गीकृत नहीं किया जा सका।",
        "outside_include": "दी गई सीमा से बाहर परिणामों में शामिल हैं: {names}।",
        "none_flagged": "किसी भी विश्लेषित बायोमार्कर परिणाम को उच्च या निम्न के रूप में चिह्नित नहीं किया गया।",
        "unknown_status": "सिस्टम {names} की स्थिति निर्धारित नहीं कर सका। जांचें कि रिपोर्ट में उपयोग योग्य संदर्भ सीमा है और निकाला गया मूल्य और इकाई सही है।",
        "abnormal_note": "ये चिह्न रिपोर्ट में मुद्रित संदर्भ सीमाओं को दर्शाते हैं। इनकी व्याख्या पूरी रिपोर्ट और प्रासंगिक नैदानिक संदर्भ के साथ की जानी चाहिए।",
        "unknown_note": "चूंकि कुछ परिणामों को वर्गीकृत नहीं किया जा सका, इसलिए यह सारांश स्थापित नहीं करता कि सभी परिणाम सामान्य हैं।",
        "all_normal_note": "किसी भी विश्लेषित परिणाम को रिपोर्ट में मुद्रित सीमाओं से बाहर चिह्नित नहीं किया गया। यह हर संभव स्वास्थ्य समस्या को बाहर नहीं करता।",
        "no_biomarkers": "इस रिपोर्ट से कोई प्रयोगशाला बायोमार्कर विश्वसनीय रूप से पहचाने नहीं गए। निकाली गई रिपोर्ट पाठ की जांच करें या मूल दस्तावेज़ की समीक्षा करें।",
    },
    "te": {
        "identified": "సిస్టమ్ {total} బయోమార్కర్ ఫలితాల(ను) గుర్తించింది: {normal} అందించిన సూచన పరిధిలో, {abnormal} ఆ పరిధి బయట, మరియు {unclassified} విశ్వసనీయంగా వర్గీకరించలేకపోయింది.",
        "outside_include": "అందించిన పరిధి బయట ఫలితాలు: {names}.",
        "none_flagged": "ఏ విశ్లేషించిన బయోమార్కర్ ఫలితం ఎక్కువ లేదా తక్కువగా గుర్తించబడలేదు.",
        "unknown_status": "సిస్టమ్ {names} స్థితిని నిర్ధారించలేకపోయింది.",
        "abnormal_note": "ఈ గుర్తులు నివేదికలో ముద్రించిన సూచన పరిధులను ప్రతిబింబిస్తాయి. పూర్తి నివేదిక మరియు వైద్య సందర్భంతో వ్యాఖ్యానించాలి.",
        "unknown_note": "కొన్ని ఫలితాలు వర్గీకరించలేనందున, అన్ని ఫలితాలు సాధారణమని ఈ సారాంశం స్థాపించదు.",
        "all_normal_note": "నివేదికలో ముద్రించిన పరిధి బయట ఏ ఫలితం గుర్తించబడలేదు. ఇది ప్రతి సాధ్యమైన ఆరోగ్య సమస్యను తోసిపుచ్చదు.",
        "no_biomarkers": "ఈ నివేదిక నుండి ప్రయోగశాల బయోమార్కర్లు విశ్వసనీయంగా గుర్తించబడలేదు.",
    },
    "ta": {
        "identified": "கணினி {total} பயோமார்க்கர் முடிவு(களை) கண்டறிந்தது: {normal} குறிப்பு வரம்பிற்குள், {abnormal} வரம்பிற்கு வெளியே, {unclassified} நம்பகமாக வகைப்படுத்த முடியவில்லை.",
        "outside_include": "வழங்கப்பட்ட வரம்பிற்கு வெளியே உள்ள முடிவுகள்: {names}.",
        "none_flagged": "பகுப்பாய்வு செய்யப்பட்ட எந்த பயோமார்க்கர் முடிவும் அதிகம் அல்லது குறைவாகக் குறிக்கப்படவில்லை.",
        "unknown_status": "கணினியால் {names} நிலையை தீர்மானிக்க முடியவில்லை.",
        "abnormal_note": "இந்த குறியீடுகள் அறிக்கையில் அச்சிடப்பட்ட குறிப்பு வரம்புகளை பிரதிபலிக்கின்றன. முழு அறிக்கை மற்றும் மருத்துவ சூழலுடன் விளக்கப்பட வேண்டும்.",
        "unknown_note": "சில முடிவுகளை வகைப்படுத்த முடியாததால், அனைத்து முடிவுகளும் இயல்பானவை என்பதை இந்த சுருக்கம் நிறுவுவதில்லை.",
        "all_normal_note": "அறிக்கையில் அச்சிடப்பட்ட வரம்புகளுக்கு வெளியே எந்த முடிவும் குறிக்கப்படவில்லை. இது ஒவ்வொரு சாத்தியமான உடல்நலப் பிரச்சினையையும் விலக்காது.",
        "no_biomarkers": "இந்த அறிக்கையிலிருந்து ஆய்வக பயோமார்க்கர்கள் நம்பகமாகக் கண்டறியப்படவில்லை.",
    },
    "kn": {
        "identified": "ಸಿಸ್ಟಮ್ {total} ಬಯೋಮಾರ್ಕರ್ ಫಲಿತಾಂಶ(ಗಳನ್ನು) ಗುರುತಿಸಿದೆ: {normal} ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಯೊಳಗೆ, {abnormal} ಹೊರಗೆ, {unclassified} ವಿಶ್ವಾಸಾರ್ಹವಾಗಿ ವರ್ಗೀಕರಿಸಲಾಗಲಿಲ್ಲ.",
        "outside_include": "ನೀಡಲಾದ ವ್ಯಾಪ್ತಿಯ ಹೊರಗಿನ ಫಲಿತಾಂಶಗಳು: {names}.",
        "none_flagged": "ಯಾವುದೇ ವಿಶ್ಲೇಷಿಸಿದ ಬಯೋಮಾರ್ಕರ್ ಫಲಿತಾಂಶವನ್ನು ಹೆಚ್ಚು ಅಥವಾ ಕಡಿಮೆ ಎಂದು ಗುರುತಿಸಲಾಗಿಲ್ಲ.",
        "unknown_status": "ಸಿಸ್ಟಮ್ {names} ಸ್ಥಿತಿಯನ್ನು ನಿರ್ಧರಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.",
        "abnormal_note": "ಈ ಗುರುತುಗಳು ವರದಿಯಲ್ಲಿ ಮುದ್ರಿತ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಳನ್ನು ಪ್ರತಿಬಿಂಬಿಸುತ್ತವೆ.",
        "unknown_note": "ಕೆಲವು ಫಲಿತಾಂಶಗಳನ್ನು ವರ್ಗೀಕರಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ, ಎಲ್ಲಾ ಫಲಿತಾಂಶಗಳು ಸಾಮಾನ್ಯ ಎಂದು ಈ ಸಾರಾಂಶ ಸ್ಥಾಪಿಸುವುದಿಲ್ಲ.",
        "all_normal_note": "ವರದಿಯಲ್ಲಿ ಮುದ್ರಿತ ವ್ಯಾಪ್ತಿಯ ಹೊರಗೆ ಯಾವುದೇ ಫಲಿತಾಂಶ ಗುರುತಿಸಲಾಗಿಲ್ಲ.",
        "no_biomarkers": "ಈ ವರದಿಯಿಂದ ಪ್ರಯೋಗಾಲಯ ಬಯೋಮಾರ್ಕರ್‌ಗಳನ್ನು ವಿಶ್ವಾಸಾರ್ಹವಾಗಿ ಗುರುತಿಸಲಾಗಿಲ್ಲ.",
    },
    "ml": {
        "identified": "സിസ്റ്റം {total} ബയോമാർക്കർ ഫലം(ങ്ങൾ) കണ്ടെത്തി: {normal} റഫറൻസ് ശ്രേണിക്കുള്ളിൽ, {abnormal} ശ്രേണിക്ക് പുറത്ത്, {unclassified} വിശ്വസനീയമായി വർഗ്ഗീകരിക്കാൻ കഴിഞ്ഞില്ല.",
        "outside_include": "നൽകിയ ശ്രേണിക്ക് പുറത്തുള്ള ഫലങ്ങൾ: {names}.",
        "none_flagged": "വിശകലനം ചെയ്ത ഒരു ബയോമാർക്കർ ഫലവും ഉയർന്നതോ കുറഞ്ഞതോ ആയി അടയാളപ്പെടുത്തിയിട്ടില്ല.",
        "unknown_status": "സിസ്റ്റത്തിന് {names} നിലയെ നിർണ്ണയിക്കാനായില്ല.",
        "abnormal_note": "ഈ അടയാളങ്ങൾ റിപ്പോർട്ടിൽ അച്ചടിച്ച റഫറൻസ് ശ്രേണികളെ പ്രതിഫലിപ്പിക്കുന്നു.",
        "unknown_note": "ചില ഫലങ്ങൾ വർഗ്ഗീകരിക്കാൻ കഴിയാത്തതിനാൽ, എല്ലാ ഫലങ്ങളും സാധാരണമാണെന്ന് ഈ സംഗ്രഹം സ്ഥാപിക്കുന്നില്ല.",
        "all_normal_note": "റിപ്പോർട്ടിൽ അച്ചടിച്ച ശ്രേണികൾക്ക് പുറത്ത് ഒരു ഫലവും അടയാളപ്പെടുത്തിയിട്ടില്ല.",
        "no_biomarkers": "ഈ റിപ്പോർട്ടിൽ നിന്ന് ലാബ് ബയോമാർക്കറുകൾ വിശ്വസനീയമായി കണ്ടെത്തിയില്ല.",
    },
    "mr": {
        "identified": "प्रणालीने {total} बायोमार्कर निकाल ओळखले: {normal} संदर्भ श्रेणीत, {abnormal} बाहेर, {unclassified} विश्वासार्हपणे वर्गीकृत करता आले नाहीत.",
        "outside_include": "दिलेल्या श्रेणीबाहेरील निकालांमध्ये: {names}.",
        "none_flagged": "कोणत्याही विश्लेषित बायोमार्कर निकालाला जास्त किंवा कमी म्हणून चिन्हांकित केले नाही.",
        "unknown_status": "प्रणालीला {names} ची स्थिती निर्धारित करता आली नाही.",
        "abnormal_note": "ही चिन्हे अहवालातील मुद्रित संदर्भ श्रेणी दर्शवतात.",
        "unknown_note": "काही निकाल वर्गीकृत करता आले नाहीत, त्यामुळे सर्व निकाल सामान्य आहेत असे हा सारांश स्थापित करत नाही.",
        "all_normal_note": "अहवालातील मुद्रित श्रेणीबाहेर कोणताही निकाल चिन्हांकित झाला नाही.",
        "no_biomarkers": "या अहवालातून प्रयोगशाळा बायोमार्कर्स विश्वासार्हपणे ओळखले गेले नाहीत.",
    },
    "bn": {
        "identified": "সিস্টেম {total} বায়োমার্কার ফলাফল চিহ্নিত করেছে: {normal} রেফারেন্স রেঞ্জের মধ্যে, {abnormal} বাইরে, {unclassified} নির্ভরযোগ্যভাবে শ্রেণীবদ্ধ করা যায়নি।",
        "outside_include": "প্রদত্ত রেঞ্জের বাইরের ফলাফল: {names}।",
        "none_flagged": "বিশ্লেষিত কোনো বায়োমার্কার ফলাফল বেশি বা কম হিসেবে চিহ্নিত হয়নি।",
        "unknown_status": "সিস্টেম {names}-এর অবস্থা নির্ধারণ করতে পারেনি।",
        "abnormal_note": "এই চিহ্নগুলি রিপোর্টে মুদ্রিত রেফারেন্স রেঞ্জ প্রতিফলিত করে।",
        "unknown_note": "কিছু ফলাফল শ্রেণীবদ্ধ করা যায়নি বলে, সমস্ত ফলাফল স্বাভাবিক তা এই সারাংশ প্রতিষ্ঠা করে না।",
        "all_normal_note": "রিপোর্টে মুদ্রিত রেঞ্জের বাইরে কোনো ফলাফল চিহ্নিত হয়নি।",
        "no_biomarkers": "এই রিপোর্ট থেকে ল্যাব বায়োমার্কার নির্ভরযোগ্যভাবে চিহ্নিত হয়নি।",
    },
}


def get_impression_phrases(lang):
    """Return dict of impression template phrases for the given language."""
    return IMPRESSION_PHRASES.get(lang, IMPRESSION_PHRASES["en"])


# =========================================================
# DOCTOR QUESTIONS TEMPLATES
# =========================================================

DOCTOR_QUESTION_TEMPLATES = {
    "en": {
        "high": "What could be contributing to my elevated {name}?",
        "low": "What could be contributing to my low {name}?",
        "patterns_together": "Do any of these findings need to be evaluated together?",
        "repeat_monitor": "Should any of these results be repeated or monitored?",
        "additional_testing": "Is any additional testing appropriate based on these findings?",
    },
    "hi": {
        "high": "मेरे बढ़े हुए {name} में क्या योगदान दे सकता है?",
        "low": "मेरे कम {name} में क्या योगदान दे सकता है?",
        "patterns_together": "क्या इनमें से किसी भी निष्कर्ष का एक साथ मूल्यांकन करने की आवश्यकता है?",
        "repeat_monitor": "क्या इनमें से किसी भी परिणाम को दोहराया या निगरानी किया जाना चाहिए?",
        "additional_testing": "क्या इन निष्कर्षों के आधार पर कोई अतिरिक्त जाँच उचित है?",
    },
    "te": {
        "high": "నా పెరిగిన {name} కు ఏమి కారణమవుతుంది?",
        "low": "నా తక్కువ {name} కు ఏమి కారణమవుతుంది?",
        "patterns_together": "ఈ ఫలితాలలో ఏవైనా కలిపి అంచనా వేయాలా?",
        "repeat_monitor": "ఈ ఫలితాలలో ఏవైనా పునరావృతం చేయాలా లేదా పర్యవేక్షించాలా?",
        "additional_testing": "ఈ ఫలితాల ఆధారంగా ఏదైనా అదనపు పరీక్ష తగినదేనా?",
    },
    "ta": {
        "high": "என் உயர்ந்த {name} க்கு என்ன பங்களிக்கும்?",
        "low": "என் குறைவான {name} க்கு என்ன பங்களிக்கும்?",
        "patterns_together": "இந்த கண்டுபிடிப்புகளில் ஏதேனும் ஒன்றாக மதிப்பீடு செய்ய வேண்டுமா?",
        "repeat_monitor": "இந்த முடிவுகளில் ஏதேனும் மீண்டும் செய்யப்பட வேண்டுமா அல்லது கண்காணிக்கப்பட வேண்டுமா?",
        "additional_testing": "இந்த கண்டுபிடிப்புகளின் அடிப்படையில் கூடுதல் பரிசோதனை தேவையா?",
    },
    "kn": {
        "high": "ನನ್ನ ಏರಿದ {name} ಗೆ ಏನು ಕಾರಣವಾಗಬಹುದು?",
        "low": "ನನ್ನ ಕಡಿಮೆ {name} ಗೆ ಏನು ಕಾರಣವಾಗಬಹುದು?",
        "patterns_together": "ಈ ಫಲಿತಾಂಶಗಳಲ್ಲಿ ಯಾವುದನ್ನಾದರೂ ಒಟ್ಟಿಗೆ ಮೌಲ್ಯಮಾಪನ ಮಾಡಬೇಕೆ?",
        "repeat_monitor": "ಈ ಫಲಿತಾಂಶಗಳಲ್ಲಿ ಯಾವುದನ್ನಾದರೂ ಪುನರಾವರ್ತಿಸಬೇಕೆ ಅಥವಾ ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಬೇಕೆ?",
        "additional_testing": "ಈ ಫಲಿತಾಂಶಗಳ ಆಧಾರದ ಮೇಲೆ ಯಾವುದಾದರೂ ಹೆಚ್ಚುವರಿ ಪರೀಕ್ಷೆ ಸೂಕ್ತವೆ?",
    },
    "ml": {
        "high": "എന്റെ ഉയർന്ന {name} ന് എന്ത് കാരണമായേക്കാം?",
        "low": "എന്റെ കുറഞ്ഞ {name} ന് എന്ത് കാരണമായേക്കാം?",
        "patterns_together": "ഈ കണ്ടെത്തലുകളിൽ ഏതെങ്കിലും ഒരുമിച്ച് വിലയിരുത്തേണ്ടതുണ്ടോ?",
        "repeat_monitor": "ഈ ഫലങ്ങളിൽ ഏതെങ്കിലും ആവർത്തിക്കുകയോ നിരീക്ഷിക്കുകയോ ചെയ്യേണ്ടതുണ്ടോ?",
        "additional_testing": "ഈ കണ്ടെത്തലുകളുടെ അടിസ്ഥാനത്തിൽ എന്തെങ്കിലും അധിക പരിശോധന ഉചിതമാണോ?",
    },
    "mr": {
        "high": "माझ्या वाढलेल्या {name} ला काय कारणीभूत असू शकते?",
        "low": "माझ्या कमी {name} ला काय कारणीभूत असू शकते?",
        "patterns_together": "यापैकी कोणत्याही निष्कर्षांचे एकत्रित मूल्यांकन करणे आवश्यक आहे का?",
        "repeat_monitor": "यापैकी कोणतेही निकाल पुन्हा करावे किंवा निरीक्षण करावे का?",
        "additional_testing": "या निष्कर्षांच्या आधारावर कोणती अतिरिक्त चाचणी योग्य आहे का?",
    },
    "bn": {
        "high": "আমার বর্ধিত {name}-এ কী অবদান রাখতে পারে?",
        "low": "আমার কম {name}-এ কী অবদান রাখতে পারে?",
        "patterns_together": "এই ফলাফলগুলির কোনোটি কি একসাথে মূল্যায়ন করা প্রয়োজন?",
        "repeat_monitor": "এই ফলাফলগুলির কোনোটি কি পুনরায় করা বা পর্যবেক্ষণ করা উচিত?",
        "additional_testing": "এই ফলাফলের ভিত্তিতে কোনো অতিরিক্ত পরীক্ষা উপযুক্ত কি?",
    },
}


def get_doctor_question_templates(lang):
    """Return doctor question templates for the given language."""
    return DOCTOR_QUESTION_TEMPLATES.get(lang, DOCTOR_QUESTION_TEMPLATES["en"])


# =========================================================
# IMAGING KNOWLEDGE TRANSLATIONS
# =========================================================

IMAGING_KNOWLEDGE = {
    "en": {
        "stones": {
            "title": "Understanding urinary stones",
            "content": (
                "A calculus is a stone-like deposit. Stones in the kidney or ureter can sometimes "
                "affect the flow of urine. Their significance depends on their size, location, symptoms and "
                "whether they cause obstruction. A healthcare professional can advise whether monitoring "
                "or further evaluation is appropriate."
            ),
        },
        "dilation": {
            "title": "Understanding urinary tract dilation",
            "content": (
                "Hydronephrosis refers to dilation of the kidney's urine-collecting system. "
                "Hydroureteronephrosis refers to dilation involving the ureter and kidney collecting "
                "system. It can occur when urine flow is partly or fully obstructed. The cause and "
                "importance need to be assessed by a clinician."
            ),
        },
    },
    "hi": {
        "stones": {
            "title": "मूत्र पथरी को समझना",
            "content": (
                "कैल्कुलस एक पथरी जैसा जमाव है। गुर्दे या मूत्रवाहिनी में पथरी कभी-कभी "
                "मूत्र प्रवाह को प्रभावित कर सकती है। इसका महत्व आकार, स्थान, लक्षणों और "
                "रुकावट पर निर्भर करता है। स्वास्थ्य पेशेवर सलाह दे सकते हैं।"
            ),
        },
        "dilation": {
            "title": "मूत्र पथ फैलाव को समझना",
            "content": (
                "हाइड्रोनेफ्रोसिस गुर्दे की मूत्र संग्रह प्रणाली के फैलाव को संदर्भित करता है। "
                "यह तब हो सकता है जब मूत्र प्रवाह आंशिक या पूर्ण रूप से अवरुद्ध हो। "
                "कारण और महत्व का मूल्यांकन चिकित्सक द्वारा किया जाना चाहिए।"
            ),
        },
    },
    "te": {
        "stones": {
            "title": "మూత్ర రాళ్ళను అర్థం చేసుకోవడం",
            "content": "కాల్క్యులస్ అనేది రాయి లాంటి నిక్షేపం. కిడ్నీ లేదా యూరెటర్‌లోని రాళ్ళు కొన్నిసార్లు మూత్ర ప్రవాహాన్ని ప్రభావితం చేయవచ్చు. వాటి ప్రాముఖ్యత పరిమాణం, స్థానం మరియు లక్షణాలపై ఆధారపడి ఉంటుంది.",
        },
        "dilation": {
            "title": "మూత్ర నాళ విస్తరణను అర్థం చేసుకోవడం",
            "content": "హైడ్రోనెఫ్రోసిస్ అనేది కిడ్నీ మూత్ర సేకరణ వ్యవస్థ విస్తరణను సూచిస్తుంది. మూత్ర ప్రవాహం పాక్షికంగా లేదా పూర్తిగా అడ్డుపడినప్పుడు ఇది సంభవించవచ్చు.",
        },
    },
    "ta": {
        "stones": {
            "title": "சிறுநீர் கற்களைப் புரிந்து கொள்ளுதல்",
            "content": "கால்குலஸ் என்பது கல் போன்ற படிவு. சிறுநீரகம் அல்லது சிறுநீர்க்குழாயில் உள்ள கற்கள் சிறுநீர் ஓட்டத்தை பாதிக்கலாம். அவற்றின் முக்கியத்துவம் அளவு, இடம் மற்றும் அறிகுறிகளைப் பொறுத்தது.",
        },
        "dilation": {
            "title": "சிறுநீர் பாதை விரிவாக்கத்தைப் புரிந்து கொள்ளுதல்",
            "content": "ஹைட்ரோநெப்ரோசிஸ் என்பது சிறுநீரகத்தின் சிறுநீர் சேகரிப்பு அமைப்பின் விரிவாக்கத்தைக் குறிக்கிறது. சிறுநீர் ஓட்டம் தடைபடும்போது இது ஏற்படலாம்.",
        },
    },
    "kn": {
        "stones": {
            "title": "ಮೂತ್ರನಾಳದ ಕಲ್ಲುಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ಕ್ಯಾಲ್ಕ್ಯುಲಸ್ ಎಂದರೆ ಕಲ್ಲಿನಂತಹ ನಿಕ್ಷೇಪ. ಮೂತ್ರಪಿಂಡ ಅಥವಾ ಮೂತ್ರನಾಳದಲ್ಲಿನ ಕಲ್ಲುಗಳು ಮೂತ್ರ ಹರಿವಿನ ಮೇಲೆ ಪ್ರಭಾವ ಬೀರಬಹುದು.",
        },
        "dilation": {
            "title": "ಮೂತ್ರನಾಳದ ಹಿಗ್ಗುವಿಕೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ಹೈಡ್ರೋನೆಫ್ರೋಸಿಸ್ ಎಂದರೆ ಮೂತ್ರಪಿಂಡದ ಮೂತ್ರ ಸಂಗ್ರಹ ವ್ಯವಸ್ಥೆಯ ಹಿಗ್ಗುವಿಕೆ.",
        },
    },
    "ml": {
        "stones": {
            "title": "മൂത്രാശയ കല്ലുകൾ മനസ്സിലാക്കൽ",
            "content": "കാൽക്കുലസ് എന്നത് കല്ല് പോലുള്ള നിക്ഷേപമാണ്. വൃക്കകളിലോ മൂത്രനാളിയിലോ ഉള്ള കല്ലുകൾ ചിലപ്പോൾ മൂത്രപ്രവാഹത്തെ ബാധിക്കാം.",
        },
        "dilation": {
            "title": "മൂത്രനാള വികാസം മനസ്സിലാക്കൽ",
            "content": "ഹൈഡ്രോനെഫ്രോസിസ് എന്നത് വൃക്കകളുടെ മൂത്ര ശേഖരണ സംവിധാനത്തിന്റെ വികാസത്തെ സൂചിപ്പിക്കുന്നു.",
        },
    },
    "mr": {
        "stones": {
            "title": "मूत्र खडे समजून घेणे",
            "content": "कॅल्क्युलस म्हणजे खड्यासारखे जमा. मूत्रपिंड किंवा मूत्रवाहिनीतील खडे कधीकधी मूत्र प्रवाहावर परिणाम करू शकतात.",
        },
        "dilation": {
            "title": "मूत्रमार्ग विस्तार समजून घेणे",
            "content": "हायड्रोनेफ्रोसिस म्हणजे मूत्रपिंडाच्या मूत्र संकलन प्रणालीचा विस्तार.",
        },
    },
    "bn": {
        "stones": {
            "title": "মূত্রনালীর পাথর বোঝা",
            "content": "ক্যালকুলাস হল পাথরের মতো জমা। কিডনি বা ইউরেটারে পাথর কখনো কখনো মূত্র প্রবাহকে প্রভাবিত করতে পারে।",
        },
        "dilation": {
            "title": "মূত্রনালী প্রসারণ বোঝা",
            "content": "হাইড্রোনেফ্রোসিস হল কিডনির মূত্র সংগ্রহ ব্যবস্থার প্রসারণ।",
        },
    },
}


IMAGING_QUESTIONS = {
    "en": {
        "stone_significance": "What is the significance of the stone's size and location?",
        "urine_flow": "Could this finding be affecting the flow of urine?",
        "followup_imaging": "Is follow-up imaging or specialist review appropriate?",
        "dilation_cause": "What could be causing the urinary tract dilation, and how should it be followed up?",
        "urgent_symptoms": "Which symptoms should prompt urgent medical attention?",
    },
    "hi": {
        "stone_significance": "पथरी के आकार और स्थान का क्या महत्व है?",
        "urine_flow": "क्या यह निष्कर्ष मूत्र प्रवाह को प्रभावित कर सकता है?",
        "followup_imaging": "क्या अनुवर्ती इमेजिंग या विशेषज्ञ समीक्षा उचित है?",
        "dilation_cause": "मूत्र पथ फैलाव का कारण क्या हो सकता है?",
        "urgent_symptoms": "कौन से लक्षणों पर तत्काल चिकित्सा ध्यान देना चाहिए?",
    },
    "te": {
        "stone_significance": "రాయి పరిమాణం మరియు స్థానం యొక్క ప్రాముఖ్యత ఏమిటి?",
        "urine_flow": "ఈ ఫలితం మూత్ర ప్రవాహాన్ని ప్రభావితం చేస్తుందా?",
        "followup_imaging": "ఫాలో-అప్ ఇమేజింగ్ లేదా నిపుణుల సమీక్ష తగినదేనా?",
        "dilation_cause": "మూత్ర నాళ విస్తరణకు కారణం ఏమిటి?",
        "urgent_symptoms": "ఏ లక్షణాలకు అత్యవసర వైద్య సహాయం అవసరం?",
    },
    "ta": {
        "stone_significance": "கல்லின் அளவு மற்றும் இடத்தின் முக்கியத்துவம் என்ன?",
        "urine_flow": "இந்த கண்டுபிடிப்பு சிறுநீர் ஓட்டத்தை பாதிக்கும் என்பது சாத்தியமா?",
        "followup_imaging": "பின்தொடர் இமேஜிங் அல்லது நிபுணர் மதிப்பாய்வு பொருத்தமானதா?",
        "dilation_cause": "சிறுநீர் பாதை விரிவாக்கத்திற்கு என்ன காரணமாக இருக்கலாம்?",
        "urgent_symptoms": "எந்த அறிகுறிகளுக்கு அவசர மருத்துவ கவனிப்பு தேவை?",
    },
    "kn": {
        "stone_significance": "ಕಲ್ಲಿನ ಗಾತ್ರ ಮತ್ತು ಸ್ಥಳದ ಮಹತ್ವವೇನು?",
        "urine_flow": "ಈ ಫಲಿತಾಂಶ ಮೂತ್ರ ಹರಿವಿನ ಮೇಲೆ ಪ್ರಭಾವ ಬೀರಬಹುದೇ?",
        "followup_imaging": "ಅನುಸರಣೆ ಇಮೇಜಿಂಗ್ ಅಥವಾ ತಜ್ಞರ ಪರಿಶೀಲನೆ ಸೂಕ್ತವೇ?",
        "dilation_cause": "ಮೂತ್ರನಾಳ ಹಿಗ್ಗುವಿಕೆಗೆ ಕಾರಣವೇನು?",
        "urgent_symptoms": "ಯಾವ ರೋಗಲಕ್ಷಣಗಳಿಗೆ ತುರ್ತು ವೈದ್ಯಕೀಯ ಗಮನ ಬೇಕು?",
    },
    "ml": {
        "stone_significance": "കല്ലിന്റെ വലിപ്പവും സ്ഥാനവും എത്രത്തോളം പ്രാധാന്യമുള്ളതാണ്?",
        "urine_flow": "ഈ കണ്ടെത്തൽ മൂത്രപ്രവാഹത്തെ ബാധിക്കുമോ?",
        "followup_imaging": "ഫോളോ-അപ്പ് ഇമേജിംഗ് അല്ലെങ്കിൽ സ്പെഷ്യലിസ്റ്റ് അവലോകനം ഉചിതമാണോ?",
        "dilation_cause": "മൂത്രനാള വികാസത്തിന് കാരണമെന്ത്?",
        "urgent_symptoms": "ഏത് ലക്ഷണങ്ങൾക്ക് അടിയന്തര വൈദ്യ ശ്രദ്ധ ആവശ്യമാണ്?",
    },
    "mr": {
        "stone_significance": "खड्याच्या आकार आणि स्थानाचे महत्त्व काय आहे?",
        "urine_flow": "हा निष्कर्ष मूत्र प्रवाहावर परिणाम करू शकतो का?",
        "followup_imaging": "अनुवर्ती इमेजिंग किंवा तज्ञ पुनरावलोकन योग्य आहे का?",
        "dilation_cause": "मूत्रमार्ग विस्ताराचे कारण काय असू शकते?",
        "urgent_symptoms": "कोणत्या लक्षणांना तात्काळ वैद्यकीय लक्ष द्यावे?",
    },
    "bn": {
        "stone_significance": "পাথরের আকার ও অবস্থানের তাৎপর্য কী?",
        "urine_flow": "এই ফলাফল কি মূত্র প্রবাহকে প্রভাবিত করতে পারে?",
        "followup_imaging": "ফলো-আপ ইমেজিং বা বিশেষজ্ঞ পর্যালোচনা উপযুক্ত কি?",
        "dilation_cause": "মূত্রনালী প্রসারণের কারণ কী হতে পারে?",
        "urgent_symptoms": "কোন উপসর্গে জরুরি চিকিৎসা মনোযোগ প্রয়োজন?",
    },
}


# =========================================================
# "NO IMPRESSION" FALLBACK TEXT
# =========================================================

NO_IMPRESSION_TEXT = {
    "en": "A clear radiology impression could not be identified from the extracted text. Please refer to the original report and discuss it with a healthcare professional.",
    "hi": "निकाले गए पाठ से स्पष्ट रेडियोलॉजी निष्कर्ष पहचाना नहीं जा सका। कृपया मूल रिपोर्ट देखें और स्वास्थ्य पेशेवर से चर्चा करें।",
    "te": "సేకరించిన వచనం నుండి స్పష్టమైన రేడియాలజీ అభిప్రాయం గుర్తించబడలేదు. దయచేసి అసలు నివేదిక చూడండి.",
    "ta": "பிரித்தெடுக்கப்பட்ட உரையிலிருந்து தெளிவான கதிரியல் கருத்தை கண்டறிய முடியவில்லை. அசல் அறிக்கையைப் பாருங்கள்.",
    "kn": "ಸಂಗ್ರಹಿಸಿದ ಪಠ್ಯದಿಂದ ಸ್ಪಷ್ಟ ರೇಡಿಯಾಲಜಿ ಅಭಿಪ್ರಾಯ ಗುರುತಿಸಲಾಗಿಲ್ಲ. ಮೂಲ ವರದಿಯನ್ನು ನೋಡಿ.",
    "ml": "എക്സ്ട്രാക്റ്റ് ചെയ്ത ടെക്സ്റ്റിൽ നിന്ന് വ്യക്തമായ റേഡിയോളജി അഭിപ്രായം കണ്ടെത്താനായില്ല. യഥാർത്ഥ റിപ്പോർട്ട് കാണുക.",
    "mr": "काढलेल्या मजकुरातून स्पष्ट रेडिओलॉजी निष्कर्ष ओळखला गेला नाही. मूळ अहवाल पहा.",
    "bn": "নিষ্কাশিত পাঠ্য থেকে স্পষ্ট রেডিওলজি ধারণা চিহ্নিত করা যায়নি। মূল রিপোর্ট দেখুন।",
}

# =========================================================
# PATTERN TRANSLATIONS
# =========================================================

PATTERN_TRANSLATIONS = {
    "en": {
        "Elevated glucose": {
            "name": "Elevated glucose",
            "description": "The glucose result is above the reference range provided in the report. Glucose results are generally interpreted together with other measurements and clinical context."
        },
        "Lipid profile pattern": {
            "name": "Lipid profile pattern",
            "description": "The report shows both a low HDL result and an elevated LDL result. These lipid measurements are commonly considered together."
        },
        "Low HDL": {
            "name": "Low HDL",
            "description": "HDL is below the reference range provided in the report and is interpreted together with the rest of the lipid profile."
        },
        "Elevated LDL": {
            "name": "Elevated LDL",
            "description": "LDL is above the reference range provided in the report and is interpreted together with the rest of the lipid profile."
        },
        "Elevated RDW": {
            "name": "Elevated RDW",
            "description": "RDW is above the reference range. It describes variation in red blood cell size and is interpreted alongside other blood-count measurements."
        },
        "Elevated C-reactive protein": {
            "name": "Elevated C-reactive protein",
            "description": "C-reactive protein is above the reference range provided in the report. CRP can increase with inflammation, but the result is non-specific and needs clinical context."
        },
        "Elevated bilirubin": {
            "name": "Elevated bilirubin",
            "description": "One or more bilirubin measurements are above the provided reference range. Bilirubin is interpreted together with other relevant results."
        },
        "Elevated white blood cell count": {
            "name": "Elevated white blood cell count",
            "description": "The white blood cell count is above the reference range provided in the report."
        },
        "Low white blood cell count": {
            "name": "Low white blood cell count",
            "description": "The white blood cell count is below the reference range provided in the report."
        },
        "Elevated platelet count": {
            "name": "Elevated platelet count",
            "description": "The platelet count is above the reference range provided in the report."
        },
        "Low platelet count": {
            "name": "Low platelet count",
            "description": "The platelet count is below the reference range provided in the report."
        }
    },
    "hi": {
        "Elevated glucose": {
            "name": "ग्लूकोज का बढ़ा हुआ स्तर",
            "description": "ग्लूकोज का स्तर रिपोर्ट में दी गई संदर्भ सीमा से अधिक है। ग्लूकोज के परिणामों की व्याख्या अन्य मापों और नैदानिक संदर्भ के साथ की जाती है।"
        },
        "Lipid profile pattern": {
            "name": "लिपिड प्रोफाइल पैटर्न",
            "description": "रिपोर्ट में कम HDL और बढ़ा हुआ LDL दोनों दिखाई देते हैं। इन लिपिड मापों को आमतौर पर एक साथ देखा जाता है।"
        },
        "Low HDL": {
            "name": "कम HDL",
            "description": "HDL संदर्भ सीमा से कम है और इसकी व्याख्या शेष लिपिड प्रोफाइल के साथ की जाती है।"
        },
        "Elevated LDL": {
            "name": "बढ़ा हुआ LDL",
            "description": "LDL संदर्भ सीमा से अधिक है और इसकी व्याख्या शेष लिपिड प्रोफाइल के साथ की जाती है।"
        },
        "Elevated RDW": {
            "name": "बढ़ा हुआ RDW",
            "description": "RDW संदर्भ सीमा से अधिक है। यह लाल रक्त कोशिकाओं के आकार में भिन्नता को दर्शाता है।"
        },
        "Elevated C-reactive protein": {
            "name": "बढ़ा हुआ सी-रिएक्टिव प्रोटीन (CRP)",
            "description": "सी-रिएक्टिव प्रोटीन संदर्भ सीमा से अधिक है। CRP सूजन के साथ बढ़ सकता है, लेकिन यह गैर-विशिष्ट है और नैदानिक संदर्भ की आवश्यकता है।"
        },
        "Elevated bilirubin": {
            "name": "बढ़ा हुआ बिलीरुबिन",
            "description": "एक या अधिक बिलीरुबिन माप संदर्भ सीमा से अधिक हैं। बिलीरुबिन की व्याख्या अन्य संबंधित परिणामों के साथ की जाती है।"
        },
        "Elevated white blood cell count": {
            "name": "बढ़ी हुई श्वेत रक्त कोशिकाएं (WBC)",
            "description": "श्वेत रक्त कोशिकाओं की संख्या संदर्भ सीमा से अधिक है।"
        },
        "Low white blood cell count": {
            "name": "कम श्वेत रक्त कोशिकाएं (WBC)",
            "description": "श्वेत रक्त कोशिकाओं की संख्या संदर्भ सीमा से कम है।"
        },
        "Elevated platelet count": {
            "name": "बढ़ी हुई प्लेटलेट संख्या",
            "description": "प्लेटलेट की संख्या संदर्भ सीमा से अधिक है।"
        },
        "Low platelet count": {
            "name": "कम प्लेटलेट संख्या",
            "description": "प्लेटलेट की संख्या संदर्भ सीमा से कम है।"
        }
    },
    "te": {
        "Elevated glucose": {
            "name": "పెరిగిన గ్లూకోజ్",
            "description": "గ్లూకోజ్ ఫలితం నివేదికలో అందించిన సూచన పరిధి కంటే ఎక్కువగా ఉంది. గ్లూకోజ్ ఫలితాలను ఇతర కొలతలు మరియు క్లినికల్ సందర్భంతో కలిపి అర్థం చేసుకుంటారు."
        },
        "Lipid profile pattern": {
            "name": "లిపిడ్ ప్రొఫైల్ నమూనా",
            "description": "నివేదిక తక్కువ HDL మరియు పెరిగిన LDL రెండింటినీ చూపిస్తుంది. ఈ లిపిడ్ కొలతలను సాధారణంగా కలిసి పరిగణిస్తారు."
        },
        "Low HDL": {
            "name": "తక్కువ HDL",
            "description": "HDL అందించిన సూచన పరిధి కంటే తక్కువగా ఉంది."
        },
        "Elevated LDL": {
            "name": "పెరిగిన LDL",
            "description": "LDL అందించిన సూచన పరిధి కంటే ఎక్కువగా ఉంది."
        },
        "Elevated RDW": {
            "name": "పెరిగిన RDW",
            "description": "RDW సూచన పరిధి కంటే ఎక్కువగా ఉంది. ఇది ఎర్ర రక్త కణాల పరిమాణంలో తేడాలను వివరిస్తుంది."
        },
        "Elevated C-reactive protein": {
            "name": "పెరిగిన సి-రియాక్టివ్ ప్రోటీన్ (CRP)",
            "description": "సి-రియాక్టివ్ ప్రోటీన్ సూచన పరిధి కంటే ఎక్కువగా ఉంది. CRP వాపుతో పెరగవచ్చు."
        },
        "Elevated bilirubin": {
            "name": "పెరిగిన బిలిరుబిన్",
            "description": "ఒకటి లేదా అంతకంటే ఎక్కువ బిలిరుబిన్ కొలతలు సూచన పరిధి కంటే ఎక్కువగా ఉన్నాయి."
        },
        "Elevated white blood cell count": {
            "name": "పెరిగిన తెల్ల రక్త కణాలు (WBC)",
            "description": "తెల్ల రక్త కణాల సంఖ్య సూచన పరిధి కంటే ఎక్కువగా ఉంది."
        },
        "Low white blood cell count": {
            "name": "తక్కువ తెల్ల రక్త కణాలు (WBC)",
            "description": "తెల్ల రక్త కణాల సంఖ్య సూచన పరిధి కంటే తక్కువగా ఉంది."
        },
        "Elevated platelet count": {
            "name": "పెరిగిన ప్లేట్‌లెట్ సంఖ్య",
            "description": "ప్లేట్‌లెట్ సంఖ్య సూచన పరిధి కంటే ఎక్కువగా ఉంది."
        },
        "Low platelet count": {
            "name": "తక్కువ ప్లేట్‌లెట్ సంఖ్య",
            "description": "ప్లేట్‌లెట్ సంఖ్య సూచన పరిధి కంటే తక్కువగా ఉంది."
        }
    },
    "ta": {
        "Elevated glucose": {
            "name": "அதிகரித்த குளுக்கோஸ்",
            "description": "குளுக்கோஸ் முடிவு குறிப்பு வரம்பை விட அதிகமாக உள்ளது. குளுக்கோஸ் முடிவுகள் பொதுவாக பிற அளவீடுகளுடன் ஒன்றாக விளக்கப்படுகின்றன."
        },
        "Lipid profile pattern": {
            "name": "கொழுப்பு விவரக்குறிப்பு வடிவம்",
            "description": "அறிக்கை குறைந்த HDL மற்றும் உயர்ந்த LDL இரண்டையும் காட்டுகிறது."
        },
        "Low HDL": {
            "name": "குறைந்த HDL",
            "description": "HDL குறிப்பு வரம்பை விட குறைவாக உள்ளது."
        },
        "Elevated LDL": {
            "name": "உயர்ந்த LDL",
            "description": "LDL குறிப்பு வரம்பை விட அதிகமாக உள்ளது."
        },
        "Elevated RDW": {
            "name": "அதிகரித்த RDW",
            "description": "RDW குறிப்பு வரம்பை விட அதிகமாக உள்ளது. இது இரத்த சிவப்பணுக்களின் அளவு மாறுபாட்டை விவரிக்கிறது."
        },
        "Elevated C-reactive protein": {
            "name": "அதிகரித்த சி-ரியாக்டிவ் புரோட்டீன் (CRP)",
            "description": "சி-ரியாக்டிவ் புரோட்டீன் குறிப்பு வரம்பை விட அதிகமாக உள்ளது."
        },
        "Elevated bilirubin": {
            "name": "அதிகரித்த பிலிரூபின்",
            "description": "பிலிரூபின் அளவீடுகள் குறிப்பு வரம்பை விட அதிகமாக உள்ளன."
        },
        "Elevated white blood cell count": {
            "name": "அதிகரித்த வெள்ளை இரத்த அணுக்கள் (WBC)",
            "description": "வெள்ளை இரத்த அணுக்களின் எண்ணிக்கை குறிப்பு வரம்பை விட அதிகமாக உள்ளது."
        },
        "Low white blood cell count": {
            "name": "குறைந்த வெள்ளை இரத்த அணுக்கள் (WBC)",
            "description": "வெள்ளை இரத்த அணுக்களின் எண்ணிக்கை குறிப்பு வரம்பை விட குறைவாக உள்ளது."
        },
        "Elevated platelet count": {
            "name": "அதிகரித்த பிளேட்லெட் எண்ணிக்கை",
            "description": "பிளேட்லெட் எண்ணிக்கை குறிப்பு வரம்பை விட அதிகமாக உள்ளது."
        },
        "Low platelet count": {
            "name": "குறைந்த பிளேட்லெட் எண்ணிக்கை",
            "description": "பிளேட்லெட் எண்ணிக்கை குறிப்பு வரம்பை விட குறைவாக உள்ளது."
        }
    },
    "kn": {
        "Elevated glucose": {
            "name": "ಹೆಚ್ಚಿದ ಗ್ಲೂಕೋಸ್",
            "description": "ಗ್ಲೂಕೋಸ್ ಫಲಿತಾಂಶವು ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಹೆಚ್ಚಿದೆ. ಇತರ ಅಳತೆಗಳೊಂದಿಗೆ ಅರ್ಥೈಸಲಾಗುತ್ತದೆ."
        },
        "Lipid profile pattern": {
            "name": "ಲಿಪಿಡ್ ಪ್ರೊಫೈಲ್ ನಮೂನೆ",
            "description": "ವರದಿಯು ಕಡಿಮೆ HDL ಮತ್ತು ಹೆಚ್ಚಿದ LDL ಎರಡನ್ನೂ ತೋರಿಸುತ್ತದೆ."
        },
        "Low HDL": {
            "name": "ಕಡಿಮೆ HDL",
            "description": "HDL ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಕಡಿಮೆಯಾಗಿದೆ."
        },
        "Elevated LDL": {
            "name": "ಹೆಚ್ಚಿದ LDL",
            "description": "LDL ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."
        },
        "Elevated RDW": {
            "name": "ಹೆಚ್ಚಿದ RDW",
            "description": "RDW ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."
        },
        "Elevated C-reactive protein": {
            "name": "ಹೆಚ್ಚಿದ ಸಿ-ರಿಯಾಕ್ಟಿವ್ ಪ್ರೋಟೀನ್ (CRP)",
            "description": "ಸಿ-ರಿಯಾಕ್ಟಿವ್ ಪ್ರೋಟೀನ್ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."
        },
        "Elevated bilirubin": {
            "name": "ಹೆಚ್ಚಿದ ಬಿಲಿರುಬಿನ್",
            "description": "ಬಿಲಿರುಬಿನ್ ಅಳತೆಗಳು ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಹೆಚ್ಚಿವೆ."
        },
        "Elevated white blood cell count": {
            "name": "ಹೆಚ್ಚಿದ ಬಿಳಿ ರಕ್ತ ಕಣಗಳು (WBC)",
            "description": "ಬಿಳಿ ರಕ್ತ ಕಣಗಳ ಸಂಖ್ಯೆ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಹೆಚ್ಚಿದೆ."
        },
        "Low white blood cell count": {
            "name": "ಕಡಿಮೆ ಬಿಳಿ ರಕ್ತ ಕಣಗಳು (WBC)",
            "description": "ಬಿಳಿ ರಕ್ತ ಕಣಗಳ ಸಂಖ್ಯೆ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಕಡಿಮೆಯಾಗಿದೆ."
        },
        "Elevated platelet count": {
            "name": "ಹೆಚ್ಚಿದ ಪ್ಲೇಟ್‌ಲೆಟ್ ಸಂಖ್ಯೆ",
            "description": "ಪ್ಲೇಟ್‌ಲೆಟ್ ಸಂಖ್ಯೆ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಹೆಚ್ಚಿದೆ."
        },
        "Low platelet count": {
            "name": "ಕಡಿಮೆ ಪ್ಲೇಟ್‌ಲೆಟ್ ಸಂಖ್ಯೆ",
            "description": "ಪ್ಲೇಟ್‌ಲೆಟ್ ಸಂಖ್ಯೆ ಉಲ್ಲೇಖ ವ್ಯಾಪ್ತಿಗಿಂತ ಕಡಿಮೆಯಾಗಿದೆ."
        }
    },
    "ml": {
        "Elevated glucose": {
            "name": "ഉയർന്ന ഗ്ലൂക്കോസ്",
            "description": "ഗ്ലൂക്കോസ് ഫലം റഫറൻസ് ശ്രേണിയേക്കാൾ ഉയർന്നതാണ്."
        },
        "Lipid profile pattern": {
            "name": "ലിപിഡ് പ്രൊഫൈൽ പാറ്റേൺ",
            "description": "റിപ്പോർട്ടിൽ കുറഞ്ഞ HDL-ഉം ഉയർന്ന LDL-ഉം കാണിക്കുന്നു."
        },
        "Low HDL": {
            "name": "കുറഞ്ഞ HDL",
            "description": "HDL റഫറൻസ് ശ്രേണിയേക്കാൾ കുറവാണ്."
        },
        "Elevated LDL": {
            "name": "ഉയർന്ന LDL",
            "description": "LDL റഫറൻസ് ശ്രേണിയേക്കാൾ ഉയർന്നതാണ്."
        },
        "Elevated RDW": {
            "name": "ഉയർന്ന RDW",
            "description": "RDW റഫറൻസ് ശ്രേണിയേക്കാൾ ഉയർന്നതാണ്."
        },
        "Elevated C-reactive protein": {
            "name": "ഉയർന്ന സി-റിയാക്ടീവ് പ്രോട്ടീൻ (CRP)",
            "description": "സി-റിയാക്ടീവ് പ്രോട്ടീൻ റഫറൻസ് ശ്രേണിയേക്കാൾ ഉയർന്നതാണ്."
        },
        "Elevated bilirubin": {
            "name": "ഉയർന്ന ബിലിറൂബിൻ",
            "description": "ബിലിറൂബിൻ അളവുകൾ റഫറൻസ് ശ്രേണിയേക്കാൾ ഉയർന്നതാണ്."
        },
        "Elevated white blood cell count": {
            "name": "ഉയർന്ന ശ്വേതരക്താണുക്കൾ (WBC)",
            "description": "ശ്വേതരക്താണുക്കളുടെ എണ്ണം റഫറൻസ് ശ്രേണിയേക്കാൾ ഉയർന്നതാണ്."
        },
        "Low white blood cell count": {
            "name": "കുറഞ്ഞ ശ്വേതരക്താണുക്കൾ (WBC)",
            "description": "ശ്വേതരക്താണുക്കളുടെ എണ്ണം റഫറൻസ് ശ്രേണിയേക്കാൾ കുറവാണ്."
        },
        "Elevated platelet count": {
            "name": "ഉയർന്ന പ്ലേറ്റ്‌ലെറ്റ് എണ്ണം",
            "description": "പ്ലേറ്റ്‌ലെറ്റ് എണ്ണം റഫറൻസ് ശ്രേണിയേക്കാൾ ഉയർന്നതാണ്."
        },
        "Low platelet count": {
            "name": "കുറഞ്ഞ പ്ലേറ്റ്‌ലെറ്റ് എണ്ണം",
            "description": "പ്ലേറ്റ്‌ലെറ്റ് എണ്ണം റഫറൻസ് ശ്രേണിയേക്കാൾ കുറവാണ്."
        }
    },
    "mr": {
        "Elevated glucose": {
            "name": "वाढलेले ग्लुकोज",
            "description": "ग्लुकोज निकाल संदर्भ श्रेणीपेक्षा जास्त आहे. इतर मोजमापांसह याचा अर्थ लावला जातो."
        },
        "Lipid profile pattern": {
            "name": "लिपिड प्रोफाइल पॅटर्न",
            "description": "अहवालात कमी HDL आणि वाढलेले LDL दोन्ही दिसून येतात."
        },
        "Low HDL": {
            "name": "कमी HDL",
            "description": "HDL संदर्भ श्रेणीपेक्षा कमी आहे."
        },
        "Elevated LDL": {
            "name": "वाढलेले LDL",
            "description": "LDL संदर्भ श्रेणीपेक्षा जास्त आहे."
        },
        "Elevated RDW": {
            "name": "वाढलेले RDW",
            "description": "RDW संदर्भ श्रेणीपेक्षा जास्त आहे."
        },
        "Elevated C-reactive protein": {
            "name": "वाढलेले सी-रिअॅक्टिव्ह प्रोटीन (CRP)",
            "description": "सी-रिअॅक्टिव्ह प्रोटीन संदर्भ श्रेणीपेक्षा जास्त आहे."
        },
        "Elevated bilirubin": {
            "name": "वाढलेले बिलीरुबिन",
            "description": "बिलीरुबिन मोजमाप संदर्भ श्रेणीपेक्षा जास्त आहे."
        },
        "Elevated white blood cell count": {
            "name": "वाढलेल्या पांढऱ्या रक्तपेशी (WBC)",
            "description": "पांढऱ्या रक्तपेशींची संख्या संदर्भ श्रेणीपेक्षा जास्त आहे."
        },
        "Low white blood cell count": {
            "name": "कमी पांढऱ्या रक्तपेशी (WBC)",
            "description": "पांढऱ्या रक्तपेशींची संख्या संदर्भ श्रेणीपेक्षा कमी आहे."
        },
        "Elevated platelet count": {
            "name": "वाढलेली प्लेटलेट संख्या",
            "description": "प्लेटलेट संख्या संदर्भ श्रेणीपेक्षा जास्त आहे."
        },
        "Low platelet count": {
            "name": "कमी प्लेटलेट संख्या",
            "description": "प्लेटलेट संख्या संदर्भ श्रेणीपेक्षा कमी आहे."
        }
    },
    "bn": {
        "Elevated glucose": {
            "name": "উচ্চ গ্লুকোজ",
            "description": "গ্লুকোজের ফলাফল রেফারেন্স রেঞ্জের চেয়ে বেশি। অন্যান্য পরিমাপের সাথে এর অর্থ নির্ধারণ করা হয়।"
        },
        "Lipid profile pattern": {
            "name": "লিপিড প্রোফাইল প্যাটার্ন",
            "description": "রিপোর্টে কম HDL এবং উচ্চ LDL উভয়ই দেখা যাচ্ছে।"
        },
        "Low HDL": {
            "name": "কম HDL",
            "description": "HDL রেফারেন্স রেঞ্জের চেয়ে কম।"
        },
        "Elevated LDL": {
            "name": "উচ্চ LDL",
            "description": "LDL রেফারেন্স রেঞ্জের চেয়ে বেশি।"
        },
        "Elevated RDW": {
            "name": "উচ্চ RDW",
            "description": "RDW রেফারেন্স রেঞ্জের চেয়ে বেশি।"
        },
        "Elevated C-reactive protein": {
            "name": "উচ্চ সি-রিঅ্যাক্টিভ প্রোটিন (CRP)",
            "description": "সি-রিঅ্যাক্টিভ প্রোটিন রেফারেন্স রেঞ্জের চেয়ে বেশি।"
        },
        "Elevated bilirubin": {
            "name": "উচ্চ বিলিরুবিন",
            "description": "বিলিরুবিনের পরিমাপ রেফারেন্স রেঞ্জের চেয়ে বেশি।"
        },
        "Elevated white blood cell count": {
            "name": "উচ্চ শ্বেত রক্তকণিকা (WBC)",
            "description": "শ্বেত রক্তকণিকার সংখ্যা রেফারেন্স রেঞ্জের চেয়ে বেশি।"
        },
        "Low white blood cell count": {
            "name": "কম শ্বেত রক্তকণিকা (WBC)",
            "description": "শ্বেত রক্তকণিকার সংখ্যা রেফারেন্স রেঞ্জের চেয়ে কম।"
        },
        "Elevated platelet count": {
            "name": "উচ্চ প্লেটলেট সংখ্যা",
            "description": "প্লেটলেট সংখ্যা রেফারেন্স রেঞ্জের চেয়ে বেশি।"
        },
        "Low platelet count": {
            "name": "কম প্লেটলেট সংখ্যা",
            "description": "প্লেটলেট সংখ্যা রেফারেন্স রেঞ্জের চেয়ে কম।"
        }
    }
}


def get_pattern_translation(pattern_name, lang):
    """Return localized pattern name and description dict."""
    patterns = PATTERN_TRANSLATIONS.get(lang, PATTERN_TRANSLATIONS["en"])
    return patterns.get(pattern_name, PATTERN_TRANSLATIONS["en"].get(pattern_name, {
        "name": pattern_name,
        "description": ""
    }))


# =========================================================
# KNOWLEDGE BASE TRANSLATIONS
# =========================================================

KNOWLEDGE_TRANSLATIONS = {
    "glucose": {
        "hi": {
            "title": "फास्टिंग ब्लड ग्लूकोज को समझना",
            "content": "फास्टिंग ब्लड ग्लूकोज उपवास के बाद रक्त में ग्लूकोज की मात्रा को मापता है। प्रयोगशाला सीमा से ऊपर का परिणाम अनुवर्ती कार्रवाई की मांग कर सकता है, लेकिन एक एकल परिणाम निदान स्थापित नहीं करता है।"
        },
        "te": {
            "title": "ఫాస్టింగ్ బ్లడ్ గ్లూకోజ్ అర్థం చేసుకోవడం",
            "content": "ఫాస్టింగ్ బ్లడ్ గ్లూకోజ్ ఉపవాసం తర్వాత రక్తంలో గ్లూకోజ్ పరిమాణాన్ని కొలుస్తుంది. సూచన పరిధి కంటే ఎక్కువ ఫలితం వచ్చినప్పుడు వైద్య సలహా అవసరం కావచ్చు."
        },
        "ta": {
            "title": "உண்ணாநிலை இரத்த குளுக்கோஸைப் புரிந்து கொள்ளுதல்",
            "content": "உண்ணாநிலை இரத்த குளுக்கோஸ் விரதத்திற்குப் பின் இரத்தத்தில் உள்ள குளுக்கோஸின் அளவை அளவிடுகிறது. ஆய்வக வரம்பிற்கு மேல் உள்ள முடிவு பின்தொடர்தலுக்கு உத்தரவாதம் அளிக்கலாம்."
        },
        "kn": {
            "title": "ಉಪವಾಸ ರಕ್ತದ ಗ್ಲೂಕೋಸ್ ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ಉಪವಾಸದ ರಕ್ತದ ಗ್ಲೂಕೋಸ್ ಉಪವಾಸದ ನಂತರ ರಕ್ತದಲ್ಲಿನ ಗ್ಲೂಕೋಸ್ ಪ್ರಮಾಣವನ್ನು ಅಳೆಯುತ್ತದೆ."
        },
        "ml": {
            "title": "ഫാസ്റ്റിംഗ് ബ്ലഡ് ഗ്ലൂക്കോസ് മനസ്സിലാക്കൽ",
            "content": "ഫാസ്റ്റിംഗ് ബ്ലഡ് ഗ്ലൂക്കോസ് ഉപവാസത്തിന് ശേഷം രക്തത്തിലെ ഗ്ലൂക്കോസിന്റെ അളവ് അളക്കുന്നു."
        },
        "mr": {
            "title": "फास्टिंग ब्लड ग्लुकोज समजून घेणे",
            "content": "फास्टिंग ब्लड ग्लुकोज उपाशी पोटी रक्तातील ग्लुकोजचे प्रमाण मोजते."
        },
        "bn": {
            "title": "ফাস্টিং ব্লাড গ্লুকোজ বোঝা",
            "content": "ফাস্টিং ব্লাড গ্লুকোজ খালি পেটে রক্তে গ্লুকোজের পরিমাণ পরিমাপ করে।"
        }
    },
    "hba1c": {
        "hi": {
            "title": "HbA1c को समझना",
            "content": "HbA1c पिछले लगभग 2 से 3 महीनों में औसत रक्त शर्करा के स्तर को मापता है। इसका उपयोग दीर्घकालिक रक्त शर्करा के मूल्यांकन के लिए किया जाता है।"
        },
        "te": {
            "title": "HbA1c ను అర్థం చేసుకోవడం",
            "content": "HbA1c గత 2 నుండి 3 నెలల్లో సగటు రక్తంలో చక్కెర స్థాయిని కొలుస్తుంది. ఇది దీర్ఘకాలిక రక్తంలో చక్కెర స్థాయిని అంచనా వేయడానికి ఉపయోగించబడుతుంది."
        },
        "ta": {
            "title": "HbA1c ஐப் புரிந்து கொள்ளுதல்",
            "content": "HbA1c கடந்த 2 முதல் 3 மாதங்களில் சராசரி இரத்த சர்க்கரை அளவை அளவிடுகிறது."
        },
        "kn": {
            "title": "HbA1c ಅನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "HbA1c ಕಳೆದ 2 ರಿಂದ 3 ತಿಂಗಳುಗಳಲ್ಲಿ ಸರಾಸರಿ ರಕ್ತದ ಸಕ್ಕರೆ ಮಟ್ಟವನ್ನು ಅಳೆಯುತ್ತದೆ."
        },
        "ml": {
            "title": "HbA1c മനസ്സിലാക്കൽ",
            "content": "HbA1c കഴിഞ്ഞ 2 മുതൽ 3 മാസങ്ങളിലെ ശരാശരി രക്തത്തിലെ പഞ്ചസാരയുടെ അളവ് അളക്കുന്നു."
        },
        "mr": {
            "title": "HbA1c समजून घेणे",
            "content": "HbA1c मागील 2 ते 3 महिन्यांमधील सरासरी रक्तातील साखरेची पातळी मोजते."
        },
        "bn": {
            "title": "HbA1c বোঝা",
            "content": "HbA1c বিগত প্রায় ২ থেকে ৩ মাসের রক্তে শর্করার গড় মাত্রা পরিমাপ করে।"
        }
    },
    "cholesterol": {
        "hi": {
            "title": "कोलेस्ट्रॉल के परिणामों को समझना",
            "content": "लिपिड प्रोफाइल में आमतौर पर एलडीएल, एचडीएल, कुल कोलेस्ट्रॉल और ट्राइग्लिसराइड्स शामिल होते हैं। कोलेस्ट्रॉल परिणामों की व्याख्या एक साथ की जाती है।"
        },
        "te": {
            "title": "కొలెస్ట్రాల్ ఫలితాలను అర్థం చేసుకోవడం",
            "content": "లిపిడ్ ప్రొఫైల్ లో సాధారణంగా LDL, HDL, మొత్తం కొలెస్ట్రాల్ మరియు ట్రైగ్లిజరైడ్స్ ఉంటాయి."
        },
        "ta": {
            "title": "கொலஸ்ட்ரால் முடிவுகளைப் புரிந்து கொள்ளுதல்",
            "content": "கொழுப்பு விவரக்குறிப்பில் பொதுவாக LDL, HDL, மொத்த கொலஸ்ட்ரால் மற்றும் ட்ரைகிளிசரைடுகள் அடங்கும்."
        },
        "kn": {
            "title": "ಕೊಲೆಸ್ಟ್ರಾಲ್ ಫಲಿತಾಂಶಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ಲಿಪಿಡ್ ಪ್ರೊಫೈಲ್ ಸಾಮಾನ್ಯವಾಗಿ LDL, HDL, ಒಟ್ಟು ಕೊಲೆಸ್ಟ್ರಾಲ್ ಮತ್ತು ಟ್ರೈಗ್ಲಿಸರೈಡ್‌ಗಳನ್ನು ಒಳಗೊಂಡಿರುತ್ತದೆ."
        },
        "ml": {
            "title": "കൊളസ്ട്രോൾ ഫലങ്ങൾ മനസ്സിലാക്കൽ",
            "content": "ലിപിഡ് പ്രൊഫൈലിൽ സാധാരണയായി LDL, HDL, ആകെ കൊളസ്ട്രോൾ, ട്രൈഗ്ലിസറൈഡുകൾ എന്നിവ ഉൾപ്പെടുന്നു."
        },
        "mr": {
            "title": "कोलेस्टेरॉलचे निकाल समजून घेणे",
            "content": "लिपिड प्रोफाइलमध्ये सामान्यतः LDL, HDL, एकूण कोलेस्टेरॉल आणि ट्रायग्लिसराइड्स असतात."
        },
        "bn": {
            "title": "কোলেস্টেরলের ফলাফল বোঝা",
            "content": "লিপিড প্রোফাইলে সাধারণত LDL, HDL, মোট কোলেস্টেরল এবং ট্রাইগ্লিসারাইড অন্তর্ভুক্ত থাকে।"
        }
    },
    "rdw": {
        "hi": {
            "title": "RDW को समझना",
            "content": "RDW लाल रक्त कोशिकाओं के आकार में भिन्नता का वर्णन करता है। बढ़ा हुआ RDW लाल कोशिकाओं के आकार में अधिक भिन्नता को इंगित करता है।"
        },
        "te": {
            "title": "RDW ను అర్థం చేసుకోవడం",
            "content": "RDW ఎర్ర రక్త కణాల పరిమాణంలో వ్యత్యాసాన్ని వివరిస్తుంది."
        },
        "ta": {
            "title": "RDW ஐப் புரிந்து கொள்ளுதல்",
            "content": "RDW இரத்த சிவப்பணுக்களின் அளவு மாறுபாட்டை விவரிக்கிறது."
        },
        "kn": {
            "title": "RDW ಅನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "RDW ಕೆಂಪು ರಕ್ತ ಕಣಗಳ ಗಾತ್ರದಲ್ಲಿನ ವ್ಯತ್ಯಾಸವನ್ನು ವಿವರಿಸುತ್ತದೆ."
        },
        "ml": {
            "title": "RDW മനസ്സിലാക്കൽ",
            "content": "RDW ചുവന്ന രക്താണുക്കളുടെ വലിപ്പ വ്യത്യാസത്തെ വിവരിക്കുന്നു."
        },
        "mr": {
            "title": "RDW समजून घेणे",
            "content": "RDW लाल रक्तपेशींच्या आकारातील फरक दर्शवतो."
        },
        "bn": {
            "title": "RDW বোঝা",
            "content": "RDW লোহিত রক্তকণিকার আকারের তারতম্য বর্ণনা করে।"
        }
    },
    "bilirubin": {
        "hi": {
            "title": "बिलीरुबिन को समझना",
            "content": "बिलीरुबिन तब बनता है जब लाल रक्त कोशिकाएं टूटती हैं और यह लिवर द्वारा संसाधित होता है। असामान्य बिलीरुबिन परिणामों की व्याख्या अन्य लिवर परीक्षणों के साथ की जाती है।"
        },
        "te": {
            "title": "బిలిరుబిన్ అర్థం చేసుకోవడం",
            "content": "ఎర్ర రక్త కణాలు విచ్ఛిన్నమైనప్పుడు బిలిరుబిన్ ఉత్పత్తి అవుతుంది మరియు కాలేయం ద్వారా ప్రాసెస్ చేయబడుతుంది."
        },
        "ta": {
            "title": "பிலிரூபினைப் புரிந்து கொள்ளுதல்",
            "content": "இரத்த சிவப்பணுக்கள் உடையும் போது பிலிரூபின் உருவாகிறது மற்றும் கல்லீரலால் செயலாக்கப்படுகிறது."
        },
        "kn": {
            "title": "ಬಿಲಿರುಬಿನ್ ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ಕೆಂಪು ರಕ್ತ ಕಣಗಳು ಒಡೆದಾಗ ಬಿಲಿರುಬಿನ್ ಉತ್ಪತ್ತಿಯಾಗುತ್ತದೆ ಮತ್ತು ಯಕೃತ್ತಿನಿಂದ ಸಂಸ್ಕರಿಸಲ್ಪಡುತ್ತದೆ."
        },
        "ml": {
            "title": "ബിലിറൂബിൻ മനസ്സിലാക്കൽ",
            "content": "ചുവന്ന രക്താണുക്കൾ നശിക്കുമ്പോഴാണ് ബിലിറൂബിൻ ഉണ്ടാകുന്നത്, ഇത് കരൾ സംസ്കരിക്കുന്നു."
        },
        "mr": {
            "title": "बिलीरुबिन समजून घेणे",
            "content": "लाल रक्तपेशी तुटतात तेव्हा बिलीरुबिन तयार होते आणि यकृत त्यावर प्रक्रिया करते."
        },
        "bn": {
            "title": "বিলিরুবিন বোঝা",
            "content": "লোহিত রক্তকণিকা ভেঙে গেলে বিলিরুবিন তৈরি হয় এবং যকৃৎ দ্বারা প্রক্রিয়াজাত হয়।"
        }
    },
    "kidney": {
        "hi": {
            "title": "गुर्दे से संबंधित रक्त परीक्षणों को समझना",
            "content": "गुर्दे के निस्पंदन (फ़िल्टरेशन) का आकलन करने के लिए क्रिएटिनिन का आमतौर पर उपयोग किया जाता है। स्वास्थ्य पेशेवर इसका मूल्यांकन अन्य नैदानिक जानकारी के साथ करते हैं।"
        },
        "te": {
            "title": "కిడ్నీ సంబంధిత రక్త పరీక్షలను అర్థం చేసుకోవడం",
            "content": "కిడ్నీ వడపోతను అంచనా వేసేటప్పుడు క్రియాటినిన్ సాధారణంగా ఉపయోగించబడుతుంది."
        },
        "ta": {
            "title": "சிறுநீரகம் தொடர்பான இரத்த பரிசோதனைகளைப் புரிந்து கொள்ளுதல்",
            "content": "சிறுநீரக வடிகட்டலை மதிப்பிடும் போது கிரியேட்டினின் பொதுவாக ஒரு குறிகாட்டியாகப் பயன்படுத்தப்படுகிறது."
        },
        "kn": {
            "title": "ಮೂತ್ರಪಿಂಡ ಸಂಬಂಧಿತ ರಕ್ತ ಪರೀಕ್ಷೆಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ಮೂತ್ರಪಿಂಡದ ಶೋಧನೆಯನ್ನು ನಿರ್ಣಯಿಸುವಾಗ ಕ್ರಿಯೇಟಿನೈನ್ ಅನ್ನು ಸಾಮಾನ್ಯವಾಗಿ ಬಳಸಲಾಗುತ್ತದೆ."
        },
        "ml": {
            "title": "വൃക്ക സംബന്ധമായ രക്തപരിശോധനകൾ മനസ്സിലാക്കൽ",
            "content": "വൃക്കകളുടെ പ്രവർത്തനം വിലയിരുത്തുമ്പോൾ ക്രിയാറ്റിനിൻ സാധാരണയായി ഒരു പ്രധാന ഘടകമായി ഉപയോഗിക്കുന്നു."
        },
        "mr": {
            "title": "मूत्रपिंडाशी संबंधित रक्त चाचण्या समजून घेणे",
            "content": "मूत्रपिंडाच्या कार्याचे मूल्यांकन करताना क्रिएटिनिनचा वापर केला जातो."
        },
        "bn": {
            "title": "কিডনি সংক্রান্ত রক্ত পরীক্ষা বোঝা",
            "content": "কিডনির কার্যকারিতা মূল্যায়নের জন্য ক্রিয়েটিনিন সাধারণত মার্কার হিসেবে ব্যবহৃত হয়।"
        }
    },
    "white_blood_cells": {
        "hi": {
            "title": "श्वेत रक्त कोशिका (WBC) परिणामों को समझना",
            "content": "श्वेत रक्त कोशिकाएं प्रतिरक्षा प्रणाली का हिस्सा हैं। सीबीसी में कुल डब्ल्यूबीसी और न्यूट्रोफिल, लिम्फोसाइट आदि शामिल हो सकते हैं।"
        },
        "te": {
            "title": "తెల్ల రక్త కణాల ఫలితాలను అర్థం చేసుకోవడం",
            "content": "తెల్ల రక్త కణాలు రోగనిరోధక వ్యవస్థలో భాగం."
        },
        "ta": {
            "title": "வெள்ளை இரத்த அணு முடிவுகளைப் புரிந்து கொள்ளுதல்",
            "content": "வெள்ளை இரத்த அணுக்கள் நோயெதிர்ப்பு மண்டலத்தின் ஒரு பகுதியாகும்."
        },
        "kn": {
            "title": "ಬಿಳಿ ರಕ್ತ ಕಣಗಳ ಫಲಿತಾಂಶಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ಬಿಳಿ ರಕ್ತ ಕಣಗಳು ರೋಗನಿರೋಧಕ ವ್ಯವಸ್ಥೆಯ ಭಾಗವಾಗಿದೆ."
        },
        "ml": {
            "title": "ശ്വേതരക്താണുക്കളുടെ ഫലങ്ങൾ മനസ്സിലാക്കൽ",
            "content": "ശ്വേതരക്താണുക്കൾ പ്രതിരോധ സംവിധാനത്തിന്റെ ഭാഗമാണ്."
        },
        "mr": {
            "title": "पांढऱ्या रक्तपेशींचे निकाल समजून घेणे",
            "content": "पांढऱ्या रक्तपेशी रोगप्रतिकारक शक्तीचा भाग आहेत."
        },
        "bn": {
            "title": "শ্বেত রক্তকণিকার ফলাফল বোঝা",
            "content": "শ্বেত রক্তকণিকা রোগ প্রতিরোধ ব্যবস্থার অংশ।"
        }
    },
    "platelets": {
        "hi": {
            "title": "प्लेटलेट काउंट को समझना",
            "content": "प्लेटलेट्स रक्त कोशिकाएं हैं जो शरीर में थक्का बनाने में मदद करती हैं। प्लेटलेट काउंट रक्त के नमूने में प्लेटलेट्स की संख्या को मापता है।"
        },
        "te": {
            "title": "ప్లేట్‌లెట్ సంఖ్యను అర్థం చేసుకోవడం",
            "content": "ప్లేట్‌లెట్లు రక్తం గడ్డకట్టడానికి సహాయపడే రక్త కణాలు."
        },
        "ta": {
            "title": "பிளேட்லெட் எண்ணிக்கையைப் புரிந்து கொள்ளுதல்",
            "content": "பிளேட்லெட்டுகள் இரத்தம் உறைவதற்கு உதவும் இரத்த அணுக்கள் ஆகும்."
        },
        "kn": {
            "title": "ಪ್ಲೇಟ್‌ಲೆಟ್ ಸಂಖ್ಯೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ಪ್ಲೇಟ್‌ಲೆಟ್‌ಗಳು ರಕ್ತ ಹೆಪ್ಪುಗಟ್ಟಲು ಸಹಾಯ ಮಾಡುವ ರಕ್ತ ಕಣಗಳಾಗಿವೆ."
        },
        "ml": {
            "title": "പ്ലേറ്റ്‌ലെറ്റ് എണ്ണം മനസ്സിലാക്കൽ",
            "content": "രക്തം കട്ടപിടിക്കാൻ സഹായിക്കുന്ന രക്തകോശങ്ങളാണ് പ്ലേറ്റ്‌ലെറ്റുകൾ."
        },
        "mr": {
            "title": "प्लेटलेट संख्या समजून घेणे",
            "content": "प्लेटलेट्स या रक्तपेशी आहेत ज्या शरीराला रक्त गोठण्यास मदत करतात."
        },
        "bn": {
            "title": "প্লেটলেট সংখ্যা বোঝা",
            "content": "প্লেটলেটগুলি রক্ত জমাট বাঁধতে সাহায্য করে।"
        }
    },
    "thyroid": {
        "hi": {
            "title": "थायरॉयड हार्मोन परीक्षणों को समझना",
            "content": "T3 और T4 थायरॉयड हार्मोन हैं। थायरॉयड परिणामों की व्याख्या लक्षणों और अन्य परीक्षणों के साथ की जाती है।"
        },
        "te": {
            "title": "థైరాయిడ్ హార్మోన్ పరీక్షలను అర్థం చేసుకోవడం",
            "content": "T3 మరియు T4 థైరాయిడ్ హార్మోన్లు."
        },
        "ta": {
            "title": "தைராய்டு ஹார்மோன் பரிசோதனைகளைப் புரிந்து கொள்ளுதல்",
            "content": "T3 மற்றும் T4 ஆகியவை தைராய்டு ஹார்மோன்கள் ஆகும்."
        },
        "kn": {
            "title": "ಥೈರಾಯ್ಡ್ ಹಾರ್ಮೋನ್ ಪರೀಕ್ಷೆಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "T3 ಮತ್ತು T4 ಥೈರಾಯ್ಡ್ ಹಾರ್ಮೋನುಗಳು."
        },
        "ml": {
            "title": "തൈറോയ്ഡ് ഹോർമോൺ പരിശോധനകൾ മനസ്സിലാക്കൽ",
            "content": "T3, T4 എന്നിവ തൈറോയ്ഡ് ഹോർമോണുകളാണ്."
        },
        "mr": {
            "title": "थायरॉईड संप्रेरक चाचण्या समजून घेणे",
            "content": "T3 आणि T4 हे थायरॉईड हार्मोन्स आहेत."
        },
        "bn": {
            "title": "থাইরয়েড হরমোন পরীক্ষা বোঝা",
            "content": "T3 এবং T4 হল থাইরয়েড হরমোন।"
        }
    },
    "liver_enzymes": {
        "hi": {
            "title": "लिवर एंजाइम परीक्षणों को समझना",
            "content": "ALT, AST, अल्कलाइन फॉस्फेटेस और GGT लिवर के स्वास्थ्य का मूल्यांकन करने के लिए महत्वपूर्ण एंजाइम हैं।"
        },
        "te": {
            "title": "కాలేయ ఎంజైమ్ పరీక్షలను అర్థం చేసుకోవడం",
            "content": "ALT, AST, ఆల్కలీన్ ఫాస్ఫటేస్ మరియు GGT కాలేయ సంబంధిత ఎంజైమ్‌లు."
        },
        "ta": {
            "title": "கல்லீரல் நொதி சோதனைகளைப் புரிந்து கொள்ளுதல்",
            "content": "ALT, AST, அல்கலைன் பாஸ்பேடேஸ் மற்றும் GGT ஆகியவை கல்லீரல் தொடர்பான நொதிகள் ஆகும்."
        },
        "kn": {
            "title": "ಯಕೃತ್ತಿನ ಕಿಣ್ವ ಪರೀಕ್ಷೆಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು",
            "content": "ALT, AST, ಆಲ್ಕಲೈನ್ ಫಾಸ್ಫಟೇಸ್ ಮತ್ತು GGT ಯಕೃತ್ತಿಗೆ ಸಂಬಂಧಿಸಿದ ಕಿಣ್ವಗಳಾಗಿವೆ."
        },
        "ml": {
            "title": "കരൾ എൻസൈം പരിശോധനകൾ മനസ്സിലാക്കൽ",
            "content": "ALT, AST, ആൽക്കലൈൻ ഫോസ്ഫേറ്റേസ്, GGT എന്നിവ കരൾ സംബന്ധമായ എൻസൈമുകളാണ്."
        },
        "mr": {
            "title": "यकृत एन्झाईम चाचण्या समजून घेणे",
            "content": "ALT, AST, अल्कधर्मी फॉस्फेटेस आणि GGT हे यकृताशी संबंधित एन्झाईम्स आहेत."
        },
        "bn": {
            "title": "যকৃতের এনজাইম পরীক্ষা বোঝা",
            "content": "ALT, AST, অ্যালকালাইন ফসফেটেজ এবং GGT হল যকৃতের সাথে সম্পর্কিত এনজাইম।"
        }
    }
}


def get_knowledge_translation(topic_id, lang):
    """Return localized knowledge item if available."""
    if lang == "en" or topic_id not in KNOWLEDGE_TRANSLATIONS:
        return None
    return KNOWLEDGE_TRANSLATIONS[topic_id].get(lang)


# =========================================================
# ORGAN TRANSLATIONS FOR IMAGING
# =========================================================

ORGAN_TRANSLATIONS = {
    "en": {
        "Left kidney and ureter": "Left kidney and ureter",
        "Right kidney": "Right kidney",
        "Left kidney": "Left kidney",
        "Kidneys": "Kidneys",
        "Ureter": "Ureter",
        "Gall bladder": "Gall bladder",
        "Liver": "Liver",
        "Pancreas": "Pancreas",
        "Spleen": "Spleen",
        "Urinary bladder": "Urinary bladder",
        "Uterus": "Uterus",
        "Ovaries": "Ovaries",
        "Imaging finding": "Imaging finding"
    },
    "hi": {
        "Left kidney and ureter": "बायां गुर्दा और मूत्रवाहिनी",
        "Right kidney": "दायां गुर्दा",
        "Left kidney": "बायां गुर्दा",
        "Kidneys": "गुर्दे",
        "Ureter": "मूत्रवाहिनी",
        "Gall bladder": "पित्ताशय",
        "Liver": "यकृत (लिवर)",
        "Pancreas": "अग्न्याशय",
        "Spleen": "प्लीहा (तिल्ली)",
        "Urinary bladder": "मूत्राशय",
        "Uterus": "गर्भाशय",
        "Ovaries": "अंडाशय",
        "Imaging finding": "इमेजिंग निष्कर्ष"
    },
    "te": {
        "Left kidney and ureter": "ఎడమ మూత్రపిండము మరియు మూత్రనాళము",
        "Right kidney": "కుడి మూత్రపిండము",
        "Left kidney": "ఎడమ మూత్రపిండము",
        "Kidneys": "మూత్రపిండాలు",
        "Ureter": "యూరెటర్",
        "Gall bladder": "పిత్తాశయం",
        "Liver": "కాలేయం",
        "Pancreas": "క్లోమం",
        "Spleen": "ప్లీహము",
        "Urinary bladder": "మూత్రాశయం",
        "Uterus": "గర్భాశయం",
        "Ovaries": "అండాశయాలు",
        "Imaging finding": "ఇమేజింగ్ ఫలితం"
    },
    "ta": {
        "Left kidney and ureter": "இடது சிறுநீரகம் மற்றும் சிறுநீர்க்குழாய்",
        "Right kidney": "வலது சிறுநீரகம்",
        "Left kidney": "இடது சிறுநீரகம்",
        "Kidneys": "சிறுநீரகங்கள்",
        "Ureter": "சிறுநீர்க்குழாய்",
        "Gall bladder": "பித்தப்பை",
        "Liver": "கல்லீரல்",
        "Pancreas": "கணையம்",
        "Spleen": "மண்ணீரல்",
        "Urinary bladder": "சிறுநீர்ப்பை",
        "Uterus": "கருப்பை",
        "Ovaries": "கருப்பைகள்",
        "Imaging finding": "இமேஜிங் கண்டுபிடிப்பு"
    },
    "kn": {
        "Left kidney and ureter": "ಎಡ ಮೂತ್ರಪಿಂಡ ಮತ್ತು ಮೂತ್ರನಾಳ",
        "Right kidney": "ಬಲ ಮೂತ್ರಪಿಂಡ",
        "Left kidney": "ಎಡ ಮೂತ್ರಪಿಂಡ",
        "Kidneys": "ಮೂತ್ರಪಿಂಡಗಳು",
        "Ureter": "ಮೂತ್ರನಾಳ",
        "Gall bladder": "ಪಿತ್ತಕೋಶ",
        "Liver": "ಯಕೃತ್ತು",
        "Pancreas": "ಮೇದೋಜೀರಕ ಗ್ರಂಥಿ",
        "Spleen": "ಗುಲ್ಮ",
        "Urinary bladder": "ಮೂತ್ರಕೋಶ",
        "Uterus": "ಗರ್ಭಾಶಯ",
        "Ovaries": "ಅಂಡಾಶಯಗಳು",
        "Imaging finding": "ಇಮೇಜಿಂಗ್ ಫಲಿತಾಂಶ"
    },
    "ml": {
        "Left kidney and ureter": "ഇടത് വൃക്കയും മൂത്രനാളിയും",
        "Right kidney": "വലത് വൃക്ക",
        "Left kidney": "ഇടത് വൃക്ക",
        "Kidneys": "വൃക്കകൾ",
        "Ureter": "മൂത്രനാളി",
        "Gall bladder": "പിത്താശയം",
        "Liver": "കരൾ",
        "Pancreas": "പാൻക്രിയാസ്",
        "Spleen": "പ്ലീഹ",
        "Urinary bladder": "മൂത്രസഞ്ചി",
        "Uterus": "ഗർഭാശയം",
        "Ovaries": "അണ്ഡാശയങ്ങൾ",
        "Imaging finding": "ഇമേജിംഗ് കണ്ടെത്തൽ"
    },
    "mr": {
        "Left kidney and ureter": "डावे मूत्रपिंड आणि मूत्रवाहिनी",
        "Right kidney": "उजवे मूत्रपिंड",
        "Left kidney": "डावे मूत्रपिंड",
        "Kidneys": "मूत्रपिंड",
        "Ureter": "मूत्रवाहिनी",
        "Gall bladder": "पित्ताशय",
        "Liver": "यकृत",
        "Pancreas": "स्वादुपिंड",
        "Spleen": "प्लीहा",
        "Urinary bladder": "मूत्राशय",
        "Uterus": "गर्भाशय",
        "Ovaries": "अंडाशय",
        "Imaging finding": "इमेजिंग निष्कर्ष"
    },
    "bn": {
        "Left kidney and ureter": "বাম কিডনি এবং ইউরেটার",
        "Right kidney": "ডান কিডনি",
        "Left kidney": "বাম কিডনি",
        "Kidneys": "কিডনি",
        "Ureter": "ইউরেটার",
        "Gall bladder": "পিত্তথলি",
        "Liver": "যকৃৎ",
        "Pancreas": "অগ্ন্যাশয়",
        "Spleen": "প্লীহা",
        "Urinary bladder": "মূত্রথলি",
        "Uterus": "জরায়ু",
        "Ovaries": "ডিম্বাশয়",
        "Imaging finding": "ইমেজিং ফলাফল"
    }
}


def get_organ_translation(organ_name, lang):
    """Return localized organ name."""
    organs = ORGAN_TRANSLATIONS.get(lang, ORGAN_TRANSLATIONS["en"])
    return organs.get(organ_name, organ_name)
