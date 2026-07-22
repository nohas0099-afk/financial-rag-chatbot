from langchain_community.vectorstores import FAISS
from step04_vector_representation import get_embedding_model

def load_retriever(store_path: str, k: int = 4):
    """Loads a saved FAISS index and returns a retriever."""
    hf_embeddings = get_embedding_model()
    vectorstore = FAISS.load_local(store_path, hf_embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": k})

if __name__ == "__main__":
    retriever = load_retriever("faiss_index", k=4)
    query = "What is a fixed income security?"
    docs = retriever.get_relevant_documents(query)
    for i, doc in enumerate(docs):
        print(f"--- Document {i+1} ---")
        print(doc.page_content)
