"""Google Cloud Run handler for clip extraction."""

import json
import os
from pathlib import Path
from flask import Flask, request, jsonify
from google.cloud import storage

from src.orchestrator import ClipExtractor


app = Flask(__name__)
storage_client = storage.Client()


@app.route('/extract', methods=['POST'])
def extract_clips():
    """
    Cloud Run endpoint.

    Expected JSON payload:
    {
        "bucket": "my-bucket",
        "key": "path/to/video.mp4",
        "transcript_key": "path/to/transcript.txt",  # optional
        "output_key": "path/to/output.json",
        "num_clips": 5,  # optional
        "min_duration": 30,  # optional
        "max_duration": 60   # optional
    }
    """
    try:
        # Parse request
        data = request.get_json()

        bucket_name = data.get('bucket')
        video_key = data.get('key')
        transcript_key = data.get('transcript_key')
        output_key = data.get('output_key', 'clips.json')

        if not bucket_name or not video_key:
            return jsonify({'error': 'Missing bucket or key'}), 400

        bucket = storage_client.bucket(bucket_name)

        # Download video
        local_video_path = f"/tmp/{Path(video_key).name}"
        print(f"Downloading {video_key} from {bucket_name}")
        blob = bucket.blob(video_key)
        blob.download_to_filename(local_video_path)

        # Download transcript if provided
        local_transcript_path = None
        if transcript_key:
            local_transcript_path = f"/tmp/{Path(transcript_key).name}"
            print(f"Downloading transcript {transcript_key}")
            transcript_blob = bucket.blob(transcript_key)
            transcript_blob.download_to_filename(local_transcript_path)

        # Initialize extractor
        extractor = ClipExtractor()

        # Apply custom settings
        if 'num_clips' in data:
            extractor.config['general']['num_clips'] = data['num_clips']
        if 'min_duration' in data:
            extractor.config['general']['min_clip_duration'] = data['min_duration']
        if 'max_duration' in data:
            extractor.config['general']['max_clip_duration'] = data['max_duration']

        # Extract clips
        print("Extracting clips...")
        clips = extractor.extract_clips(
            input_path=local_video_path,
            transcript_path=local_transcript_path
        )

        # Upload results
        result_json = json.dumps(clips, indent=2)
        print(f"Uploading results to {output_key}")
        output_blob = bucket.blob(output_key)
        output_blob.upload_from_string(result_json, content_type='application/json')

        # Cleanup
        os.remove(local_video_path)
        if local_transcript_path:
            os.remove(local_transcript_path)

        return jsonify({
            'message': 'Success',
            'clips': clips,
            'output_location': f"gs://{bucket_name}/{output_key}"
        })

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
