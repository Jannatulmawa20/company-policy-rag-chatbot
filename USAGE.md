# Getting Started

Follow these steps to run the Policy Assistant locally:

1. Create and activate a virtual environment (recommended):
   - PowerShell: `python -m venv venv; .\venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `python -m pip install -r requirements.txt`
3. Set your Gemini API key (one-time):
   - Create a `.env` file with:
     ```text
     GEMINI_API_KEY=your_key_here
     ```
   - Or set it in PowerShell: `$env:GEMINI_API_KEY="your_key_here"`
4. Build the embeddings & FAISS index (required once or when documents change):
   - `python ingest.py`
5. Run the app (choose one of the following):
   - Direct Streamlit run: `streamlit run app.py`
   - Use the helper runner: `python run.py` (or `python -m run`) — this checks env and helps run `ingest.py` if needed.

Useful Commands & Tips

- Run ingest and then immediately start the app:
  - `python run.py --ingest --run`
- Change the Streamlit port: `python run.py --port 8502`
- If you see `GEMINI_API_KEY not set`, ensure your `.env` file is present or export the variable in your shell.
- If `faiss_index.bin` is missing, run `python ingest.py` to recreate `models/faiss_index.bin` and `models/metadata.pkl`.
