import os
import streamlit as st
from step05_create_chroma_store import build_and_save_vectorstore
from step06_retrieve_context import load_retriever
from step07_prompting import load_llm, create_rag_chain
 
st.set_page_config(page_title="MIT 15.401 Finance Theory RAG", layout="wide")
st.title("MIT 15.401 Finance Theory QA Assistant")
 
INDEX_PATH = "faiss_index"
PDF_PATH = "df418b972d36cd53ae5c375b8af61e53_MIT15_401F08_lec04.pdf"
 
 
@st.cache_resource
def initialize_rag():
    # Build vectorstore if it does not exist
    if not os.path.exists(INDEX_PATH):
        with st.spinner("Processing document and generating vector index..."):
            build_and_save_vectorstore(PDF_PATH, INDEX_PATH)
 
    retriever = load_retriever(INDEX_PATH, k=4)
    llm = load_llm()
    qa_chain = create_rag_chain(llm, retriever)
    return qa_chain
 
 
def format_source_pages(source_documents):
    """Turn retrieved chunks' metadata into a human-readable, de-duplicated
    'Source: page N' line so the user can check the answer against the PDF."""
    if not source_documents:
        return None
 
    # PyPDFLoader stores 0-indexed page numbers in metadata["page"]
    pages = sorted({doc.metadata.get("page") for doc in source_documents if doc.metadata.get("page") is not None})
    if not pages:
        return None
 
    human_pages = [p + 1 for p in pages]  # convert to 1-indexed for the reader
    if len(human_pages) == 1:
        return f"📄 Source: page {human_pages[0]}"
    return f"📄 Sources: pages {', '.join(str(p) for p in human_pages)}"
 
 
rag_chain = initialize_rag()
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
# Display previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.caption(msg["sources"])
 
# Handle input
if user_query := st.chat_input("Ask a question about Fixed-Income Securities..."):
 
    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )
 
    with st.chat_message("user"):
        st.markdown(user_query)
 
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
                response = rag_chain.invoke({"question": user_query})
 
                answer = response.get("answer", "No answer returned.")
                sources = format_source_pages(response.get("source_documents"))
 
                st.markdown(answer)
                if sources:
                    st.caption(sources)
 
            except Exception as e:
                st.error(str(e))
                answer = "Error"
                sources = None
 
    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
