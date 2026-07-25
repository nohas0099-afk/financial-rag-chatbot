"""Small reusable UI pieces shared by sidebar / dashboard / chat."""
import streamlit as st
import streamlit.components.v1 as components


def status_row(items: list[tuple[str, str]]):
    """items: list of (label, value) pairs rendered as glass chips."""
    chips = "".join(
        f"""<div class="status-chip">
                <div class="status-chip__label">{label}</div>
                <div class="status-chip__value">{value}</div>
            </div>"""
        for label, value in items
    )
    st.markdown(f'<div class="status-row">{chips}</div>', unsafe_allow_html=True)


def copy_button(text: str, key: str):
    """A tiny self-contained HTML/JS copy-to-clipboard button (runs in an
    iframe via components.html so the JS reliably executes)."""
    safe_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("</", "<\\/")
    components.html(
        f"""
        <style>
            body {{ margin:0; }}
            .copy-btn {{
                font-family: Inter, sans-serif; font-size: 11px; cursor: pointer;
                background: rgba(255,255,255,0.06); color: #9CA3AF;
                border: 1px solid rgba(255,255,255,0.1); border-radius: 999px;
                padding: 3px 10px; transition: color 0.15s ease;
            }}
            .copy-btn:hover {{ color: #10B981; border-color: rgba(16,185,129,0.4); }}
        </style>
        <button class="copy-btn" onclick="
            navigator.clipboard.writeText(`{safe_text}`);
            this.innerText='Copied ✓';
            setTimeout(() => this.innerText='Copy', 1200);
        ">Copy</button>
        """,
        height=28,
    )
