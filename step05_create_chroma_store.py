from langchain_community.vectorstores import FAISS
from step01_documents import load_documents
from step03_chunking import chunk_documents
from step04_vector_representation import get_embedding_model

def build_and_save_vectorstore(pdf_path: str, save_path: str):
    """Loads, chunks, embeds, and saves FAISS vector index locally."""
    data = load_documents(pdf_path)
    splits = chunk_documents(data)
    hf_embeddings = get_embedding_model()
    
    vectorstore = FAISS.from_documents(splits, hf_embeddings)
    vectorstore.save_local(save_path)
    print(f"Vector store saved successfully at '{save_path}'")
    return vectorstore

if __name__ == "__main__":
    build_and_save_vectorstore("/content/df418b972d36cd53ae5c375b8af61e53_MIT15_401F08_lec04.pdf", "faiss_index")
