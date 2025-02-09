import streamlit as st
import app.pages as pages
import app.utils as utils
import app.prompts as prompts

# App title
pages.show_home()
pages.show_sidebar()

# Home page
st.title("✍️Style Writer")

st.session_state.content = st.text_area(
    "Paste your content here:", st.session_state.content, 200
)

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

with st.expander("Reference Example:"):
    st.session_state.example = st.text_area("✨Example", st.session_state.example, 200)

# debug = st.checkbox("Debug")

if st.button(
    ":blue[Rewrite Content]",
    key="extract",
    disabled=st.session_state.content == ""
    or st.session_state.style == ""
    or st.session_state.example == "",
):
    with st.container(border=True):
        with st.spinner("Processing..."):
            st.session_state.output = prompts.rewrite_content(False)
            utils.save_output()
