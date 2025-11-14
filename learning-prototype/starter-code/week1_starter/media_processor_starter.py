"""
Week 1 Starter Code: Media Processor
File: media_processor_starter.py

INSTRUCTIONS:
1. Read through the code
2. Fill in the TODO sections
3. Run the tests at the bottom
4. Compare with solution when done

TIPS:
- Use subprocess.run() for FFmpeg commands
- Check return codes and handle errors
- Test with small files first
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
        # TODO: Check if FFmpeg is installed
        # Hint: Run 'ffmpeg -version' and check if it succeeds

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

        Example:
            >>> processor = MediaProcessor()
            >>> duration = processor.get_duration("video.mp4")
            >>> print(f"Video is {duration} seconds long")
        """
        # TODO: Use ffprobe to get duration
        #
        # Command structure:
        # ffprobe -v error -show_entries format=duration -of json input.mp4
        #
        # Steps:
        # 1. Build the command as a list
        # 2. Run it with subprocess.run()
        # 3. Parse the JSON output
        # 4. Extract and return the duration

        cmd = [
            'ffprobe',
            '-v', 'error',                    # Quiet mode
            '-show_entries', 'format=duration',  # Get duration
            '-of', 'json',                    # Output as JSON
            file_path
        ]

        # YOUR CODE HERE
        # Hint: result = subprocess.run(cmd, ...)
        # Hint: data = json.loads(result.stdout)
        # Hint: return float(data['format']['duration'])

        raise NotImplementedError("TODO: Implement get_duration()")

    def extract_audio(self,
                     video_path: str,
                     output_path: str,
                     sample_rate: int = 22050) -> str:
        """
        Extract audio from a video file.

        Args:
            video_path: Path to input video
            output_path: Where to save the audio
            sample_rate: Audio sample rate in Hz (default: 22050)

        Returns:
            Path to the extracted audio file

        Example:
            >>> processor = MediaProcessor()
            >>> audio_file = processor.extract_audio("video.mp4", "audio.wav")
            >>> print(f"Audio saved to: {audio_file}")
        """
        # TODO: Use ffmpeg to extract audio
        #
        # Command structure:
        # ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 22050 -ac 1 -y audio.wav
        #
        # Flags explained:
        # -i       : Input file
        # -vn      : No video (audio only)
        # -acodec  : Audio codec (pcm_s16le = uncompressed WAV)
        # -ar      : Audio sample rate
        # -ac      : Audio channels (1 = mono, 2 = stereo)
        # -y       : Overwrite output file if exists

        cmd = [
            'ffmpeg',
            '-i', video_path,
            # YOUR CODE HERE: Add the rest of the flags
        ]

        # Run the command
        # YOUR CODE HERE

        # Check if output file was created
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

        Example:
            >>> processor = MediaProcessor()
            >>> processor.seconds_to_time(125)
            '02:05'
            >>> processor.seconds_to_time(3665)
            '61:05'  # Note: Can exceed 60 minutes
        """
        # TODO: Implement time conversion
        #
        # Steps:
        # 1. Calculate minutes: seconds // 60
        # 2. Calculate remaining seconds: seconds % 60
        # 3. Format as "MM:SS" with leading zeros
        #
        # Hints:
        # - Use // for integer division
        # - Use % for modulo (remainder)
        # - Use f-string with :02d for zero-padding

        # YOUR CODE HERE
        minutes = 0  # Calculate this
        secs = 0     # Calculate this

        raise NotImplementedError("TODO: Implement seconds_to_time()")

    def time_to_seconds(self, time_str: str) -> float:
        """
        Convert time string to seconds.

        Supports: MM:SS or HH:MM:SS format

        Args:
            time_str: Time string (e.g., "02:05" or "1:30:45")

        Returns:
            Time in seconds

        Example:
            >>> processor = MediaProcessor()
            >>> processor.time_to_seconds("02:05")
            125.0
            >>> processor.time_to_seconds("1:30:45")
            5445.0
        """
        # TODO: Implement time conversion
        #
        # Steps:
        # 1. Split string by ':'
        # 2. Check how many parts (2 for MM:SS, 3 for HH:MM:SS)
        # 3. Convert each part to integer
        # 4. Calculate total seconds
        #
        # Hints:
        # - use .split(':')
        # - len(parts) tells you the format
        # - hours * 3600 + minutes * 60 + seconds

        parts = time_str.split(':')

        # YOUR CODE HERE

        raise NotImplementedError("TODO: Implement time_to_seconds()")

    def has_video_stream(self, file_path: str) -> bool:
        """
        Check if a media file has a video stream.

        Args:
            file_path: Path to media file

        Returns:
            True if video stream exists, False otherwise

        Example:
            >>> processor = MediaProcessor()
            >>> processor.has_video_stream("video.mp4")
            True
            >>> processor.has_video_stream("audio.mp3")
            False
        """
        # TODO: Use ffprobe to detect video stream
        #
        # Command:
        # ffprobe -v error -select_streams v:0 -show_entries stream=codec_type -of json input.mp4
        #
        # If video exists, the JSON will have 'streams' array
        # If no video, 'streams' will be empty

        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',  # Select first video stream
            '-show_entries', 'stream=codec_type',
            '-of', 'json',
            file_path
        ]

        # YOUR CODE HERE
        # Hint: Check if data['streams'] is not empty

        raise NotImplementedError("TODO: Implement has_video_stream()")


# ============================================================
# TESTS - Run this file to test your implementation
# ============================================================

def run_tests():
    """Test the MediaProcessor implementation."""
    print("\n" + "="*60)
    print("TESTING MEDIA PROCESSOR")
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

    except NotImplementedError:
        print("⚠ Not yet implemented\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")

    # Test 2: File Operations (requires test file)
    print("Test 2: File Operations")
    print("-" * 40)

    # Check for sample data
    test_video = "../../../sample_data/sample_video.mp4"

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

        except NotImplementedError:
            print("⚠ Not yet implemented\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")
    else:
        print(f"⚠ Test file not found: {test_video}")
        print("  Run setup_environment.sh to generate test files\n")

    print("="*60)
    print("Testing complete!")
    print("Compare your implementation with the solution.")
    print("="*60 + "\n")


if __name__ == '__main__':
    run_tests()
