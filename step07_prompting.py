from langchain_huggingface import HuggingFacePipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from transformers import pipeline
 
 
QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful teaching assistant for an MIT finance course. "
        "Use ONLY the context below to answer the question. "
        "Write your answer as one or two complete, well-formed sentences in "
        "your own words. Do not just copy a fragment or list marker from the "
        "context. If the context does not contain the answer, respond with: "
        "\"The document does not contain enough information to answer that.\"\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer in a full sentence:"
    ),
)
 
 
def load_llm():
    # Runs entirely on-device (CPU) -- no Hugging Face Inference Providers,
    # no API token billing, no "402 Payment Required", no "model not
    # supported by provider" errors.
    #
    # flan-t5-base (~250M params) gives noticeably better, more coherent
    # answers than flan-t5-small (~80M) while still running fine on CPU.
    # If you hit an out-of-memory crash on deployment, drop back to
    # "google/flan-t5-small".
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=256,
        min_new_tokens=16,     # discourage one-word/fragment answers
        num_beams=4,           # beam search instead of greedy decoding = more coherent output
        repetition_penalty=1.3,
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
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True,
    )
 
