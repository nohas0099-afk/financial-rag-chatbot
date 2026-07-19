# 📈 Fixed-Income Securities — RAG Chatbot

A Streamlit app that lets you chat with MIT 15.401 *Finance Theory*,
Lectures 4–6: **Fixed-Income Securities** (Andrew W. Lo), using a
Retrieval-Augmented Generation (RAG) pipeline:

`PDF → chunk → embed (MiniLM) → FAISS vector store → local LLM (Flan-T5 / TinyLlama) → answer + cited sources`

This is a cleaned-up, Streamlit-ified version of the original Colab/Jupyter
notebook pipeline (LangChain `RetrievalQA` over a `FAISS` index).

## Features

- 📄 Comes with the lecture PDF bundled in `data/lecture.pdf`; you can also
  upload your own PDF from the sidebar.
- 🔎 Adjustable chunking (`chunk_size`, `chunk_overlap`) and retrieval depth (`k`).
- 🤖 Choice of local, no-API-key-needed models (Flan-T5-small/base or TinyLlama).
- 💬 Chat interface with conversation history and expandable source citations
  (page number + snippet) for every answer.
- ⚡ Cached embeddings/index/model so repeated questions are fast.

## Run locally

```bash
git clone <your-repo-url>
cd fixed-income-rag
python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
streamlit run app.py
```

The first question will take a minute or two while the embedding model and
the LLM are downloaded from Hugging Face — after that, everything is cached.

## Deploy for free on Streamlit Community Cloud

1. **Push this folder to GitHub.**
   ```bash
   cd fixed-income-rag
   git init
   git add .
   git commit -m "Fixed-income RAG chatbot"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
3. Click **New app**, pick your repo/branch, and set the main file to `app.py`.
4. Click **Deploy**. Streamlit Cloud will install `requirements.txt` and launch the app.

> **Note on resources:** Streamlit Community Cloud's free tier has limited
> CPU/RAM. `Flan-T5 Small` is the safest default for that tier. `TinyLlama`
> and `Flan-T5 Base` work but may be slow on the first load since the model
> weights need to download and run on CPU.

## Project structure

```
fixed-income-rag/
├── app.py              # Streamlit app (RAG pipeline + chat UI)
├── requirements.txt    # Pinned dependencies for reproducible deploys
├── data/
│   └── lecture.pdf      # Bundled MIT 15.401 lecture (fixed-income securities)
└── README.md
```

## Credits

Lecture material: *15.401 Finance Theory I*, MIT OpenCourseWare, Fall 2008,
Andrew W. Lo. © 2007–2008 Andrew W. Lo. Licensed under a Creative Commons
license via MIT OpenCourseWare (http://ocw.mit.edu). Used here for
educational, non-commercial purposes.
