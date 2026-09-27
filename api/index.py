from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download_reel():
    try:
        data = request.get_json() or {}
        url = data.get('url')
        
        if not url:
            return jsonify({"success": False, "error": "Instagram URL is required."}), 400
        
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        # Optional: Handle cookies if Instagram blocks unauthenticated requests
        cookies_content = os.environ.get('INSTA_COOKIES')
        if cookies_content:
            cookie_file_path = '/tmp/cookies.txt'
            with open(cookie_file_path, 'w') as f:
                f.write(cookies_content)
            ydl_opts['cookiefile'] = cookie_file_path

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
        error_msg = str(e)
        if "login required" in error_msg.lower() or "empty media response" in error_msg.lower():
            error_msg = "Instagram is blocking cloud server requests. Please configure cookies (see instructions below)."
        return jsonify({"success": False, "error": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)