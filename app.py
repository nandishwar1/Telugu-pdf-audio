import streamlit as st
import pymupdf

st.title("Telugu PDF Text Reader")

uploaded_file = st.file_uploader(
    "Upload a Telugu PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    pdf_data = uploaded_file.read()
    document = pymupdf.open(
        stream=pdf_data,
        filetype="pdf"
    )

    page_text = []

    for page in document:
        page_text.append(page.get_text())

    text = " ".join(page_text).strip()

    if text:
        st.subheader("Extracted Telugu Text")
        st.text_area(
            "Text preview",
            text,
            height=400
        )
    else:
        st.error(
            "No text found. This may be a scanned PDF and needs OCR."
        )
