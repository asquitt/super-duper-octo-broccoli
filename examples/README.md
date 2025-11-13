# Examples

This directory contains example usage and sample files for the Multimodal Clip Extractor.

## Files

- `example_usage.py` - Python examples showing different use cases
- `sample_transcript.txt` - Sample transcript file format
- `sample_transcript.srt` - Sample SRT subtitle format

## Quick Start

### 1. Basic Usage

```python
from src.orchestrator import ClipExtractor

extractor = ClipExtractor()
clips = extractor.extract_clips(
    input_path="video.mp4",
    output_path="clips.json"
)
```

### 2. With Transcript

```python
clips = extractor.extract_clips(
    input_path="video.mp4",
    transcript_path="transcript.txt",
    output_path="clips.json"
)
```

### 3. Export Clips

```python
extractor.export_clips(
    input_path="video.mp4",
    clips=clips,
    output_dir="./output_clips"
)
```

## Sample Transcript Formats

### Plain Text (transcript.txt)

```
This is the first sentence of the transcript.
This is the second sentence.
And so on...
```

### SRT Format (transcript.srt)

```
1
00:00:00,000 --> 00:00:05,000
This is the first subtitle.

2
00:00:05,000 --> 00:00:10,000
This is the second subtitle.
```

## Testing Locally

For testing without a real video file:

1. Download a sample video (Creative Commons licensed)
2. Place it in the `examples/` directory
3. Run the examples:

```bash
cd examples
python example_usage.py
```

## Cloud Examples

See `deployment/` directory for cloud-specific examples:

- AWS Lambda
- Google Cloud Run
- Azure Container Instances
