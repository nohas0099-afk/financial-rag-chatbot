from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """Loads Hugging Face Sentence Transformers embeddings."""
    model_path = "sentence-transformers/all-MiniLM-L6-v2"

    model_kwargs = {
        "device": "cpu"
    }

    encode_kwargs = {
        "normalize_embeddings": False
    }

    embeddings = HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )

    return embeddings
