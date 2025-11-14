# Week 1: Foundations - Media Processing Basics

**Goal**: Understand media processing fundamentals and set up your development environment.

---

## 📚 Learning Objectives

By the end of this week, you will:
- ✅ Understand how media files are structured (audio, video, containers)
- ✅ Use FFmpeg to manipulate media files
- ✅ Extract audio from video files
- ✅ Get metadata (duration, format, codec)
- ✅ Set up a working development environment

---

## 🎯 What We're Building This Week

A simple media processor that can:
1. Extract audio from video files
2. Get video/audio metadata
3. Convert time formats (seconds ↔ HH:MM:SS)
4. Extract video frames

---

## 📖 Concepts to Understand

### 1. Media File Structure

```
Video File (e.g., MP4)
│
├── Container Format (MP4, AVI, MOV)
│   │
│   ├── Video Stream
│   │   ├── Codec (H.264, VP9, etc.)
│   │   └── Video Frames (images over time)
│   │
│   ├── Audio Stream
│   │   ├── Codec (AAC, MP3, etc.)
│   │   └── Audio Samples (waveform)
│   │
│   └── Metadata
│       ├── Duration
│       ├── Resolution
│       └── Bitrate
```

### 2. FFmpeg Basics

FFmpeg is a command-line tool for media processing:

```bash
# Get video info
ffmpeg -i video.mp4

# Extract audio
ffmpeg -i video.mp4 -vn -acodec pcm_s16le output.wav

# Extract frames
ffmpeg -i video.mp4 -vf fps=1 frame_%04d.jpg
```

**Key Flags:**
- `-i`: Input file
- `-vn`: No video (audio only)
- `-acodec`: Audio codec
- `-ar`: Audio sample rate
- `-ac`: Audio channels (1=mono, 2=stereo)
- `-vf`: Video filter
- `-y`: Overwrite output

### 3. Audio Basics

**Sample Rate**: Samples per second (Hz)
- CD quality: 44,100 Hz
- Speech: 16,000 Hz (sufficient)
- Our project: 22,050 Hz (good balance)

**Channels**:
- Mono: 1 channel (what we'll use)
- Stereo: 2 channels (L and R)

**Format**:
- WAV: Uncompressed (large, high quality)
- MP3: Compressed (smaller, lossy)
- We'll use WAV for processing

---

## 💻 Starter Code

### File: `media_processor.py`

```python
"""
Week 1 Starter Code: Media Processor
Your task: Implement the TODO sections
"""

import subprocess
import json
import os


class MediaProcessor:
    """Process media files using FFmpeg."""

    def __init__(self):
        """Initialize media processor."""
        # TODO: Check if FFmpeg is installed
        # Hint: Use subprocess.run(['ffmpeg', '-version'])
        pass

    def get_duration(self, file_path: str) -> float:
        """
        Get duration of media file in seconds.

        Args:
            file_path: Path to media file

        Returns:
            Duration in seconds

        Example:
            >>> processor = MediaProcessor()
            >>> duration = processor.get_duration("video.mp4")
            >>> print(f"Duration: {duration}s")
        """
        # TODO: Use ffprobe to get duration
        # Command: ffprobe -v error -show_entries format=duration -of json input.mp4
        # Hint: Use subprocess.run() and json.loads()

        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            file_path
        ]

        # YOUR CODE HERE
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])

    def extract_audio(self, video_path: str, output_path: str,
                     sample_rate: int = 22050) -> str:
        """
        Extract audio from video file.

        Args:
            video_path: Path to video file
            output_path: Where to save audio
            sample_rate: Audio sample rate (Hz)

        Returns:
            Path to extracted audio file

        Example:
            >>> processor = MediaProcessor()
            >>> audio = processor.extract_audio("video.mp4", "audio.wav")
        """
        # TODO: Use ffmpeg to extract audio
        # Command: ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 22050 -ac 1 -y audio.wav

        # YOUR CODE HERE
        # Hints:
        # - Use subprocess.run()
        # - Check if output file was created
        # - Return output_path

        pass

    def seconds_to_time(self, seconds: float) -> str:
        """
        Convert seconds to MM:SS format.

        Args:
            seconds: Time in seconds

        Returns:
            Time string in MM:SS format

        Example:
            >>> processor = MediaProcessor()
            >>> processor.seconds_to_time(125)
            '02:05'
        """
        # TODO: Implement time conversion
        # Hints:
        # - Use // for integer division
        # - Use % for remainder
        # - Format as MM:SS with leading zeros

        # YOUR CODE HERE
        pass

    def time_to_seconds(self, time_str: str) -> float:
        """
        Convert time string to seconds.

        Args:
            time_str: Time in HH:MM:SS or MM:SS format

        Returns:
            Time in seconds

        Example:
            >>> processor = MediaProcessor()
            >>> processor.time_to_seconds("02:05")
            125.0
        """
        # TODO: Implement time conversion
        # Hints:
        # - Split by ':'
        # - Handle both MM:SS and HH:MM:SS
        # - Convert to seconds

        # YOUR CODE HERE
        pass

    def has_video_stream(self, file_path: str) -> bool:
        """
        Check if file has a video stream.

        Args:
            file_path: Path to media file

        Returns:
            True if video stream exists

        Example:
            >>> processor = MediaProcessor()
            >>> processor.has_video_stream("video.mp4")
            True
            >>> processor.has_video_stream("audio.mp3")
            False
        """
        # TODO: Use ffprobe to detect video stream
        # Command: ffprobe -v error -select_streams v:0 -show_entries stream=codec_type -of json input.mp4

        # YOUR CODE HERE
        pass


# ============================================================
# TEST YOUR CODE
# ============================================================

def test_media_processor():
    """Test the media processor."""
    print("Testing MediaProcessor...")

    processor = MediaProcessor()

    # Test 1: Time conversion
    print("\nTest 1: Time Conversion")
    print(f"125 seconds = {processor.seconds_to_time(125)}")  # Should be 02:05
    print(f"02:05 = {processor.time_to_seconds('02:05')} seconds")  # Should be 125

    # Test 2: Duration (if you have a test file)
    # Uncomment and add your test file path
    # test_file = "path/to/your/test/video.mp4"
    # if os.path.exists(test_file):
    #     duration = processor.get_duration(test_file)
    #     print(f"\nTest 2: Duration = {duration}s")

    print("\n✓ Tests complete!")


if __name__ == '__main__':
    test_media_processor()
```

---

## ✏️ Exercises

### Exercise 1: FFmpeg Exploration

Create a file `exercise1_ffmpeg.sh`:

```bash
#!/bin/bash
# Exercise 1: Explore FFmpeg

# 1. Generate a test audio file (5 seconds, 440Hz tone)
echo "Generating test audio..."
# TODO: Add ffmpeg command to generate audio

# 2. Generate a test video file (5 seconds, test pattern)
echo "Generating test video..."
# TODO: Add ffmpeg command to generate video

# 3. Extract audio from the video
echo "Extracting audio..."
# TODO: Add ffmpeg command to extract audio

# 4. Get video information
echo "Getting video info..."
# TODO: Add ffprobe command to get info

echo "Complete!"
```

### Exercise 2: Python Media Info

Create `exercise2_media_info.py`:

```python
"""
Exercise 2: Get detailed media information
"""

import subprocess
import json


def get_media_info(file_path):
    """
    Get comprehensive media file information.

    TODO: Implement this function to return:
    - Duration
    - Format (container)
    - Video codec (if exists)
    - Audio codec (if exists)
    - Resolution (if video)
    - Bitrate
    """
    # YOUR CODE HERE
    pass


def print_media_info(file_path):
    """Print media info in a nice format."""
    info = get_media_info(file_path)

    print(f"\nMedia Information: {file_path}")
    print("=" * 50)
    # TODO: Print the information nicely


if __name__ == '__main__':
    # Test with your file
    test_file = "path/to/test/file.mp4"
    print_media_info(test_file)
```

---

## 🎯 Tasks for This Week

### Beginner Tasks
1. ✅ Install FFmpeg
2. ✅ Implement `seconds_to_time()`
3. ✅ Implement `time_to_seconds()`
4. ✅ Test with sample files

### Intermediate Tasks
5. ✅ Implement `get_duration()`
6. ✅ Implement `extract_audio()`
7. ✅ Implement `has_video_stream()`
8. ✅ Complete Exercise 1

### Advanced Tasks
9. ✅ Complete Exercise 2
10. ✅ Add error handling to all functions
11. ✅ Write unit tests
12. ✅ Create a CLI tool

---

## 📝 Notes

### Important Concepts

**Container vs Codec**:
- Container: How data is packaged (MP4, AVI, MOV)
- Codec: How data is compressed (H.264, AAC)
- Same container can have different codecs

**Sample Rate**:
- Higher = better quality, larger file
- 22,050 Hz is good for speech analysis
- Nyquist theorem: Must be 2x highest frequency

**Mono vs Stereo**:
- Mono (1 channel): Enough for most analysis
- Stereo (2 channels): Better for music
- We use mono to simplify processing

### Common FFmpeg Errors

1. **"command not found"**: FFmpeg not installed
2. **"Invalid argument"**: Check file path
3. **"No such file"**: File doesn't exist
4. **"Conversion failed"**: Codec issues

### Debugging Tips

```bash
# Check FFmpeg version
ffmpeg -version

# Get detailed file info
ffprobe -v error -show_format -show_streams input.mp4

# Test with a simple command
ffmpeg -f lavfi -i sine=frequency=1000:duration=5 test.wav
```

---

## 🔍 Testing Your Solution

Create `test_week1.py`:

```python
"""
Week 1 Test Suite
Run this to validate your implementation
"""

import os
from media_processor import MediaProcessor


def test_time_conversion():
    """Test time conversion functions."""
    processor = MediaProcessor()

    # Test seconds to time
    assert processor.seconds_to_time(0) == "00:00"
    assert processor.seconds_to_time(65) == "01:05"
    assert processor.seconds_to_time(125) == "02:05"

    # Test time to seconds
    assert processor.time_to_seconds("00:00") == 0
    assert processor.time_to_seconds("01:05") == 65
    assert processor.time_to_seconds("02:05") == 125

    print("✓ Time conversion tests passed")


def test_media_processing():
    """Test media processing (if test files available)."""
    # Add your tests here
    print("✓ Media processing tests passed")


if __name__ == '__main__':
    test_time_conversion()
    test_media_processing()
    print("\n✅ All Week 1 tests passed!")
```

---

## 📚 Resources

### Learn More:

1. **FFmpeg Documentation**: https://ffmpeg.org/documentation.html
2. **Audio Basics**: https://www.izotope.com/en/learn/digital-audio-basics-sample-rate-and-bit-depth.html
3. **Python subprocess**: https://docs.python.org/3/library/subprocess.html

### Sample Commands:

```bash
# Generate test audio (sine wave)
ffmpeg -f lavfi -i "sine=frequency=1000:duration=5" test.wav

# Generate test video (color pattern)
ffmpeg -f lavfi -i testsrc=duration=10:size=1280x720:rate=30 test.mp4

# Extract first 30 seconds
ffmpeg -i input.mp4 -t 30 -c copy first30.mp4

# Convert to different format
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
```

---

## ✅ Completion Checklist

Before moving to Week 2, ensure you can:

- [ ] Install and run FFmpeg commands
- [ ] Extract audio from video files
- [ ] Get video duration and metadata
- [ ] Convert between time formats
- [ ] Understand containers vs codecs
- [ ] Handle file paths correctly
- [ ] Run error-free code

---

## 🎓 Next Steps

Once you've completed Week 1:
1. Review your solution
2. Compare with provided solution
3. Make sure all tests pass
4. Move to **Week 2: Audio Emotion Detection**

---

**Ready for Week 2?** → `week2_audio.md`
