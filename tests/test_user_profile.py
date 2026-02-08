import pytest
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from user_profile import UserProfileManager

@pytest.fixture
def mock_profile(tmp_path):
    # Setup a temp file for the profile
    d = tmp_path / "data"
    d.mkdir()
    p_file = d / "test_profile.json"
    
    # Patch the global PROFILE_FILE in the module (simple monkeypatch)
    import user_profile
    original_path = user_profile.PROFILE_FILE
    user_profile.PROFILE_FILE = p_file
    
    manager = UserProfileManager()
    yield manager
    
    # Teardown
    user_profile.PROFILE_FILE = original_path

def test_learning_loop(mock_profile):
    # Simulate user correcting "teh" -> "the"
    mock_profile.learn_from_correction("teh", "the")
    
    # Check if "the" is now a frequent word
    assert "the" in mock_profile.data["accepted_words"]
    assert mock_profile.data["accepted_words"]["the"] == 1

def test_ignore_lexicon(mock_profile):
    # User ignores "GitHub"
    mock_profile.add_to_lexicon("GitHub")
    assert "GitHub" in mock_profile.data["lexicon"]
