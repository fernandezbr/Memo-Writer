import streamlit as st
import app.utils as utils


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
    if "source" not in st.session_state:
        st.session_state.source = ""
    if "style" not in st.session_state:
        st.session_state.style = ""
    if "example" not in st.session_state:
        st.session_state.example = ""
    if "guidelines" not in st.session_state:
        st.session_state.guidelines = ""
    if "content" not in st.session_state:
        st.session_state.content = ""
    if "instructions" not in st.session_state:
        st.session_state.instructions = ""
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "assistant" not in st.session_state:
        st.session_state.assistant = ""

    # st.markdown(
    #     """
    #     <style>
    #     .block-container {
    #         padding-top: 1rem;
    #         # padding-bottom: 1rem;
    #         # padding-left: 1rem;
    #         # padding-right: 1rem;
    #     }
    #     .stAppDeployButton {
    #         display: none;
    #     }
    #     .st-emotion-cache-15ecox0 {
    #         display: none;
    #     }
    #     .viewerBadge_container__r5tak {
    #         display: none;
    #     }
    #     .styles_viewerBadge__CvC9N {
    #         display: none;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )


# display the sidebar
def show_sidebar():
    with st.sidebar:
        with st.container(border=True):
            st.page_link("app.py", label="Style Writer", icon="✍️")
            st.page_link("pages/reader.py", label="Style Reader", icon="✨")
            st.page_link("pages/outputs.py", label="Generated Outputs", icon="📚")

        st.image(
            "https://github.com/robrita/PISA-GenAI/blob/main/img/banner.png?raw=true",
        )
        st.write("Powered by Azure OpenAI.")


# select subject from dropdown
def select_subject():
    subjects = {
        "Science": "science",
        "Mathematics": "math",
        "Reading": "reading",
        "Financial literacy": "financial_literacy",
        "Creative Thinking": "creative_thinking",
        "Global competence": "global_competence",
        "Collaborative problem solving": "problem_solving",
    }

    subject_selected = st.selectbox("Select a Subject:", options=list(subjects.keys()))
    subject = subjects[subject_selected]
    return subject_selected, subject
