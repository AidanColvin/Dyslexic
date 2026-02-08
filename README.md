# NeuroRead: AI-Powered Literacy & Dyslexia Assistant

**NeuroRead** is a hybrid browser extension designed to democratize web accessibility for neurodivergent users. By bridging a lightweight Firefox frontend with a robust Python NLP backend, it provides real-time content adaptation, stylometric analysis, and multi-modal reading assistance (Text-to-Speech, Dictation, and Visual Overrides).

This tool moves beyond simple "overlay" extensions by using server-side natural language processing to understand the *context* of text, not just the spelling.

---

## Key Features

### 1. Visual Cognitive Load Management

* **Dyslexia-Friendly Font Overrides:** Instantly reflow web content into **OpenDyslexic**, **Arial**, or **Times New Roman** to reduce visual crowding.
* **Dynamic Typography:** Real-time adjustment of font size, line height, and letter spacing to suit individual reading needs.
* **Reader Mode:** Strips distractions from cluttered webpages, isolating text for focused reading.

### 2. Smart Reading Assistance

* **Contextual Definitions:** Double-click any word to retrieve its definition, part of speech, and usage examples.
* **Phonetic Breakdown:** Displays IPA phonetic spelling (e.g., */kəmˈpjuːtər/*) to aid in decoding.
* **Integrated Text-to-Speech (TTS):** One-click audio playback using Google's TTS API, allowing users to "read with their ears" without leaving the DOM.

### 3. Stylometric & Authorship Analysis (The "Brain")

* **Complexity Scoring:** Analyzes sentence structure to calculate "Average Sentence Complexity" and "vocabulary richness" (Type-Token Ratio).
* **Authorship Attribution:** Uses vector-based distance calculation to compare current text against known author signatures (e.g., Hemingway vs. Shakespeare style).
* **Algorithm:** Utilizes weighted feature vectors including:
* Average Word Length
* Hapax Legomena (Unique words ratio)
* Sentence Phrase Density



### 4. Active Learning & Annotation

* **Smart Dictation:** Speech-to-text input for form fields and essays, powered by backend processing for higher accuracy.
* **Web Annotation:** Highlight text and attach sticky notes/comments directly to the webpage DOM.
* **PDF Intelligence:** capable of extracting text from browser-rendered PDFs for summarization and commenting (currently in beta).

---

## System Architecture

NeuroRead utilizes a **Hybrid Client-Server Architecture** to overcome browser resource limitations.

1. **The Frontend (Firefox Extension):**
* **Stack:** JavaScript (ES6), HTML5, CSS3, WebExtension API.
* **Role:** Handles DOM manipulation (font injection), user events (clicks/highlighting), and captures audio for dictation. It acts as the "Face" of the application.


2. **The Backend (Python API):**
* **Stack:** Python 3.10, Flask, TextBlob, Scikit-learn.
* **Role:** The "Brain." It receives raw text/audio from the browser, performs heavy NLP computations (tokenization, vectorization, sentiment analysis), and returns structured JSON data.
* **Why this approach?** Offloading logic to Python allows for the use of advanced ML libraries (`numpy`, `scikit-learn`) that are not natively available or performant in client-side JavaScript.



---

## Installation & Setup

### Prerequisites

* Firefox Browser (Developer Edition or Standard)
* Python 3.8+
* Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/neuro-read.git
cd neuro-read

```

### Step 2: Initialize the Backend

Navigate to the root directory where `app.py` is located.

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the Flask Server
python app.py

```

*Output should indicate: `Running on http://127.0.0.1:5000*`

### Step 3: Load the Extension

1. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`.
2. Click **"Load Temporary Add-on..."**.
3. Navigate to the `extension/` folder in this repo and select the `manifest.json` file.
4. The NeuroRead icon should appear in your toolbar.

---

## Usage Guide

### Reading Mode

1. Click the **NeuroRead Icon** in the toolbar.
2. Select your preferred font (e.g., "OpenDyslexic") and adjust the size slider.
3. The active webpage will instantly update.

### Dictionary & Pronunciation

1. **Double-click** any word on a webpage.
2. A tooltip will appear containing:
* The Definition.
* Phonetic spelling.
* A **Speaker Icon**.


3. Click the Speaker Icon to hear the pronunciation.

### Analyzing Text Complexity

1. Highlight a paragraph of text.
2. Right-click and select **"Analyze Selection with NeuroRead"**.
3. The popup will display the "Stylometric Signature" (Sentence length, complexity score, and estimated reading level).

---

## Project Structure

```text
neuro-read/
├── app.py                 # Flask Entry Point
├── logic.py               # Core NLP & Stylometry Algorithms
├── requirements.txt       # Python Dependencies
├── known_authors/         # Reference corpus for authorship attribution
│   ├── hemingway.txt
│   └── ...
└── extension/             # Firefox WebExtension Source
    ├── manifest.json      # Extension Config
    ├── content.js         # DOM Interaction Script
    ├── background.js      # Event Listeners
    ├── popup.html         # UI Layout
    ├── popup.js           # UI Logic
    └── assets/            # Icons and Fonts

```

---

## Roadmap

* **v1.1:** Integration of Transformer models (HuggingFace) for context-aware grammar correction.
* **v1.2:** "Save to Drive" feature for annotated PDF research papers.
* **v2.0:** Mobile App integration via React Native.

## Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
