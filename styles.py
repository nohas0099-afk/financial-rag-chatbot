import streamlit as st

# دالة لحقن الكود وتطبيقه
def inject_theme():
    THEME_CSS = """
    <style>
    /* تعريف المتغيرات اللونية بناءً على التصميم */
    :root {
        --bg-primary: #3d3b32;          /* لون الخلفية الأساسي الزيتي المتوسط */
        --bg-secondary: #21201a;        /* لون الشريط الجانبي الزيتي الداكن جداً */
        
        --glass-bg: rgba(64, 61, 53, 0.7); /* كروت زجاجية بلمسة زيتية */
        --glass-border: #635f52;        /* حدود الكروت الزجاجية */

        --gold-primary: #a39b83;        /* اللون الذهبي/البرونزي الأساسي للأزرار والنصوص */
        --gold-hover: #b8af96;          /* لون ذهبي فاتح عند التمرير */
        
        --text-primary: #FFFFFF;        /* نصوص بيضاء أساسية */
        --text-secondary: #c9c3b1;      /* نصوص ذهبية باهتة ثانوية */
        --text-muted: #807a68;          /* نصوص باهتة جداً */

        --radius: 12px;
        --radius-pills: 999px;
    }

    /* ---------- تنظيف واجهة StreamlitChrome ---------- */
    /* إخفاء القائمة الرئيسية والترويسة والتذييل الافتراضي */
    #MainMenu, header, footer {visibility: hidden; height: 0;}
    [data-testid="stToolbar"] {display: none;}
    
    /* ضبط حواشي الصفحة الرئيسية وتوسيع المحتوى */
    .block-container {
        padding-top: 1.5rem; 
        padding-bottom: 3rem; 
        max-width: 1200px;
    }

    /* ---------- الخلفية الأساسية المتدرجة ---------- */
    [data-testid="stAppViewContainer"]{
        background: linear-gradient(
            135deg,
            #48453a 0%,    /* زيتي فاتح فوق */
            #3d3b32 50%,   /* زيتي متوسط وسط */
            #302e27 100%   /* زيتي داكن تحت */
        ) !important;
    }

    /* ---------- تنسيق الشريط الجانبي (Sidebar) ---------- */
    [data-testid="stSidebar"]{
        background: linear-gradient(
            180deg,
            #2a2922 0%,    /* زيتي داكن جداً فوق */
            #1b1a15 100%   /* أسود زيتي تحت */
        ) !important;
        border-right: 1px solid #48453a !important;
    }

    /* ---------- تنسيق النصوص العامة ---------- */
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
        color: var(--text-primary) !important;
        font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    }

    /* ---------- تنسيق الكروت الزجاجية (Glass Cards) ---------- */
    /* يُستخدم في كروت الاقتراحات ومربعات LLM */
    .st_emotion_cache_1v0mbdj { /* كلاس كروت الاقتراحات (قد يتغير في تحديثات Streamlit) */
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius) !important;
        padding: 20px !important;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
        cursor: pointer !important;
        text-align: center !important;
    }
    
    /* تأثير التمرير على الكروت */
    .st_emotion_cache_1v0mbdj:hover {
        transform: translateY(-5px) !important;
        border-color: var(--gold-hover) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
    }

    /* تنسيق كودجيتات الـ Markdown داخل كروت الاقتراحات */
    .st_emotion_cache_1v0mbdj strong {
        color: var(--gold-primary) !important;
        font-size: 1rem !important;
        display: block !important;
        margin-top: 10px !important;
    }
    
    .st_emotion_cache_1v0mbdj .stMarkdown {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    /* ---------- تنسيق الأزرار الذهبية (Buttons) ---------- */
    /* زر + New chat والأزرار الأخرى */
    .stButton > button {
        background: linear-gradient(to right, #8c836d, #a39b83) !important; /* تدرج ذهبي برونزي */
        color: #FFFFFF !important;
        border: 1px solid #635f52 !important;
        border-radius: var(--radius) !important;
        font-weight: 600 !important;
        transition: background 0.3s ease, border-color 0.3s ease !important;
        width: 100% !important; /* لتأخذ الأزرار كامل العرض في الجنب */
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #a39b83, #b8af96) !important;
        border-color: #736d5e !important;
        color: #FFFFFF !important;
    }
    
    /* أزرار الـ pills (مثل PDF, DOCX...) */
    .st_emotion_cache_1p3d7v1 { /* كلاس الـ pills */
        background-color: transparent !important;
        border: 1px solid #48453a !important;
        color: var(--text-muted) !important;
        border-radius: var(--radius-pills) !important;
        font-size: 0.8rem !important;
    }

    /* ---------- تنسيق منطقة رفع الملفات (File Uploader) ---------- */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploaderDropzone"]{
        background: #2a2922 !important;
        border: 2px dashed #545144 !important;
        border-radius: var(--radius) !important;
        margin-bottom: 10px !important;
    }

    [data-testid="stFileUploader"] *{
        color: #e3decb !important;
    }

    /* زر Browse files داخل مربع الرفع */
    [data-testid="stFileUploader"] button {
        background: var(--glass-bg) !important;
        color: var(--gold-primary) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius) !important;
        font-weight: 500 !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background-color: #48453a !important;
        border-color: #736d5e !important;
        color: #FFFFFF !important;
    }

    /* ---------- تنسيق حقول الإدخال (Inputs & Textarea) ---------- */
    /* مربع Chat Input */
    [data-testid="stChatInput"] textarea {
        background: #23221c !important; /* لون داكن جداً داخل المربع */
        color: #FFFFFF !important;
        border: 1px solid #545144 !important;
        border-radius: var(--radius-pills) !important;
        padding-left: 1rem !important;
    }
    
    /* جعل حافة مربع الشات ذهبية عند التركيز */
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--gold-primary) !important;
        box-shadow: 0 0 10px rgba(163,155,131,0.3) !important;
    }

    /* ---------- تنسيق جرو الشات (Chat Messages) ---------- */
    .stChatMessage {
        margin-bottom: 15px !important;
    }

    /* رسائل المستخدم (User) */
    [data-testid="stChatMessage"] {
        border-radius: 18px 18px 4px 18px !important; /* زوايا دائرية مختلفة */
        border: 1px solid #48453a !important;
    }
    
    /* رسائل المساعد (Assistant) */
    .stChatMessage.st_emotion_cache_1v0mbdj { /* مساعد (تستخدم كروت الاقتراحات كرسائل) */
        border-radius: 18px 18px 18px 4px !important;
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
    }

    /* ---------- إزالة المساحات البيضاء وتعديل الحواشي ---------- */
    /* إزالة الخلفية البيضاء الافتراضية في منطقة الشات السفلي */
    [data-testid="stBottom"] {
        background: transparent !important;
    }
    
    /* تعديل تنسيق الـ Bottom container */
    [data-testid="stChatInput"] {
        background: transparent !important;
        border-top: none !important;
        padding-bottom: 1rem !important;
    }
    
    /* التأكد من عدم وجود مساحات بيضاء بين الجرو والمنطقة السفلية */
    div.st_emotion_cache_qdbtli {
        background: transparent !important;
    }

    /* ---------- تنسيق الأيقونات وعناصر الـ Markdown ---------- */
    /* جعل أيقونات الاقتراحات برونزية */
    .stMarkdown .st_emotion_cache_1ekf893, /* كلاس أيقونات Streamlit الافتراضية */
    .stMarkdown strong + span { /* كلاس الأيقونات بعد العناوين (في الكروت) */
        color: var(--gold-primary) !important;
        font-size: 1.5rem !important;
    }
    
    /* تنسيق أيقونة "زيتي" المائية في الخلفية */
    .stMarkdown:contains("زيتي") h1 {
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        opacity: 0.05 !important; /* شفافة جداً لتبدو مائية */
        font-size: 10rem !important;
        z-index: -1 !important;
    }
    </style>
    """
    # حقن الكود كـ Markdown
    st.markdown(THEME_CSS, unsafe_allow_html=True)

# استدعاء الدالة لتطبيق التصميم
inject_theme()

# --- الآن يمكنك البدء في إضافة محتوى Streamlit الخاص بك ---
# مثال لإضافة المحتوى كما في الصورة:

with st.sidebar:
    # صورة الملف الشخصي والاسم
    col1, col2 = st.columns([1, 4])
    with col1:
        # يمكنك إضافة صورتك الشخصية هنا (اختياري)
        # st.image("path_to_profile_photo.jpg", width=40)
        pass
    with col2:
        st.markdown("### Finance Theory\nAI Assistant")

    # زر New chat
    st.button("+ New chat")
    
    st.markdown("#### ADD COURSE MATERIAL")
    # File uploader
    st.file_uploader("Drag and drop files here", type=['pdf', 'docx', 'txt'])
    
    # Pills مثال
    st.markdown("`PDF` `DOCX` `TXT`")
    
    # أقسام أخرى
    st.markdown("#### DOCUMENT LIBRARY")
    st.markdown("""
        Chat history
        Settings
        About
        LLM
        FLAN-15-Base (Local)
        EMBEDDING MODEL
        all-Minilm-L6-v2
    """)

# الصفحة الرئيسية
st.markdown("# Finance Theory AI Assistant")
st.markdown("Ask questions about bonds, fixed income securities, credit risk, duration, yield curves, and the 2008 financial crisis.")

# شبكة الاقتراحات
col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container():
        st.markdown("**Explain bond pricing**")
        st.button("Ask", key="ask1")
with col2:
    with st.container():
        st.markdown("**What is duration?**")
        st.button("Ask", key="ask2")
with col3:
    with st.container():
        st.markdown("**Explain credit risk**")
        st.button("Ask", key="ask3")
with col4:
    with st.container():
        st.markdown("**What caused the 2008 financial crisis?**")
        st.button("Ask", key="ask4")

# أيقونة "زيتي" المائية (كـ Markdown)
st.markdown("<h1>زيتي</h1>", unsafe_allow_html=True)

# حقل الشات
st.chat_input("Ask anything about your financial documents...")
