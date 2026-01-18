import os
import pickle
import numpy as np
import faiss

from config import genai, EMBED_MODEL  


MODEL = "gemini-2.5-flash"


class RAGEngine:
    def __init__(self, top_k=4):
        self.top_k = top_k

        index_path = "models/faiss_index.bin"
        meta_path = "models/metadata.pkl"

        if not os.path.exists(index_path) or not os.path.exists(meta_path):
            raise FileNotFoundError(
                "FAISS index or metadata not found. Please run `python ingest.py` first."
            )

        # Load FAISS index & metadata
        self.index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)

    # ---------- EMBED QUERY ----------
    def embed_query(self, text: str) -> np.ndarray:
       
        if not text or not text.strip():
            raise ValueError("Query cannot be empty.")

        vec = EMBED_MODEL.encode(text, convert_to_numpy=True).astype("float32").reshape(1, -1)
        return vec

    # ---------- RETRIEVE ----------
    def retrieve(self, query: str):
        
        query_vec = self.embed_query(query)
        distances, indices = self.index.search(query_vec, self.top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
           
            if idx < 0 or idx >= len(self.metadata):
                continue 
                
            meta = self.metadata[idx]
            results.append({
                "rank": rank,
                "score": float(distances[0][rank]),
                "doc": meta["doc"],
                "chunk_id": meta["chunk_id"],
                "text": meta["text"],
            })
        return results

    # ---------- BUILD PROMPT ----------
    def build_prompt(self, question: str, retrieved):
        
        context_blocks = []
        for r in retrieved:
            block = f"Source Document: {r['doc']} (Chunk: {r['chunk_id']})\nContent: {r['text']}"
            context_blocks.append(block)

        context = "\n\n".join(context_blocks)

        prompt = f"""
You are a company policy assistant chatbot.

Use ONLY the context below (company policies) to answer the user's question.
If the answer is not clearly found in the context, reply exactly with:
"I cannot find this information."

### CONTEXT:
{context}

### QUESTION:
{question}

### ANSWER (in clear, simple English):
"""
        return prompt

    # ---------- GENERATE ANSWER ----------
    def generate_answer(self, question: str):
        
        retrieved = self.retrieve(question)
        
       
        if not retrieved:
             return {
                "answer": "I cannot find this information.",
                "sources": [],
            }

        prompt = self.build_prompt(question, retrieved)

        
        model = genai.GenerativeModel(MODEL)
        
        try:
            response = model.generate_content(prompt)
            
            
            if hasattr(response, "text"):
                answer_text = response.text
            else:
                
                answer_text = "I cannot find this information."
                
                print(f"Warning: Response object has no 'text' attribute. Response: {response}")

        except Exception as e:
            
            print(f"Error during generation: {e}")
            answer_text = "Sorry, I encountered an error while processing your request."

        return {
            "answer": answer_text,
            "sources": retrieved,
        }