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

rag_chain = initialize_rag()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle input
if user_query := st.chat_input("Ask a question about Fixed-Income Securities..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
    response = rag_chain.invoke({"question": user_query})

    st.write(response)   # مؤقتًا لمعرفة ماذا يرجع الـ RAG

    answer = response.get("answer", "No answer returned.")
    st.markdown(answer)

except Exception as e:
    st.error(str(e))
            
    st.session_state.messages.append({"role": "assistant", "content": answer})
