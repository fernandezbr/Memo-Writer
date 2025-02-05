import streamlit as st
import app.pages as pages
import app.evaluate as evaluate
import app.utils as utils

from dotenv import load_dotenv

load_dotenv()

# App title
pages.show_home()
pages.show_sidebar()

st.title("✨Style Reader")

st.session_state.content = st.text_area(
    "Paste your content here:", st.session_state.content
)

with st.expander("LLM Instructions:"):
    st.session_state.instructions = st.text_area(
        "✨Instructions", st.session_state.instructions
    )

with st.expander("Training Content:"):
    st.session_state.user = st.text_area("✨Content", st.session_state.user)

with st.expander("Training Output:"):
    st.session_state.assistant = st.text_area("✨Output", st.session_state.assistant)

# subject_selected, subject = pages.select_subject()

# topic = st.selectbox("Select a Topic:", options=list(utils.get_data(subject, 0)))

# # PISA questions
# if topic:
#     with st.container(border=True):
#         topic_data = utils.get_data(subject, topic)
#         st.session_state.context = topic_data["context"]
#         st.session_state.question = topic_data["question"]
#         st.session_state.answer = topic_data["answer"]
#         st.session_state.topic = topic_data["topic"]

#         st.write(st.session_state.context)
#         st.markdown(
#             f"""<span style="color: blue;">**Question**: {st.session_state.question}</span>""",
#             unsafe_allow_html=True,
#         )

if st.button(
    ":blue[Extract Writing Style]",
    key="extract",
    disabled=st.session_state.content == ""
    or st.session_state.instructions == ""
    or st.session_state.user == ""
    or st.session_state.assistant == "",
):
    with st.container(border=True):
        with st.spinner("Processing..."):
            evaluate.extract_style()
