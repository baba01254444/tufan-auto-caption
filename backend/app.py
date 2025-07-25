from flask import Flask, request, jsonify
import os
import whisper
import uuid

app = Flask(__name__)
model = whisper.load_model("base")

@app.route("/process", methods=["POST"])
def process():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files["video"]
    filename = f"temp_{uuid.uuid4().hex}.mp4"
    video.save(filename)

    result = model.transcribe(filename)
    os.remove(filename)

    return jsonify({"text": result["text"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
