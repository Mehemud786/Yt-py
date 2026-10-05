from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import os
import re
from yt_dlp import YoutubeDL

app = Flask(__name__)

DOWNLOAD_DIR = "/data/data/com.termux/files/home/storage/shared/Download"

download_status = {"progress": 0, "status": "Idle"}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/get-info", methods=["POST"])
def get_info():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"success": False, "message": "No URL provided."})
    
    try:
        ydl_opts = {'extract_flat': False, 'skip_download': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "success": True,
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration_string", "")
            })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

def run_download(url, format_type):
    global download_status
    download_status["progress"] = 0
    download_status["status"] = "Starting..."
    
    try:
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
        
        if format_type == "audio_320":
            command = [
                "yt-dlp", "--newline", "-x",
                "--audio-format", "mp3", "--audio-quality", "320k",
                "-P", output_template, url
            ]
        else:
            format_string = f"bestvideo[height<={format_type}]+bestaudio/best[height<={format_type}]"
            command = [
                "yt-dlp", "--newline", "-f", format_string,
                "-P", output_template, url
            ]
            
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
        )
        
        for line in process.stdout:
            match = re.search(r'(\d+\.\d+)%', line)
            if match:
                percent = float(match.group(1))
                download_status["progress"] = percent
                download_status["status"] = f"Downloading... {percent}%"
                
        process.wait()
        if process.returncode == 0:
            download_status["progress"] = 100
            download_status["status"] = "Download completed successfully!"
        else:
            download_status["status"] = "Download encountered an error."
    except Exception as e:
        download_status["status"] = f"Error: {str(e)}"

@app.route("/start-download", methods=["POST"])
def start_download():
    url = request.form.get("url")
    format_type = request.form.get("format_type", "720")
    if url:
        threading.Thread(target=run_download, args=(url, format_type)).start()
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route("/progress", methods=["GET"])
def progress():
    return jsonify(download_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)