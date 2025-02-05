import streamlit as st
import app.utils as utils


def extract_style():
    # system = [st.session_state.instructions]

    messages = [
        {"role": "system", "content": st.session_state.instructions},
        {"role": "user", "content": st.session_state.user},
        {"role": "assistant", "content": st.session_state.assistant},
        {"role": "user", "content": st.session_state.content},
    ]

    # st.write(messages)
    return utils.chat(messages, 0)


def rewrite_content():
    system = [
        "You are an expert writer assistant. Rewrite the user input based on the following writing style, guidelines and user example.\n",
        f"<writingStyle>{st.session_state.style}</writingStyle>\n",
        f"<writingGuidelines>{st.session_state.guidelines}</writingGuidelines>\n",
        f"<userExamples>{st.session_state.example}</userExamples>",
    ]

    messages = [
        {"role": "system", "content": "\n".join(system)},
        {"role": "user", "content": st.session_state.source},
    ]

    # st.write(messages)
    return utils.chat(messages, 0.7)
