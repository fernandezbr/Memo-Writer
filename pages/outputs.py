import streamlit as st
import app.pages as pages
import app.generate as generate
import app.utils as utils

# App title
pages.show_home()
pages.show_sidebar()

st.title("📚Generated Outputs")
