import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from dyslexic_logic import calculate_visual_distance, generate_candidates, get_phonetic_code

def test_phonetic_hashing():
    # "frend" and "friend" should sound the same
    assert get_phonetic_code("frend") == get_phonetic_code("friend")
    # "sity" and "city" should sound the same
    assert get_phonetic_code("sity") == get_phonetic_code("city")

def test_visual_distance_bias():
    # 'b' vs 'd' should be closer than 'b' vs 'z' due to dyslexic weighting
    dist_bd = calculate_visual_distance("bad", "dad")
    dist_bz = calculate_visual_distance("bad", "zaz")
    assert dist_bd < dist_bz, "Visual confusion (b/d) should cost less than random typo"

def test_candidate_generation():
    dictionary = ["friend", "apple", "banana"]
    candidates = generate_candidates("frend", dictionary)
    assert "friend" in candidates
    assert "banana" not in candidates
