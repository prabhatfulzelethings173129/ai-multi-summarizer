import streamlit as st
from transformers import pipeline
from gtts import gTTS
import pytesseract
from PIL import Image
from youtube_transcript_api import YouTubeTranscriptApi
import fitz  # PyMuPDF

# Title
st.title("🔥 AI Text Summarizer (All-in-One)")

# Load model
summarizer = pipeline("summarization")

# OPTION SELECT
option = st.selectbox("Choose Input Type", ["Text", "PDF", "Image", "YouTube"])

input_text = ""

# ---------------- TEXT ----------------
if option == "Text":
    input_text = st.text_area("Enter your text")

# ---------------- PDF ----------------
elif option == "PDF":
    pdf_file = st.file_uploader("Upload PDF", type="pdf")
    if pdf_file:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in doc:
            input_text += page.get_text()

# ---------------- IMAGE ----------------
elif option == "Image":
    img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if img_file:
        image = Image.open(img_file)
        input_text = pytesseract.image_to_string(image)

# ---------------- YOUTUBE ----------------
elif option == "YouTube":
    url = st.text_input("Enter YouTube URL")
    if url:
        try:
            video_id = url.split("v=")[-1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            input_text = " ".join([i['text'] for i in transcript])
        except:
            st.error("Could not fetch transcript")

# ---------------- SUMMARIZE ----------------
if st.button("Summarize"):
    if input_text.strip() == "":
        st.warning("No text found!")
    else:
        input_text = input_text[:1000]  # fix error
        summary = summarizer(input_text, max_length=100, min_length=30, do_sample=False)
        summary_text = summary[0]['summary_text']

        st.subheader("Summary:")
        st.write(summary_text)

        # AUDIO
        tts = gTTS(summary_text)
        tts.save("summary.mp3")
        st.audio("summary.mp3")