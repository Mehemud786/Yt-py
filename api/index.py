import os
from flask import Flask, render_template, request, jsonify
from pytubefix import YouTube

# Get absolute path to the project root for templates
basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, '../templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
        
    try:
        yt = YouTube(url)
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
        return jsonify({'error': str(e)}), 500