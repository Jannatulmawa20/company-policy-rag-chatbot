# config.py

import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your environment or .env file.")

# Initialize the GenAI client for LLM
genai.configure(api_key=GEMINI_API_KEY)

# Use local embedding model (no API calls needed)
EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

__all__ = ["genai", "EMBED_MODEL"]
