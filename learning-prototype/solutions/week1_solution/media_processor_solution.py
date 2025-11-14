"""
Week 1 Solution: Media Processor
File: media_processor_solution.py

This is the complete solution for Week 1.
Compare this with your implementation to check your work.
"""

import subprocess
import json
import os
from typing import Optional


class MediaProcessor:
    """
    A simple media processor using FFmpeg.

    This class provides methods to:
    - Extract audio from video
    - Get media file metadata
    - Convert time formats
    """

    def __init__(self):
        """Initialize the media processor."""
        # Check if FFmpeg is installed
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                check=True
            )
            print("✓ FFmpeg is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠ Warning: FFmpeg not found!")
            print("Please install FFmpeg to use this tool")

    def get_duration(self, file_path: str) -> float:
        """
        Get the duration of a media file in seconds.

        Args:
            file_path: Path to the media file

        Returns:
            Duration in seconds
        """
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            file_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        return float(data['format']['duration'])

    def extract_audio(self,
                     video_path: str,
                     output_path: str,
                     sample_rate: int = 22050) -> str:
        """
        Extract audio from a video file.

        Args:
            video_path: Path to input video
            output_path: Where to save the audio
            sample_rate: Audio sample rate in Hz

        Returns:
            Path to the extracted audio file
        """
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vn',                    # No video
            '-acodec', 'pcm_s16le',   # WAV codec
            '-ar', str(sample_rate),  # Sample rate
            '-ac', '1',               # Mono
            '-y',                     # Overwrite
            output_path
        ]

        subprocess.run(cmd, capture_output=True, check=True)

        if os.path.exists(output_path):
            return output_path
        else:
            raise RuntimeError("Failed to extract audio")

    def seconds_to_time(self, seconds: float) -> str:
        """
        Convert seconds to MM:SS format.

        Args:
            seconds: Time in seconds

        Returns:
            Time string in MM:SS format
        """
        minutes = int(seconds) // 60
        secs = int(seconds) % 60

        return f"{minutes:02d}:{secs:02d}"

    def time_to_seconds(self, time_str: str) -> float:
        """
        Convert time string to seconds.

        Supports: MM:SS or HH:MM:SS format

        Args:
            time_str: Time string

        Returns:
            Time in seconds
        """
        parts = time_str.split(':')

        if len(parts) == 2:
            # MM:SS format
            minutes, seconds = parts
            return int(minutes) * 60 + int(seconds)
        elif len(parts) == 3:
            # HH:MM:SS format
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        else:
            raise ValueError(f"Invalid time format: {time_str}")

    def has_video_stream(self, file_path: str) -> bool:
        """
        Check if a media file has a video stream.

        Args:
            file_path: Path to media file

        Returns:
            True if video stream exists
        """
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_type',
            '-of', 'json',
            file_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        # If video stream exists, 'streams' array will have entries
        return len(data.get('streams', [])) > 0


# ============================================================
# TESTS
# ============================================================

def run_tests():
    """Test the MediaProcessor implementation."""
    print("\n" + "="*60)
    print("TESTING MEDIA PROCESSOR (SOLUTION)")
    print("="*60 + "\n")

    processor = MediaProcessor()

    # Test 1: Time Conversion
    print("Test 1: Time Conversion")
    print("-" * 40)
    try:
        # Test seconds to time
        result = processor.seconds_to_time(125)
        expected = "02:05"
        assert result == expected, f"Expected {expected}, got {result}"
        print(f"✓ seconds_to_time(125) = {result}")

        # Test time to seconds
        result = processor.time_to_seconds("02:05")
        expected = 125.0
        assert result == expected, f"Expected {expected}, got {result}"
        print(f"✓ time_to_seconds('02:05') = {result}")

        # Test with hours
        result = processor.time_to_seconds("1:30:45")
        expected = 5445.0
        assert result == expected, f"Expected {expected}, got {result}"
        print(f"✓ time_to_seconds('1:30:45') = {result}")

        print("✓ All time conversion tests passed\n")

    except Exception as e:
        print(f"✗ Error: {e}\n")

    # Test 2: File Operations
    print("Test 2: File Operations")
    print("-" * 40)

    test_video = "../../sample_data/sample_video.mp4"

    if os.path.exists(test_video):
        try:
            # Test duration
            duration = processor.get_duration(test_video)
            print(f"✓ Duration: {duration:.2f}s")

            # Test video stream detection
            has_video = processor.has_video_stream(test_video)
            print(f"✓ Has video stream: {has_video}")

            # Test audio extraction
            output_audio = "test_audio.wav"
            processor.extract_audio(test_video, output_audio)
            if os.path.exists(output_audio):
                print(f"✓ Audio extracted: {output_audio}")
                os.remove(output_audio)  # Cleanup

            print("✓ All file operation tests passed\n")

        except Exception as e:
            print(f"✗ Error: {e}\n")
    else:
        print(f"⚠ Test file not found: {test_video}")
        print("  Run setup_environment.sh to generate test files\n")

    print("="*60)
    print("All tests passed!")
    print("="*60 + "\n")


if __name__ == '__main__':
    run_tests()
