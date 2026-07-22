from langchain import hub
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
def load_llm():
    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        max_new_tokens=128,
        do_sample=False,
        return_full_text=False,
    )

    return HuggingFacePipeline(pipeline=pipe)
def create_rag_chain(llm, retriever):
    """Creates a conversational retrieval chain with memory."""
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    chat_qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )
    return chat_qa
