from readability import Document
import requests
from bs4 import BeautifulSoup, Comment
from typing import Dict, Any, Optional

# --- DYSLEXIA CSS DEFAULTS ---
# These inject the specific visual tweaks you requested into the clean HTML
DEFAULT_CSS = """
<style>
    :root {
        --bg-color: #FDFBF7;       /* Cream/Off-white (User preference) */
        --text-color: #333333;     /* Dark Gray (Not pure black) */
        --font-family: 'Arial', sans-serif; 
        --line-height: 1.5;
        --letter-spacing: 0.035em; /* ~35% increase equivalent */
        --max-width: 75ch;         /* ~60-75 characters per line */
    }
    body {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: var(--font-family);
        line-height: var(--line-height);
        letter-spacing: var(--letter-spacing);
        max-width: var(--max-width);
        margin: 0 auto;
        padding: 2rem;
        text-align: left !important; /* Force Left Align */
    }
    /* Kill "Fluff" Styling */
    i, em { font-style: normal; } /* Remove italics */
    b, strong { font-weight: 700; color: #222; } /* Limit bold to keywords */
    u { text-decoration: none; } /* Remove underlines */
    
    /* Accessibility Structure */
    h1, h2, h3 { color: #005a9c; } /* Clear headers (Color + Size) */
    a { text-decoration: underline; color: #0044CC; } /* Distinct links */
    p { margin-bottom: 1.5em; } /* Generous paragraph spacing */
</style>
"""

def fetch_and_clean_url(url: str, user_prefs: Optional[Dict] = None) -> Dict[str, Any]:
    """
    fetches a webpage, extracts the main content, strips distractions,
    and wraps it in a dyslexia-friendly html container
    """
    try:
        # 1. Fetch Raw HTML
        # In production, use a proper User-Agent to avoid blocking
        response = requests.get(url, timeout=10, headers={"User-Agent": "NeuroRead/1.0"})
        if response.status_code != 200:
            return {"error": "Failed to retrieve page"}

        # 2. Extract "Main Content" (Reader View)
        # using readability-lxml to find the article body and ignore sidebars/ads
        doc = Document(response.text)
        summary_html = doc.summary()
        title = doc.title()

        # 3. Clean and Sanitize (The "Kill Fluff" Step)
        soup = BeautifulSoup(summary_html, "html.parser")

        # Remove distractions and accessibility hazards
        for tag in soup(["script", "style", "iframe", "noscript", "svg"]):
            tag.decompose()
        
        # Strip hostile attributes (inline styles that force justification or fonts)
        for tag in soup.find_all(True):
            if tag.has_attr('style'):
                del tag['style']
            if tag.has_attr('class'):
                del tag['class']
            if tag.has_attr('align'):
                del tag['align'] # Kill justified text

        # 4. Construct Final HTML
        # We wrap the clean content in our simplified structure
        clean_body = str(soup)
        
        # In a real app, you would generate dynamic CSS based on 'user_prefs'
        # e.g., if user_prefs['bg'] == 'blue', change --bg-color
        
        final_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{title} - NeuroRead View</title>
            {DEFAULT_CSS}
        </head>
        <body>
            <header>
                <h1>{title}</h1>
                <hr>
            </header>
            <main>
                {clean_body}
            </main>
        </body>
        </html>
        """

        return {
            "title": title,
            "html": final_html,
            "original_url": url
        }

    except Exception as e:
        return {"error": str(e)}
