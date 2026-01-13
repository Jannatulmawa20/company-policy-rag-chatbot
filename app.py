import streamlit as st
import time
from rag_utils import RAGEngine

# Page Configuration
st.set_page_config(page_title="Company Policy Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for a cleaner look (Optional)
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_engine():
    """Loads the RAG engine once to avoid reloading on every interaction."""
    try:
        engine = RAGEngine(top_k=4)
        return engine
    except FileNotFoundError as e:
        st.error(f"⚠️ Error: {e}. Please run 'python ingest.py' first.")
        return None

def main():
    st.title("🤖 Policy Assistant")
    st.caption("Ask questions about company policies, leave, or HR guidelines.")

    # 1. Load RAG Engine
    engine = get_engine()
    if engine is None:
        return

    # 2. Initialize Chat History in Session State
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your HR Policy Assistant. How can I help you today?"}
        ]

    # 3. Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. Handle User Input (Chat Input handles 'Enter' automatically)
    if prompt := st.chat_input("Type your question here..."):
        
        # Add User Message to History & Display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            with st.spinner("Thinking..."):
                try:
                    # Get answer from RAG Engine
                    result = engine.generate_answer(prompt)
                    answer_text = result["answer"]
                    sources = result["sources"]

                    # Display Answer
                    message_placeholder.markdown(answer_text)

                    # Display Sources (Citations) nicely below the answer
                    if sources:
                        with st.expander("📚 View Sources & Context"):
                            for s in sources:
                                st.markdown(f"**Document:** `{s['doc']}` (Score: {s['score']:.4f})")
                                st.caption(f"_{s['text'].strip()}_")
                                st.divider()
                    
                    # Add Assistant Message (Answer + Sources info) to History
                    # Note: We store only the text answer in history to keep it clean, 
                    # but you could append source info string if you want it persistent.
                    st.session_state.messages.append({"role": "assistant", "content": answer_text})

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()