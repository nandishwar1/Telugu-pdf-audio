import streamlit as st
import pymupdf

st.title("Telugu PDF Text Reader")

uploaded_file = st.file_uploader(
    "Upload a Telugu PDF",
    type=["pdf"]
)

if uploaded_file:
    document = pymupdf.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text() + "
"

    if text.strip():
        st.text_area(
            "Extracted Telugu text",
            text,
            height=400
        )
    else:
        st.error(
            "No text found. This may be a scanned PDF and needs OCR."
        )
