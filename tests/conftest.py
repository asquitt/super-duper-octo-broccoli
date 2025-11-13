"""Pytest configuration and fixtures."""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.test_data_generator import TestDataGenerator


@pytest.fixture(scope="session")
def test_data_dir():
    """Create temporary directory for test data."""
    temp_dir = tempfile.mkdtemp(prefix="clip_extractor_test_")
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def test_audio_file(test_data_dir):
    """Generate test audio file."""
    audio_path = os.path.join(test_data_dir, "test_audio.wav")
    try:
        TestDataGenerator.generate_test_audio(audio_path, duration=30.0)
        if os.path.exists(audio_path):
            yield audio_path
        else:
            pytest.skip("FFmpeg not available or audio generation failed")
    except Exception as e:
        pytest.skip(f"Could not generate test audio: {e}")


@pytest.fixture(scope="session")
def test_video_file(test_data_dir):
    """Generate test video file."""
    video_path = os.path.join(test_data_dir, "test_video.mp4")
    try:
        TestDataGenerator.generate_test_video(video_path, duration=30.0)
        if os.path.exists(video_path):
            yield video_path
        else:
            pytest.skip("FFmpeg not available or video generation failed")
    except Exception as e:
        pytest.skip(f"Could not generate test video: {e}")


@pytest.fixture
def test_transcript():
    """Generate test transcript."""
    return TestDataGenerator.generate_test_transcript(num_sentences=10)


@pytest.fixture
def test_transcript_with_timestamps():
    """Generate test transcript with timestamps."""
    return TestDataGenerator.generate_test_transcript_with_timestamps(num_segments=10)


@pytest.fixture
def sample_config():
    """Sample configuration dictionary."""
    return {
        'general': {
            'num_clips': 3,
            'min_clip_duration': 10,
            'max_clip_duration': 20,
            'overlap_threshold': 0.3
        },
        'audio': {
            'enabled': True,
            'sample_rate': 22050,
            'frame_length': 2048,
            'hop_length': 512,
            'emotion': {
                'window_size': 3.0,
                'mfcc_coefficients': 13
            }
        },
        'text': {
            'enabled': True,
            'model': 'distilbert-base-uncased',
            'topic': {
                'window_size': 10
            }
        },
        'visual': {
            'enabled': True,
            'sampling': {
                'fps': 1
            },
            'face_detection': {
                'enabled': False  # Disable for speed in tests
            },
            'motion_detection': {
                'enabled': True,
                'threshold': 25
            }
        },
        'fusion': {
            'strategy': 'weighted',
            'weights': {
                'audio': 0.35,
                'text': 0.40,
                'visual': 0.25
            },
            'title_generation': {
                'enabled': True,
                'max_length': 60,
                'style': 'engaging',
                'include_emoji': True
            },
            'ranking': {
                'min_score': 0.3
            }
        },
        'processing': {
            'temp_dir': tempfile.gettempdir(),
            'cache_dir': tempfile.gettempdir(),
            'cleanup_temp': True
        }
    }
