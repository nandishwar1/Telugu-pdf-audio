import streamlit as st
import pymupdf
from google.cloud import texttospeech

st.set_page_config(
    page_title="Telugu PDF to Audio",
    page_icon="🔊"
)

st.title("Telugu PDF to Audio")
st.write("Upload a Telugu PDF and convert its text into an MP3 audio file.")

uploaded_file = st.file_uploader(
    "Upload Telugu PDF",
    type=["pdf"]
)

voice_name = st.selectbox(
    "Select voice",
    [
        "te-IN-Standard-A",
        "te-IN-Standard-B"
    ]
)

speech_rate = st.slider(
    "Speech speed",
    min_value=0.7,
    max_value=1.3,
    value=1.0,
    step=0.05
)

if uploaded_file is not None:
    if st.button("Extract text and convert to audio"):
        with st.spinner("Reading PDF..."):
            pdf_bytes = uploaded_file.read()
            document = pymupdf.open(stream=pdf_bytes, filetype="pdf")

            pages = []
            for page in document:
                pages.append(page.get_text())

            text = "
".join(pages).strip()

        if not text:
            st.error(
                "No selectable text was found. This may be a scanned PDF. "
                "OCR support must be added."
            )
        else:
            st.subheader("Extracted Telugu text")
            st.text_area("Text preview", text, height=250)

            with st.spinner("Creating Telugu audio..."):
                client = texttospeech.TextToSpeechClient()

                synthesis_input = texttospeech.SynthesisInput(
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
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config
                )

            st.success("Audio created successfully.")

            st.audio(response.audio_content, format="audio/mp3")

            st.download_button(
                label="Download MP3",
                data=response.audio_content,
                file_name="telugu_audio.mp3",
                mime="audio/mpeg"
            )
