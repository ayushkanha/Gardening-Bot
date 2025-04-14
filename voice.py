import streamlit as st 
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import os
import speech_recognition as sr
from transformers import pipeline as pl

def text_to_speech(text, lang='en', c=0):
    tts = gTTS(text=text, lang=lang)
    audio_file = f"output{c}.mp3"
    tts.save(audio_file)
    return audio_file


def transcribe(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        file_path = tmpfile.name
        tmpfile.write(uploaded_file.read())

    st.sidebar.sidebaraudio(uploaded_file, format="audio/wav")
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(file_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        st.info("🔄 Transcribing... Please wait!")
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.sidebar.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.sidebar.error("❌ API error. Check internet connection.")
    os.remove(file_path)
    return ""
