THEME_CSS = """
<style>
:root {
    --bg-primary: #6F4E37;
    --bg-secondary: #8B6B5C;

    --glass-bg: #8B6B5C;
    --glass-border: #C2A38F;

    --emerald: #DCC2A8;
    --navy: #8B6B5C;

    --text-primary: #FFFFFF;
    --text-secondary: #F8F5F2;

    --radius: 16px;
}
/* ---------- Streamlit chrome cleanup ---------- */
#MainMenu, header, footer {visibility: hidden; height: 0;}
[data-testid="stToolbar"] {display: none;}
.block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px;}
[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #6F4E37 0%,
        #8B6B5C 50%,
        #A67C6B 100%
    );
}
[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #6F4E37,
        #8B6B5C
    );
    border-right: 1px solid #C2A38F;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"]{
    background:rgba(74,44,42,.95)!important;
    color:#FFFFFF!important;
    border:2px solid #B76E79!important;
    border-radius:999px!important;
}
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
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #FFFFFF;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
}
.hero p {
    color: #FFFFFF;
    font-size: 1.02rem;
    max-width: 620px;
    margin: 0 auto;
}
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
.suggestion-card__title {
    font-weight: 600;
    margin-top: 6px;
    color: #FFFFFF;
}
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
.sidebar-brand { display: flex; align-items: center; gap: 12px; padding: 6px 0 16px 0; }
.sidebar-brand__logo {
    width: 42px; height: 42px; border-radius: 10px;
    background: linear-gradient(135deg, var(--emerald), var(--navy));
    display: flex; align-items: center; justify-content: center; font-size: 1.3rem;
}
.sidebar-brand__name { 
    font-weight: 700; 
    font-size: 1.4rem !important; /* تكبير الخط هنا */
    line-height: 1.2; 
}
.sidebar-brand__tag {
    font-size: 0.95rem !important; /* تكبير الخط الفرعي هنا */
    color: #FFFFFF;
}
.sidebar-section-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #FFFFFF;
    margin: 14px 0 6px 2px;
}
.doc-item {
    display: flex; justify-content: space-between; font-size: 0.82rem;
    padding: 6px 8px; border-radius: 8px; margin-bottom: 4px;
    background: rgba(255,255,255,0.02);
}
.doc-item__pages {
    color: #FFFFFF;
}
/* ---------- Streamlit Buttons ---------- */
.stButton > button {
    background: #6D4C41 !important;
    color: #FFFFFF !important;
    border: 1px solid #A1887F !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background: #7B564B !important;
    color: #FFFFFF !important;
}

/* ---------- File Uploader ---------- */
[data-testid="stFileUploader"],
[data-testid="stFileUploaderDropzone"]{
    background: #8B6B5C !important;
    border: 2px dashed #DCC2A8 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] *{
    color: white !important;
}

[data-testid="stFileUploader"] button {
    background-color: #6D4C41 !important;
    color: #FFFFFF !important;
    border: 1px solid #C2A38F !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] button:hover {
    background-color: #7B564B !important;
    border-color: #DCC2A8 !important;
}

/* ---------- Chat Area ---------- */
[data-testid="stBottom"] {
    background: #A67C6B !important;
}

[data-testid="stChatInput"] {
    background: #A67C6B !important;
    border-top: none !important;
}

[data-testid="stChatInput"] textarea {
    background: #6D4C41 !important;
    color: #FFFFFF !important;
}

[data-testid="stChatInput"] button {
    background: #6D4C41 !important;
    color: white !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

.main .block-container {
    background: transparent !important;
}

div.st-emotion-cache-qdbtli {
    background: #A67C6B !important;
}
</style>
"""
