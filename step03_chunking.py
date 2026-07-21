from langchain_text_splitters import RecursiveCharacterTextSplitter
from step01_documents import load_documents

def chunk_documents(data):
    """Splits loaded documents into smaller chunks for vectorization."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", ".", "\n", " ", ""]
    )
    all_splits = text_splitter.split_documents(data)
    print(f"Total chunks created: {len(all_splits)}")
    return all_splits

if __name__ == "__main__":
    data = load_documents("/content/df418b972d36cd53ae5c375b8af61e53_MIT15_401F08_lec04.pdf")
    splits = chunk_documents(data)
