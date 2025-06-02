from flask import Flask, request
import speech_recognition as sr
from pydub import AudioSegment
import os
import uuid

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_audio():
    if 'audio' not in request.files:
        return "No audio file provided", 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return "No selected file", 400

    # Generate temp filenames
    webm_path = f"temp_{uuid.uuid4()}.webm"
    wav_path = f"temp_{uuid.uuid4()}.wav"

    try:
        audio_file.save(webm_path)

        # Convert .webm to .wav using pydub (requires ffmpeg)
        sound = AudioSegment.from_file(webm_path, format="webm")
        sound.export(wav_path, format="wav")

        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print("📝 You said:", text)

        return {"transcription": text}, 200

    except sr.UnknownValueError:
        return "Could not understand audio", 400
    except Exception as e:
        print("❌ Error:", e)
        return "Internal server error", 500
    finally:
        if os.path.exists(webm_path): os.remove(webm_path)
        if os.path.exists(wav_path): os.remove(wav_path)

if __name__ == "__main__":
    app.run(debug=True)
