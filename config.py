# config.py

import google.generativeai as genai

# 🔑 তোমার আসল Gemini API KEY বসাও
GEMINI_API_KEY = "AIzaSyBBTlU8QoattS7Fam0vXI3dosNKed-Tg-s"

# এক জায়গায় model name রাখি
EMBED_MODEL = "models/text-embedding-004"

# Configure client
genai.configure(api_key=GEMINI_API_KEY)

# অন্য ফাইলে use করার জন্য expose করি
__all__ = ["genai", "EMBED_MODEL"]
