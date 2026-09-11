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
    # 1. CORE MULTILINGUAL DEMO CASES REQUIRED BY SIH
    # ==========================================================
    def test_hindi_input(self):
        """
        Test Hindi voice transcript input:
        "Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha."
        """
        input_text = "Ye bamboo ki tokri hai. Isko banane mein mujhe do din lagte hain. Meri maa ne mujhe ye banana sikhaya tha."
        res = self.mock_service.process_transcript(input_text, language="hi")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.title, "Bamboo Basket")
        self.assertEqual(res.material, "Bamboo")
        self.assertEqual(res.category, "Bamboo & Cane Craft")
        self.assertEqual(res.production_time, "2 days")
        self.assertEqual(res.sentiment, "Nostalgia")
        self.assertEqual(res.narrative_type, "Family craft")
        self.assertIn("mother", res.story.lower())
        self.assertTrue(len(res.description_english) > 20)
        self.assertTrue(len(res.description_hindi) > 20)
        self.assertTrue(any("bamboo" in tag for tag in res.tags))
        self.assertTrue(any("basket" in tag for tag in res.tags))

    def test_hindi_handwoven_textile_input(self):
        """
        Test Hindi handwoven textile transcript:
        "Yeh haath se buna hua Chanderi silk dupatta hai. Isme paanch din lagte hain. Humari peedhiyan yeh kaam karti aa rahi hain."
        """
        input_text = "Yeh haath se buna hua Chanderi silk dupatta hai. Isme paanch din lagte hain. Humari peedhiyan yeh kaam karti aa rahi hain."
        res = self.mock_service.process_transcript(input_text, language="hi")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Chanderi Silk")
        self.assertEqual(res.category, "Textiles & Handloom")
        self.assertEqual(res.production_time, "5 days")
        self.assertEqual(res.sentiment, "Nostalgia")
        self.assertEqual(res.narrative_type, "Traditional heritage")
        self.assertIn("generation", res.story.lower())
        self.assertTrue(any("silk" in tag for tag in res.tags))
        self.assertTrue(any("chanderi" in tag for tag in res.tags))

    def test_english_input(self):
        """
        Test English voice input:
        "This is a hand-carved teak wood elephant sculpture. It takes around four days to carve and polish. I learned wood carving from my grandfather with great pride."
        """
        input_text = "This is a hand-carved teak wood elephant sculpture. It takes around four days to carve and polish. I learned wood carving from my grandfather with great pride."
        res = self.mock_service.process_transcript(input_text, language="en")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Teak Wood")
        self.assertEqual(res.category, "Woodcraft")
        self.assertEqual(res.production_time, "4 days")
        self.assertEqual(res.sentiment, "Pride")
        self.assertEqual(res.narrative_type, "Family craft")
        self.assertIn("grandfather", res.story.lower())
        self.assertEqual(res.detected_language, "en")
        self.assertTrue(any("woodcraft" in tag for tag in res.tags))

    def test_cotton_dupatta_women_group_example(self):
        """
        Test the core SIH prompt example:
        "This is a handwoven cotton dupatta made by our women’s group. It takes three days to make and uses traditional weaving patterns."
        """
        input_text = "This is a handwoven cotton dupatta made by our women’s group. It takes three days to make and uses traditional weaving patterns."
        res = self.mock_service.process_transcript(input_text, language="en")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.title, "Handwoven Cotton Dupatta")
        self.assertIn("Cotton", res.material)
        self.assertEqual(res.production_time, "3 days")
        self.assertIsNone(res.dimensions, "Must not hallucinate dimensions when unstated")
        self.assertEqual(res.narrative_type, "Community-made")
        self.assertEqual(res.sentiment, "Neutral")
        self.assertIn("women", res.story.lower())
        self.assertTrue(any("cotton" in tag for tag in res.tags))
        self.assertTrue(any("dupatta" in tag for tag in res.tags))

    def test_dimensions_extraction_and_no_hallucination(self):
        """
        When dimensions are communicated (e.g. 120cm x 80cm), they are extracted.
        When unstated, dimensions must remain None.
        """
        with_dims = self.mock_service.process_transcript("Handcrafted wood stool 40cm x 40cm x 45cm made in 2 days.")
        self.assertEqual(with_dims.dimensions, "40cm x 40cm x 45cm")

        without_dims = self.mock_service.process_transcript("Simple clay diya crafted in 1 day.")
        self.assertIsNone(without_dims.dimensions)

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
        positive, neutral, heritage, family_tradition, craftsmanship_pride, cultural_significance
        """
        # Family craft / tradition cue
        res_fam = self.mock_service.process_transcript("Mere pitaji ne mujhe lakdi par naqashi ka kaam sikhaya tha.")
        self.assertIn(res_fam.narrative_type, ["Family craft", "family_tradition"])
        self.assertIn(res_fam.sentiment, ["Nostalgia", "Pride", "positive"])

        # Traditional heritage / Generations cue
        res_her = self.mock_service.process_transcript("Hamare gaon mein pichli kayi peedhiyon se peetal ke bartan banaye jaate hain.")
        self.assertIn(res_her.narrative_type, ["Traditional heritage", "cultural_heritage"])
        self.assertEqual(res_her.sentiment, "Nostalgia")

        # Craftsmanship pride / Handmade journey cue
        res_pride = self.mock_service.process_transcript("I make these fine products with immense pride in our artisan techniques.")
        self.assertIn(res_pride.narrative_type, ["Handmade journey", "craftsmanship_pride"])
        self.assertIn(res_pride.sentiment, ["Pride", "craftsmanship_pride"])

    # ==========================================================
    # 4. ERROR HANDLING & RESILIENCE (NO CRASHES)
    # ==========================================================
    def test_empty_voice(self):
        """Empty voice input should return a safe structured fallback, never crash."""
        res_empty = self.mock_service.process_transcript("")
        self.assertIsInstance(res_empty, ProductCatalogNLPOutput)
        self.assertIsNotNone(res_empty.title)
        self.assertEqual(res_empty.sentiment, "Neutral")
        self.assertIsNone(res_empty.production_time)
        self.assertIsNone(res_empty.story)

        res_spaces = self.mock_service.process_transcript("    ")
        self.assertIsInstance(res_spaces, ProductCatalogNLPOutput)
        self.assertEqual(res_spaces.sentiment, "Neutral")

    def test_unsupported_language(self):
        """Regional, mixed, or unsupported language code input without crash."""
        res = self.mock_service.process_transcript("Sundar handmade matka clay pot 1 day", language="bengali")
        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Terracotta Clay")

    def test_missing_fields_graceful_defaults(self):
        """
        When artisan speech does not mention dimensions, production time, or story,
        the system provides sensible non-crashing defaults.
        """
        res = self.mock_service.process_transcript("Simple handmade craft piece")
        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertIsNotNone(res.title)
        self.assertIsNotNone(res.category)
        self.assertIsNotNone(res.material)
        self.assertIsNone(res.dimensions)  # Expected null per contract (no hallucination)
        self.assertIsNone(res.production_time)  # Expected null when uncommunicated (no hallucination)
        self.assertIsInstance(res.tags, list)
        self.assertGreaterEqual(len(res.tags), 1)

    def test_malformed_response_handling(self):
        """
        Verifies that partial or malformed dict inputs are safely coerced
        by ProductCatalogNLPOutput without failing schema validation.
        """
        partial_data = {
            "title": "Terracotta Pot",
            "description_english": "Natural clay pot",
            "description_hindi": "मिट्टी का बर्तन",
            "category": "Pottery & Ceramics",
            "material": "Clay",
            # dimensions omitted
            # production_time omitted
            # tags omitted
        }
        output = ProductCatalogNLPOutput(**partial_data)
        self.assertEqual(output.title, "Terracotta Pot")
        self.assertEqual(output.tags, [])  # default factory works
        self.assertIsNone(output.dimensions)
        self.assertIsNone(output.production_time)

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

    def test_catalogue_generation_does_not_invent_story(self):
        """Catalogue generation keeps story/narrative null when notes contain no cues."""
        res = generate_catalogue_nlp({
            "title": "Bamboo Basket",
            "category": "Bamboo & Cane Craft",
            "material": "Bamboo",
            "description_english": "A bamboo basket for storage."
        }, mock=True)
        self.assertIsNone(res["story"])
        self.assertEqual(res["sentiment"], "Neutral")
        self.assertIsNone(res["narrative_type"])

    # ==========================================================
    # 6. VERIFIED 7-LANGUAGE MULTILINGUAL NLP TESTS
    # ==========================================================
    def test_bengali_input(self):
        """Tests Bengali voice/text transcript input."""
        transcript = "এটি একটি বাঁশের তৈরি ঝুড়ি। এটি তৈরি করতে ২ দিন সময় লাগে। আমার মা আমাকে এটি তৈরি করতে শিখিয়েছিলেন।"
        res = self.mock_service.process_transcript(transcript, language="bn")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Bamboo")
        self.assertEqual(res.category, "Bamboo & Cane Craft")
        self.assertEqual(res.production_time, "2 days")
        self.assertEqual(res.sentiment, "Nostalgia")
        self.assertEqual(res.narrative_type, "Family craft")
        self.assertEqual(res.detected_language, "bn")
        self.assertTrue(len(res.description_english) > 20)
        self.assertTrue(len(res.description_hindi) > 20)

    def test_marathi_input(self):
        """Tests Marathi voice/text transcript input."""
        transcript = "ही बांबूची टोपली आहे. हे बनवण्यासाठी दोन दिवस लागतात. माझ्या आईने मला हे शिकवले आहे."
        res = self.mock_service.process_transcript(transcript, language="mr")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Bamboo")
        self.assertEqual(res.category, "Bamboo & Cane Craft")
        self.assertEqual(res.production_time, "2 days")
        self.assertEqual(res.sentiment, "Nostalgia")
        self.assertEqual(res.narrative_type, "Family craft")
        self.assertEqual(res.detected_language, "mr")

    def test_assamese_input(self):
        """Tests Assamese voice/text transcript input."""
        transcript = "এইটো এটা বাঁহৰ খৰাহী। এইটো বনাবলৈ ২ দিন লাগে। মোৰ মায়ে মোক এইটো বনাবলৈ শিকাইছিল।"
        res = self.mock_service.process_transcript(transcript, language="as")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Bamboo")
        self.assertEqual(res.category, "Bamboo & Cane Craft")
        self.assertEqual(res.production_time, "2 days")
        self.assertEqual(res.sentiment, "Nostalgia")
        self.assertEqual(res.narrative_type, "Family craft")
        self.assertEqual(res.detected_language, "as")

    def test_tamil_input(self):
        """Tests Tamil voice/text transcript input."""
        transcript = "இது ஒரு அழகான தேக்கு மர யானை சிற்பம். இதை செய்ய 4 நாட்கள் ஆகும். என் தாத்தா எனக்கு பெருமையுடன் கற்றுக் கொடுத்தார்."
        res = self.mock_service.process_transcript(transcript, language="ta")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Teak Wood")
        self.assertEqual(res.category, "Woodcraft")
        self.assertEqual(res.production_time, "4 days")
        self.assertEqual(res.sentiment, "Pride")
        self.assertEqual(res.narrative_type, "Family craft")
        self.assertEqual(res.detected_language, "ta")

    def test_telugu_input(self):
        """Tests Telugu voice/text transcript input."""
        transcript = "ఇది చేనేత పట్టు చీర. ఇది తయారు చేయడానికి 5 రోజులు పడుతుంది. మా తరాలుగా ఈ సాంప్రదాయం కొనసాగుతోంది."
        res = self.mock_service.process_transcript(transcript, language="te")

        self.assertIsInstance(res, ProductCatalogNLPOutput)
        self.assertEqual(res.material, "Chanderi Silk")
        self.assertEqual(res.category, "Textiles & Handloom")
        self.assertEqual(res.production_time, "5 days")
        self.assertEqual(res.sentiment, "Nostalgia")
        self.assertEqual(res.narrative_type, "Traditional heritage")
        self.assertEqual(res.detected_language, "te")

    def test_multilingual_production_time_parsing(self):
        """Verifies duration parsing across all 7 supported language conventions."""
        from ai.nlp.demo_data import extract_production_time
        self.assertEqual(extract_production_time("takes 3 days to weave"), "3 days")
        self.assertEqual(extract_production_time("banane mein 3 din lagte hain"), "3 days")
        self.assertEqual(extract_production_time("৩ দিন সময় লাগে"), "3 days")
        self.assertEqual(extract_production_time("दोन दिवस लागतात"), "2 days")
        self.assertEqual(extract_production_time("2 நாட்கள் ஆகும்"), "2 days")
        self.assertEqual(extract_production_time("5 రోజులు పడుతుంది"), "5 days")
        self.assertEqual(extract_production_time("3 ghante"), "3 hours")
        self.assertEqual(extract_production_time("2 hafte"), "2 weeks")

    def test_language_detection_all_7_languages(self):
        """Verifies language identification across the 7 supported languages."""
        from ai.nlp.demo_data import detect_language
        self.assertEqual(detect_language("Handcrafted bamboo craft from rural artisans"), "en")
        self.assertEqual(detect_language("यह हाथ से बनी बांस की टोकरी है"), "hi")
        self.assertEqual(detect_language("এটি একটি বাঁশের তৈরি সুন্দর ঝুড়ি"), "bn")
        self.assertEqual(detect_language("ही सुंदर बांबूची टोपली आहे"), "mr")
        self.assertEqual(detect_language("এইটো আমাৰ বাবে তৈয়াৰ কৰা বাঁহৰ খৰাহী"), "as")
        self.assertEqual(detect_language("இது ஒரு கைவினைப் பொருள்"), "ta")
        self.assertEqual(detect_language("ఇది అందమైన చేతివృత్తి కళాఖండం"), "te")


if __name__ == "__main__":
    unittest.main()

