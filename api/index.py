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
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
        
    try:
        # Initialize pytubefix
        yt = YouTube(url)
        
        streams = []
        # Fetch progressive streams
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
        # Print full error traceback to Vercel logs for debugging
        error_details = traceback.format_exc()
        print(error_details)
        return jsonify({'error': f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)