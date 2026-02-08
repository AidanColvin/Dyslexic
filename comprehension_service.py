import requests
from typing import Dict, Optional, List

# We reuse the Dictionary API for real examples
API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"

def get_comprehension_aid(word: str) -> Dict[str, str]:
    """
    Fetches an example sentence and generates a read-aloud link.
    Helps user distinguish 'their' vs 'there' via context.
    """
    example_sentence = "No example available."
    definition = ""
    
    try:
        response = requests.get(API_URL.format(word), timeout=2)
        if response.status_code == 200:
            data = response.json()[0]
            # Try to find an example in meanings
            for meaning in data.get("meanings", []):
                for dfn in meaning.get("definitions", []):
                    if "example" in dfn:
                        example_sentence = dfn["example"]
                        definition = dfn.get("definition", "")
                        break
                if example_sentence != "No example available.":
                    break
    except Exception:
        pass # Fallback to defaults if API fails

    return {
        "word": word,
        "example": example_sentence,
        "definition": definition,
        # Frontend will use this endpoint to play audio on hover
        "audio_endpoint": f"/voice/speak?text={word}. For example: {example_sentence}"
    }

def generate_homophone_warning(word: str) -> Optional[str]:
    """
    Returns a warning if the word is a common homophone.
    """
    homophones = {
        "their": "Check: 'their' means possession (their house).",
        "there": "Check: 'there' means location (over there).",
        "they're": "Check: 'they're' means 'they are'.",
        "to": "Check: 'to' indicates direction.",
        "too": "Check: 'too' means also or excessive.",
        "two": "Check: 'two' is the number 2."
    }
    return homophones.get(word.lower())
