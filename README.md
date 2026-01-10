#  Company Policy Chatbot (Google Gemini RAG)

This is an AI-powered chatbot designed to answer questions about company policies using Retrieval-Augmented Generation (RAG). It uses Google Gemini as the LLM and Streamlit for the user interface.

##  Features
- Context-Aware Answers: Reads your PDF/Text policy documents to provide accurate answers.
- Source Citations: Shows exactly which document and section the answer came from.
- Interactive UI: Clean, chat-based interface built with Streamlit.
- Google Gemini Integration: Utilizes the power of Gemini Pro for natural language understanding.

## Project Structure

├── data/
│   └── policies/        # Put your Policy PDFs or Text files here
├── app.py               # Main Streamlit application
├── ingest.py            # Script to process documents and create embeddings
├── rag_utils.py         # Helper functions for RAG logic
├── requirements.txt     # List of python dependencies
├── .env                 # API Key configuration file
└── README.md            # Project documentation