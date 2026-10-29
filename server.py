from flask import Flask, request, send_from_directory
from werkzeug import secure_filename
import os
import time 

app = Flask(__name__)
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "upload")
RELEASES      = os.path.join(BASE_DIR, "releases")
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if not file.filename:
        return "No selected file", 400

    # Sanitize client-supplied name, then never trust it for the final path
    safe_name = secure_filename(file.filename)
    if not safe_name:
        return "Invalid filename", 400

    # Preserve every exfil: received_<unix_ts>_<safe_name>
    dest_name = f"received_{int(time.time())}_{safe_name}"
    dest = os.path.join(UPLOAD_FOLDER, dest_name)

    # Belt-and-suspenders: ensure resolved path stays inside UPLOAD_FOLDER
    if os.path.commonpath([os.path.abspath(dest), UPLOAD_FOLDER]) != UPLOAD_FOLDER:
        return "Invalid path", 400

    file.save(dest)
    return "File uploaded successfully", 200


@app.route("/latest.json")
def manifest():
    return send_from_directory(RELEASES, "latest.json")

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(RELEASES, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)