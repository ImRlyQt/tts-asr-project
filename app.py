from flask import Flask, request, jsonify, send_file
import whisper
from TTS.api import TTS
import os

app = Flask(__name__)

# Załaduj model Whisper
whisper_model = whisper.load_model("base")

# Modele TTS dla języków
tts_models = {
    "en": "tts_models/en/ljspeech/tacotron2-DDC",
    "pl": "tts_models/pl/mai_female/vits"
}

# Załaduj model domyślnie na angielski
tts_model = TTS(tts_models["en"]).to("cpu")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    """Rozpoznawanie mowy z pliku audio"""
    if "file" not in request.files:
        return jsonify({"error": "Brak pliku audio"}), 400

    file = request.files["file"]
    language = request.form.get("language", "en")  # Domyślnie angielski
    filepath = "temp_audio.wav"
    file.save(filepath)

    # Przetwarzanie audio przez Whisper
    result = whisper_model.transcribe(filepath, language=language)
    os.remove(filepath)

    return jsonify({"transcription": result["text"]})


@app.route("/synthesize", methods=["POST"])
def synthesize_speech():
    """Zamiana tekstu na mowę"""
    data = request.get_json()
    if not data or "text" not in data or "language" not in data:
        return jsonify({"error": "Brak tekstu lub języka"}), 400
    
    text = data["text"]
    language = data["language"]

     # Wybierz odpowiedni model TTS
    if language not in tts_models:
        return jsonify({"error": "Nieobsługiwany język"}), 400
    
    tts_model = TTS(tts_models[language]).to("cpu")
    output_path = "output_speech.wav"

    # Generowanie mowy
    tts_model.tts_to_file(text=text, file_path=output_path)

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
