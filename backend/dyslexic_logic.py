import re

class DyslexicAssistant:
    def __init__(self):
        self.correction_map = {
            "becuase": "because",
            "dont": "don't",
            "didnt": "didn't",
            "cant": "can't",
            "wont": "won't",
            "isnt": "isn't",
            "arent": "aren't",
            "couldnt": "couldn't",
            "shouldnt": "shouldn't",
            "frend": "friend",
            "teh": "the"
        }

    def correct_text(self, text):
        words = re.findall(r"[\w']+|[.,!?;]", text)
        corrected_words = []
        for word in words:
            lower_word = word.lower()
            if lower_word in self.correction_map:
                replacement = self.correction_map[lower_word]
                if word[0].isupper():
                    replacement = replacement.capitalize()
                corrected_words.append(replacement)
            else:
                corrected_words.append(word)
        result = " ".join(corrected_words)
        for char in [".", ",", "!", "?", ";"]:
            result = result.replace(f" {char}", char)
        return result
