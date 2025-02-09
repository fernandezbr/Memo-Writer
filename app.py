import streamlit as st
import app.pages as pages
import app.utils as utils
import app.prompts as prompts
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
from io import BytesIO

# App title
pages.show_home()
pages.show_sidebar()

# Home page
st.title("✍️Style Writer")

# Content input
st.session_state.content = st.text_area(
    "Content Data:", st.session_state.content, 200
)

uploaded_files = st.file_uploader(
    "Upload Content Files:", 
    type=["pdf", "docx", "pptx"], 
    accept_multiple_files=True,
    help="Upload PDF, Word, or PowerPoint files"
)

# Extract text from uploaded files
extracted_text = ""
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        if file_type == 'pdf':
            pdf_reader = PdfReader(BytesIO(uploaded_file.read()))
            for page in pdf_reader.pages:
                extracted_text += page.extract_text() + "\n"
                
        elif file_type == 'docx':
            doc = Document(BytesIO(uploaded_file.read()))
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    extracted_text += paragraph.text + "\n"
                    
        elif file_type == 'pptx':
            prs = Presentation(BytesIO(uploaded_file.read()))
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        if shape.text.strip():
                            extracted_text += shape.text + "\n"

# Combine text area and extracted content
st.session_state.contentAll = st.session_state.content or extracted_text

if extracted_text:
    st.session_state.contentAll = st.session_state.content + "\n" + extracted_text

with st.expander("Reference Style:"):
    # Extracting the 'style' values into a list
    styles = [item["style"] for item in utils.get_styles()]
    style = st.selectbox("Select a Style:", options=styles, index=None)

    # Assigning the selected style to the session state
    if style:
        st.session_state.style = style

        # Assigning the selected example to the session state
        filtered = next(
            (item for item in utils.get_styles() if item["style"] == style), None
        )
        st.session_state.example = filtered["example"]
    st.session_state.style = st.text_area("✨Style", st.session_state.style)

with st.expander("Reference Guidelines:"):
    st.session_state.guidelines = st.text_area(
        "✨Guidelines", st.session_state.guidelines, 200
    )

with st.expander("Reference Examples:"):
    st.session_state.example = st.text_area("✨Examples", st.session_state.example, 200)

if st.button(
    ":blue[Rewrite Content]",
    key="extract",
    disabled=st.session_state.contentAll == ""
    or st.session_state.style == ""
    or st.session_state.example == "",
):
    with st.container(border=True):
        with st.spinner("Processing..."):
            st.session_state.output = prompts.rewrite_content(False)
            utils.save_output()
