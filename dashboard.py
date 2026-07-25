import streamlit as st

SUGGESTIONS = [
    ("💵", "Explain bond pricing", "Explain how bond pricing works."),
    ("⏱", "What is duration?", "What is duration in fixed-income securities, and why does it matter?"),
    ("🛡", "Explain credit risk", "Explain credit risk in fixed-income securities."),
    ("🏦", "What caused the 2008 financial crisis?", "What caused the 2008 financial crisis?"),
]


def render_dashboard():
    st.markdown(
        """<div class="hero slide-up">
            <h1>Finance Theory AI Assistant</h1>
            <p>Ask questions about bonds, fixed-income securities, credit risk, duration,
            yield curves, and the 2008 financial crisis.</p>
        </div>""",
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    for col, (icon, title, prompt) in zip(cols, SUGGESTIONS):
        with col:
            st.markdown(
                f"""<div class="suggestion-card fade-in">
                    <div class="suggestion-card__icon">{icon}</div>
                    <div class="suggestion-card__title">{title}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button("Ask", key=f"suggestion_{title}", use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()
