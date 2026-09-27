from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__, static_folder='../public', template_folder='../public')

@app.route('/')
def serve_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/download', methods=['POST'])
def download_reel():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"success": False, "error": "Instagram URL is required."}), 400
        
        # Configure yt-dlp to extract the direct video URL without downloading locally
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'Instagram Reel')
            thumbnail = info.get('thumbnail')
            
        return jsonify({
            "success": True,
            "download_url": video_url,
            "title": title,
            "thumbnail": thumbnail
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)