import streamlit as st
import requests
import tempfile
import os

st.title("ASR + TTS Service")

languages = {
    "en": "Angielski",
    "pl": "Polski"
}

# --- Przechowywanie języka w sesji ---
if "asr_language" not in st.session_state:
    st.session_state.asr_language = "en"

if "tts_language" not in st.session_state:
    st.session_state.tts_language = "en"

# --- ASR (Whisper) ---
st.header("🎙️ Rozpoznawanie mowy (ASR)")
asr_language = st.radio("Wybierz język", ["en", "pl"], format_func=lambda x: languages[x], key="asr_language")

audio_file = st.file_uploader("Wgraj plik audio", type=["wav", "mp3", "m4a"])

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio_path = temp_audio.name

    with open(temp_audio_path, "rb") as f:
        response = requests.post("http://localhost:5000/transcribe", files={"file": f}, data={"language": st.session_state.asr_language})

    os.remove(temp_audio_path)

    if response.status_code == 200:
        transcription = response.json().get("transcription", "")
        st.write("Transkrypcja:")
        st.success(transcription)
    else:
        st.error("Błąd w transkrypcji. Sprawdź API.")

# --- TTS (Coqui) ---
st.header("🗣️ Synteza mowy (TTS)")
tts_language = st.radio("Wybierz język", ["en", "pl"], format_func=lambda x: languages[x], key="tts_language")

text_input = st.text_area("Wpisz tekst do syntezy mowy")

if st.button("🔊 Generuj mowę"):
    if text_input:
        response = requests.post("http://localhost:5000/synthesize", json={"text": text_input, "language": st.session_state.tts_language})

        if response.status_code == 200:
            output_audio_path = "output_speech.wav"
            with open(output_audio_path, "wb") as f:
                f.write(response.content)

            st.audio(output_audio_path)
        else:
            st.error("Błąd w syntezie mowy.")
    else:
        st.warning("Wpisz tekst!")