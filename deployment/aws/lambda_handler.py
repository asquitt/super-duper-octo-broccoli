"""AWS Lambda handler for clip extraction."""

import json
import os
import boto3
from pathlib import Path

from src.orchestrator import ClipExtractor


s3_client = boto3.client('s3')


def handler(event, context):
    """
    AWS Lambda handler.

    Expected event format:
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
        # Parse event
        bucket = event.get('bucket')
        video_key = event.get('key')
        transcript_key = event.get('transcript_key')
        output_key = event.get('output_key', 'clips.json')

        if not bucket or not video_key:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing bucket or key'})
            }

        # Download video from S3
        local_video_path = f"/tmp/{Path(video_key).name}"
        print(f"Downloading {video_key} from {bucket}")
        s3_client.download_file(bucket, video_key, local_video_path)

        # Download transcript if provided
        local_transcript_path = None
        if transcript_key:
            local_transcript_path = f"/tmp/{Path(transcript_key).name}"
            print(f"Downloading transcript {transcript_key}")
            s3_client.download_file(bucket, transcript_key, local_transcript_path)

        # Initialize extractor
        extractor = ClipExtractor()

        # Apply custom settings from event
        if 'num_clips' in event:
            extractor.config['general']['num_clips'] = event['num_clips']
        if 'min_duration' in event:
            extractor.config['general']['min_clip_duration'] = event['min_duration']
        if 'max_duration' in event:
            extractor.config['general']['max_clip_duration'] = event['max_duration']

        # Extract clips
        print("Extracting clips...")
        clips = extractor.extract_clips(
            input_path=local_video_path,
            transcript_path=local_transcript_path
        )

        # Upload results to S3
        result_json = json.dumps(clips, indent=2)
        print(f"Uploading results to {output_key}")
        s3_client.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=result_json,
            ContentType='application/json'
        )

        # Cleanup
        os.remove(local_video_path)
        if local_transcript_path:
            os.remove(local_transcript_path)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Success',
                'clips': clips,
                'output_location': f"s3://{bucket}/{output_key}"
            })
        }

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
