"""
Financial RAG Assistant -- UI orchestration layer.

This file wires together the frontend modules (styles, sidebar,
dashboard, chat, upload) with the unmodified backend pipeline
(step01-step07). It does not implement any retrieval, chunking,
embedding, or generation logic itself -- it only calls into step06
(load_retriever) and step07 (load_llm, create_rag_chain), exactly as
the original app.py did.
"""
import os
import streamlit as st

from styles import inject_theme
from sidebar import render_sidebar
from dashboard import render_dashboard
from chat import render_message, render_loading, format_source_pages
from upload import INDEX_PATH, bootstrap_default_document
from step06_retrieve_context import load_retriever
from step07_prompting import load_llm, create_rag_chain

st.set_page_config(page_title="Financial AI Assistant", layout="wide", page_icon="📈")
inject_theme()

# ---------------------------------------------------------------- state ----
for key, default in {
    "messages": [],
    "index_version": 0,
    "chat_session": 0,
    "pending_prompt": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def _on_index_updated():
    st.session_state.index_version += 1
    st.rerun()


# ------------------------------------------------------------ backend ------
@st.cache_resource(show_spinner=False)
def get_llm():
    return load_llm()  # step07, unchanged


@st.cache_resource(show_spinner=False)
def get_qa_chain(_llm, index_version: int, chat_session: int):
    # Re-runs only when the index changes or "New chat" is clicked --
    # otherwise Streamlit reuses the cached chain (and its memory)
    # across every rerun, same as the original app.py's initialize_rag().
    retriever = load_retriever(INDEX_PATH, k=4)  # step06, unchanged
    return create_rag_chain(_llm, retriever)  # step07, unchanged


llm = get_llm()

# ------------------------------------------------------------- sidebar -----
render_sidebar(on_index_updated=_on_index_updated)

# --------------------------------------------------------------- main ------
bootstrap_default_document()  # auto-indexes ./default_docs/*.pdf on first run, if present
index_ready = os.path.exists(INDEX_PATH)

if not index_ready:
    st.markdown(
        """<div class="hero slide-up">
            <h1>Finance Theory AI Assistant</h1>
            <p>No course material indexed yet. Add the MIT Finance Theory lecture PDF to
            <code>default_docs/</code>, or upload a PDF from the sidebar, to get started.</p>
        </div>""",
        unsafe_allow_html=True,
    )
    st.stop()

qa_chain = get_qa_chain(llm, st.session_state.index_version, st.session_state.chat_session)

if len(st.session_state.messages) == 0 and st.session_state.pending_prompt is None:
    render_dashboard()

for i, msg in enumerate(st.session_state.messages):
    render_message(msg["role"], msg["content"], msg.get("sources"), msg_index=i)

user_query = st.chat_input("Ask anything about your financial documents...")
if st.session_state.pending_prompt:
    user_query = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    render_message("user", user_query)

    loading_placeholder = render_loading()
    try:
        response = qa_chain.invoke({"question": user_query})
        answer = response.get("answer", "No answer returned.")
        sources = format_source_pages(response.get("source_documents"))
    except Exception as e:
        answer = f"Something went wrong generating a response: {e}"
        sources = None
    loading_placeholder.empty()

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
    render_message("assistant", answer, sources, msg_index=len(st.session_state.messages) - 1)
