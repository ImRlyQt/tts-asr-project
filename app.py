from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)

# Załaduj model Whisper
model = whisper.load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "Brak pliku audio"}), 400

    file = request.files["file"]
    filepath = os.path.join("temp_audio.wav")
    file.save(filepath)

    # Przetwarzanie audio przez Whisper
    result = model.transcribe(filepath)

    # Usuwanie pliku po przetworzeniu
    os.remove(filepath)

    return jsonify({"transcription": result["text"]})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
