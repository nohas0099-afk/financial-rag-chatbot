from langchain_huggingface import HuggingFacePipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from transformers import pipeline
 
 
def load_llm():
    # Runs entirely on-device (CPU) -- no Hugging Face Inference Providers,
    # no API token billing, no "402 Payment Required", no "model not
    # supported by provider" errors. Trade-off: answer quality is lower
    # than a 7B+ hosted model since flan-t5-small is only ~80M parameters.
    #
    # If your deployment has more RAM headroom, try "google/flan-t5-base"
    # (~250M params, noticeably better answers) by changing the model
    # name below.
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        max_new_tokens=256,
    )
    return HuggingFacePipeline(pipeline=pipe)
 
 
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
