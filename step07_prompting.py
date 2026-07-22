from langchain import hub
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

def load_llm():
    """Loads quantized language model using Hugging Face Pipeline."""
    model_id = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        
    )
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=1024
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
