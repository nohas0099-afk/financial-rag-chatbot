import streamlit as st
from helpers import load_indexed_files
from upload import render_upload_widget, INDEX_PATH


def render_sidebar(on_index_updated):
    with st.sidebar:
        st.markdown(
            """<div class="sidebar-brand">
                <div class="sidebar-brand__logo">📈</div>
                <div>
                    <div class="sidebar-brand__name">Finance Theory</div>
                    <div class="sidebar-brand__tag">AI Assistant</div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

        if st.button("＋ New chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_session += 1
            st.rerun()

        st.markdown('<div class="sidebar-section-title">Add course material</div>', unsafe_allow_html=True)
        render_upload_widget(on_success=on_index_updated)

        st.markdown('<div class="sidebar-section-title">Document library</div>', unsafe_allow_html=True)
        indexed = load_indexed_files()
        if not indexed:
            st.caption("No documents indexed yet.")
        else:
            for f in indexed:
                st.markdown(
                    f"""<div class="doc-item">
                        <span>📄 {f['name']}</span>
                        <span class="doc-item__pages">{f['pages']}p</span>
                    </div>""",
                    unsafe_allow_html=True,
                )

        with st.expander("Chat history"):
            if len(st.session_state.messages) == 0:
                st.caption("Nothing yet this session.")
            else:
                for m in st.session_state.messages:
                    if m["role"] == "user":
                        st.caption(f"• {m['content'][:60]}")

        with st.expander("Settings"):
            st.caption("Model and index paths are fixed to the configured backend.")

        with st.expander("About"):
            st.caption(
                "A Retrieval-Augmented Generation assistant for MIT 15.401 Finance "
                "Theory -- ask about bonds, fixed-income securities, credit risk, "
                "duration, yield curves, and the 2008 financial crisis. Runs fully "
                "on local, open-source models."
            )

        st.markdown("---")
        num_docs = len(load_indexed_files())
        import os
        vector_status = "Ready" if os.path.exists(INDEX_PATH) else "Empty"
        st.markdown(
            f"""
            <div class="status-row" style="flex-direction:column;">
                <div class="status-chip"><div class="status-chip__label">LLM</div>
                    <div class="status-chip__value">FLAN-T5-Base (Local)</div></div>
                <div class="status-chip"><div class="status-chip__label">Embedding model</div>
                    <div class="status-chip__value">all-MiniLM-L6-v2</div></div>
                <div class="status-chip"><div class="status-chip__label">Vector store</div>
                    <div class="status-chip__value">FAISS · {vector_status}</div></div>
                <div class="status-chip"><div class="status-chip__label">Indexed documents</div>
                    <div class="status-chip__value">{num_docs}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
