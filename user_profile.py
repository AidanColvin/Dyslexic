from pathlib import Path
from typing import Dict, Any, List, Tuple
import json
import time
import difflib
import logging

# Setup Logging
logger = logging.getLogger(__name__)
PROFILE_FILE = Path("user_profile_data.json")

# Default weights for new users
DEFAULT_WEIGHTS = {
    "visual_substitution": 1.0,  # b vs d, p vs q
    "phonetic_swap": 1.0,        # f vs v
    "vowel_error": 1.0,          # e vs a
    "transposition": 1.0         # teh vs the
}

class UserProfileManager:
    """
    Manages user-specific data: error patterns, custom lexicon, and preferences.
    Persists data to JSON (in production, use SQLite/PostgreSQL).
    """
    
    def __init__(self):
        self.data = self._load_profile()

    def _load_profile(self) -> Dict[str, Any]:
        """Loads user profile from disk or creates default."""
        if not PROFILE_FILE.exists():
            return {
                "error_counts": {},       # Tracks how often specific errors occur e.g. "b->d": 5
                "adaptive_weights": DEFAULT_WEIGHTS.copy(),
                "lexicon": [],            # Words user clicked "Ignore" on
                "accepted_words": {},     # Frequency map of accepted words
                "ui_preferences": {
                    "font": "Arial",
                    "contrast": "normal"
                }
            }
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load profile: {e}")
            return {}

    def _save_profile(self) -> None:
        """Persists current state to disk."""
        try:
            with open(PROFILE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")

    def learn_from_correction(self, misspelling: str, chosen_word: str) -> None:
        """
        The Core Learning Loop:
        Analyzes the diff between what was typed and what was chosen.
        Updates weights to 'expect' this type of error more in the future.
        """
        # 1. Update Vocabulary Frequency
        self.data["accepted_words"][chosen_word] = self.data["accepted_words"].get(chosen_word, 0) + 1
        
        # 2. Analyze the specific error pattern
        matcher = difflib.SequenceMatcher(None, misspelling, chosen_word)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                # Check for single char visual swaps (e.g. b -> d)
                snippet_miss = misspelling[i1:i2]
                snippet_corr = chosen_word[j1:j2]
                
                if len(snippet_miss) == 1 and len(snippet_corr) == 1:
                    error_key = f"{snippet_miss}->{snippet_corr}"
                    self._increment_error_count(error_key)
                    
                    # If this is a known dyslexic swap, boost the category weight
                    if snippet_miss in ['b', 'd', 'p', 'q'] and snippet_corr in ['b', 'd', 'p', 'q']:
                        self.data["adaptive_weights"]["visual_substitution"] += 0.1

        self._save_profile()

    def _increment_error_count(self, key: str) -> None:
        """Helper to track specific error frequencies."""
        self.data["error_counts"][key] = self.data["error_counts"].get(key, 0) + 1

    def add_to_lexicon(self, word: str) -> None:
        """Adds a word to the 'Ignore' list (User's personal dictionary)."""
        if word not in self.data["lexicon"]:
            self.data["lexicon"].append(word)
            self._save_profile()

    def get_personalization_factor(self, candidate: str, misspelling: str) -> float:
        """
        Returns a multiplier score (1.0 - 2.0) based on how well this candidate 
        matches the user's historical error profile.
        """
        score = 1.0
        weights = self.data["adaptive_weights"]
        
        # If user frequently uses this word, boost it
        if candidate in self.data["accepted_words"]:
            score += 0.2
            
        # Check if this correction fixes a 'visual substitution' and user makes those often
        # (Simplified logic for prototype: if candidate fixes b/d and weight is high)
        if weights["visual_substitution"] > 1.5:
             if ('b' in misspelling and 'd' in candidate) or ('d' in misspelling and 'b' in candidate):
                 score += 0.3

        return score

    def get_ui_recommendations(self) -> Dict[str, str]:
        """
        Analyzes error patterns to suggest UI tweaks.
        If many visual errors (b/d), suggest OpenDyslexic font.
        """
        # Calculate total visual errors
        visual_errors = 0
        for key, count in self.data["error_counts"].items():
            if any(char in key for char in ['b', 'd', 'p', 'q']):
                visual_errors += count
                
        rec = self.data["ui_preferences"].copy()
        if visual_errors > 5:
            rec["font"] = "OpenDyslexic"
            rec["spacing"] = "1.5"
            
        return rec
