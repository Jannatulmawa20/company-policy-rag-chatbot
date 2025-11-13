import os
import pickle
import numpy as np
import faiss

from config import genai, EMBED_MODEL  # genai client + embed model config theke

# [CODE UPDATE]
# "gemini-1.5-flash" মডেলটি 404 Not Found এরর দিচ্ছিল।
# আমরা এটিকে "gemini-pro" তে পরিবর্তন করেছি, যা জেনারেশনের জন্য সহজলভ্য।
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
        """Query text ke Gemini diye embedding vector e convert kore."""
        if not text or not text.strip():
            raise ValueError("Query cannot be empty.")

        result = genai.embed_content(
            model=EMBED_MODEL,
            content=text,
            task_type="RETRIEVAL_QUERY" # Query embedding এর জন্য task_type যোগ করা ভালো
        )

        vec = np.array(result["embedding"], dtype="float32").reshape(1, -1)
        return vec

    # ---------- RETRIEVE ----------
    def retrieve(self, query: str):
        """User query er sathe shobcheye relevant chunks ber kore."""
        query_vec = self.embed_query(query)
        distances, indices = self.index.search(query_vec, self.top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            # নিশ্চিত করুন যে idx মেটাডেটার সীমার মধ্যে আছে
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
        """Context + question diye final prompt toiri kore Gemini ke dey."""
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
        """Main function: retrieve + prompt + Gemini diye final answer."""
        retrieved = self.retrieve(question)
        
        # যদি কোনো রিলেভেন্ট কনটেক্সট না পাওয়া যায়
        if not retrieved:
             return {
                "answer": "I cannot find this information.",
                "sources": [],
            }

        prompt = self.build_prompt(question, retrieved)

        # জেনারেশনের জন্য মডেল ইনিশিয়ালাইজ করুন
        model = genai.GenerativeModel(MODEL)
        
        try:
            response = model.generate_content(prompt)
            
            # response.text ব্যবহার করা নিরাপদ
            if hasattr(response, "text"):
                answer_text = response.text
            else:
                # ফলব্যাক (যদি response.text অ্যাট্রিবিউট না থাকে)
                answer_text = "I cannot find this information."
                # আপনি এখানে এরর লগ করতে পারেন
                print(f"Warning: Response object has no 'text' attribute. Response: {response}")

        except Exception as e:
            # API কল ফেইল হলে একটি ফলব্যাক উত্তর দিন
            print(f"Error during generation: {e}")
            answer_text = "Sorry, I encountered an error while processing your request."

        return {
            "answer": answer_text,
            "sources": retrieved,
        }