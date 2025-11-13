# Usage Guide

Comprehensive guide for using the Multimodal Clip Extractor.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Options](#advanced-options)
3. [Configuration](#configuration)
4. [Cloud Usage](#cloud-usage)
5. [API Reference](#api-reference)

## Basic Usage

### Command Line Interface

#### Process a video file

```bash
python main.py --input video.mp4 --output clips.json
```

#### Process audio with transcript

```bash
python main.py --input audio.mp3 --transcript transcript.txt --output clips.json
```

#### Export clips as separate videos

```bash
python main.py --input video.mp4 --export-clips ./output_clips
```

### Python API

```python
from src.orchestrator import ClipExtractor

# Initialize
extractor = ClipExtractor()

# Extract clips
clips = extractor.extract_clips(
    input_path="video.mp4",
    output_path="clips.json"
)

# Print results
for clip in clips:
    print(f"{clip['title']}: {clip['start_time']} - {clip['end_time']}")
```

## Advanced Options

### Customize Clip Parameters

```bash
# Extract 10 clips, each 45-90 seconds
python main.py --input video.mp4 \
  --num-clips 10 \
  --min-duration 45 \
  --max-duration 90
```

### Disable Specific Modalities

```bash
# Audio and text only (no visual analysis)
python main.py --input video.mp4 --no-visual

# Text only
python main.py --input video.mp4 --no-audio --no-visual
```

### Custom Configuration

```bash
# Use custom config file
python main.py --input video.mp4 --config my_config.yaml
```

## Configuration

### Config File Structure

Edit `config/config.yaml` to customize behavior:

```yaml
general:
  num_clips: 5
  min_clip_duration: 30
  max_clip_duration: 60

audio:
  enabled: true
  emotion:
    mfcc_coefficients: 13

text:
  enabled: true
  model: "distilbert-base-uncased"

visual:
  enabled: true
  sampling:
    fps: 1

fusion:
  strategy: "weighted"
  weights:
    audio: 0.35
    text: 0.40
    visual: 0.25
```

### Environment Variables

Override config with environment variables:

```bash
export CLIP_EXTRACTOR_NUM_CLIPS=3
export CLIP_EXTRACTOR_MIN_DURATION=45
export CLIP_EXTRACTOR_MAX_DURATION=75

python main.py --input video.mp4
```

## Cloud Usage

### AWS Lambda

#### Deploy

```bash
cd deployment/aws
./deploy.sh
```

#### Invoke

```bash
aws lambda invoke \
  --function-name clip-extractor \
  --payload '{
    "bucket": "my-bucket",
    "key": "videos/input.mp4",
    "output_key": "results/clips.json",
    "num_clips": 5
  }' \
  response.json
```

#### Python SDK

```python
import boto3
import json

lambda_client = boto3.client('lambda')

response = lambda_client.invoke(
    FunctionName='clip-extractor',
    Payload=json.dumps({
        'bucket': 'my-bucket',
        'key': 'videos/input.mp4',
        'output_key': 'results/clips.json'
    })
)

result = json.loads(response['Payload'].read())
print(result)
```

### Google Cloud Run

#### Deploy

```bash
cd deployment/gcp
./deploy.sh
```

#### Invoke

```bash
curl -X POST https://clip-extractor-xxx.run.app/extract \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "bucket": "my-bucket",
    "key": "videos/input.mp4",
    "output_key": "results/clips.json",
    "num_clips": 5
  }'
```

### Azure Container Instances

#### Deploy

```bash
cd deployment/azure
./deploy.sh
```

#### Use

```bash
# Upload video to Azure Storage
az storage blob upload \
  --account-name clipextractorstorage \
  --container-name videos \
  --name input.mp4 \
  --file video.mp4

# Run container with video path
az container exec \
  --resource-group clip-extractor-rg \
  --name clip-extractor \
  --exec-command "python main.py --input /mnt/videos/input.mp4"
```

## API Reference

### ClipExtractor

Main orchestrator class.

#### `__init__(config_path: Optional[str] = None)`

Initialize the extractor.

**Parameters:**
- `config_path`: Path to custom config YAML (optional)

#### `extract_clips(input_path: str, transcript_path: Optional[str] = None, output_path: Optional[str] = None) -> List[Dict]`

Extract clips from video/audio.

**Parameters:**
- `input_path`: Path to video or audio file
- `transcript_path`: Path to transcript file (optional)
- `output_path`: Path to save results JSON (optional)

**Returns:**
- List of clip dictionaries with metadata

**Clip Dictionary Format:**
```python
{
    'start_time': '04:12',      # MM:SS format
    'end_time': '04:45',
    'title': 'Amazing Insight!',
    'score': 0.92,              # Overall score (0-1)
    'audio_score': 0.89,        # Audio emotion score
    'text_score': 0.95,         # Text topic score
    'visual_score': 0.92,       # Visual engagement score
    'duration': 33.0            # Duration in seconds
}
```

#### `export_clips(input_path: str, clips: List[Dict], output_dir: str)`

Export clips as separate video files.

**Parameters:**
- `input_path`: Original video file path
- `clips`: List of clips from extract_clips()
- `output_dir`: Directory to save clip files

### EmotionDetector

Audio emotion detection.

#### `analyze(audio_path: str) -> List[Dict]`

Analyze audio for emotional intensity.

**Returns:**
- List of time-stamped emotion scores

### TopicAnalyzer

Text topic analysis.

#### `analyze(transcript: str, timestamps: List[Dict] = None) -> List[Dict]`

Analyze transcript for topics and keywords.

**Returns:**
- List of time-stamped topic scores

### EngagementDetector

Visual engagement detection.

#### `analyze(video_path: str) -> List[Dict]`

Analyze video for visual engagement.

**Returns:**
- List of time-stamped engagement scores

## Output Format

### JSON Output

```json
[
  {
    "start_time": "04:12",
    "end_time": "04:45",
    "title": "The Crazy Secret to Low-Cost AI! 🤯",
    "score": 0.92,
    "audio_score": 0.89,
    "text_score": 0.95,
    "visual_score": 0.92,
    "duration": 33.0
  },
  {
    "start_time": "12:34",
    "end_time": "13:08",
    "title": "Why This Changes Everything",
    "score": 0.87,
    "audio_score": 0.84,
    "text_score": 0.91,
    "visual_score": 0.86,
    "duration": 34.0
  }
]
```

## Performance Tips

### Speed Up Processing

1. **Reduce video resolution**: Pre-process video to 720p or lower
2. **Disable visual analysis**: Use `--no-visual` for audio/podcasts
3. **Lower sampling rate**: Edit config to reduce FPS
4. **Use shorter clips**: Process in chunks for long videos

### Optimize Memory

1. **Close other applications**: Free up RAM
2. **Process in chunks**: Split long videos
3. **Use minimal dependencies**: Install requirements-minimal.txt
4. **Increase swap**: If on Linux, increase swap space

### Improve Accuracy

1. **Provide transcript**: Manual transcripts are more accurate
2. **Adjust thresholds**: Tune config.yaml thresholds
3. **Use full requirements**: Install all dependencies
4. **Higher sampling rate**: Process more frames (slower)

## Troubleshooting

### Common Issues

#### "FFmpeg not found"

**Solution**: Install FFmpeg and ensure it's in PATH

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

#### "Out of memory"

**Solution**: Reduce memory usage

```bash
# Use audio-only
python main.py --input video.mp4 --no-visual

# Or process smaller files
ffmpeg -i large_video.mp4 -t 300 small_video.mp4  # First 5 minutes
```

#### "No clips found"

**Solution**: Lower thresholds in config.yaml

```yaml
fusion:
  ranking:
    min_score: 0.3  # Lower from 0.5
```

#### "Processing too slow"

**Solution**: Optimize settings

```yaml
visual:
  sampling:
    fps: 0.5  # Process every 2 seconds instead of every second
```

## Best Practices

### Input Preparation

1. **Audio Quality**: Use good audio quality for best emotion detection
2. **Video Quality**: 720p is sufficient; 4K is overkill
3. **Transcript**: Provide clean transcripts when available
4. **File Size**: Split very large files (>2 hours) into chunks

### Configuration Tuning

1. **Start with defaults**: Test with default config first
2. **Adjust gradually**: Change one parameter at a time
3. **Test and iterate**: Process sample clips to tune settings
4. **Document changes**: Keep notes on what works

### Production Deployment

1. **Use cloud storage**: Store videos in S3/GCS/Azure
2. **Set up monitoring**: Track processing times and errors
3. **Implement retries**: Handle transient failures
4. **Cache results**: Store processed clips metadata

## Examples

See the `examples/` directory for more detailed examples:

- `example_usage.py` - Python API examples
- `sample_transcript.txt` - Example transcript format
- `README.md` - Additional examples and tips

## Support

For issues, questions, or contributions:

- GitHub Issues: https://github.com/asquitt/super-duper-octo-broccoli/issues
- Documentation: README.md, INSTALL.md
- Examples: examples/ directory
