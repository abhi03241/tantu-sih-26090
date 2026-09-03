"""
NLP & Voice Processing Module
Maintained by Team Member M (AI/NLP/Voice/Sentiment)
Integrated into TANTU Backend core workflow.
"""
from typing import Dict, Any, List


def process_voice_transcript(transcript: str, language: str = "hi", mock: bool = True) -> Dict[str, Any]:
    """
    Converts audio transcript/voice input from rural artisans into structured catalogue data.
    Analyzes sentiment, extracts key attributes, and generates English + Hindi translations.
    """
    if mock or not transcript:
        return {
            "title": "हस्तनिर्मित पारंपरिक क्राफ्ट (Handcrafted Traditional Craft)",
            "description_english": f"Beautiful handcrafted item described by artisan: '{transcript}'. Features traditional regional techniques, natural materials, and authentic craftsmanship.",
            "description_hindi": f"कारीगर द्वारा वर्णित सुंदर हस्तनिर्मित वस्तु: '{transcript}'। प्राकृतिक सामग्री और प्रामाणिक शिल्प कौशल का अनूठा मिश्रण।",
            "category": "Handicrafts & Decor",
            "material": "Natural Organic Fibers",
            "tags": ["handcrafted", "artisanal", "authentic", "regional-art", "eco-friendly"],
            "story": "Crafted with passion using heritage skills passed down across generations in rural artisan clusters.",
            "sentiment": "Positive, proud, culturally rich",
            "narrative_type": "Heritage Artisan Story",
            "detected_language": language
        }

    # Placeholder for Team Member M's real NLP pipeline (e.g. Whisper + IndicNLP / LLM)
    return {
        "title": f"Artisan Craft ({transcript[:20]}...)",
        "description_english": transcript,
        "description_hindi": "कारीगर उत्पाद विवरण",
        "category": "General Craft",
        "material": "Handmade Material",
        "tags": ["artisan", "handloom"],
        "story": "Unique artisan narrative",
        "sentiment": "Neutral",
        "narrative_type": "Standard Narrative",
        "detected_language": language
    }


def generate_catalogue_nlp(product_info: Dict[str, Any], mock: bool = True) -> Dict[str, Any]:
    """
    Generates rich marketing description, cultural story narrative, tags, and sentiment score.
    """
    title = product_info.get("title", "Artisan Craft")
    category = product_info.get("category", "Handicraft")
    material = product_info.get("material", "Natural Material")
    raw_desc = product_info.get("description_english", "")

    if mock:
        return {
            "description_english": f"Premium {title} crafted using high-grade {material}. Designed by skilled Indian artisans, combining durability with timeless aesthetic appeal. {raw_desc}",
            "description_hindi": f"उच्च गुणवत्ता वाले {material} से बना प्रीमियम {title}। कुशल भारतीय कारीगरों द्वारा डिज़ाइन किया गया, जो स्थायित्व को पारंपरिक सुंदरता के साथ जोड़ता है।",
            "category": category,
            "material": material,
            "tags": [category.lower().replace(" ", "-"), material.lower().replace(" ", "-"), "sih-artisan", "make-in-india", "authentic"],
            "story": f"This piece embodies centuries of craft legacy. Each unit of {title} represents hours of focused handiwork, supporting local artisan livelihoods.",
            "sentiment": "Very Positive (0.92)",
            "narrative_type": "Empowerment & Sustainability"
        }

    return {
        "description_english": f"{title} - {raw_desc}",
        "description_hindi": title,
        "category": category,
        "material": material,
        "tags": ["craft"],
        "story": "Handcrafted legacy piece",
        "sentiment": "Positive",
        "narrative_type": "Artisan Narrative"
    }
