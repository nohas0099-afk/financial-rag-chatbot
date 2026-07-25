"""
All CSS for the app lives here as a single injected block. Nothing in
here touches the RAG pipeline -- purely presentational.
"""
import streamlit as st

THEME_CSS = """
<style>
:root {
    /* Palette derived from the exact image tone */
    --bg-primary: #3d3b32;
    --bg-secondary: #2f2d26;

    --glass-bg: #403e35;
    --glass-border: #635f52;

    --emerald: #a39b83;
    --navy: #2d2b24;

    --text-primary: #FFFFFF;
    --text-secondary: #c9c3b1;

    --radius: 16px;
}

/* ---------- Streamlit chrome cleanup ---------- */
#MainMenu, header, footer {visibility: hidden; height: 0;}
[data-testid="stToolbar"] {display: none;}
.block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px;}

/* ---------- Main Background ---------- */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #48453a 0%,
        #3d3b32 50%,
        #302e27 100%
    ) !important;
}

/* ---------- Sidebar Background & Border ---------- */
[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #2a2922 0%,
        #201f1a 100%
    ) !important;
    border-right: 1px solid #48453a !important;
}

/* ---------- General Typography ---------- */
html,
body,
[class*="css"],
p,
span,
label,
div,
small,
h1,
h2,
h3,
h4,
h5,
h6 {
    color: #FFFFFF !important;
    font-family: "Inter", "Segoe UI", sans-serif;
}

/* ---------- Animations ---------- */
@keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
@keyframes slideUp { from {opacity: 0; transform: translateY(14px);} to {opacity: 1; transform: translateY(0);} }
@keyframes glow { 0%,100% {box-shadow: 0 0 0px rgba(163,155,131,0);} 50% {box-shadow: 0 0 18px rgba(163,155,131,0.35);} }
@keyframes blink { 0%,100% {opacity: 0.2;} 50% {opacity: 1;} }
.fade-in { animation: fadeIn 0.4s ease both; }
.slide-up { animation: slideUp 0.45s cubic-bezier(.2,.8,.2,1) both; }

/* ---------- Glass card base ---------- */
.glass-card {
    background: #38362e !important;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid #545144 !important;
    border-radius: var(--radius);
    padding: 18px 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35);
}

/* ---------- Dashboard hero ---------- */
.hero { text-align: center; padding: 2.5rem 0 1.5rem 0; }
.hero h1 {
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #FFFFFF;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}
.hero p {
    color: #e3decb;
    font-size: 1.02rem;
    max-width: 620px;
    margin: 0 auto;
}

/* ---------- Suggestion cards ---------- */
.suggestion-card {
    background: #38362e;
    border: 1px solid #545144;
    border-radius: var(--radius);
    padding: 18px;
    height: 100%;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}
.suggestion-card:hover {
    transform: translateY(-4px);
    border-color: #8c836d;
    box-shadow: 0 8px 28px rgba(0,0,0,0.3);
}
.suggestion-card__icon { font-size: 1.4rem; }
.suggestion-card__title {
    font-weight: 600;
    margin-top: 6px;
    color: #FFFFFF;
}

/* ---------- Status bar / sidebar footer ---------- */
.status-row { display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0 18px 0; }
.status-chip {
    flex: 1; min-width: 130px;
    background: #2a2922; border: 1px solid #48453a;
    border-radius: 12px; padding: 10px 12px;
}
.status-chip__label { font-size: 0.72rem; color: #a39b83; text-transform: uppercase; letter-spacing: 0.04em; }
.status-chip__value { font-size: 0.92rem; font-weight: 600; margin-top: 2px; color: #FFFFFF; }

/* ---------- Chat bubbles ---------- */
.msg-row { display: flex; margin: 10px 0; }
.msg-row--user { justify-content: flex-end; }
.msg-row--assistant { justify-content: flex-start; }
.bubble-user {
    background: #25241e;
    color: white; border-radius: 18px 18px 4px 18px;
    padding: 12px 16px; max-width: 75%;
    border: 1px solid #48453a;
}
.bubble-assistant {
    background: #38362e; border: 1px solid #545144;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px; max-width: 80%; backdrop-filter: blur(10px);
}
.source-chip {
    display: inline-block; margin-top: 8px; font-size: 0.78rem;
    color: #d1c9b4; background: rgba(163,155,131,0.15);
    border: 1px solid rgba(163,155,131,0.3); border-radius: 999px; padding: 3px 10px;
}

/* ---------- Loading dots ---------- */
.loading-dots { display: inline-flex; gap: 4px; margin-top: 6px; }
.loading-dots span {
    width: 6px; height: 6px; border-radius: 50%; background: #a39b83;
    animation: blink 1.2s infinite;
}
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

/* ---------- Upload ---------- */
.upload-card {
    border: 1px solid #545144; background: #2a2922;
    border-radius: 12px; padding: 10px 14px; margin-bottom: 8px;
}
.upload-card--success { border-color: #8c836d; }
.upload-card--error { border-color: rgba(239,68,68,0.4); }
.upload-card__name { font-weight: 600; font-size: 0.9rem; }
.upload-card__meta { font-size: 0.78rem; color: #a39b83; margin-top: 2px; }
.upload-format-row { display: flex; gap: 6px; margin: 6px 0 14px 0; }
.format-chip {
    font-size: 0.72rem; padding: 3px 9px; border-radius: 999px;
    border: 1px solid #48453a; color: #a39b83;
}
.format-chip--active { color: #FFFFFF; border-color: #8c836d; }

/* ---------- Sidebar sections ---------- */
.sidebar-brand { display: flex; align-items: center; gap: 12px; padding: 6px 0 16px 0; }
.sidebar-brand__logo {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, #545144, #2a2922);
    display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
    border: 1px solid #635f52;
}
.sidebar-brand__name { 
    font-weight: 700; 
    font-size: 1.25rem !important;
    line-height: 1.2; 
}
.sidebar-brand__tag {
    font-size: 0.85rem !important;
    color: #c9c3b1;
}
.sidebar-section-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #a39b83;
    margin: 14px 0 6px 2px;
}
.doc-item {
    display: flex; justify-content: space-between; font-size: 0.82rem;
    padding: 6px 8px; border-radius: 8px; margin-bottom: 4px;
    background: rgba(255,255,255,0.03);
    border: 1px solid #38362e;
}
.doc-item__pages {
    color: #a39b83;
}

/* ---------- Streamlit Buttons ---------- */
.stButton > button {
    background: #38362e !important;
    color: #FFFFFF !important;
    border: 1px solid #545144 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background: #48453a !important;
    border-color: #736d5e !important;
    color: #FFFFFF !important;
}

/* ---------- File Uploader & Browse Button Fix ---------- */
[data-testid="stFileUploader"],
[data-testid="stFileUploaderDropzone"]{
    background: #2a2922 !important;
    border: 2px dashed #545144 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] *{
    color: #e3decb !important;
}

/* زر Browse files */
[data-testid="stFileUploader"] button {
    background-color: #38362e !important;
    color: #FFFFFF !important;
    border: 1px solid #545144 !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] button:hover {
    background-color: #48453a !important;
    border-color: #736d5e !important;
}

/* ---------- Chat Area ---------- */
[data-testid="stBottom"] {
    background: #302e27 !important;
}

[data-testid="stChatInput"] {
    background: #302e27 !important;
    border-top: none !important;
}

/* مربع الكتابة */
[data-testid="stChatInput"] textarea {
    background: #23221c !important;
    color: #FFFFFF !important;
    border: 1px solid #545144 !important;
}

/* زر الإرسال */
[data-testid="stChatInput"] button {
    background: #38362e !important;
    color: white !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

.main .block-container {
    background: transparent !important;
}

div.st-emotion-cache-qdbtli {
    background: #302e27 !important;
}
</style>
"""

def inject_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)
