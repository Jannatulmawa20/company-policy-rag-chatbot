import os
import pickle
import numpy as np
import faiss
from PyPDF2 import PdfReader

# config.py theke configured genai ar EMBED_MODEL ene nicchi
from config import genai, EMBED_MODEL

DATA_DIR = "data/policies"
MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)


def load_document(path):
    
    if path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif path.endswith(".pdf"):
        reader = PdfReader(path)
        texts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
        return "\n".join(texts)
    return ""


def chunk_text(text, max_len=400):
    
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_len - 50):
        chunk = " ".join(words[i:i + max_len])
        chunks.append(chunk)
    return chunks


def embed_texts(text_list):
    
    vectors = EMBED_MODEL.encode(text_list, convert_to_numpy=True)
    return vectors.astype("float32")


def ingest_documents():
    print("[INFO] Reading policy files...")

    if not os.path.isdir(DATA_DIR):
        print(f"[ERROR] Data directory not found: {DATA_DIR}")
        return

    files = [f for f in os.listdir(DATA_DIR) if f.endswith((".txt", ".pdf"))]

    all_chunks = []
    metadata = []

    for file in files:
        full_path = os.path.join(DATA_DIR, file)
        text = load_document(full_path)

        if not text.strip():
            print(f"[WARN] Empty document skipped: {file}")
            continue

        chunks = chunk_text(text)

        for idx, ch in enumerate(chunks):
            all_chunks.append(ch)
            metadata.append({
                "doc": file,
                "chunk_id": idx,
                "text": ch
            })

        print(f"[INFO] Processed: {file} ({len(chunks)} chunks)")

    print(f"[INFO] Total Chunks: {len(all_chunks)}")

    if not all_chunks:
        print("[ERROR] No chunks found. Check your data/policies folder.")
        return

    # Embeddings
    print("[INFO] Generating embeddings (Gemini)...")
    vectors = embed_texts(all_chunks)

    # Build FAISS
    print("[INFO] Building FAISS index...")
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    # Save index & metadata
    index_path = os.path.join(MODEL_DIR, "faiss_index.bin")
    meta_path = os.path.join(MODEL_DIR, "metadata.pkl")

    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(metadata, f)

    print(f"[SUCCESS] Ingestion completed!")
    print(f"[SUCCESS] Saved index to: {index_path}")
    print(f"[SUCCESS] Saved metadata to: {meta_path}")


if __name__ == "__main__":
    ingest_documents()
