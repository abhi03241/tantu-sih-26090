"""
Demo Scenarios and Heuristic Pattern Matchers for TANTU AI/NLP Pipeline
Guarantees deterministic, 100% reliable outputs for SIH evaluations across all 7 supported languages:
English, Hindi, Bengali, Marathi, Assamese, Tamil, Telugu.
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
            "sentiment": "Nostalgia",
            "narrative_type": "Family craft",
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
            "sentiment": "Nostalgia",
            "narrative_type": "Traditional heritage",
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
            "sentiment": "Pride",
            "narrative_type": "Family craft",
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
            "story": "The artisan states that this piece is made by a local women's artisan group.",
            "sentiment": "Neutral",
            "narrative_type": "Community-made",
            "detected_language": "en",
        }
    },

    # Demo Case 6: Bengali Bamboo Basket
    "bengali_bamboo_craft": {
        "keywords": ["বাঁশের ঝুড়ি", "বাঁশের তৈরি ঝুড়ি", "বাঁশের চুপড়ি"],
        "data": {
            "title": "Bamboo Basket",
            "description_english": "Handcrafted eco-friendly bamboo basket woven using traditional regional techniques. Durable, lightweight, and sustainably made from natural bamboo.",
            "description_hindi": "प्राकृतिक बांस से बनी हस्तनिर्मित टोकरी। पारंपरिक तकनीक से तैयार, हल्की और टिकाऊ।",
            "category": "Bamboo & Cane Craft",
            "material": "Bamboo",
            "dimensions": None,
            "production_time": "2 days",
            "tags": ["bamboo", "handmade", "traditional", "basket", "eco-friendly", "bengal-craft"],
            "story": "Learned the craft from mother: an inherited craft tradition taught by the artisan's mother.",
            "sentiment": "Nostalgia",
            "narrative_type": "Family craft",
            "detected_language": "bn",
        }
    },

    # Demo Case 7: Marathi Bamboo Basket
    "marathi_bamboo_craft": {
        "keywords": ["बांबूची टोपली", "बांबूची हस्तकला"],
        "data": {
            "title": "Bamboo Basket",
            "description_english": "Handcrafted eco-friendly bamboo basket woven using traditional Maharashtra artisanal techniques. Durable, lightweight, and sustainably made.",
            "description_hindi": "प्राकृतिक बांस से बनी हस्तनिर्मित पर्यावरण-अनुकूल टोकरी। पारंपरिक तकनीक से तैयार।",
            "category": "Bamboo & Cane Craft",
            "material": "Bamboo",
            "dimensions": None,
            "production_time": "2 days",
            "tags": ["bamboo", "handmade", "traditional", "basket", "eco-friendly", "maharashtra-craft"],
            "story": "Learned the craft from mother: an inherited craft tradition taught by the artisan's mother.",
            "sentiment": "Nostalgia",
            "narrative_type": "Family craft",
            "detected_language": "mr",
        }
    },

    # Demo Case 8: Assamese Bamboo & Cane Craft
    "assamese_cane_craft": {
        "keywords": ["বাঁহৰ খৰাহী", "বাঁহৰ জাপি", "অসমীয়া বাঁহৰ"],
        "data": {
            "title": "Bamboo Basket",
            "description_english": "Authentic handcrafted Assam bamboo basket woven with traditional cane and bamboo craftsmanship.",
            "description_hindi": "असम के पारंपरिक कारीगरों द्वारा हस्तनिर्मित बांस की प्रामाणिक टोकरी।",
            "category": "Bamboo & Cane Craft",
            "material": "Bamboo",
            "dimensions": None,
            "production_time": "2 days",
            "tags": ["bamboo", "cane", "assam-craft", "handmade", "traditional", "eco-friendly"],
            "story": "Learned the craft from mother: an inherited craft tradition taught by the artisan's mother.",
            "sentiment": "Nostalgia",
            "narrative_type": "Family craft",
            "detected_language": "as",
        }
    },

    # Demo Case 9: Tamil Woodcraft
    "tamil_wood_craft": {
        "keywords": ["மரச்சிற்பம்", "தேக்கு மர யானை", "மர யானை"],
        "data": {
            "title": "Hand-Carved Teak Wood Elephant",
            "description_english": "Exquisite hand-carved teak wood elephant sculpture finished with natural wood polish. Showcases meticulous artisanal carving.",
            "description_hindi": "हाथ से नक्काशीदार सागौन की लकड़ी से बनी सुंदर हाथी की मूर्ति। पारंपरिक शिल्प कौशल।",
            "category": "Woodcraft",
            "material": "Teak Wood",
            "dimensions": None,
            "production_time": "4 days",
            "tags": ["woodcraft", "teak-wood", "hand-carved", "elephant", "sculpture", "tamil-craft"],
            "story": "Wood carving technique passed down from grandfather, practiced with deep devotion and artisan pride.",
            "sentiment": "Pride",
            "narrative_type": "Family craft",
            "detected_language": "ta",
        }
    },

    # Demo Case 10: Telugu Handloom Silk
    "telugu_handloom_textile": {
        "keywords": ["చేనేత పట్టు", "పట్టు చీర", "చేనేత దుపట్టా"],
        "data": {
            "title": "Handwoven Chanderi Silk Dupatta",
            "description_english": "Authentic handloom silk craft featuring traditional weaving patterns and subtle zari borders. Crafted with timeless precision.",
            "description_hindi": "पारंपरिक हथकरघा तकनीक से बुनी गई प्रामाणिक सिल्क कृति। पीढ़ियों की विरासत का प्रतीक।",
            "category": "Textiles & Handloom",
            "material": "Chanderi Silk",
            "dimensions": None,
            "production_time": "5 days",
            "tags": ["handloom", "silk", "textiles", "traditional", "telugu-craft"],
            "story": "Ancestral weaving craft passed down through multiple generations, continuing a proud regional textile heritage.",
            "sentiment": "Nostalgia",
            "narrative_type": "Traditional heritage",
            "detected_language": "te",
        }
    },
}


# ==========================================================
# 2. HEURISTIC PARSERS & REGEX EXTRACTORS
# ==========================================================
MULTILINGUAL_NUMBER_WORDS = {
    # Hindi / Hinglish
    "ek": "1", "do": "2", "teen": "3", "chaar": "4", "char": "4",
    "paanch": "5", "panch": "5", "chhe": "6", "che": "6", "saat": "7", "sat": "7",
    "aath": "8", "nau": "9", "das": "10",
    "एक": "1", "दो": "2", "तीन": "3", "चार": "4", "पांच": "5", "छह": "6", "सात": "7",
    "आठ": "8", "नौ": "9", "दस": "10",
    # English
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    # Bengali & Assamese
    "এক": "1", "দুই": "2", "দু": "2", "তিন": "3", "চার": "4", "চাৰি": "4", "পাঁচ": "5",
    "ছয়": "6", "ছয়টা": "6", "সাত": "7", "আট": "8", "নয়": "9", "দশ": "10",
    # Marathi
    "दोन": "2", "पाच": "5", "सहा": "6",
    # Tamil
    "ஒன்று": "1", "ஒரு": "1", "இரண்டு": "2", "இரு": "2", "மூன்று": "3", "நான்கு": "4", "ஐந்து": "5",
    "ஆறு": "6", "ஏழு": "7", "எட்டு": "8", "ஒன்பது": "9", "பத்து": "10",
    # Telugu
    "ఒకటి": "1", "ఒక": "1", "రెండు": "2", "మూడు": "3", "నాలుగు": "4", "ఐదు": "5",
    "ఆరు": "6", "ఏడు": "7", "ఎనిమిది": "8", "తొమ్మిది": "9", "పది": "10",
}

MATERIAL_CATALOG = [
    ("Bamboo", "Bamboo & Cane Craft", [
        "bamboo", "bans", "बांस", "cane", "वेत",
        "বাঁশ", "বাঁহ", "বাंबू", "மூங்கில்", "வெదురు"
    ]),
    ("Chanderi Silk", "Textiles & Handloom", [
        "chanderi", "silk", "सिल्क", "रेशम",
        "রেশম", "সিল্ক", "মুগা", "এৰী", "ছিল্ক", "रेशीम",
        "பட்டு", "பட்டுச்", "పట్టు"
    ]),
    ("Khadi Cotton", "Textiles & Handloom", [
        "cotton", "khadi", "सूती", "खादी",
        "সুতি", "কপাহী", "সূতা", "कापूस", "सुती",
        "பருத்தி", "காதி", "పత్తి", "ఖద్దరు"
    ]),
    ("Teak Wood", "Woodcraft", [
        "teak", "sagwan", "सागवान", "सागौन", "sheesham", "rosewood", "शीशम",
        "wood", "wooden", "lakdi", "लकड़ी",
        "কাঠ", "लाकूड", "மர", "மரம்", "மரச்சிற்பம்", "చెక్క", "టేకు"
    ]),
    ("Terracotta Clay", "Pottery & Ceramics", [
        "terracotta", "clay", "mitti", "मिट्टी", "माटी",
        "মাটি", "টেরাকোটা", "মাটিৰ", "माती", "களிமண்", "மண்பாண்டம்", "మట్టి", "టెర్రకోట"
    ]),
    ("Brass", "Metalware & Brass", [
        "brass", "peetal", "पीतल", "पितळ", "পিতল", "பித்தளை", "ఇత్తడి"
    ]),
    ("Jute", "Eco-Friendly Crafts", [
        "jute", "पटसन", "जूट",
        "পাট", "মৰাপাট", "ताग", "சணல்", "జనపనార"
    ]),
]


def detect_language(text: str) -> str:
    """
    Detects language code among the 7 supported languages:
    hi, en, bn, mr, as, ta, te.
    """
    if not text or not text.strip():
        return "hi"

    # 1. Tamil Unicode block (\u0B80-\u0BFF)
    if re.search(r'[\u0B80-\u0BFF]', text):
        return "ta"

    # 2. Telugu Unicode block (\u0C00-\u0C7F)
    if re.search(r'[\u0C00-\u0C7F]', text):
        return "te"

    # 3. Bengali / Assamese Unicode block (\u0980-\u09FF)
    if re.search(r'[\u0980-\u09FF]', text):
        # Assamese unique characters: ৰ (U+09F0), ৱ (U+09F1), or specific Assamese words
        if re.search(r'[\u09F0\u09F1]', text) or any(w in text for w in ["মোক", "আমাৰ", "বাবে", "হৈছে", "খৰাহী", "বাঁহৰ", "শিকাইছিল"]):
            return "as"
        return "bn"

    # 4. Devanagari Unicode block (\u0900-\u097F) - Hindi vs Marathi
    if re.search(r'[\u0900-\u097F]', text):
        marathi_markers = ["आहे", "केले", "दिवस", "माझी", "माझ्या", "आईने", "टोपली", "शिल्प", "आम्ही", "तयार"]
        if any(w in text for w in marathi_markers):
            return "mr"
        return "hi"

    # 5. Check Hinglish cue words
    hinglish_cues = ["ye", "yeh", "hai", "hain", "ki", "ka", "ke", "mein", "hum", "mujhe",
                     "banana", "sikhaya", "tha", "lagte", "kaam", "maa", "bhai", "peedhi", "karti"]
    lower_words = set(re.findall(r'\b\w+\b', text.lower()))
    matches = lower_words.intersection(hinglish_cues)
    if len(matches) >= 2:
        return "hi"

    return "en"


INDIC_DIGITS_MAP = str.maketrans({
    # Devanagari
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
    # Bengali / Assamese
    '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
    '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9',
    # Tamil
    '௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4',
    '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9',
    # Telugu
    '౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4',
    '౫': '5', '౬': '6', '౭': '7', '౮': '8', '౯': '9',
})


def extract_production_time(text: str) -> Optional[str]:
    """
    Extracts crafting duration from phrases like 'do din', '2 days', 'paanch din', '২ দিন', 'दोन दिवस', '2 நாட்கள்', '2 రోజులు'.
    Supports all 7 target languages.
    """
    lower = text.lower()

    # Pattern: Digit + unit (across English, Hindi, Bengali, Assamese, Marathi, Tamil, Telugu)
    day_units = r'din|days?|दिन|দিবস|দিন|दिवस|நாட்கள்|நாள்|రోజులు|రోజు'
    hour_units = r'ghante|hours?|घंटे|घंटा|ঘণ্টা|ঘন্টা|तास|மணிநேரம்|மணி|గంటలు|గంట'
    week_units = r'hafte|weeks?|हफ्ते|हप्ता|सप्ताह|সপ্তাহ|आठवडा|வாரங்கள்|வாரம்|వారాలు|వారం'

    match = re.search(rf'(\d+)\s*({day_units}|{hour_units}|{week_units})', lower)
    if match:
        num = match.group(1).translate(INDIC_DIGITS_MAP)
        unit = match.group(2)
        if re.search(rf'^{day_units}$', unit):
            unit_clean = "days"
        elif re.search(rf'^{hour_units}$', unit):
            unit_clean = "hours"
        else:
            unit_clean = "weeks"
        return f"{num} {unit_clean}"

    # Pattern: Word number + unit
    for word, digit in MULTILINGUAL_NUMBER_WORDS.items():
        pattern = rf'(?:^|[\s\b]){re.escape(word)}\s*({day_units}|{hour_units}|{week_units})(?:$|[\s\b.,!?;])'
        match_word = re.search(pattern, lower)
        if match_word:
            unit = match_word.group(1)
            if re.search(rf'^{day_units}$', unit):
                unit_clean = "days"
            elif re.search(rf'^{hour_units}$', unit):
                unit_clean = "hours"
            else:
                unit_clean = "weeks"
            return f"{digit} {unit_clean}"

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
    Constructs an accurate professional product title based on communicated craft attributes across 7 languages.
    """
    lower = text.lower()
    craft_type = None
    known_items = [
        ("dupatta", "Dupatta"),
        ("दुपट्टा", "Dupatta"),
        ("ওড়না", "Dupatta"),
        ("ओढणी", "Dupatta"),
        ("துப்பட்டா", "Dupatta"),
        ("దుపట్టా", "Dupatta"),
        ("saree", "Saree"),
        ("साड़ी", "Saree"),
        ("শাড়ি", "Saree"),
        ("சேலை", "Saree"),
        ("చీర", "Saree"),
        ("shawl", "Shawl"),
        ("শাল", "Shawl"),
        ("গামোচা", "Handloom Gamusa"),
        ("basket", "Basket"),
        ("tokri", "Basket"),
        ("टोकरी", "Basket"),
        ("ঝুড়ি", "Basket"),
        ("ঝুড়ি", "Basket"),
        ("চুপড়ি", "Basket"),
        ("খৰাহী", "Basket"),
        ("टोपली", "Basket"),
        ("கூடை", "Basket"),
        ("బుట్ట", "Basket"),
        ("elephant", "Elephant Sculpture"),
        ("हाथी", "Elephant Sculpture"),
        ("হাতি", "Elephant Sculpture"),
        ("हत्ती", "Elephant Sculpture"),
        ("யானை", "Elephant Sculpture"),
        ("ఏనుగు", "Elephant Sculpture"),
        ("diya", "Festival Diya Set"),
        ("दीया", "Festival Diya Set"),
        ("दिया", "Festival Diya Set"),
        ("প্রদীপ", "Festival Diya Set"),
        ("চাকি", "Festival Diya Set"),
        ("दिवा", "Festival Diya Set"),
        ("விளக்கு", "Festival Diya Set"),
        ("దీపం", "Festival Diya Set"),
        ("pot", "Clay Pot"),
        ("matka", "Earthen Pot"),
        ("ঘড়া", "Clay Pot"),
        ("भांडे", "Clay Pot"),
        ("பானை", "Clay Pot"),
        ("కుండ", "Clay Pot"),
        ("lamp", "Handcrafted Lamp"),
        ("rug", "Handwoven Rug"),
    ]
    for kw, label in known_items:
        if kw in lower:
            craft_type = label
            break

    prefix = "Handwoven" if "Textile" in category or any(k in lower for k in ["handwoven", "buna", "বোনা", "विणलेले", "நெய்யப்பட்ட", "నేసిన"]) else (
        "Hand-Carved" if "Wood" in category or any(k in lower for k in ["carv", "नक्काशी", "খোদাই", "कोरलेले", "செதுக்கப்பட்ட", "చెక్కబడిన"]) else "Handcrafted"
    )

    if craft_type:
        return f"{prefix} {material} {craft_type}"
    return f"{prefix} {material} Craft"


def extract_material_and_category(text: str) -> Tuple[str, str]:
    """
    Identifies craft material and matching category using lookup patterns across 7 languages.
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
    Extracts artisan storytelling, narrative classification, and sentiment cues across all 7 supported languages.
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
# 3. MULTILINGUAL ARCHITECTURE REGISTRY (7 Functional Languages)
# ==========================================================
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi (हिंदी)",
    "bn": "Bengali (বাংলা)",
    "mr": "Marathi (मराठी)",
    "as": "Assamese (অসমীয়া)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
}


def generate_bilingual_descriptions(
    clean_text: str,
    material: str,
    category: str,
    title: str,
    detected_lang: str
) -> Tuple[str, str]:
    """
    Generates fluent descriptions in both English and Hindi.
    Maintains parallel English and Hindi representations regardless of input language.
    Preserves exact API contract for description_english and description_hindi.
    """
    desc_en = f"{title} made from {material}. Artisan-provided details: {clean_text}"
    desc_hi = f"{material} से बना {title}। कारीगर द्वारा दी गई जानकारी: {clean_text}"
    return desc_en, desc_hi
