"""
Fixed-Income Securities RAG Chatbot
------------------------------------
A Streamlit app that lets you chat with the MIT 15.401 "Fixed-Income
Securities" lecture (Andrew W. Lo). Built from the original Colab
notebook pipeline (PyPDFLoader -> chunk -> embed -> FAISS -> LLM),
cleaned up and wrapped in a Streamlit UI so it can be deployed for
free on Streamlit Community Cloud straight from GitHub.
"""

import os
import tempfile

import streamlit as st

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Fixed-Income Securities Q&A",
    page_icon="📈",
    layout="wide",
)

DEFAULT_PDF_PATH = os.path.join(os.path.dirname(__file__), "df418b972d36cd53ae5c375b8af61e53_MIT15_401F08_lec04.pdf")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LOCAL_MODELS = {
    "Flan-T5 Small (fast, low RAM)": "google/flan-t5-small",
    "Flan-T5 Base (better quality)": "google/flan-t5-base",
    "TinyLlama-1.1B-Chat (heavier)": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
}

# ----------------------------------------------------------------------
# Cached pipeline pieces
# ----------------------------------------------------------------------


@st.cache_resource(show_spinner=False)
def load_embedder():
    from langchain_community.embeddings import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
    )


@st.cache_resource(show_spinner=False)
def build_vectorstore(pdf_bytes: bytes, chunk_size: int, chunk_overlap: int):
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # PyPDFLoader needs a real file path
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", ".", "\n", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    embedder = load_embedder()
    vectorstore = FAISS.from_documents(chunks, embedder)

    os.remove(tmp_path)
    return vectorstore, len(chunks)


@st.cache_resource(show_spinner=False)
def load_llm(model_id: str, max_new_tokens: int, temperature: float):
    import torch
    from langchain_community.llms import HuggingFacePipeline
    from transformers import AutoTokenizer, pipeline

    is_seq2seq = "t5" in model_id.lower() or "flan" in model_id.lower()

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    if is_seq2seq:
        from transformers import AutoModelForSeq2SeqLM

        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
        task = "text2text-generation"
    else:
        from transformers import AutoModelForCausalLM

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        )
        task = "text-generation"

    pipe = pipeline(
        task,
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        temperature=max(temperature, 0.01),
        do_sample=temperature > 0,
        
    )
    return HuggingFacePipeline(pipeline=pipe)


@st.cache_resource(show_spinner=False)
def build_qa_chain(_vectorstore, _llm, k: int):
    from langchain.chains import RetrievalQA

    retriever = _vectorstore.as_retriever(search_kwargs={"k": k})
    chain = RetrievalQA.from_chain_type(
        llm=_llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
    )
    return chain


# ----------------------------------------------------------------------
# Sidebar controls
# ----------------------------------------------------------------------
st.sidebar.title("⚙️ Settings")

uploaded_pdf = st.sidebar.file_uploader(
    "Use your own PDF (optional)", type=["pdf"], help="Defaults to the bundled MIT 15.401 lecture on fixed-income securities."
)

model_label = st.sidebar.selectbox("Model", list(LOCAL_MODELS.keys()), index=0)
model_id = LOCAL_MODELS[model_label]

top_k = st.sidebar.slider("Chunks retrieved (k)", min_value=1, max_value=8, value=4)
chunk_size = st.sidebar.slider("Chunk size", 200, 1000, 500, step=50)
chunk_overlap = st.sidebar.slider("Chunk overlap", 0, 300, 100, step=25)
max_new_tokens = st.sidebar.slider("Max answer tokens", 32, 512, 128, step=32)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.1, step=0.05)

st.sidebar.markdown("---")
st.sidebar.caption(
    "First run downloads the embedding + language models, so it can take "
    "a minute. Subsequent questions are fast thanks to caching."
)

# ----------------------------------------------------------------------
# Main layout
# ----------------------------------------------------------------------
st.title("📈 Fixed-Income Securities — Chat with the Lecture")
st.write(
    "Ask questions about bond valuation, duration, term structure, credit "
    "risk, and the sub-prime crisis, grounded in MIT 15.401 Lecture 4–6 "
    "(Andrew W. Lo)."
)

if uploaded_pdf is not None:
    pdf_bytes = uploaded_pdf.read()
    source_label = uploaded_pdf.name
else:
    with open(DEFAULT_PDF_PATH, "rb") as f:
        pdf_bytes = f.read()
    source_label = "MIT15_401F08_lec04.pdf (bundled)"

st.caption(f"📄 Source document: **{source_label}**")

with st.spinner("Indexing document..."):
    vectorstore, n_chunks = build_vectorstore(pdf_bytes, chunk_size, chunk_overlap)
st.caption(f"Indexed into {n_chunks} chunks using `{EMBED_MODEL}`.")

with st.spinner(f"Loading model `{model_id}` (first time only)..."):
    llm = load_llm(model_id, max_new_tokens, temperature)

qa_chain = build_qa_chain(vectorstore, llm, top_k)

# ----------------------------------------------------------------------
# Chat history
# ----------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources"):
                for i, src in enumerate(msg["sources"]):
                    st.markdown(f"**Source {i+1} — Page {src['page']}**")
                    st.text(src["snippet"])

sample_questions = [
    "What is Macaulay Duration?",
    "How do you value a coupon bond?",
    "What is the expectations hypothesis?",
    "What caused the sub-prime crisis?",
]
cols = st.columns(len(sample_questions))
clicked_question = None
for col, q in zip(cols, sample_questions):
    if col.button(q, use_container_width=True):
        clicked_question = q

user_input = st.chat_input("Ask a question about fixed-income securities...")
question = clicked_question or user_input

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = qa_chain.invoke({"query": question})
            answer = result["result"].strip()
            sources = []
            for doc in result.get("source_documents", []):
                page = doc.metadata.get("page", "unknown")
                page = page + 1 if isinstance(page, int) else page
                sources.append({"page": page, "snippet": doc.page_content[:300]})

        st.markdown(answer)
        if sources:
            with st.expander("Sources"):
                for i, src in enumerate(sources):
                    st.markdown(f"**Source {i+1} — Page {src['page']}**")
                    st.text(src["snippet"])

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )

if st.session_state.messages:
    if st.sidebar.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()
