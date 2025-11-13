"""Generate synthetic test data for testing without real video files."""

import numpy as np
import os
from pathlib import Path
import subprocess
import json
from typing import List, Dict, Tuple


class TestDataGenerator:
    """Generate synthetic audio, video, and transcripts for testing."""

    @staticmethod
    def generate_test_audio(output_path: str, duration: float = 60.0,
                          frequencies: List[float] = None) -> str:
        """
        Generate test audio file using FFmpeg.

        Args:
            output_path: Path to save audio file
            duration: Duration in seconds
            frequencies: List of frequencies to generate

        Returns:
            Path to generated audio file
        """
        if frequencies is None:
            frequencies = [440, 880, 1320]  # A4, A5, E6

        # Create directory if needed
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

        # Generate multiple sine waves
        freq_str = '+'.join([f'sine=frequency={f}' for f in frequencies])

        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', f'{freq_str}:duration={duration}',
            '-ar', '22050',
            '-ac', '1',
            '-y',
            output_path
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not generate audio with FFmpeg: {e}")
            return None

    @staticmethod
    def generate_test_video(output_path: str, duration: float = 60.0,
                          width: int = 640, height: int = 480) -> str:
        """
        Generate test video file using FFmpeg.

        Args:
            output_path: Path to save video file
            duration: Duration in seconds
            width: Video width
            height: Video height

        Returns:
            Path to generated video file
        """
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', f'testsrc=duration={duration}:size={width}x{height}:rate=30',
            '-f', 'lavfi',
            '-i', f'sine=frequency=1000:duration={duration}',
            '-pix_fmt', 'yuv420p',
            '-y',
            output_path
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not generate video with FFmpeg: {e}")
            return None

    @staticmethod
    def generate_test_transcript(num_sentences: int = 20) -> str:
        """
        Generate test transcript text.

        Args:
            num_sentences: Number of sentences to generate

        Returns:
            Generated transcript text
        """
        templates = [
            "This is an important point about {topic}.",
            "Let me explain how {topic} works.",
            "The key insight here is {topic}.",
            "You might be wondering about {topic}.",
            "Here's what you need to know about {topic}.",
            "The most surprising thing about {topic} is this.",
            "Let's dive deeper into {topic}.",
            "This changes everything about {topic}.",
            "The secret to {topic} is actually quite simple.",
            "What most people don't understand about {topic}.",
        ]

        topics = [
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "neural networks",
            "data science",
            "natural language processing",
            "computer vision",
            "reinforcement learning",
            "model training",
            "feature engineering",
        ]

        transcript = []
        for i in range(num_sentences):
            template = templates[i % len(templates)]
            topic = topics[i % len(topics)]
            sentence = template.format(topic=topic)
            transcript.append(sentence)

        return ' '.join(transcript)

    @staticmethod
    def generate_test_transcript_with_timestamps(num_segments: int = 10,
                                                avg_duration: float = 5.0) -> List[Dict]:
        """
        Generate transcript with timestamps.

        Args:
            num_segments: Number of transcript segments
            avg_duration: Average duration per segment

        Returns:
            List of segments with timestamps
        """
        segments = []
        current_time = 0.0

        for i in range(num_segments):
            duration = avg_duration + np.random.uniform(-1, 1)
            text = TestDataGenerator.generate_test_transcript(num_sentences=1)

            segments.append({
                'start': current_time,
                'end': current_time + duration,
                'text': text
            })

            current_time += duration

        return segments

    @staticmethod
    def generate_ground_truth_clips(total_duration: float, num_clips: int = 5,
                                   clip_duration: Tuple[float, float] = (30, 60)) -> List[Dict]:
        """
        Generate ground truth clips for evaluation.

        Args:
            total_duration: Total video duration
            num_clips: Number of clips to generate
            clip_duration: (min, max) duration for clips

        Returns:
            List of ground truth clips
        """
        clips = []
        min_duration, max_duration = clip_duration

        # Generate non-overlapping clips
        available_ranges = [(0, total_duration)]

        for i in range(num_clips):
            if not available_ranges:
                break

            # Pick a random range
            range_idx = np.random.randint(0, len(available_ranges))
            range_start, range_end = available_ranges[range_idx]

            # Generate clip duration
            duration = np.random.uniform(min_duration, max_duration)
            duration = min(duration, range_end - range_start)

            if duration < min_duration:
                available_ranges.pop(range_idx)
                continue

            # Generate clip start within range
            max_start = range_end - duration
            start = np.random.uniform(range_start, max_start)
            end = start + duration

            clips.append({
                'start_time': start,
                'end_time': end,
                'score': np.random.uniform(0.7, 1.0)
            })

            # Update available ranges
            available_ranges.pop(range_idx)
            if start > range_start:
                available_ranges.append((range_start, start))
            if end < range_end:
                available_ranges.append((end, range_end))

        return sorted(clips, key=lambda x: x['start_time'])

    @staticmethod
    def create_test_dataset(output_dir: str, num_videos: int = 3) -> Dict:
        """
        Create a complete test dataset.

        Args:
            output_dir: Directory to save test data
            num_videos: Number of test videos to generate

        Returns:
            Dictionary with paths and metadata
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        dataset = {
            'videos': [],
            'metadata_file': str(output_dir / 'dataset_metadata.json')
        }

        for i in range(num_videos):
            video_name = f"test_video_{i+1}"
            duration = np.random.uniform(60, 180)  # 1-3 minutes

            # Generate video
            video_path = str(output_dir / f"{video_name}.mp4")
            TestDataGenerator.generate_test_video(video_path, duration=duration)

            # Generate transcript
            transcript_text = TestDataGenerator.generate_test_transcript(num_sentences=30)
            transcript_path = str(output_dir / f"{video_name}_transcript.txt")
            with open(transcript_path, 'w') as f:
                f.write(transcript_text)

            # Generate ground truth clips
            ground_truth = TestDataGenerator.generate_ground_truth_clips(
                duration, num_clips=5
            )
            ground_truth_path = str(output_dir / f"{video_name}_ground_truth.json")
            with open(ground_truth_path, 'w') as f:
                json.dump(ground_truth, f, indent=2)

            dataset['videos'].append({
                'name': video_name,
                'video_path': video_path,
                'transcript_path': transcript_path,
                'ground_truth_path': ground_truth_path,
                'duration': duration
            })

        # Save dataset metadata
        with open(dataset['metadata_file'], 'w') as f:
            json.dump(dataset, f, indent=2)

        return dataset
