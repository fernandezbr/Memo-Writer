import os
import json
import time
import requests
import pandas as pd
import streamlit as st

from datetime import datetime
from openai import AzureOpenAI
from azure.cosmos import CosmosClient, exceptions

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

# Initialize Cosmos DB client
cosmos_client = CosmosClient(
    url=os.environ["AZURE_COSMOS_ENDPOINT"],
    credential=os.environ["AZURE_COSMOS_KEY"]
)

# Get database and container references
database = cosmos_client.get_database_client(os.environ["AZURE_COSMOS_DATABASE"])
styles_container = database.get_container_client("styles")
outputs_container = database.get_container_client("outputs")

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
    try:
        items = list(styles_container.read_all_items())
        return items
    except exceptions.CosmosHttpResponseError as e:
        st.error(f"An error occurred while fetching styles: {e}")
        return []


# save style to database
def save_style():
    try:
        now = datetime.now()
        st.session_state.styleId = str(int(time.time() * 1000))
        new_style = {
            "id": st.session_state.styleId,
            "updatedAt": now.isoformat(),
            "name": "",
            "style": st.session_state.style,
            "example": st.session_state.example,
        }
        styles_container.create_item(body=new_style)
    except exceptions.CosmosHttpResponseError as e:
        st.error(f"An error occurred while saving style: {e}")


# save output to database
def save_output():
    try:
        now = datetime.now()
        new_output = {
            "id": str(int(time.time() * 1000)),
            "updatedAt": now.isoformat(),
            "content": st.session_state.contentAll,
            "styleId": st.session_state.styleId,
            "output": st.session_state.output,
        }
        outputs_container.create_item(body=new_output)
    except exceptions.CosmosHttpResponseError as e:
        st.error(f"An error occurred while saving output: {e}")


# get outputs from database
def get_outputs():
    try:
        items = list(outputs_container.read_all_items())
        # Convert to DataFrame
        df = pd.DataFrame(items)
        # Only drop 'id' column if it exists
        if 'id' in df.columns:
            df = df.drop(columns=["id"])
        # Display the DataFrame in Streamlit
        st.dataframe(df)
    except exceptions.CosmosHttpResponseError as e:
        st.error(f"An error occurred while fetching outputs: {e}")
