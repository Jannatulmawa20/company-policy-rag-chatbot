# config.py

import google.generativeai as genai


import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your environment or .env file.")


EMBED_MODEL = "models/text-embedding-004"

# Configure client
genai.configure(api_key=GEMINI_API_KEY)


__all__ = ["genai", "EMBED_MODEL"]
