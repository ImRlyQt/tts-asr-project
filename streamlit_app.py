import streamlit as st
import requests
import tempfile
import os

st.title("ASR Service – Whisper")

# Nagrywanie dźwięku
audio_file = st.file_uploader("Wgraj plik audio", type=["wav", "mp3", "m4a"])

if audio_file:
    # Zapisz plik tymczasowo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name

    # Wysyłanie do API
    with open(temp_audio_path, "rb") as f:
        response = requests.post("http://localhost:5000/transcribe", files={"file": f})

    os.remove(temp_audio_path)  # Usuń plik po przetworzeniu

    if response.status_code == 200:
        transcription = response.json().get("transcription", "")
        st.success("Transkrypcja:")
        st.write(transcription)
    else:
        st.error("Błąd w transkrypcji. Sprawdź API.")

