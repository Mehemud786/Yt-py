from flask import Flask, request, jsonify
from flask_cors import CORS
from pytubefix import YouTube

app = Flask(__name__)
CORS(app)

@app.route('/api/info', methods=['POST'])
def get_video_info():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
        
    try:
        # Initialize pytubefix YouTube object
        yt = YouTube(url)
        streams = []
        
        # Collect progressive MP4 streams available
        for stream in yt.streams.filter(file_extension='mp4', progressive=True):
            streams.append({
                'resolution': stream.resolution,
                'file_extension': stream.subtype,
                'url': stream.url
            })
            
        # Get audio-only format stream (.m4a)
        audio_stream = yt.streams.get_audio_only()
        audio_url = audio_stream.url if audio_stream else None
        
        return jsonify({
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'author': yt.author,
            'streams': streams,
            'audio_url': audio_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)