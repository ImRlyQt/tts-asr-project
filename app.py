from flask import Flask, request, jsonify, send_file
import whisper
from TTS.api import TTS
import os

app = Flask(__name__)

# Załaduj model Whisper
whisper_model = whisper.load_model("base")

# Załaduj model Coqui TTS
tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC").to("cpu")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "Brak pliku audio"}), 400

    file = request.files["file"]
    filepath = os.path.join("temp_aud.wav")
    file.save(filepath)

    # Przetwarzanie audio przez Whisper
    result = whisper_model.transcribe(filepath)

    # Usuwanie pliku po przetworzeniu
    os.remove(filepath)

    return jsonify({"transcription": result["text"]})


@app.route("/synthesize", methods=["POST"])
def synthesize_speech():
    """Zamiana tekstu na mowę"""
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Brak tekstu"}), 400

    text = data["text"]
    output_path = "output_speech.wav"

    # Ustawienie języka polskiego
    tts_model.tts_to_file(text=text, file_path=output_path)

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
