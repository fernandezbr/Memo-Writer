import streamlit as st
import app.pages as pages
import app.utils as utils

# App title
pages.show_home()
pages.show_sidebar()

st.title("📚Generated Outputs")

# Display the generated outputs
utils.get_outputs()
