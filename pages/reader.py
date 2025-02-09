import streamlit as st
import app.pages as pages
import app.utils as utils
import app.prompts as prompts

from dotenv import load_dotenv

load_dotenv()

# App title
pages.show_home()
pages.show_sidebar()

st.title("✨Style Reader")

st.session_state.example = st.text_area(
    "Reference Example:", st.session_state.example, 400
)

# debug = st.checkbox("Debug")

if st.button(
    ":blue[Extract Writing Style]",
    key="extract",
    disabled=st.session_state.example == "",
):
    with st.container(border=True):
        with st.spinner("Processing..."):
            st.session_state.style = prompts.extract_style(False)
            utils.save_style()
