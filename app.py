from flask import Flask, render_template, request, jsonify
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

DOWNLOAD_DIR = "/storage/emulated/0/Download"
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
        # Bypass cookies by specifying the mobile client extractor argument
        ydl_opts = {
            'extract_flat': False, 
            'skip_download': True,
            'extractor_args': {'youtube': {'player_client': ['mweb', 'android']}}
        }
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

@app.route("/start-download", methods=["POST"])
def start_download():
    url = request.form.get("url")
    format_type = request.form.get("format_type", "720")
    
    if not url:
        return jsonify({"success": False, "message": "No URL provided."})
    
    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
        
        ydl_opts = {
            'outtmpl': output_template,
            'newline': True,
            'extractor_args': {'youtube': {'player_client': ['mweb', 'android']}}
        }
        
        if format_type == "audio_320":
            ydl_opts['format'] = 'bestaudio'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }]
        else:
            ydl_opts['format'] = f"bestvideo[height<={format_type}]+bestaudio/best[height<={format_type}]"
            
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        download_status["progress"] = 100
        download_status["status"] = "Download completed successfully!"
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/progress", methods=["GET"])
def progress():
    return jsonify(download_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)