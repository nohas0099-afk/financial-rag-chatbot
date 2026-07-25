import streamlit as st
from components import copy_button


def format_source_pages(source_documents):
    """Unchanged in spirit from the original app.py -- turns retrieved
    chunk metadata into a human-readable 'Source: page N' string."""
    if not source_documents:
        return None
    pages = sorted(
        {doc.metadata.get("page") for doc in source_documents if doc.metadata.get("page") is not None}
    )
    if not pages:
        return None
    human_pages = [p + 1 for p in pages]
    if len(human_pages) == 1:
        return f"Source: page {human_pages[0]}"
    return f"Sources: pages {', '.join(str(p) for p in human_pages)}"


def render_message(role: str, content: str, sources: str = None, msg_index: int = 0):
    if role == "user":
        st.markdown(
            f"""<div class="msg-row msg-row--user fade-in">
                <div class="bubble-user">{content}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        source_html = f'<div class="source-chip">📎 {sources}</div>' if sources else ""
        st.markdown(
            f"""<div class="msg-row msg-row--assistant fade-in">
                <div class="bubble-assistant">{content}{source_html}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        copy_button(content, key=f"copy_{msg_index}")


def render_loading():
    placeholder = st.empty()
    placeholder.markdown(
        """<div class="msg-row msg-row--assistant">
            <div class="bubble-assistant">
                Thinking
                <div class="loading-dots"><span></span><span></span><span></span></div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )
    return placeholder
