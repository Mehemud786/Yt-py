import os
import traceback
from flask import Flask, render_template, request, jsonify
from pytubefix import YouTube

basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, '../templates')

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
        # Bypass potential client restrictions using a standard user agent
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
        
        streams = []
        # Filter progressive MP4 streams safely
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
        print(f"Error processing URL: {err_msg}")
        print(traceback.format_exc())
        
        # Friendly message if YouTube blocks Vercel's server IP
        if "Sign in to confirm" in err_msg or "bot" in err_msg.lower():
            return jsonify({
                'error': 'YouTube blocked this cloud server IP (Bot detection). Vercel serverless functions cannot reliably fetch YouTube streams. Consider hosting this on a local machine or a private VPS.'
            }), 400
            
        return jsonify({'error': f'Failed to fetch video: {err_msg}'}), 400

if __name__ == '__main__':
    app.run(debug=True)