import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory


def load_llm():
    token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

    llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    huggingfacehub_api_token=token,
    task="text-generation",
    temperature=0.1,
    max_new_tokens=128,
)

print("HF Token loaded:", token[:10])

return llm


def create_rag_chain(llm, retriever):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True,
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
    )
