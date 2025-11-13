# Quick Start Guide

Get started with the Multimodal Clip Extractor in 5 minutes.

## Installation (2 minutes)

### Step 1: Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Step 2: Install Python Dependencies

```bash
# Minimal installation (faster, for testing)
pip install -r requirements-minimal.txt

# OR full installation (includes all features)
pip install -r requirements.txt
```

## Basic Usage (3 minutes)

### Example 1: Extract Clips from Video

```bash
python main.py --input video.mp4 --output clips.json
```

**Output:**
```json
[
  {
    "start_time": "04:12",
    "end_time": "04:45",
    "title": "The Crazy Secret to Low-Cost AI! 🤯",
    "score": 0.92
  }
]
```

### Example 2: With Custom Parameters

```bash
python main.py \
  --input video.mp4 \
  --num-clips 10 \
  --min-duration 30 \
  --max-duration 60 \
  --output results.json
```

### Example 3: Export Video Clips

```bash
python main.py \
  --input video.mp4 \
  --export-clips ./clips_folder
```

This creates separate video files:
- `clips_folder/clip_01_04-12.mp4`
- `clips_folder/clip_02_12-34.mp4`
- etc.

## Docker Usage (Alternative)

### Build and Run

```bash
# Build image
docker build -t clip-extractor .

# Create directories
mkdir input output

# Place your video
cp video.mp4 input/

# Run
docker run \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  clip-extractor \
  --input /input/video.mp4 \
  --output /output/clips.json
```

## Testing Without Video

Use the example transcript:

```bash
# Create a test audio file (requires ffmpeg)
ffmpeg -f lavfi -i "sine=frequency=1000:duration=60" test_audio.wav

# Process with example transcript
python main.py \
  --input test_audio.wav \
  --transcript examples/sample_transcript.txt \
  --output test_clips.json
```

## Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--input` | Video/audio file | `--input video.mp4` |
| `--transcript` | Transcript file | `--transcript transcript.txt` |
| `--output` | Output JSON file | `--output clips.json` |
| `--num-clips` | Number of clips | `--num-clips 5` |
| `--min-duration` | Min clip seconds | `--min-duration 30` |
| `--max-duration` | Max clip seconds | `--max-duration 60` |
| `--export-clips` | Export directory | `--export-clips ./output` |
| `--no-audio` | Disable audio analysis | `--no-audio` |
| `--no-text` | Disable text analysis | `--no-text` |
| `--no-visual` | Disable visual analysis | `--no-visual` |

## Troubleshooting

### Error: "FFmpeg not found"

**Solution:** Install FFmpeg and ensure it's in your PATH

```bash
ffmpeg -version  # Should show version info
```

### Error: "Out of memory"

**Solution:** Disable visual analysis for audio-only content

```bash
python main.py --input audio.mp3 --no-visual
```

### Error: "No clips found"

**Solution:** Lower the score threshold in `config/config.yaml`

```yaml
fusion:
  ranking:
    min_score: 0.3  # Lower from default 0.5
```

## Next Steps

1. **Read full documentation:** See [README.md](README.md)
2. **Customize configuration:** Edit [config/config.yaml](config/config.yaml)
3. **Try examples:** Check [examples/](examples/)
4. **Deploy to cloud:** See [deployment/](deployment/)

## Getting Help

- **Documentation:** README.md, INSTALL.md, USAGE.md
- **Issues:** https://github.com/asquitt/super-duper-octo-broccoli/issues
- **Examples:** examples/ directory

---

**Ready to extract clips?**

```bash
python main.py --input your_video.mp4 --output clips.json
```

That's it! 🎉
