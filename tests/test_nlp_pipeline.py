"""
Unit & Integration Tests for TANTU AI/NLP & Voice Pipeline (SIH PS 26090)
Maintained by Team Member M (AI/NLP/Voice/Sentiment)
"""
import sys
import os
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.nlp.schemas import ProductCatalogNLPOutput, VoiceTranscriptionResult
from ai.nlp.service import MockNLPService, RealNLPService, get_nlp_service
from ai.nlp.voice_and_story import (
    process_voice_transcript,
    process_voice_audio,
    generate_catalogue_nlp,
)


class TestNLPVoicePipeline(unittest.TestCase):
    def setUp(self):
        self.mock_service = MockNLPService()
        self.real_service = RealNLPService()

    # ==========================================================
    # 1. CORE DEMO CASES REQUIRED BY SIH
    # ==========================================================
    def test_demo_case_1_hindi_bamboo_basket(self):
        """
        Demo Case 1: Hindi Bamboo Basket
        Artisan: "Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha."
        """
        input_text = "Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha."
        res = self.mock_service.process_transcript(input_text, language="hi")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.title, "Bamboo Basket")
        self.assertEqual(res.material, "Bamboo")
        self.assertEqual(res.category, "Bamboo & Cane Craft")
        self.assertEqual(res.production_time, "2 days")
        self.assertEqual(res.sentiment, "positive")
        self.assertEqual(res.narrative_type, "family_tradition")
        self.assertIn("mother", res.story.lower())
        self.assertTrue(len(res.description_english) > 20)
        self.assertTrue(len(res.description_hindi) > 20)
        self.assertTrue(any("bamboo" in tag for tag in res.tags))
        self.assertTrue(any("basket" in tag for tag in res.tags))

    def test_demo_case_2_hindi_handwoven_textile(self):
        """
        Demo Case 2: Hindi Handwoven Textile
        Artisan: "Yeh haath se buna hua Chanderi silk dupatta hai. Isme paanch din lagte hain. Humari peedhiyan yeh kaam karti aa rahi hain."
        """
        input_text = "Yeh haath se buna hua Chanderi silk dupatta hai. Isme paanch din lagte hain. Humari peedhiyan yeh kaam karti aa rahi hain."
        res = self.mock_service.process_transcript(input_text, language="hi")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Chanderi Silk")
        self.assertEqual(res.category, "Textiles & Handloom")
        self.assertEqual(res.production_time, "5 days")
        self.assertEqual(res.sentiment, "craftsmanship pride")
        self.assertEqual(res.narrative_type, "cultural_heritage")
        self.assertIn("generation", res.story.lower())
        self.assertTrue(any("silk" in tag for tag in res.tags))
        self.assertTrue(any("chanderi" in tag for tag in res.tags))

    def test_demo_case_3_english_wooden_craft(self):
        """
        Demo Case 3: English Wooden Craft
        Artisan: "This is a hand-carved teak wood elephant sculpture. It takes around four days to carve and polish. I learned wood carving from my grandfather with great pride."
        """
        input_text = "This is a hand-carved teak wood elephant sculpture. It takes around four days to carve and polish. I learned wood carving from my grandfather with great pride."
        res = self.mock_service.process_transcript(input_text, language="en")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Teak Wood")
        self.assertEqual(res.category, "Woodcraft")
        self.assertEqual(res.production_time, "4 days")
        self.assertEqual(res.sentiment, "positive")
        self.assertEqual(res.narrative_type, "craftsmanship_pride")
        self.assertIn("grandfather", res.story.lower())
        self.assertEqual(res.detected_language, "en")
        self.assertTrue(any("woodcraft" in tag for tag in res.tags))

    # ==========================================================
    # 2. OUTPUT CONTRACT & SCHEMA INTEGRITY
    # ==========================================================
    def test_output_schema_contract(self):
        """
        Verifies that extracted data contains all required keys of the shared Product schema.
        """
        res_dict = process_voice_transcript("Ye bamboo ki tokri hai.", mock=True)

        expected_fields = [
            "title",
            "description_english",
            "description_hindi",
            "category",
            "material",
            "dimensions",
            "production_time",
            "tags",
            "story",
            "sentiment",
            "narrative_type",
        ]
        for field in expected_fields:
            self.assertIn(field, res_dict, f"Missing required contract field: {field}")

        self.assertIsInstance(res_dict["tags"], list)
        self.assertIsInstance(res_dict["title"], str)
        self.assertIsInstance(res_dict["description_english"], str)
        self.assertIsInstance(res_dict["description_hindi"], str)

    # ==========================================================
    # 3. SENTIMENT & HERITAGE NARRATIVE CLASSIFICATION
    # ==========================================================
    def test_sentiment_and_heritage_classification(self):
        """
        Checks classification into allowed, objective categories:
        positive, neutral, heritage, family tradition, craftsmanship pride, cultural significance
        """
        # Family tradition cue
        res_fam = self.mock_service.process_transcript("Mere pitaji ne mujhe lakdi par naqashi ka kaam sikhaya tha.")
        self.assertEqual(res_fam.narrative_type, "family_tradition")
        self.assertEqual(res_fam.sentiment, "positive")

        # Heritage / Generations cue
        res_her = self.mock_service.process_transcript("Hamare gaon mein pichli kayi peedhiyon se peetal ke bartan banaye jaate hain.")
        self.assertEqual(res_her.narrative_type, "cultural_heritage")
        self.assertEqual(res_her.sentiment, "heritage")

        # Pride cue
        res_pride = self.mock_service.process_transcript("I make these silk sarees with immense pride in our village craft.")
        self.assertEqual(res_pride.narrative_type, "craftsmanship_pride")
        self.assertEqual(res_pride.sentiment, "craftsmanship pride")

    # ==========================================================
    # 4. ERROR HANDLING & RESILIENCE (NO CRASHES)
    # ==========================================================
    def test_empty_voice_transcript(self):
        """Empty voice input should return a safe structured fallback, never crash."""
        res_empty = self.mock_service.process_transcript("")
        self.assertIsInstance(res_empty, ProductCatalogNLPOutput)
        self.assertIsNotNone(res_empty.title)
        self.assertEqual(res_empty.sentiment, "neutral")

        res_spaces = self.mock_service.process_transcript("    ")
        self.assertIsInstance(res_spaces, ProductCatalogNLPOutput)
        self.assertEqual(res_spaces.sentiment, "neutral")

    def test_unsupported_language_graceful_handling(self):
        """Regional or mixed language input without crash."""
        res = self.mock_service.process_transcript("Sundar handmade matka clay pot 1 day", language="bengali")
        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Terracotta Clay")

    def test_real_nlp_service_fallback(self):
        """
        RealNLPService must automatically fall back to MockNLPService
        when API keys are missing or invalid, ensuring 100% demo uptime.
        """
        # Test without API keys
        res = self.real_service.process_transcript("Ye bamboo ki tokri hai.")
        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Bamboo")

    # ==========================================================
    # 5. AUDIO TRANSCRIPTION & PIPELINE ENTRYPOINTS
    # ==========================================================
    def test_audio_transcription(self):
        """Simulates audio speech-to-text processing."""
        sample_audio = b"\x00\x01\x02\x03\x04\x05"
        trans_res = self.mock_service.transcribe_audio(sample_audio, language="hi")
        self.assertIsInstance(trans_res, VoiceTranscriptionResult)
        self.assertTrue(len(trans_res.transcript) > 0)
        self.assertGreater(trans_res.confidence, 0.9)

    def test_process_voice_audio_wrapper(self):
        """Tests high-level process_voice_audio function."""
        sample_audio = b"\x00\x01\x02\x03"
        product_dict = process_voice_audio(sample_audio, language="hi", mock=True)
        self.assertIn("title", product_dict)
        self.assertIn("description_english", product_dict)
        self.assertIn("description_hindi", product_dict)

    def test_generate_catalogue_nlp(self):
        """Tests rich marketing description and storytelling tags generator."""
        product_info = {
            "title": "Chanderi Silk Saree",
            "category": "Textiles & Handloom",
            "material": "Silk",
            "description_english": "Fine handwoven saree with gold motifs."
        }
        res = generate_catalogue_nlp(product_info, mock=True)
        self.assertIn("description_english", res)
        self.assertIn("description_hindi", res)
        self.assertIn("story", res)
        self.assertIn("tags", res)
        self.assertIsInstance(res["tags"], list)


if __name__ == "__main__":
    unittest.main()
