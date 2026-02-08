# 🧠 NeuroRead: AI-Powered Literacy & Dyslexia Assistant

> **"Democratizing web accessibility through server-side intelligence."**

**NeuroRead** is a hybrid browser extension and Python AI backend designed to bridge the gap between standard web content and neurodivergent processing needs. Unlike simple "overlay" extensions that just change fonts, NeuroRead uses **Natural Language Processing (NLP)**, **Stylometric Analysis**, and **Deep Learning** to understand the *context* of text, not just its spelling.

It provides real-time content adaptation, authorship analysis, and multi-modal reading assistance (Text-to-Speech, Dictation, and Visual Overrides).

---

## 🚀 Key Features & Capabilities

### 1. 👁️ Visual Cognitive Load Management
* **Dyslexia-Friendly Reflow:** Instantly injects **OpenDyslexic**, **Arial**, or **Times New Roman** fonts to reduce visual crowding.
* **Bionic Reading Mode:** Highlights the first few letters of every word to guide the eye and improve reading speed.
* **Distraction-Free Reader:** Strips ads, sidebars, and navigational clutter, isolating the core text for focused consumption.
* **Dynamic Typography:** Real-time adjustment of line height, letter spacing, and font size.

### 2. 🧠 The "Brain": Stylometric & AI Analysis
* **Complexity Scoring:** Analyzes sentence structure to calculate "Average Sentence Complexity" and "Vocabulary Richness" (Type-Token Ratio).
* **Authorship Attribution:** Uses vector-based distance calculations to compare text against known styles (e.g., distinguishing academic formal vs. blog casual).
    * *Algorithm:* Weighted feature vectors including **Hapax Legomena** (unique word ratio) and **Sentence Phrase Density**.
* **Contextual Re-Ranking (BERT):** Uses Hugging Face Transformers to distinguish between homophones (*their/there/they're*) based on sentence context.

### 3. 🛡️ Dyslexia Correction Engine
* **Phonetic Hashing:** Converts words to their IPA sound codes (e.g., /kəmˈpjuːtər/) to catch phonetic spelling errors (e.g., "frend" $\rightarrow$ "friend").
* **Visual Distance Weighting:** The algorithm understands that neurodivergent users confuse specific shapes. It prioritizes corrections based on visual similarity (e.g., weighting 'b'/'d' swaps lower than random typos).

### 4. 🗣️ Multi-Modal Assistance
* **Smart Dictation:** Speech-to-text input for forms and essays, processed by the backend for higher accuracy than standard browser APIs.
* **Integrated Text-to-Speech (TTS):** One-click audio playback allowing users to "read with their ears" without leaving the DOM.
* **Contextual Definitions:** Double-click any word to retrieve its definition, part of speech, and phonetic breakdown.

---

## 🏗️ System Architecture

NeuroRead utilizes a **Hybrid Client-Server Architecture** to overcome browser resource limitations.

### **The Frontend (Firefox Extension)**
* **Stack:** JavaScript (ES6), HTML5, CSS3, WebExtension API.
* **Role:** The "Face". Handles DOM manipulation (font injection), user events (clicks/highlighting), and captures audio.

### **The Backend (Python API)**
* **Stack:** Python 3.10+, Flask, Transformers (BERT), Scikit-learn, TextBlob.
* **Role:** The "Brain". Offloads heavy NLP computations (tokenization, vectorization, sentiment analysis) from the client to the server.

---

## 📂 Project Structure

\`\`\`text
neuro-read/
├── backend/                  # The Intelligence Layer
│   ├── app.py                # Flask API Gateway & Entry Point
│   ├── dyslexic_logic.py     # Phonetic Hashing & Visual Distance Algorithms
│   ├── context_engine.py     # BERT Transformer Model for Contextualization
│   ├── structure_analyzer.py # Stylometry, Complexity Scoring & HTML Parsing
│   └── user_profile.py       # Active Learning (User Corrections & Lexicon)
├── extension/                # The Browser Interface
│   ├── manifest.json         # Extension Configuration
│   ├── content.js            # DOM Injection (Reader Mode/Fonts)
│   ├── background.js         # API Communication
│   ├── popup.html            # User Interface (Menu)
│   └── assets/               # Icons & Fonts
├── config/                   # Environment Configurations
│   ├── public_mode.env       # Open Access Settings
│   └── private_mode.env      # Secured/API Key Settings
├── tests/                    # Diagnostic Suite
│   ├── test_dyslexic_logic.py
│   ├── test_api_integration.py
│   └── ...
├── run.py                    # Root Launcher
├── Procfile                  # Cloud Deployment Config (Render/Heroku)
└── requirements.txt          # Python Dependencies
\`\`\`

---

## 🛠️ Installation & Setup

### Prerequisite: Python Backend
1.  **Clone the Repo:**
    \`\`\`bash
    git clone https://github.com/AidanColvin/neuro-read.git
    cd neuro-read
    \`\`\`

2.  **Install Dependencies:**
    \`\`\`bash
    # Create virtual environment (Recommended)
    python -m venv venv
    source venv/bin/activate
    
    # Install libraries
    pip install -r requirements.txt
    \`\`\`

3.  **Start the Server:**
    \`\`\`bash
    python run.py
    \`\`\`
    *Output:* \`Running on http://0.0.0.0:5000\`

### Loading the Extension
1.  Open Firefox and navigate to \`about:debugging\`.
2.  Click **"This Firefox"** > **"Load Temporary Add-on"**.
3.  Navigate to the \`extension/\` folder and select \`manifest.json\`.
4.  The NeuroRead icon will appear in your toolbar.

---

## 🧪 Usage Guide

**1. Reading Mode**
* Click the NeuroRead Icon.
* Toggle "Reader Mode" to strip distractions.
* Select "OpenDyslexic" font and adjust size.

**2. Analyzing Text Complexity**
* Highlight a paragraph.
* Right-click and select **"Analyze Selection with NeuroRead"**.
* View the "Stylometric Signature" (Reading Level & Complexity Score).

**3. Dictionary & Pronunciation**
* Double-click any word.
* A tooltip appears with the definition, IPA phonetics, and a Speaker icon for TTS.

---

## 🗺️ Roadmap
* **v1.1:** Integration of Transformer models (HuggingFace) for context-aware grammar correction. (Completed)
* **v1.2:** "Save to Drive" feature for annotated PDF research papers.
* **v2.0:** Mobile App integration via React Native.

---

## 🤝 Contributing
Contributions are welcome! Please read \`CONTRIBUTING.md\` for details on our code of conduct and the process for submitting pull requests.

**Author:** Aidan Colvin
**License:** MIT
EOF












OG

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
