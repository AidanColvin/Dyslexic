import os
import logging
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from pathlib import Path

# Import your robust modules (ensure these files exist from previous steps)
import suggestion_pipeline
import user_profile
import readability_service
import pdf_reflow_service
import structure_analyzer

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeuroRead-Backend")

app = Flask(__name__)

# CRITICAL: Allow CORS for all domains so the Extension (which runs on any URL) can talk to this.
# In production, you might restrict this, but for Codespaces + Extension, we need wildcard access.
CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_request
def handle_preflight():
    """
    Handle CORS preflight requests for browser extensions.
    """
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, X-User-ID")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response

def get_user_id():
    """
    Helper to extract the unique User ID sent by the extension.
    This ensures 'Private' learning profiles for each user.
    """
    # Default to 'public_guest' if the extension doesn't send an ID
    return request.headers.get("X-User-ID", "public_guest")

# --- 1. DYSLEXIA & LEARNING ENDPOINTS ---

@app.route("/dyslexia/v2/suggest", methods=["POST"])
def suggest_robust():
    """
    Main spellcheck endpoint. 
    Personalizes results based on the X-User-ID header.
    """
    user_id = get_user_id()
    data = request.get_json()
    sentence = data.get("sentence", "")
    misspelled = data.get("misspelled_word", "").lower()
    
    # Load dictionary (In production, load this once globally)
    from nltk.corpus import words as nltk_words
    english_vocab = [w.lower() for w in nltk_words.words() if len(w) > 2]

    # Pass user_id to pipeline to load specific profile
    result = suggestion_pipeline.get_robust_suggestions(
        sentence, 
        misspelled, 
        english_vocab,
        user_id=user_id 
    )
    
    return jsonify(result)

@app.route("/dyslexia/feedback", methods=["POST"])
def feedback():
    """
    Learning Endpoint.
    Records when a user accepts/ignores a suggestion to update their private profile.
    """
    user_id = get_user_id()
    data = request.get_json()
    
    suggestion_pipeline.handle_user_feedback(
        data.get("misspelling"),
        data.get("chosen"),
        data.get("action"),
        user_id=user_id
    )
    
    return jsonify({"status": "learned", "user": user_id})

# --- 2. READER MODE & PDF ENDPOINTS ---

@app.route("/view/reader-mode", methods=["POST"])
def reader_mode():
    """
    Takes a URL and returns a cleaned, dyslexia-friendly HTML version.
    Using POST to avoid URL encoding issues in query params.
    """
    data = request.get_json()
    url = data.get("url")
    
    if not url: 
        return jsonify({"error": "No URL provided"}), 400
        
    result = readability_service.fetch_and_clean_url(url)
    return jsonify(result) # Returns { html: "...", title: "..." }

@app.route("/view/condense", methods=["POST"])
def condense():
    """
    Analyzes text to extract structure (Headings, Bullets).
    """
    data = request.get_json()
    text = data.get("text", "")
    structure = structure_analyzer.extract_key_structure(text)
    return jsonify(structure)

# --- 3. SYSTEM STATUS ---

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online", 
        "backend": "NeuroRead v2.0",
        "mode": "Codespace Public"
    })

if __name__ == "__main__":
    # In Codespaces, we must run on 0.0.0.0 to expose the port
    app.run(host="0.0.0.0", port=5000, debug=True)
