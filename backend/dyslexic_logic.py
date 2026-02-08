from metaphone import doublemetaphone
from Levenshtein import distance as lev_distance
from typing import List, Dict, Set, Tuple, Optional
import re

# --- CONFIGURATION: DYSLEXIC ERROR PATTERNS ---

# 1. Visual Confusions (Mirroring/Rotation)
# Dyslexic users often confuse letters with similar shapes.
VISUAL_CONFUSIONS = {
    'b': ['d', 'p', 'q', 'h'],
    'd': ['b', 'p', 'q', 'g'],
    'p': ['q', 'b', 'd'],
    'q': ['p', 'b', 'd'],
    'm': ['w', 'n'],
    'w': ['m', 'v'],
    'n': ['u', 'h', 'r'],
    'u': ['n', 'v'],
    'f': ['t', 'j'],
    't': ['f', 'j'],
    'l': ['i', '1'],
    'i': ['l', 'j']
}

# 2. Phonetic Confusions (Sound-alikes)
# Mapping sounds that are often swapped in writing.
PHONETIC_CONFUSIONS = {
    'f': ['v', 'ph'],
    'v': ['f'],
    's': ['z', 'c'],
    'z': ['s'],
    'k': ['c', 'q'],
    'c': ['k', 's'],
    'j': ['g', 'dg'],
    'g': ['j']
}

# 3. Common Vowel Swaps (Phonological Ambiguity)
VOWELS = set('aeiouy')

def get_phonetic_code(word: str) -> str:
    """
    returns the primary double metaphone code for a word
    used to group words by how they sound, ignoring spelling
    """
    if not word: 
        return ""
    return doublemetaphone(word)[0]

def calculate_visual_distance(s1: str, s2: str) -> float:
    """
    calculates edit distance with discounts for visual similarities
    swapping 'b' for 'd' costs 0.5 instead of 1.0
    """
    # optimization: if identical, distance is 0
    if s1 == s2:
        return 0.0
        
    # use dynamic programming for weighted edit distance
    n, m = len(s1), len(s2)
    # create matrix
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1): dp[i][0] = float(i)
    for j in range(m + 1): dp[0][j] = float(j)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            char1 = s1[i-1]
            char2 = s2[j-1]
            
            # Base cost: 0 if match, 1 if substitution
            cost = 0.0 if char1 == char2 else 1.0
            
            # Apply Dyslexia Discounts
            if cost == 1.0:
                # check visual confusion (b vs d)
                if char2 in VISUAL_CONFUSIONS.get(char1, []):
                    cost = 0.4  # High likelihood error
                # check phonetic confusion (f vs v)
                elif char2 in PHONETIC_CONFUSIONS.get(char1, []):
                    cost = 0.6
                # check vowel swap (e vs a)
                elif char1 in VOWELS and char2 in VOWELS:
                    cost = 0.7

            dp[i][j] = min(
                dp[i-1][j] + 1.0,    # Deletion
                dp[i][j-1] + 1.0,    # Insertion
                dp[i-1][j-1] + cost  # Substitution
            )
            
            # Check for Transposition (swapped adjacent letters: 'teh' -> 'the')
            if i > 1 and j > 1:
                if s1[i-1] == s2[j-2] and s1[i-2] == s2[j-1]:
                    dp[i][j] = min(dp[i][j], dp[i-2][j-2] + 0.5) # Transposition cost

    return dp[n][m]

def generate_candidates(misspelled_word: str, dictionary: List[str], top_n: int = 25) -> List[str]:
    """
    generates a list of robust candidate words using a multi-pass sieve approach:
    1. exact phonetic match (metaphone)
    2. visual/dyslexic weighted edit distance
    3. standard levenshtein for fallback
    """
    misspelled_word = misspelled_word.lower()
    target_phonetic = get_phonetic_code(misspelled_word)
    
    candidates_scored = []
    
    # Pass 1: Filter dictionary for broad matches first (Optimization)
    # In production, this loop should be replaced by a database query or pre-computed hash map
    
    for word in dictionary:
        word = word.lower()
        
        # Heuristic 1: Phonetic Match (Strongest signal for dyslexia)
        # "frend" -> "friend" (Both hash to 'FRNT')
        word_phonetic = get_phonetic_code(word)
        phonetic_dist = lev_distance(target_phonetic, word_phonetic)
        
        # If sounds are identical or very close
        if phonetic_dist <= 1:
            # Calculate precise visual distance
            vis_dist = calculate_visual_distance(misspelled_word, word)
            candidates_scored.append((word, vis_dist))
            continue
            
        # Heuristic 2: Edit Distance Cutoff
        # Only check expensive visual distance if lengths are close
        if abs(len(word) - len(misspelled_word)) <= 2:
            vis_dist = calculate_visual_distance(misspelled_word, word)
            # Threshold: Allow up to 3 "edits" if they are dyslexic-weighted
            if vis_dist <= 3.0:
                candidates_scored.append((word, vis_dist))

    # Sort by lowest distance (best match)
    candidates_scored.sort(key=lambda x: x[1])
    
    # Return just the words
    return [c[0] for c in candidates_scored[:top_n]]
