import streamlit as st
import pymupdf
from google.cloud import texttospeech

st.set_page_config(
    page_title="Telugu PDF to Audio",
    page_icon="🔊"
)

st.title("Telugu PDF to Audio")

uploaded_file = st.file_uploader(
    "Upload a Telugu PDF",
    type=["pdf"]
)

voice_name = st.selectbox(
    "Choose Telugu voice",
    [
        "te-IN-Standard-A",
        "te-IN-Standard-B"
    ]
)

speech_rate = st.slider(
    "Speech speed",
    0.7,
    1.3,
    1.0,
    0.05
)

if uploaded_file is not None:
    if st.button("Convert to Audio"):
        with st.spinner("Extracting text from PDF..."):
            pdf_data = uploaded_file.read()

            document = pymupdf.open(
                stream=pdf_data,
                filetype="pdf"
            )

            page_text = []

            for page in document:
                page_text.append(page.get_text())

            text = " ".join(page_text).strip()

        if not text:
            st.error(
                "No text found. This may be a scanned PDF and needs OCR."
            )
        else:
            st.subheader("Extracted Telugu Text")
            st.text_area(
                "Text preview",
                text,
                height=300
            )

            with st.spinner("Creating Telugu audio..."):
                client = texttospeech.TextToSpeechClient()

                input_text = texttospeech.SynthesisInput(
                    text=text
                )

                voice = texttospeech.VoiceSelectionParams(
                    language_code="te-IN",
                    name=voice_name
                )

                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=speech_rate
                )

                response = client.synthesize_speech(
                    input=input_text,
                    voice=voice,
                    audio_config=audio_config
                )

            st.success("Audio created successfully.")

            st.audio(
                response.audio_content,
                format="audio/mp3"
            )

            st.download_button(
                label="Download MP3",
                data=response.audio_content,
                file_name="telugu_audio.mp3",
                mime="audio/mpeg"
        )
