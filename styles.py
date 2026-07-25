"""
All CSS for the app lives here as a single injected block. Nothing in
here touches the RAG pipeline -- purely presentational.
"""
import streamlit as st

THEME_CSS = """
<style>
:root {
    --bg-primary: #0B1220;
    --bg-secondary: #111827;
    --glass-bg: rgba(17, 24, 39, 0.55);
    --glass-border: #374151;
    --emerald: #10B981;
    --navy: #1E3A8A;
    --text-primary: #FFFFFF;
    --text-secondary: #9CA3AF;
    --radius: 16px;
}

/* ---------- Streamlit chrome cleanup ---------- */
#MainMenu, header, footer {visibility: hidden; height: 0;}
[data-testid="stToolbar"] {display: none;}
.block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px;}
[data-testid="stAppViewContainer"] {background: radial-gradient(circle at 20% 0%, #101c34 0%, var(--bg-primary) 55%);}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-secondary) 0%, #0b1220 100%);
    border-right: 1px solid var(--glass-border);
}
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] {
    background: var(--glass-bg) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 999px !important;
}
html, body, [class*="css"] {
    color: var(--text-primary);
    font-family: "Inter", "Segoe UI", sans-serif;
}

/* ---------- Animations ---------- */
@keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
@keyframes slideUp { from {opacity: 0; transform: translateY(14px);} to {opacity: 1; transform: translateY(0);} }
@keyframes glow { 0%,100% {box-shadow: 0 0 0px rgba(16,185,129,0);} 50% {box-shadow: 0 0 18px rgba(16,185,129,0.35);} }
@keyframes blink { 0%,100% {opacity: 0.2;} 50% {opacity: 1;} }
.fade-in { animation: fadeIn 0.4s ease both; }
.slide-up { animation: slideUp 0.45s cubic-bezier(.2,.8,.2,1) both; }

/* ---------- Glass card base ---------- */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 18px 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
}

/* ---------- Dashboard hero ---------- */
.hero { text-align: center; padding: 2.5rem 0 1.5rem 0; }
.hero h1 {
    font-size: 2.4rem; font-weight: 700; margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #E5E7EB, var(--emerald) 55%, var(--navy));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p { color: var(--text-secondary); font-size: 1.02rem; max-width: 620px; margin: 0 auto; }

/* ---------- Suggestion cards ---------- */
.suggestion-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 18px;
    height: 100%;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}
.suggestion-card:hover {
    transform: translateY(-4px);
    border-color: rgba(16,185,129,0.45);
    box-shadow: 0 8px 28px rgba(16,185,129,0.12);
}
.suggestion-card__icon { font-size: 1.4rem; }
.suggestion-card__title { font-weight: 600; margin-top: 6px; }

/* ---------- Status bar / sidebar footer ---------- */
.status-row { display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0 18px 0; }
.status-chip {
    flex: 1; min-width: 130px;
    background: var(--glass-bg); border: 1px solid var(--glass-border);
    border-radius: 12px; padding: 10px 12px;
}
.status-chip__label { font-size: 0.72rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em; }
.status-chip__value { font-size: 0.92rem; font-weight: 600; margin-top: 2px; color: var(--emerald); }

/* ---------- Chat bubbles ---------- */
.msg-row { display: flex; margin: 10px 0; }
.msg-row--user { justify-content: flex-end; }
.msg-row--assistant { justify-content: flex-start; }
.bubble-user {
    background: linear-gradient(135deg, var(--navy), #16296b);
    color: white; border-radius: 18px 18px 4px 18px;
    padding: 12px 16px; max-width: 75%;
}
.bubble-assistant {
    background: var(--glass-bg); border: 1px solid var(--glass-border);
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px; max-width: 80%; backdrop-filter: blur(10px);
}
.source-chip {
    display: inline-block; margin-top: 8px; font-size: 0.78rem;
    color: var(--emerald); background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3); border-radius: 999px; padding: 3px 10px;
}

/* ---------- Loading dots ---------- */
.loading-dots { display: inline-flex; gap: 4px; margin-top: 6px; }
.loading-dots span {
    width: 6px; height: 6px; border-radius: 50%; background: var(--emerald);
    animation: blink 1.2s infinite;
}
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

/* ---------- Upload ---------- */
.upload-card {
    border: 1px solid var(--glass-border); background: var(--glass-bg);
    border-radius: 12px; padding: 10px 14px; margin-bottom: 8px;
}
.upload-card--success { border-color: rgba(16,185,129,0.4); }
.upload-card--error { border-color: rgba(239,68,68,0.4); }
.upload-card__name { font-weight: 600; font-size: 0.9rem; }
.upload-card__meta { font-size: 0.78rem; color: var(--text-secondary); margin-top: 2px; }
.upload-format-row { display: flex; gap: 6px; margin: 6px 0 14px 0; }
.format-chip {
    font-size: 0.72rem; padding: 3px 9px; border-radius: 999px;
    border: 1px solid var(--glass-border); color: var(--text-secondary);
}
.format-chip--active { color: var(--emerald); border-color: rgba(16,185,129,0.4); }

/* ---------- Sidebar sections ---------- */
.sidebar-brand { display: flex; align-items: center; gap: 10px; padding: 6px 0 16px 0; }
.sidebar-brand__logo {
    width: 34px; height: 34px; border-radius: 10px;
    background: linear-gradient(135deg, var(--emerald), var(--navy));
    display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
}
.sidebar-brand__name { font-weight: 700; font-size: 1.02rem; line-height: 1.1; }
.sidebar-brand__tag { font-size: 0.72rem; color: var(--text-secondary); }
.sidebar-section-title {
    font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--text-secondary); margin: 14px 0 6px 2px;
}
.doc-item {
    display: flex; justify-content: space-between; font-size: 0.82rem;
    padding: 6px 8px; border-radius: 8px; margin-bottom: 4px;
    background: rgba(255,255,255,0.02);
}
.doc-item__pages { color: var(--text-secondary); }
</style>
"""


def inject_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)
