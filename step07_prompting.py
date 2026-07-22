import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
 
 
def load_llm():
    token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
 
    # IMPORTANT:
    # The old "api-inference.huggingface.co" text-generation endpoint used by
    # `task="text-generation"` is Hugging Face's legacy Inference API and is
    # being retired for more and more models — that's what caused the
    # "Failed to resolve 'api-inference.huggingface.co'" error you saw.
    #
    # HF now routes serverless inference through its "Inference Providers"
    # system (router.huggingface.co). langchain-huggingface talks to that
    # automatically if you DON'T pass task="text-generation" and instead
    # wrap the endpoint in ChatHuggingFace, which uses the chat-completions
    # style API.
    #
    # Also: TinyLlama-1.1B-Chat is a small hobby model that is frequently
    # NOT hosted/warm on the free serverless tier, which causes failures on
    # its own even once the URL issue is fixed. Swap in a model you've
    # confirmed is available (see note below).
    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-7B-Instruct",  # swap for any model you've verified works, see note below
        huggingfacehub_api_token=token,
        provider="auto",       # let HF pick a provider that currently serves this model
        temperature=0.1,
        max_new_tokens=256,
    )
 
    chat_model = ChatHuggingFace(llm=llm)
 
    return chat_model
 
 
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
