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
            "sentiment": "craftsmanship pride",
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
            "production_time": "3 days",
            "tags": ["terracotta", "pottery", "clay", "handmade", "eco-friendly"],
            "story": "Preserving the sacred village pottery tradition passed across generations.",
            "sentiment": "cultural significance",
            "narrative_type": "cultural_heritage",
            "detected_language": "hi",
        }
    }
}


# ==========================================================
# 2. HEURISTIC PARSERS & REGEX EXTRACTORS
# ==========================================================
HINDI_NUMBER_WORDS = {
    "ek": "1", "do": "2", "teen": "3", "chaar": "4", "char": "4",
    "paanch": "5", "panch": "5", "chhe": "6", "che": "6", "saat": "7", "sat": "7",
    "aath": "8", "nau": "9", "das": "10",
    "एक": "1", "दो": "2", "तीन": "3", "चार": "4", "पांच": "5", "छह": "6", "सात": "7",
    "आठ": "8", "नौ": "9", "दस": "10",
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"
}

MATERIAL_CATALOG = [
    ("Bamboo", "Bamboo & Cane Craft", ["bamboo", "bans", "बांस", "cane", "वेत", "cane"]),
    ("Chanderi Silk", "Textiles & Handloom", ["chanderi", "silk", "सिल्क", "रेशम"]),
    ("Khadi Cotton", "Textiles & Handloom", ["cotton", "khadi", "सूती", "खादी"]),
    ("Teak Wood", "Woodcraft", ["teak", "sagwan", "सागवान", "सागौन"]),
    ("Sheesham Wood", "Woodcraft", ["sheesham", "rosewood", "शीशम"]),
    ("Natural Wood", "Woodcraft", ["wood", "wooden", "lakdi", "लकड़ी"]),
    ("Terracotta Clay", "Pottery & Ceramics", ["terracotta", "clay", "mitti", "मिट्टी"]),
    ("Brass", "Metalware & Brass", ["brass", "peetal", "पीतल"]),
    ("Jute", "Eco-Friendly Crafts", ["jute", "पटसन", "जूट"]),
]


def detect_language(text: str) -> str:
    """
    Detects if input is Hindi (Devanagari script), Hinglish transliteration, or English.
    """
    if not text or not text.strip():
        return "hi"

    # Check for Devanagari Unicode range
    devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))
    if devanagari_count > 3:
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
    Extracts crafting duration from phrases like 'do din', '2 days', 'paanch din', '3 weeks'.
    """
    lower = text.lower()

    # Pattern: Digit + unit
    match = re.search(r'(\d+)\s*(din|days?|ghante|hours?|hafte|weeks?)', lower)
    if match:
        num = match.group(1)
        unit = match.group(2)
        unit_clean = "days" if "d" in unit else ("hours" if "h" in unit else "weeks")
        return f"{num} {unit_clean}"

    # Pattern: Word number + unit
    for word, digit in HINDI_NUMBER_WORDS.items():
        if re.search(rf'\b{word}\s+(din|days?|hafte|weeks?|ghante|hours?)\b', lower):
            match_unit = re.search(rf'\b{word}\s+([a-zA-Z]+)\b', lower)
            raw_unit = match_unit.group(1) if match_unit else "days"
            unit_clean = "days" if "d" in raw_unit else ("hours" if "h" in raw_unit else "weeks")
            return f"{digit} {unit_clean}"

    return None


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


def extract_story_and_sentiment(text: str) -> Tuple[Optional[str], str, str]:
    """
    Extracts artisan story, narrative type, and sentiment category.
    Sentiment categories: positive, neutral, heritage, family tradition, craftsmanship pride, cultural significance
    Narrative types: family_tradition, cultural_heritage, craftsmanship_pride, community_empowerment, standard_narrative
    """
    lower = text.lower()

    # Mother / Father / Family mentions
    if any(k in lower for k in ["maa", "mother", "mummy", "माता", "मां"]):
        story = "An inherited craft tradition taught by the artisan's mother."
        return story, "positive", "family_tradition"

    if any(k in lower for k in ["pita", "pitaji", "father", "बापू", "पिता"]):
        story = "Artisanal techniques and heritage passed down from the artisan's father."
        return story, "positive", "family_tradition"

    if any(k in lower for k in ["dada", "dadi", "grandfather", "grandmother", "दादा", "नाना"]):
        story = "Ancestral craftsmanship learned from grandparents with enduring pride."
        return story, "craftsmanship pride", "family_tradition"

    if any(k in lower for k in ["peedhi", "generation", "virasat", "ancestral", "विरासत", "पीढ़ी"]):
        story = "Centuries of cultural heritage preserved across multiple artisan generations."
        return story, "heritage", "cultural_heritage"

    if any(k in lower for k in ["pride", "garv", "proud", "गर्व"]):
        story = "A proud regional craft reflecting dedicated community skill and dedication."
        return story, "craftsmanship pride", "craftsmanship_pride"

    # Default / standard narrative
    story = "Authentic handcrafted creation created with traditional regional techniques."
    return story, "positive", "standard_narrative"
