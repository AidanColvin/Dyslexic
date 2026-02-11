import unittest
from dyslexic.dyslexic_logic import DyslexicAssistant

class TestDyslexicLogic(unittest.TestCase):
    def setUp(self):
        self.assistant = DyslexicAssistant()

    def test_corrections(self):
        # Testing spelling 'because'
        self.assertEqual(self.assistant.correct_text("becuase"), "because")
        
        # Testing abbreviations/grammar
        self.assertEqual(self.assistant.correct_text("dont"), "don't")
        self.assertEqual(self.assistant.correct_text("didnt"), "didn't")
        
        # Testing full sentence
        text = "My frend dont like it becuase it didnt work."
        expected = "My friend don't like it because it didn't work."
        self.assertEqual(self.assistant.correct_text(text), expected)

if __name__ == "__main__":
    unittest.main()
