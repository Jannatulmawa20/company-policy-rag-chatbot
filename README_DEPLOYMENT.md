# Deployment Guide

## Option 1: Deploy to Streamlit Cloud

### Prerequisites:
- GitHub account (code already on GitHub)
- Streamlit Cloud account

### Steps:
1. **Sign in to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign in with GitHub"

2. **Create new app**
   - Click "Create app"
   - Select repository: `company-policy-rag-chatbot`
   - Select branch: `main`
   - Set main file path: `app.py`

3. **Add Secrets**
   - In the app settings, go to "Secrets"
   - Add your `GEMINI_API_KEY`:
     ```
     GEMINI_API_KEY = "your_api_key_here"
     ```

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at: `https://company-policy-rag-chatbot.streamlit.app`

---

## Option 2: Deploy to Hugging Face Spaces

### Prerequisites:
- Hugging Face account
- Git installed

### Steps:
1. **Create a Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Name: `company-policy-rag-chatbot`
   - License: Select one
   - Space SDK: **Streamlit**
   - Visibility: Public/Private

2. **Clone the Space repo**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/company-policy-rag-chatbot
   cd company-policy-rag-chatbot
   ```

3. **Copy your files**
   ```bash
   cp -r /path/to/your/files/* .
   ```

4. **Push to Hugging Face**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push
   ```

5. **Add Secrets**
   - Go to Space Settings
   - Add Repository Secret:
     - Name: `GEMINI_API_KEY`
     - Value: `your_api_key_here`

6. **Your app is live!**
   - Access at: `https://huggingface.co/spaces/YOUR_USERNAME/company-policy-rag-chatbot`

---

## File Structure Required for Deployment

```
├── app.py
├── config.py
├── ingest.py
├── rag_utils.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── data/
│   └── policies/
│       ├── Conduct & Ethics Policy.txt
│       ├── Human Resource - HR Policy.txt
│       ├── Information & Security Policy.txt
│       ├── leave_policy.txt
│       ├── general_rules.txt
│       └── remote_work_policy.txt
└── models/ (generated after running ingest.py)
    ├── faiss_index.bin
    └── metadata.pkl
```

---

## Important Notes

⚠️ **Before deploying:**
1. Run `python ingest.py` locally to generate FAISS index and metadata
2. Commit `models/` folder to Git (or regenerate on deployment)
3. Add `GEMINI_API_KEY` to Secrets in both platforms
4. Ensure all policy files are in `data/policies/`

💡 **Tips:**
- Both platforms auto-deploy on git push
- Streamlit Cloud is faster to setup
- Hugging Face Spaces is great for community sharing
- You can use both simultaneously!
