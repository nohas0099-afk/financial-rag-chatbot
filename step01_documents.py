from langchain_community.document_loaders import PyPDFLoader

def load_documents(file_path: str):
    """Loads a PDF document using PyPDFLoader."""
    loader = PyPDFLoader(file_path)
    data = loader.load()
    print(f"Loaded {len(data)} pages from {file_path}")
    return data

if __name__ == "__main__":
    # Test loading document
    pdf_path = "/content/df418b972d36cd53ae5c375b8af61e53_MIT15_401F08_lec04.pdf"
    data = load_documents(pdf_path)
