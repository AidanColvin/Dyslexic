from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import logging
import os

# --- IMPORT YOUR MODULES ---
import logic              # Stylometry
import speech_service     # TTS / STT
import text_service       # Summarization / Basic NLP
import ai_grammar         # T5 Grammar Correction
import dyslexic_logic     # Phonetic Hashing / Edit Distance
import context_engine     # BERT Context Ranking
import pdf_service        # PDF Text Extraction
import dictionary_service # Definitions
import notes_service      # User Annotations

# --- CONFIGURATION ---
app = Flask(__name__)
CORS(app) # Allow Firefox Extension to connect

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeuroRead")

# --- SYSTEM ENDPOINTS ---

@app.route("/status", methods=["GET"])
def health_check():
    """
    verifies system status and module availability
    """
    return jsonify({
        "status": "online",
        "modules": {
            "ai_grammar": ai_grammar._grammar_model is not None,
            "context_engine": context_engine._fill_mask is not None
        }
    })

# --- DYSLEXIA & GRAMMAR ENDPOINTS ---

@app.route("/dyslexia/suggest", methods=["POST"])
def suggest_correction():
    """
    advanced spellcheck using dyslexic heuristics + bert context
    expects json: { "sentence": "...", "misspelled_word": "..." }
    """
    data = request.get_json()
    sentence = data.get("sentence", "")
    misspelled = data.get("misspelled_word", "").lower()
    
    if not sentence or not misspelled:
        return jsonify({"error": "Missing inputs"}), 400

    # 1. Generate Candidates (Phonetic + Weighted Distance)
    # Note: In production, load a real dict. Using a small set for demo safety.
    # You should load a full word list in global scope.
    candidates = dyslexic_logic.generate_candidates(misspelled, ["friend", "said", "city", "from"]) 
    
    # 2. Contextual Ranking (BERT)
    ranked = context_engine.rank_candidates_by_context(sentence, misspelled, candidates)
    
    return jsonify({"suggestions": ranked})

@app.route("/nlp/smart-correct", methods=["POST"])
def smart_correct():
    """
    full sentence grammar correction using T5 transformer
    expects json: { "text": "..." }
    """
    data = request.get_json()
    text = data.get("text", "")
    
    try:
        result = ai_grammar.fix_contextual_grammar(text)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Grammar Error: {e}")
        return jsonify({"error": "Processing failed"}), 500

# --- READING ASSISTANCE ENDPOINTS ---

@app.route("/read/define", methods=["POST"])
def define_word():
    """
    fetches definition and audio url for a word
    expects json: { "word": "..." }
    """
    data = request.get_json()
    word = data.get("word", "")
    
    details = dictionary_service.fetch_word_details(word)
    if not details:
        return jsonify({"found": False}), 404
        
    return jsonify({"found": True, "data": details})

@app.route("/read/analyze-style", methods=["POST"])
def analyze_style():
    """
    calculates stylometric signature (complexity, authorship)
    expects json: { "text": "..." }
    """
    data = request.get_json()
    text = data.get("text", "")
    signature = logic.make_signature(text)
    return jsonify({"signature": signature})

@app.route("/read/pdf-text", methods=["POST"])
def parse_pdf():
    """
    extracts text from an uploaded pdf file
    expects multipart/form-data: { "file": <pdf_blob> }
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    text = pdf_service.extract_text_from_pdf_bytes(file.read())
    
    return jsonify({"text_length": len(text), "content": text})

# --- VOICE & NOTES ENDPOINTS ---

@app.route("/voice/speak", methods=["POST"])
def speak():
    """
    text-to-speech generation
    returns mp3 audio file
    """
    data = request.get_json()
    text = data.get("text", "")
    file_path = speech_service.text_to_audio_file(text)
    return send_file(file_path, mimetype="audio/mpeg")

@app.route("/voice/dictate", methods=["POST"])
def dictate():
    """
    speech-to-text transcription
    expects audio file upload
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio"}), 400
    
    # Save temp and process
    audio_file = request.files['audio']
    temp_path = Path("temp") / audio_file.filename
    audio_file.save(temp_path)
    
    text = speech_service.audio_file_to_text(str(temp_path))
    speech_service.cleanup_temp_file(str(temp_path))
    
    return jsonify({"transcription": text})

@app.route("/notes/add", methods=["POST"])
def add_note():
    """
    saves a user annotation
    expects json: { "url": "...", "text": "...", "comment": "..." }
    """
    data = request.get_json()
    note = notes_service.add_note(
        data.get("url"), 
        data.get("selected_text"), 
        data.get("comment")
    )
    return jsonify(note)

@app.route("/notes/get", methods=["GET"])
def get_notes():
    """
    retrieves notes for a specific url
    expects query param: ?url=...
    """
    url = request.args.get("url")
    notes = notes_service.get_notes_for_url(url)
    return jsonify({"notes": notes})

if __name__ == "__main__":
    # Pre-load heavy models to avoid lag on first request
    print("Initializing AI Models...")
    ai_grammar.load_model()
    context_engine.load_context_model()
    
    # Run server
    app.run(host="0.0.0.0", port=5000, debug=True)
