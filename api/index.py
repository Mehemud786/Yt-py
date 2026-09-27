import os
import traceback
from flask import Flask, render_template, request, jsonify
from pytubefix import YouTube

# Safely point Flask to the local templates folder inside the api directory
basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, 'templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    data = request.get_json() or {}
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
        
    try:
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
        streams = []
        for stream in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution'):
            if stream.resolution:
                streams.append({
                    'resolution': stream.resolution,
                    'url': stream.url
                })
                
        return jsonify({
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'streams': streams
        })
    except Exception as e:
        err_msg = str(e)
        print(traceback.format_exc())
        
        if "Sign in to confirm" in err_msg or "bot" in err_msg.lower():
            return jsonify({
                'error': 'YouTube blocked Vercel’s server IP (Bot detection). Try hosting this locally or on a standard VPS.'
            }), 400
            
        return jsonify({'error': f'Failed to fetch video: {err_msg}'}), 400

if __name__ == '__main__':
    app.run(debug=True)