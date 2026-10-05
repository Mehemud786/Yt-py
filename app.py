from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

DOWNLOAD_DIR = "/data/data/com.termux/files/home/storage/shared/Download"

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        url = request.form.get("url")
        format_type = request.form.get("format_type", "720")
        
        if url:
            try:
                output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
                
                # Check if audio extraction was selected
                if format_type == "audio_320":
                    command = [
                        "yt-dlp",
                        "-x",
                        "--audio-format", "mp3",
                        "--audio-quality", "320k",
                        "-P", output_template,
                        url
                    ]
                    success_msg = "MP3 (320kbps) downloaded successfully! Check your phone's Download folder."
                else:
                    # Video resolution formatting
                    format_string = f"bestvideo[height<={format_type}]+bestaudio/best[height<={format_type}]"
                    command = [
                        "yt-dlp",
                        "-f", format_string,
                        "-P", output_template,
                        url
                    ]
                    success_msg = f"Download successful ({format_type}p video)! Check your phone's Download folder."
                
                subprocess.run(command, check=True)
                message = success_msg
            except Exception as e:
                message = f"Error processing request: {str(e)}"
                
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)