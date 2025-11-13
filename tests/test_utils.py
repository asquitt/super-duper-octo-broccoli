"""Tests for utility modules."""

import pytest
import os
import tempfile
from src.utils.video_processor import VideoProcessor
from src.utils.config_loader import ConfigLoader
from src.utils.test_data_generator import TestDataGenerator


def test_video_processor_time_conversion():
    """Test time conversion utilities."""
    processor = VideoProcessor()

    # Test seconds to time string
    assert processor.seconds_to_time(0) == "00:00"
    assert processor.seconds_to_time(65) == "01:05"
    assert processor.seconds_to_time(125) == "02:05"

    # Test time string to seconds
    assert processor.time_to_seconds("00:00") == 0
    assert processor.time_to_seconds("01:05") == 65
    assert processor.time_to_seconds("02:05") == 125
    assert processor.time_to_seconds("1:30:45") == 5445


def test_video_processor_duration(test_video_file):
    """Test getting video duration."""
    processor = VideoProcessor()
    duration = processor.get_duration(test_video_file)
    assert duration > 0
    assert duration < 60  # Our test video is 30 seconds


def test_video_processor_has_video_stream(test_video_file, test_audio_file):
    """Test video stream detection."""
    processor = VideoProcessor()

    # Video file should have video stream
    assert processor.has_video_stream(test_video_file) is True

    # Audio file should not have video stream
    assert processor.has_video_stream(test_audio_file) is False


def test_config_loader_default():
    """Test loading default config."""
    try:
        config = ConfigLoader()
        assert config.get('general.num_clips') == 5
        assert config.get('audio.enabled') is True
    except FileNotFoundError:
        pytest.skip("Config file not found")


def test_config_loader_get_with_default():
    """Test get with default value."""
    try:
        config = ConfigLoader()
        # Existing key
        assert config.get('general.num_clips', default=999) == 5
        # Non-existing key
        assert config.get('nonexistent.key', default=123) == 123
    except FileNotFoundError:
        pytest.skip("Config file not found")


def test_test_data_generator_transcript():
    """Test transcript generation."""
    transcript = TestDataGenerator.generate_test_transcript(num_sentences=5)
    assert len(transcript) > 0
    assert '.' in transcript  # Should have sentences


def test_test_data_generator_transcript_with_timestamps():
    """Test transcript with timestamps generation."""
    segments = TestDataGenerator.generate_test_transcript_with_timestamps(num_segments=5)
    assert len(segments) == 5
    assert all('start' in seg for seg in segments)
    assert all('end' in seg for seg in segments)
    assert all('text' in seg for seg in segments)
    # Verify timestamps are sequential
    for i in range(len(segments) - 1):
        assert segments[i]['end'] <= segments[i+1]['start'] + 0.1  # Small tolerance


def test_test_data_generator_ground_truth_clips():
    """Test ground truth clip generation."""
    clips = TestDataGenerator.generate_ground_truth_clips(
        total_duration=120.0,
        num_clips=5,
        clip_duration=(10, 20)
    )
    assert len(clips) <= 5  # May be fewer if duration constraints
    assert all('start_time' in clip for clip in clips)
    assert all('end_time' in clip for clip in clips)
    # Verify clips are within bounds
    for clip in clips:
        assert clip['start_time'] >= 0
        assert clip['end_time'] <= 120.0
        assert clip['end_time'] > clip['start_time']
        duration = clip['end_time'] - clip['start_time']
        assert 10 <= duration <= 20


def test_test_data_generator_audio_generation(test_data_dir):
    """Test audio file generation."""
    audio_path = os.path.join(test_data_dir, "generated_audio.wav")
    result = TestDataGenerator.generate_test_audio(audio_path, duration=5.0)
    if result:
        assert os.path.exists(audio_path)
        assert os.path.getsize(audio_path) > 0
    else:
        pytest.skip("FFmpeg not available")


def test_test_data_generator_video_generation(test_data_dir):
    """Test video file generation."""
    video_path = os.path.join(test_data_dir, "generated_video.mp4")
    result = TestDataGenerator.generate_test_video(video_path, duration=5.0)
    if result:
        assert os.path.exists(video_path)
        assert os.path.getsize(video_path) > 0
    else:
        pytest.skip("FFmpeg not available")
