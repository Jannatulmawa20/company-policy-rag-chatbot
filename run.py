"""run.py — Helper script to prepare environment and launch the Streamlit app

Usage examples:
  python run.py                 # Launch Streamlit on default port
  python run.py --port 8502     # Launch on port 8502
  python run.py --ingest        # Run `python ingest.py` then exit
  python run.py --ingest --run  # Run ingest then start Streamlit
  python -m run                 # Same as `python run.py`
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
MODEL_DIR = ROOT / "models"
INDEX_PATH = MODEL_DIR / "faiss_index.bin"


def check_env():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("[WARN] GEMINI_API_KEY not set. Add it in a .env file or export it in your environment.")
        print("[TIP] Example (PowerShell): $env:GEMINI_API_KEY=\"your_key_here\"")
        return False
    return True


def run_ingest():
    print("[INFO] Running ingest.py to build embeddings and FAISS index...")
    cmd = [sys.executable, "ingest.py"]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("[ERROR] ingest.py failed. Inspect output above.")
        return False
    print("[SUCCESS] Ingest finished.")
    return True


def run_streamlit(port: int = 8501, host: str = "localhost"):
    if not INDEX_PATH.exists():
        print(f"[WARN] FAISS index not found at {INDEX_PATH}. Run `python ingest.py` first or use `--ingest` flag.")
    # Use `python -m streamlit run` to make sure the venv's interpreter is used
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", str(port), "--server.address", host]
    print("[INFO] Launching Streamlit with command:")
    print(" ".join(cmd))
    # Use exec to directly replace the current process with streamlit process if possible
    try:
        os.execv(cmd[0], cmd)
    except Exception:
        # Fallback to subprocess
        subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="Run and manage the Policy Assistant Streamlit app")
    parser.add_argument("--ingest", action="store_true", help="Run ingest.py to rebuild embeddings/index")
    parser.add_argument("--run", action="store_true", help="Run Streamlit after any checks (default if not --ingest alone)")
    parser.add_argument("--port", type=int, default=8501, help="Port to run Streamlit on")
    parser.add_argument("--host", type=str, default="localhost", help="Host address for Streamlit")
    args = parser.parse_args()

    env_ok = check_env()

    if args.ingest:
        success = run_ingest()
        if not success:
            sys.exit(1)
        # if user requested run as well, continue
        if not args.run:
            return

    # If not ingest-only, launch the app
    run_streamlit(port=args.port, host=args.host)


if __name__ == "__main__":
    main()
