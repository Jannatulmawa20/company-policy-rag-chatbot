# HR & Company Policy Chatbot – Advanced RAG System with Google Gemini

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-orange)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-green)](https://ai.google.dev/)

---

## Getting Started ✅

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

### Useful Commands & Tips 🔧

- Run ingest and then immediately start the app:
  - `python run.py --ingest --run`
- Change the Streamlit port: `python run.py --port 8502`
- If you see `GEMINI_API_KEY not set`, ensure your `.env` file is present or export the variable in your shell.
- If `faiss_index.bin` is missing, run `python ingest.py` to recreate `models/faiss_index.bin` and `models/metadata.pkl`.

---

[![RAG](https://img.shields.io/badge/Architecture-Retrieval-Augmented%20Generation-purple)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A production-oriented Retrieval-Augmented Generation (RAG) chatbot** that answers questions about company/HR policies directly from your internal PDF/text documents — with **source citations**, **hallucination mitigation**, and a clean interactive interface.

Built as a strong portfolio project to demonstrate hands-on expertise in **RAG pipelines**, **LLM integration**, **vector search**, **document ingestion**, and **deployable AI applications** — perfect for Mid-Level AI Engineer roles.

### Live Demo Screenshot (Example Interaction)

Here’s how the chatbot looks and responds in action:

<p align="center">
  <a href="images/img.png"><img src="images/img.png" alt="Policy Assistant screenshot" width="900"/></a>
</p>

> The company's leave policy includes:  
> • **Annual Leave**: Full-time employees receive 20 working days of paid annual leave per year. Must be requested at least 3 days in advance and requires approval from the reporting manager or HR.  
> • **Sick Leave**: Employees receive 10 days of paid sick leave per year. A medical certificate is required for sick leave longer than 2 consecutive days. Sick leave should be informed before working hours whenever possible.  
> • **Casual Leave**: Employees may take up to 5 days per year for personal or urgent matters. It must be informed at least 1 day ahead, except in emergencies.

### ✨ Key Features

- **Grounded & Accurate Responses** — Strictly uses content from your policy documents only
- **Source Citations with Metadata** — Displays document name, chunk ID, and similarity score for full traceability
- **Anti-Hallucination Safeguards** — Strict prompt forces "I cannot find this information" when context is missing
- **Flexible Document Support** — Handles both `.pdf` and `.txt` files
- **Interactive & User-Friendly** — Beautiful chat interface built with Streamlit
- **Modular Design** — Easy to extend (memory, hybrid search, different LLMs/DBs)

### Tech Stack

| Category              | Tools & Technologies                              |
|-----------------------|---------------------------------------------------|
| Language              | Python 3.10+                                      |
| UI/Framework          | Streamlit                                         |
| LLM                   | Google Gemini 2.5 Flash / Pro                     |
| Embeddings            | Google `text-embedding-004`                       |
| Vector Database       | FAISS (Flat L2 Index)                             |
| Document Processing   | PyPDF2                                            |
| Others                | NumPy, pickle, python-dotenv                      |

### Project Structure

```text
Chatbox-HR-Policy/
├── data/
│   └── policies/               # ← Put your HR/Company policy PDFs or .txt files here
├── models/                     # Auto-generated: FAISS index + metadata (gitignored)
├── .venv/                      # Virtual environment (gitignored)
├── app.py                      # Main Streamlit chat application
├── ingest.py                   # Document loader, chunker, embedder & FAISS builder
├── rag_utils.py                # Core RAG engine (retrieval + prompt + generation)
├── config.py                   # Gemini configuration & API setup
├── requirements.txt            # All dependencies
├── .env                        # Your GEMINI_API_KEY (gitignored)
├── .gitignore
└── README.md