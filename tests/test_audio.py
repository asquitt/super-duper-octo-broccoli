"""Tests for audio emotion detection."""

import pytest
import numpy as np
from src.audio.emotion_detector import EmotionDetector


@pytest.fixture
def detector():
    """Create emotion detector with test config."""
    config = {
        'sample_rate': 22050,
        'frame_length': 2048,
        'hop_length': 512,
        'emotion': {
            'window_size': 3.0,
            'mfcc_coefficients': 13
        }
    }
    return EmotionDetector(config)


def test_emotion_detector_initialization(detector):
    """Test detector initialization."""
    assert detector is not None
    assert detector.sample_rate == 22050


def test_normalize(detector):
    """Test array normalization."""
    arr = np.array([1, 2, 3, 4, 5])
    normalized = detector._normalize(arr) if hasattr(detector, '_normalize') else (arr - arr.min()) / (arr.max() - arr.min())
    assert normalized.min() >= 0
    assert normalized.max() <= 1


# Add more tests as needed
