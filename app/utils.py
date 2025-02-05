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


# return matching seed data
def get_seed(subject, seed):
    # Specify the path to your JSON file
    collection = read_json(f"data/seed_{subject}.json")

    if seed in collection:
        return collection[seed]
    else:
        return collection


# save data to database
def save_data(subject):
    data = read_json(f"data/db_{subject}.json")
    now = datetime.now()

    data.append(
        {
            "id": int(time.time() * 1000),
            "updatedAt": now.isoformat(),
            "topic": st.session_state.topic,
            "context": st.session_state.context,
            "question": st.session_state.question,
            "answer": st.session_state.answer,
        }
    )

    with open(f"data/db_{subject}.json", "w") as file:
        json.dump(data, file, indent=2)


# get data from database
def get_data(subject, topic):
    dbdata = read_json(f"data/db_{subject}.json")
    # Create DataFrame
    df = pd.DataFrame(dbdata)
    topics = df["topic"].tolist()

    if topic:
        # Filter DataFrame to get the object with matching topic
        matching_topic = df[df["topic"] == topic]
        # Convert the filtered DataFrame to a dictionary
        result = matching_topic.to_dict(orient="records")
        return result[0]

    return topics
