import os
import json
import time
import requests
import pandas as pd
import streamlit as st

from datetime import datetime
from openai import AzureOpenAI

# create a config dictionary
config = {
    "endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    "model": os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
}

# Initialize OpenAI client
clientAOAI = AzureOpenAI(
    azure_endpoint=config["endpoint"],
    api_version=config["api_version"],
    api_key=config["api_key"],
)


# log tracing
def trace(col2, label, message):
    with col2:
        with st.expander(f"{label}:"):
            st.write(message)
            # print(f"{label}: {message}")


# get request api
def get_request(url):
    response = requests.get(url)
    return response.json()


# chat completion
def chat(
    messages=[],
    temperature=0.7,
    streaming=True,
    format="text",
):
    try:
        # Response generation
        full_response = ""
        message_placeholder = st.empty()

        for completion in clientAOAI.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=temperature,
            stream=streaming,
            response_format={"type": format},
        ):

            if completion.choices and completion.choices[0].delta.content is not None:
                full_response += completion.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        return full_response

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Function to read a JSON file
def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            collection = json.load(file)
            return collection
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# get styles from database
def get_styles():
    return read_json("data/db_styles.json")


# save style to database
def save_style():
    data = read_json("data/db_styles.json")
    now = datetime.now()

    data.append(
        {
            "id": int(time.time() * 1000),
            "updatedAt": now.isoformat(),
            "style": st.session_state.style,
            "example": st.session_state.example,
        }
    )

    with open("data/db_styles.json", "w") as file:
        json.dump(data, file, indent=2)


# save output to database
def save_output():
    data = read_json("data/db_outputs.json")
    now = datetime.now()

    data.append(
        {
            "id": int(time.time() * 1000),
            "updatedAt": now.isoformat(),
            "content": st.session_state.content,
            "style": st.session_state.style,
            "output": st.session_state.output,
        }
    )

    with open("data/db_outputs.json", "w") as file:
        json.dump(data, file, indent=2)


# get outputs from database
def get_outputs():
    # Convert to DataFrame and drop the 'id' column
    dbdata = read_json("data/db_outputs.json")
    df = pd.DataFrame(dbdata).drop(columns=["id"])

    # Display the DataFrame in Streamlit
    st.dataframe(df)
