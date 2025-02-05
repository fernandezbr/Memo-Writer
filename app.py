import streamlit as st
import app.pages as pages
import app.evaluate as evaluate
from dotenv import load_dotenv

load_dotenv()

# App title
pages.show_home()
pages.show_sidebar()

# Home page
st.title("✍️Style Writer")

st.session_state.source = st.text_area(
    "Paste your content here:", st.session_state.source
)

with st.expander("Reference Style:"):
    st.session_state.style = st.text_area("✨Style", st.session_state.style)

with st.expander("Reference Guidelines:"):
    st.session_state.guidelines = st.text_area(
        "✨Guidelines", st.session_state.guidelines
    )

with st.expander("Reference Example:"):
    st.session_state.example = st.text_area("✨Example", st.session_state.example)

if st.button(
    ":blue[Rewrite Content]",
    key="extract",
    disabled=st.session_state.source == ""
    or st.session_state.style == ""
    or st.session_state.example == "",
):
    with st.container(border=True):
        with st.spinner("Processing..."):
            evaluate.rewrite_content()
