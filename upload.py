"""
Upload handling.

IMPORTANT: this module does not change the RAG logic at all. It calls
step05.build_and_save_vectorstore() -- completely unmodified -- to turn
each uploaded PDF into its own FAISS index, then merges that index into
the main on-disk store using FAISS.merge_from(), a stock LangChain
FAISS method (the same class step05/step06 already use). No backend
file is edited to make this work.
"""
import os
import shutil
import tempfile

import streamlit as st
from langchain_community.vectorstores import FAISS

from step01_documents import load_documents
from step04_vector_representation import get_embedding_model
from step05_create_chroma_store import build_and_save_vectorstore
from helpers import format_file_size, append_indexed_file

UPLOAD_DIR = "uploaded_docs"
INDEX_PATH = "faiss_index"
DEFAULT_DOCS_DIR = "default_docs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DEFAULT_DOCS_DIR, exist_ok=True)


def bootstrap_default_document():
    """
    On first launch (no FAISS index on disk yet), auto-index whichever
    PDF(s) are placed in DEFAULT_DOCS_DIR -- this is how the MIT Finance
    Theory lecture PDF becomes the assistant's base knowledge source
    without a hardcoded absolute path. Drop the PDF file into
    ./default_docs/ and it is indexed automatically the first time the
    app runs. Uses step05, unchanged. No-op if an index already exists
    or no default PDF is present.
    """
    if os.path.exists(INDEX_PATH):
        return
    pdfs = sorted(f for f in os.listdir(DEFAULT_DOCS_DIR) if f.lower().endswith(".pdf"))
    if not pdfs:
        return

    first_path = os.path.join(DEFAULT_DOCS_DIR, pdfs[0])
    build_and_save_vectorstore(first_path, INDEX_PATH)  # step05, unchanged
    num_pages = len(load_documents(first_path))  # step01, unchanged
    append_indexed_file(pdfs[0], os.path.getsize(first_path), num_pages)

    # merge in any additional default PDFs the same way uploads are merged
    for extra_name in pdfs[1:]:
        extra_path = os.path.join(DEFAULT_DOCS_DIR, extra_name)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_index_path = os.path.join(tmp_dir, "extra_index")
            build_and_save_vectorstore(extra_path, tmp_index_path)
            embeddings = get_embedding_model()
            main_store = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
            new_store = FAISS.load_local(tmp_index_path, embeddings, allow_dangerous_deserialization=True)
            main_store.merge_from(new_store)
            main_store.save_local(INDEX_PATH)
        append_indexed_file(extra_name, os.path.getsize(extra_path), len(load_documents(extra_path)))


def _already_indexed(filename: str) -> bool:
    from helpers import load_indexed_files
    return any(f["name"] == filename for f in load_indexed_files())


def index_uploaded_pdf(uploaded_file) -> int:
    """
    Saves an uploaded PDF, runs it through the existing step01/03/04/05
    pipeline, and merges the result into the main FAISS store at
    INDEX_PATH. Returns the number of pages indexed.
    """
    dest_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(dest_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Use step01 only to report a page count back to the UI -- the actual
    # indexing pipeline (step01 -> step03 -> step04 -> step05) still runs
    # again, unmodified, inside build_and_save_vectorstore.
    num_pages = len(load_documents(dest_path))

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_index_path = os.path.join(tmp_dir, "new_index")
        build_and_save_vectorstore(dest_path, tmp_index_path)  # step05, unchanged

        embeddings = get_embedding_model()  # step04, unchanged
        new_store = FAISS.load_local(
            tmp_index_path, embeddings, allow_dangerous_deserialization=True
        )

        if os.path.exists(INDEX_PATH):
            main_store = FAISS.load_local(
                INDEX_PATH, embeddings, allow_dangerous_deserialization=True
            )
            main_store.merge_from(new_store)
            main_store.save_local(INDEX_PATH)
        else:
            shutil.copytree(tmp_index_path, INDEX_PATH)

    append_indexed_file(uploaded_file.name, uploaded_file.size, num_pages)
    return num_pages


def render_upload_widget(on_success):
    """
    Renders the upload control. `on_success` is called (no args) after a
    new file has been successfully indexed, so the caller can bump its
    cache-busting index_version and rerun.
    """
    uploaded_files = st.file_uploader(
        "Add finance theory course material",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="Add extra lecture notes or readings as PDF. DOCX / TXT support is planned.",
        key="pdf_uploader",
    )

    st.markdown(
        """<div class="upload-format-row">
            <span class="format-chip format-chip--active">PDF</span>
            <span class="format-chip">DOCX · soon</span>
            <span class="format-chip">TXT · soon</span>
        </div>""",
        unsafe_allow_html=True,
    )

    if not uploaded_files:
        return

    new_files = [f for f in uploaded_files if not _already_indexed(f.name)]
    if not new_files:
        return

    for uploaded_file in new_files:
        card = st.empty()
        card.markdown(
            f"""<div class="upload-card fade-in">
                <div class="upload-card__name">📄 {uploaded_file.name}</div>
                <div class="upload-card__meta">{format_file_size(uploaded_file.size)} · Processing…</div>
                <div class="loading-dots"><span></span><span></span><span></span></div>
            </div>""",
            unsafe_allow_html=True,
        )
        try:
            num_pages = index_uploaded_pdf(uploaded_file)
            card.markdown(
                f"""<div class="upload-card upload-card--success fade-in">
                    <div class="upload-card__name">✅ {uploaded_file.name}</div>
                    <div class="upload-card__meta">{format_file_size(uploaded_file.size)} · {num_pages} pages ·
                    embedded &amp; indexed</div>
                </div>""",
                unsafe_allow_html=True,
            )
        except Exception as e:
            card.markdown(
                f"""<div class="upload-card upload-card--error fade-in">
                    <div class="upload-card__name">⚠ {uploaded_file.name}</div>
                    <div class="upload-card__meta">Failed to index: {e}</div>
                </div>""",
                unsafe_allow_html=True,
            )

    on_success()
