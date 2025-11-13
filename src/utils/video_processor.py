"""Video processing utilities using ffmpeg."""

import subprocess
import os
from pathlib import Path
from typing import Optional, Tuple
import json


class VideoProcessor:
    """Handle video/audio extraction and processing using ffmpeg."""

    @staticmethod
    def get_duration(file_path: str) -> float:
        """Get the duration of a video/audio file in seconds."""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            file_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return float(data['format']['duration'])
        except (subprocess.CalledProcessError, KeyError, ValueError) as e:
            raise RuntimeError(f"Failed to get duration: {e}")

    @staticmethod
    def extract_audio(video_path: str, output_path: Optional[str] = None,
                     sample_rate: int = 22050) -> str:
        """Extract audio from video file."""
        if output_path is None:
            output_path = str(Path(video_path).with_suffix('.wav'))

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit
            '-ar', str(sample_rate),  # Sample rate
            '-ac', '1',  # Mono
            '-y',  # Overwrite
            output_path
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to extract audio: {e.stderr.decode()}")

    @staticmethod
    def has_video_stream(file_path: str) -> bool:
        """Check if file has a video stream."""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_type',
            '-of', 'json',
            file_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return len(data.get('streams', [])) > 0
        except (subprocess.CalledProcessError, KeyError):
            return False

    @staticmethod
    def extract_frames(video_path: str, output_dir: str, fps: int = 1) -> str:
        """Extract frames from video at specified FPS."""
        os.makedirs(output_dir, exist_ok=True)

        output_pattern = os.path.join(output_dir, 'frame_%06d.jpg')

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'fps={fps}',
            '-q:v', '2',  # Quality
            '-y',
            output_pattern
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_dir
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to extract frames: {e.stderr.decode()}")

    @staticmethod
    def get_video_info(file_path: str) -> dict:
        """Get comprehensive video information."""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries',
            'format=duration,size,bit_rate:stream=codec_type,codec_name,width,height,r_frame_rate',
            '-of', 'json',
            file_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, KeyError) as e:
            raise RuntimeError(f"Failed to get video info: {e}")

    @staticmethod
    def time_to_seconds(time_str: str) -> float:
        """Convert time string (HH:MM:SS or MM:SS) to seconds."""
        parts = time_str.split(':')
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + float(s)
        elif len(parts) == 2:
            m, s = parts
            return int(m) * 60 + float(s)
        else:
            return float(parts[0])

    @staticmethod
    def seconds_to_time(seconds: float) -> str:
        """Convert seconds to time string (MM:SS)."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    @staticmethod
    def extract_clip(video_path: str, start_time: float, end_time: float,
                    output_path: str) -> str:
        """Extract a clip from video file."""
        duration = end_time - start_time

        cmd = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', video_path,
            '-t', str(duration),
            '-c', 'copy',  # Copy codec (fast)
            '-y',
            output_path
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to extract clip: {e.stderr.decode()}")
