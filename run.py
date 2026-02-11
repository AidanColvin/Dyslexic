from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from dyslexic.app import app

if __name__ == "__main__":
    print("Starting Dyslexic...")
    app.run(host="0.0.0.0", port=5000)
