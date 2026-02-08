from textblob import TextBlob
from typing import Dict, List, Any

def get_word_details(word: str) -> Dict[str, Any]:
    """
    given a single word
    return dictionary with definition and parts of speech
    uses textblob as a lightweight offline proxy
    """
    blob = TextBlob(word)
    # textblob definitions can be list of synsets
    # for a robust tool, this often connects to wordnet
    # here we use a simple structure for the api response
    
    return {
        "word": word,
        "definitions": blob.words[0].definitions if blob.words else [],
        "part_of_speech": blob.tags[0][1] if blob.tags else "UNKNOWN"
    }

def summarize_text(text: str) -> List[str]:
    """
    given a long text string
    extract key noun phrases to act as a summary
    return list of key points
    """
    blob = TextBlob(text)
    # in a full production app, use transformers (bart/t5)
    # here we use noun phrase extraction for speed/offline capability
    return list(blob.noun_phrases)

def correct_grammar(text: str) -> str:
    """
    given a text string
    return the string with semantic spelling correction applied
    """
    blob = TextBlob(text)
    return str(blob.correct())
