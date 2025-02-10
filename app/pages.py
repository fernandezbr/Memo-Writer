import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def show_home():
    st.set_page_config(
        page_title="BSP Writer",
        page_icon="✍️",
        layout="wide",
        # initial_sidebar_state="collapsed",
    )
    st.logo(
        "https://upload.wikimedia.org/wikipedia/commons/c/cb/Bangko_Sentral_ng_Pilipinas_2020_logo.png",
        link="https://www.bsp.gov.ph/SitePages/Default.aspx",
    )
    # Initial states
    if "content" not in st.session_state:
        st.session_state.content = ""
    if "contentAll" not in st.session_state:
        st.session_state.contentAll = ""
    if "style" not in st.session_state:
        st.session_state.style = ""
    if "guidelines" not in st.session_state:
        st.session_state.guidelines = ""
    if "example" not in st.session_state:
        st.session_state.example = ""
    if "exampleText" not in st.session_state:
        st.session_state.exampleText = ""
    if "output" not in st.session_state:
        st.session_state.output = ""

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem;
            # padding-bottom: 1rem;
            # padding-left: 1rem;
            # padding-right: 1rem;
        }
        .stAppDeployButton {
            display: none;
        }
        .st-emotion-cache-15ecox0 {
            display: none;
        }
        .viewerBadge_container__r5tak {
            display: none;
        }
        .styles_viewerBadge__CvC9N {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# display the sidebar
def show_sidebar():
    with st.sidebar:
        with st.container(border=True):
            st.page_link("app.py", label="Style Writer", icon="✍️")
            st.page_link("pages/reader.py", label="Style Reader", icon="✨")
            st.page_link("pages/outputs.py", label="Generated Outputs", icon="📚")

        st.image(
            "https://github.com/robrita/Memo-Writer/blob/main/img/banner.png?raw=true",
        )
        st.write("Powered by Azure OpenAI.")
