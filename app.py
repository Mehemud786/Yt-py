from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

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

@app.route("/start-download", methods=["POST"])
def start_download():
    url = request.form.get("url")
    format_type = request.form.get("format_type", "720")
    
    if not url:
        return jsonify({"success": False, "message": "No URL provided."})
    
    try:
        # Extract direct playable stream URL to avoid serverless timeout & missing ffmpeg error
        ydl_opts = {'format': 'best' if format_type != "audio_320" else 'bestaudio'}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_url = info.get("url")
            
        if download_url:
            return jsonify({
                "success": True, 
                "download_url": download_url,
                "message": "Link generated successfully!"
            })
        else:
            return jsonify({"success": False, "message": "Could not extract media stream."})
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)