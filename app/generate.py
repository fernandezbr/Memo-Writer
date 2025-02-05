import json
import streamlit as st
import app.utils as utils


def pisa_question(subject_selected, subject, seed):
    with st.spinner("Processing ..."):
        # results = json.loads(pisa_seed(subject, seed))
        results = json.loads(pisa_generate(subject_selected, subject, seed))
        # st.write(results)
        st.session_state.context = results["Context"]
        st.session_state.question = results["Question"]
        st.session_state.answer = results["Answer"]
        st.session_state.topic = results["Topic"]


def pisa_generate(subject_selected, subject, seed):
    topics = utils.get_data(subject, 0)

    system = [
        "You are an expert PISA exam generator.",
        f"Your goal is to generate a PISA exam question along with it's context and answer for {subject_selected} subject.",
        "Response should be in valid JSON format only.\n",
        "# Response JSON Schema",
        "{",
        "Context: The context of the question",
        "Question: The question",
        "Answer: The correct and concise answer",
        "Topic: The topic of the context",
        "}\n",
        f"Generate PISA exam question NOT related to the following topics: {json.dumps(topics)}",
    ]

    prompt = [
        {"role": "system", "content": "\n".join(system)},
        {
            "role": "user",
            "content": f"Give me a sample PISA exam question along with context related to {subject_selected}.",
        },
        {
            "role": "assistant",
            "content": json.dumps(utils.get_seed(subject, seed)),
        },
    ]

    user = [
        {
            "role": "user",
            "content": f"More practice PISA exam question related to {subject_selected}.",
        },
    ]

    messages = prompt + user
    st.write(messages)
    return utils.chat(messages, 0.7, 800, True, "json_object")


def pisa_seed(subject, seed):
    seeds = utils.get_seed(subject, seed)
    system = [
        "You are an expert in PISA exam.",
        "Your goal is to provide a correct and concise answer and topic, given a PISA exam question along with it's context below.",
        f"Context: {seeds['Context']}",
        f"Question: {seeds['Question']}\n",
        "Response should be in valid JSON format only.",
        "# Response JSON Schema",
        "{",
        "Topic: The topic of the context",
        "Answer: The correct and concise answer",
        "}",
        "Take a deep breath and think through step by step.",
    ]

    messages = [
        {"role": "system", "content": "\n".join(system)},
    ]

    # st.write(messages)
    return utils.chat(messages, 0, 800, True, "json_object")
