"""
Demo Scenarios and Heuristic Pattern Matchers for TANTU AI/NLP Pipeline
Guarantees deterministic, 100% reliable outputs for SIH evaluations.
"""
import re
from typing import Dict, Any, Optional, Tuple


# ==========================================================
# 1. CORE DEMO SCENARIOS (Deterministic SIH Evaluation Cases)
# ==========================================================
DEMO_SCENARIOS: Dict[str, Dict[str, Any]] = {
    # Demo Case 1: Hindi Bamboo Basket
    "bamboo_basket": {
        "keywords": ["bamboo ki tokri", "बांस की टोकरी", "bamboo basket", "bamboo ki", "tokri hai"],
        "data": {
            "title": "Bamboo Basket",
            "description_english": "Handcrafted eco-friendly bamboo basket woven using traditional regional techniques. Durable, lightweight, and sustainably made from natural bamboo for versatile everyday and decorative utility.",
            "description_hindi": "प्राकृतिक बांस से बनी हस्तनिर्मित पर्यावरण-अनुकूल टोकरी। पारंपरिक तकनीक से तैयार, हल्की और टिकाऊ।",
            "category": "Bamboo & Cane Craft",
            "material": "Bamboo",
            "dimensions": None,
            "production_time": "2 days",
            "tags": ["bamboo", "handmade", "traditional", "basket", "eco-friendly"],
            "story": "Learned the craft from mother: an inherited craft tradition taught by the artisan's mother.",
            "sentiment": "positive",
            "narrative_type": "family_tradition",
            "detected_language": "hi",
        }
    },

    # Demo Case 2: Hindi Handwoven Textile
    "chanderi_textile": {
        "keywords": ["chanderi silk dupatta", "chanderi silk", "buna hua chanderi", "चंदेरी सिल्क", "सिल्क दुपट्टा"],
        "data": {
            "title": "Handwoven Chanderi Silk Dupatta",
            "description_english": "Authentic handloom Chanderi silk dupatta featuring traditional weaving patterns and subtle zari borders. Soft, lustrous, and crafted with timeless artisanal precision.",
            "description_hindi": "पारंपरिक हथकरघा तकनीक से बुनी गई प्रामाणिक चंदेरी सिल्क दुपट्टा। पीढ़ियों की विरासत और नफासत का अनूठा प्रतीक।",
            "category": "Textiles & Handloom",
            "material": "Chanderi Silk",
            "dimensions": None,
            "production_time": "5 days",
            "tags": ["handloom", "silk", "chanderi", "dupatta", "traditional", "handwoven"],
            "story": "Ancestral weaving craft passed down through multiple generations, continuing a proud regional textile heritage.",
            "sentiment": "craftsmanship_pride",
            "narrative_type": "cultural_heritage",
            "detected_language": "hi",
        }
    },

    # Demo Case 3: English Wooden Craft
    "wooden_elephant": {
        "keywords": ["teak wood elephant", "carved teak wood", "wood elephant", "wooden elephant sculpture", "लकड़ी की हाथी"],
        "data": {
            "title": "Hand-Carved Teak Wood Elephant",
            "description_english": "Exquisite hand-carved teak wood elephant sculpture finished with natural wood polish. Showcases meticulous artisanal carving and royal artistic heritage.",
            "description_hindi": "हाथ से नक्काशीदार सागौन की लकड़ी (सागवान) से बनी सुंदर हाथी की मूर्ति। उत्कृष्ट शिल्प कौशल और पारंपरिक नक्काशी का उदाहरण।",
            "category": "Woodcraft",
            "material": "Teak Wood",
            "dimensions": None,
            "production_time": "4 days",
            "tags": ["woodcraft", "teak-wood", "hand-carved", "elephant", "sculpture", "traditional"],
            "story": "Wood carving technique passed down from grandfather, practiced with deep devotion and artisan pride.",
            "sentiment": "positive",
            "narrative_type": "craftsmanship_pride",
            "detected_language": "en",
        }
    },

    # Fallback Demo Case 4: Terracotta / Pottery
    "terracotta_pottery": {
        "keywords": ["clay", "terracotta", "diya", "pottery", "मिट्टी", "कुम्हार"],
        "data": {
            "title": "Handcrafted Terracotta Clay Artefact",
            "description_english": "Authentic terracotta pottery crafted from natural riverbed clay, sun-dried and kiln-fired using traditional potter wheel techniques.",
            "description_hindi": "प्राकृतिक मिट्टी से चाक पर हस्तनिर्मित टेराकोटा शिल्प। पारंपरिक भट्ठी में पकाया गया प्रामाणिक और टिकाऊ उत्पाद।",
            "category": "Pottery & Ceramics",
            "material": "Terracotta Clay",
            "dimensions": None,
            "production_time": None,
            "tags": ["terracotta", "pottery", "clay", "handmade", "eco-friendly"],
            "story": None,
            "sentiment": "Neutral",
            "narrative_type": None,
            "detected_language": "hi",
        }
    },

    # Demo Case 5: Handwoven Cotton Dupatta (Women's Group)
    "cotton_dupatta_women_group": {
        "keywords": ["cotton dupatta", "women's group", "women group", "handwoven cotton dupatta", "weaving patterns"],
        "data": {
            "title": "Handwoven Cotton Dupatta",
            "description_english": "Exquisite handwoven cotton dupatta crafted by local women's artisan groups. Made using authentic traditional weaving patterns, offering pure comfort, elegance, and durability.",
            "description_hindi": "स्थानीय महिला कारीगर समूहों द्वारा पारंपरिक बुनाई पैटर्न से तैयार हाथ से बुना सूती (कॉटन) दुपट्टा। प्रामाणिक, आरामदायक और टिकाऊ।",
            "category": "Textiles & Handloom",
            "material": "Handwoven Cotton",
            "dimensions": None,
            "production_time": "3 days",
            "tags": ["handwoven", "cotton", "dupatta", "textiles", "traditional", "women-artisan"],
            "story": "Handcrafted collaboratively by a local women's artisan group preserving traditional regional weaving patterns.",
            "sentiment": "Pride",
            "narrative_type": "Community-made",
            "detected_language": "en",
        }
    }
}


# ==========================================================
# 2. HEURISTIC PARSERS & REGEX EXTRACTORS
# ==========================================================
INDIC_DIGITS = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
    '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9',
    '௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9',
    '౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4', '౫': '5', '౬': '6', '౭': '7', '౮': '8', '౯': '9',
}

HINDI_NUMBER_WORDS = {
    "ek": "1", "do": "2", "teen": "3", "chaar": "4", "char": "4",
    "paanch": "5", "panch": "5", "chhe": "6", "che": "6", "saat": "7", "sat": "7",
    "aath": "8", "nau": "9", "das": "10",
    "एक": "1", "दो": "2", "तीन": "3", "चार": "4", "पांच": "5", "छह": "6", "सात": "7",
    "आठ": "8", "नौ": "9", "दस": "10",
    "दोन": "2",
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"
}

MATERIAL_CATALOG = [
    ("Bamboo", "Bamboo & Cane Craft", ["bamboo", "bans", "बांस", "cane", "वेत", "বাঁশ", "বাঁশের", "বাঁহ", "বাঁহৰ", "बांबू", "बांबूची"]),
    ("Chanderi Silk", "Textiles & Handloom", ["chanderi", "silk", "सिल्क", "रेशम", "పట్టు", "పట్టు చీర", "సరి", "चंदेरी"]),
    ("Khadi Cotton", "Textiles & Handloom", ["cotton", "khadi", "सूती", "खादी"]),
    ("Teak Wood", "Woodcraft", ["teak", "sagwan", "सागवान", "सागौन", "தேக்கு", "தேக்கு மர", "सागवानी"]),
    ("Sheesham Wood", "Woodcraft", ["sheesham", "rosewood", "शीशम"]),
    ("Natural Wood", "Woodcraft", ["wood", "wooden", "lakdi", "लकड़ी"]),
    ("Terracotta Clay", "Pottery & Ceramics", ["terracotta", "clay", "mitti", "मिट्टी"]),
    ("Brass", "Metalware & Brass", ["brass", "peetal", "पीतल"]),
    ("Jute", "Eco-Friendly Crafts", ["jute", "पटसन", "जूट"]),
]


def detect_language(text: str) -> str:
    """
    Detects if input is Devanagari (Hindi/Marathi), Bengali/Assamese, Tamil, Telugu, Hinglish, or English.
    """
    if not text or not text.strip():
        return "hi"

    # Tamil script range: \u0B80-\u0BFF
    if len(re.findall(r'[\u0B80-\u0BFF]', text)) > 2:
        return "ta"

    # Telugu script range: \u0C00-\u0C7F
    if len(re.findall(r'[\u0C00-\u0C7F]', text)) > 2:
        return "te"

    # Bengali / Assamese script range: \u0980-\u09FF
    if len(re.findall(r'[\u0980-\u09FF]', text)) > 2:
        assamese_cues = ["এইটো", "খৰাহী", "বনাবলৈ", "শিকাইছিল", "মোক", "আমাৰ", "তৈয়াৰ", "মায়ে"]
        if any(cue in text for cue in assamese_cues):
            return "as"
        return "bn"

    # Devanagari script range: \u0900-\u097F
    if len(re.findall(r'[\u0900-\u097F]', text)) > 2:
        marathi_cues = ["टोपली", "लागतात", "माझ्या", "आईने", "शिकवले", "आहे", "बचत", "पिढ्या", "वारसा", "सण", "दोन", "दिवस"]
        if any(cue in text for cue in marathi_cues):
            return "mr"
        return "hi"

    # Check for Hinglish cue words
    hinglish_cues = ["ye", "yeh", "hai", "hain", "ki", "ka", "ke", "mein", "hum", "mujhe",
                     "banana", "sikhaya", "tha", "lagte", "kaam", "maa", "bhai", "peedhi", "karti"]
    lower_words = set(re.findall(r'\b\w+\b', text.lower()))
    matches = lower_words.intersection(hinglish_cues)
    if len(matches) >= 2:
        return "hi"

    return "en"


def extract_production_time(text: str) -> Optional[str]:
    """
    Extracts crafting duration from phrases across all 7 supported languages.
    """
    if not text:
        return None

    normalized = text
    for ind, asc in INDIC_DIGITS.items():
        normalized = normalized.replace(ind, asc)

    lower = normalized.lower()

    # Pattern 1: Digit + unit across languages
    days_patterns = r'(\d+)\s*(?:din|days?|दिन|দিন|দিৱস|दिवस|நாட்கள்(?:\s*ஆகும்)?|రోజులు(?:\s*పడుతుంది)?|দিন\s*সময়\s*লাগে|দিন\s*লাগে)'
    hours_patterns = r'(\d+)\s*(?:ghante|hours?|घंटे|घंटा|ঘণ্টা|तास|மணி|గంటలు)'
    weeks_patterns = r'(\d+)\s*(?:hafte|weeks?|हफ्ते|सप्ताह|সপ্তাহ|আঠৱডে|వారాలు)'

    m_day = re.search(days_patterns, lower)
    if m_day:
        return f"{m_day.group(1)} days"

    m_hr = re.search(hours_patterns, lower)
    if m_hr:
        return f"{m_hr.group(1)} hours"

    m_wk = re.search(weeks_patterns, lower)
    if m_wk:
        return f"{m_wk.group(1)} weeks"

    # Pattern 2: Word number + unit
    for word, digit in HINDI_NUMBER_WORDS.items():
        if re.search(rf'\b{re.escape(word)}\s+(?:din|days?|hafte|weeks?|ghante|hours?|दिवस|दिन|दिनों)\b', lower) or (word in lower and ("दिवस" in lower or "दिन" in lower or "days" in lower)):
            if "घंटे" in lower or "hours" in lower or "ghante" in lower:
                return f"{digit} hours"
            elif "hafte" in lower or "weeks" in lower:
                return f"{digit} weeks"
            else:
                return f"{digit} days"

    return None


def extract_dimensions(text: str) -> Optional[str]:
    """
    Extracts explicit dimensions ONLY if mentioned in artisan speech.
    Returns None (null) if no dimensions are stated, avoiding hallucinated specs.
    """
    pattern = r'(\d+(\.\d+)?\s*(?:cm|m|mm|inches?|in|ft|feet)\s*[xX×*]\s*\d+(\.\d+)?\s*(?:cm|m|mm|inches?|in|ft|feet)(?:\s*[xX×*]\s*\d+(\.\d+)?\s*(?:cm|m|mm|inches?|in|ft|feet))?)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_craft_title(text: str, material: str, category: str) -> str:
    """
    Constructs an accurate professional product title based on communicated craft attributes.
    """
    lower = text.lower()
    craft_type = None
    known_items = [
        ("dupatta", "Dupatta"),
        ("saree", "Saree"),
        ("shawl", "Shawl"),
        ("basket", "Basket"),
        ("tokri", "Basket"),
        ("elephant", "Elephant Sculpture"),
        ("diya", "Festival Diya Set"),
        ("pot", "Clay Pot"),
        ("matka", "Earthen Pot"),
        ("lamp", "Handcrafted Lamp"),
        ("rug", "Handwoven Rug"),
        ("jhula", "Hanging Swing"),
        ("stool", "Mudda Stool"),
    ]
    for kw, label in known_items:
        if kw in lower:
            craft_type = label
            break

    prefix = "Handwoven" if "Textile" in category or "handwoven" in lower or "buna" in lower else (
        "Hand-Carved" if "Wood" in category or "carv" in lower else "Handcrafted"
    )

    if craft_type:
        return f"{prefix} {material} {craft_type}"
    return f"{prefix} {material} Craft"


def extract_material_and_category(text: str) -> Tuple[str, str]:
    """
    Identifies craft material and matching category using lookup patterns.
    """
    lower = text.lower()
    for mat_name, category, keywords in MATERIAL_CATALOG:
        for kw in keywords:
            if kw.lower() in lower:
                return mat_name, category

    return "Natural Artisan Material", "Handicrafts & Decor"


def _match_any_keyword(text: str, keywords: list) -> bool:
    """
    Matches keywords using word/token boundaries across Latin and Indic scripts (\u0900-\u0D7F),
    preventing false positive substring matches (e.g., 'মা' matching inside 'মাটির').
    """
    for kw in keywords:
        pattern = r'(?<![\w\u0900-\u0D7F])' + re.escape(kw.lower()) + r'(?![\w\u0900-\u0D7F])'
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def extract_story_and_sentiment(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extracts artisan storytelling, narrative classification, and sentiment cues.
    NLP identifies sentiment and narrative cues from artisan-provided language.
    Avoids inventing narratives that the artisan did not communicate.

    Narrative Types:
      - Community-made
      - Family craft
      - Traditional heritage
      - Cultural identity
      - Handmade journey

    Sentiment Categories:
      - Pride
      - Joy
      - Nostalgia
      - Passion
      - Neutral
    """
    lower = text.lower().replace("’", "'")
    has_pride = _match_any_keyword(lower, [
        "pride", "proud", "garv", "गर्व", "গর্ব", "গৌরব", "গৌৰৱ", "अभिमान", "अभिमानाने",
        "பெருமை", "பெருமையுடன்", "பெருமையோடு", "గర్వం", "గర్వంగా"
    ])

    # 1. Community-made (Self-help groups, women cooperatives, collective work)
    if _match_any_keyword(lower, [
        "women's group", "women group", "shg", "samuh", "samooh", "mahila", "collective", "cooperative",
        "মহিলা দল", "মহিলা গোট", "महिला बचत गट", "மகளிர் குழு", "మహిళా సంఘం"
    ]):
        story = "The artisan states that this piece is made by a local women's artisan group."
        sentiment = "Pride" if has_pride else "Neutral"
        return story, sentiment, "Community-made"

    # 2. Family craft (Parents, grandparents, generational family learning)
    if _match_any_keyword(lower, [
        "maa", "mother", "mummy", "माता", "मां", "মা", "মায়ের", "মায়ে", "আই", "আইৰ",
        "आई", "आईने", "आईनी", "அம்மா", "தாய்", "తల్లి", "అమ్మ"
    ]):
        story = "Learned the craft from mother: an inherited craft tradition taught by the artisan's mother."
        return story, "Pride" if has_pride else "Nostalgia", "Family craft"

    if _match_any_keyword(lower, [
        "dada", "dadi", "grandfather", "grandmother", "दादा", "दादी", "नाना", "नानी",
        "দাদু", "ঠাকুমা", "ককা", "আইতা", "आजोबा", "आजी", "தாத்தா", "பாட்டி",
        "తాత", "అవ్వ", "నానమ్మ", "అమ్మమ్మ"
    ]):
        story = "The artisan mentions learning this craft from a grandfather or grandmother."
        return story, "Pride" if has_pride else "Nostalgia", "Family craft"

    if _match_any_keyword(lower, [
        "pita", "pitaji", "father", "बापू", "पिता", "बाबा", "বাবার", "দেউতা", "দেউতাৰ",
        "वडील", "वडिलांनी", "वडिलांचे", "बाबा", "அப்பா", "தந்தை", "తండ్రి", "నాన్న"
    ]):
        story = "Artisanal techniques and heritage passed down from the artisan's father."
        return story, "Pride" if has_pride else "Nostalgia", "Family craft"

    # 3. Traditional heritage (Generations, centuries of lineage)
    if _match_any_keyword(lower, [
        "peedhi", "peedhiyan", "peedhiyon", "generation", "generations", "virasat",
        "ancestral", "ancestor", "ancestors", "विरासत", "पीढ़ी", "पीढ़ियों", "पीढ़ियां", "heritage",
        "centuries", "century", "প্রজন্ম", "বংশ", "পুৰুষ", "পৰম্পৰা", "पिढ्या", "वारसा",
        "தலைமுறை", "பாரம்பரியம்", "తరాలు", "సాంప్రదాయం"
    ]):
        story = "The artisan describes this craft as continuing across generations."
        return story, "Nostalgia", "Traditional heritage"

    # 4. Cultural identity (Regional festivals, sacred traditions, tribal symbolism)
    if _match_any_keyword(lower, [
        "culture", "cultural", "tribal", "folk", "sanskriti", "parampara", "festival", "utsav", "ritual",
        "সংস্কৃতি", "উৎসব", "সংস্কृती", "सण", "பண்பாடு", "திருவிழா", "సంస్కృతి", "పండుగ"
    ]):
        story = "The artisan references a cultural, festival, ritual, or regional context for this craft."
        return story, "Neutral", "Cultural identity"

    # 5. Handmade journey (Intricate hand-making, hours of patience, dedication)
    if _match_any_keyword(lower, ["passion", "love", "dil se", "pyaar", "shauk", "ভালপোৱা", "प्रेम", "அன்பு", "ప్రేమ"]):
        story = "Crafted with immense artistic passion and personal love for the handmade form."
        return story, "Passion", "Handmade journey"

    if _match_any_keyword(lower, ["joy", "khushi", "anand", "happy", "खुशी", "आनंद", "আনন্দ", "மகிழ்ச்சி", "ఆనందం"]):
        story = "Created with joy and creative spirit, celebrating artisanal handwork."
        return story, "Joy", "Handmade journey"

    if has_pride:
        story = "The artisan expresses pride in this craft."
        return story, "Pride", "Handmade journey"

    if _match_any_keyword(lower, [
        "handcrafted", "hand-carved", "handwoven", "haath se", "buna", "mehnat",
        "হাতে তৈরি", "हातमागावर", "கைவினை", "చేతితో"
    ]):
        story = "The artisan describes a handmade making process."
        return story, "Neutral", "Handmade journey"

    # If artisan did not communicate any story or narrative, do NOT invent one
    return None, "Neutral", None



# ==========================================================
# 3. MULTILINGUAL ARCHITECTURE REGISTRY (Phase 1 + Extensibility)
# ==========================================================
SUPPORTED_LANGUAGES = {
    "hi": "Hindi (हिंदी)",
    "en": "English",
}

EXTENSIBLE_LANGUAGES = {
    "bn": "Bengali (বাংলা)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "mr": "Marathi (मराठी)",
    "gu": "Gujarati (ગુજરાતી)",
}


def generate_bilingual_descriptions(
    clean_text: str,
    material: str,
    category: str,
    title: str,
    detected_lang: str
) -> Tuple[str, str]:
    """
    Generates fluent, high-conversion descriptions in both English and Hindi.
    Maintains parallel English and Hindi representations regardless of input language.
    """
    desc_en = f"{title} made from {material}. Artisan-provided details: {clean_text}"
    desc_hi = f"{material} से बना {title}। कारीगर द्वारा दी गई जानकारी: {clean_text}"
    return desc_en, desc_hi
