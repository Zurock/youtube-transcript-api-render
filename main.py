from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",               # standard watch URL
        r"youtu\.be/([a-zA-Z0-9_-]{11})",       # shortened URL
        r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})"  # shorts
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_url = request.args.get('url')
    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([item['text'] for item in transcript])
        return jsonify({'transcript': full_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
