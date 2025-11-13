import streamlit as st
from rag_utils import RAGEngine

# --- পেজ কনফিগারেশন (শুরুতে থাকা ভালো) ---
st.set_page_config(page_title="Company Policy Chatbot", page_icon="📘")

# --- মূল অপটিমাইজেশন ---
# @st.cache_resource RAG ইঞ্জিনকে মেমরিতে ক্যাশে করে রাখে।
# এটি শুধু প্রথমবার লোড হবে, প্রতিবার বাটন ক্লিকে নয়।
@st.cache_resource
def get_engine():
    """RAG ইঞ্জিন লোড করে এবং ক্যাশে করে রাখে।"""
    st.write("Loading RAG Engine... (This happens only once)")
    try:
        engine = RAGEngine(top_k=4)
        return engine
    except FileNotFoundError as e:
        st.error(f"Error: {e}. Please run 'python ingest.py' first.")
        return None

def main():
    st.title("📘 Company Policy Chatbot (Google Gemini RAG)")
    st.write("Ask questions based on the policy documents in `data/policies/`")

    # ক্যাশে থেকে ইঞ্জিন লোড করুন
    engine = get_engine()

    # ইঞ্জিন লোড না হলে অ্যাপ বন্ধ করুন
    if engine is None:
        return

    query = st.text_input("Your question:", placeholder="e.g., What is the sick leave policy?")

    if st.button("Get Answer"):
        # --- ইনপুট ভ্যালিডেশন ---
        if not query or not query.strip():
            st.error("Please enter a question.")
        else:
            # --- লোডিং স্পিনার (UX Improvement) ---
            with st.spinner("Searching policies and generating answer..."):
                try:
                    result = engine.generate_answer(query)

                    st.subheader("Answer:")
                    st.write(result["answer"])

                    # --- সোর্স দেখানোর উন্নত পদ্ধতি ---
                    if result["sources"]:
                        st.subheader("Sources:")
                        with st.expander("Click to see retrieved sources"):
                            for s in result["sources"]:
                                # সোর্সকে আরও সুন্দরভাবে দেখান
                                st.info(
                                    f"Source: **{s['doc']}** (Chunk: {s['chunk_id']})\n"
                                    f"Score: {s['score']:.4f}\n\n"
                                    f"---\n{s['text']}"
                                )
                    else:
                        st.write("No specific sources were retrieved for this answer.")
                
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()