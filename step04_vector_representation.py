from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    """Loads Hugging Face Sentence Transformers embeddings."""
    model_path = "sentence-transformers/all-MiniLM-l6-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    hf = HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return hf
