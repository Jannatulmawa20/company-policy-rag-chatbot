# config.py

import google.generativeai as genai


GEMINI_API_KEY = "AIzaSyBBTlU8QoattS7Fam0vXI3dosNKed-Tg-s"


EMBED_MODEL = "models/text-embedding-004"

# Configure client
genai.configure(api_key=GEMINI_API_KEY)


__all__ = ["genai", "EMBED_MODEL"]
