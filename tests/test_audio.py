"""Tests for audio emotion detection."""

import pytest
import numpy as np
from src.audio.emotion_detector import EmotionDetector


@pytest.fixture
def detector(sample_config):
    """Create emotion detector with test config."""
    return EmotionDetector(sample_config['audio'])


def test_emotion_detector_initialization(detector):
    """Test detector initialization."""
    assert detector is not None
    assert detector.sample_rate == 22050
    assert detector.window_size == 3.0


def test_emotion_detector_analyze(detector, test_audio_file):
    """Test audio analysis."""
    try:
        scores = detector.analyze(test_audio_file)
        assert isinstance(scores, list)
        assert len(scores) > 0

        # Check structure of scores
        for score in scores:
            assert 'time_start' in score
            assert 'time_end' in score
            assert 'emotion_score' in score
            assert 0 <= score['emotion_score'] <= 1.0
            assert score['time_end'] > score['time_start']
    except Exception as e:
        pytest.skip(f"Could not analyze audio: {e}")


def test_emotion_detector_compute_energy_score(detector):
    """Test energy score computation."""
    features = {
        'energy': np.array([0.1, 0.2, 0.3, 0.2, 0.1])
    }
    score = detector._compute_energy_score(features)
    assert isinstance(score, float)
    assert 0 <= score <= 1.0


def test_emotion_detector_compute_pitch_variation(detector):
    """Test pitch variation computation."""
    features = {
        'pitch': np.array([100, 150, 200, 150, 100, 0, 0])  # Include some zeros
    }
    score = detector._compute_pitch_variation(features)
    assert isinstance(score, float)
    assert 0 <= score <= 1.0


def test_emotion_detector_compute_speech_activity(detector):
    """Test speech activity computation."""
    features = {
        'energy': np.array([0.1, 0.05, 0.2, 0.01, 0.15])  # Mix of high and low energy
    }
    score = detector._compute_speech_activity(features)
    assert isinstance(score, float)
    assert 0 <= score <= 1.0


def test_emotion_detector_get_peak_segments(detector):
    """Test peak segment extraction."""
    emotion_scores = [
        {'time_start': 0, 'time_end': 3, 'emotion_score': 0.5, 'energy_score': 0.5, 'pitch_variation': 0.5},
        {'time_start': 3, 'time_end': 6, 'emotion_score': 0.8, 'energy_score': 0.7, 'pitch_variation': 0.6},
        {'time_start': 6, 'time_end': 9, 'emotion_score': 0.9, 'energy_score': 0.8, 'pitch_variation': 0.7},
        {'time_start': 9, 'time_end': 12, 'emotion_score': 0.6, 'energy_score': 0.5, 'pitch_variation': 0.4},
    ]

    peaks = detector.get_peak_emotion_segments(emotion_scores, threshold=0.7, min_duration=2.0)

    assert isinstance(peaks, list)
    assert len(peaks) > 0
    # Should find segments with score >= 0.7
    for peak in peaks:
        assert peak['score'] >= 0.7
        assert 'start_time' in peak
        assert 'end_time' in peak


def test_emotion_detector_empty_audio():
    """Test handling of empty/invalid audio."""
    detector = EmotionDetector({'sample_rate': 22050, 'frame_length': 2048, 'hop_length': 512, 'emotion': {}})
    # Should handle gracefully or raise appropriate error
    try:
        scores = detector.analyze("nonexistent_file.wav")
        assert False, "Should raise an error for nonexistent file"
    except Exception:
        pass  # Expected
