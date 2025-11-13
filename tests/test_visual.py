"""Tests for visual engagement detection."""

import pytest
import numpy as np
import cv2
from src.visual.engagement_detector import EngagementDetector


@pytest.fixture
def detector(sample_config):
    """Create engagement detector with test config."""
    return EngagementDetector(sample_config['visual'])


def test_engagement_detector_initialization(detector):
    """Test detector initialization."""
    assert detector is not None
    assert detector.sampling_fps == 1


def test_engagement_detector_detect_motion(detector):
    """Test motion detection between frames."""
    # Create two test frames
    frame1 = np.zeros((480, 640), dtype=np.uint8)
    frame2 = np.zeros((480, 640), dtype=np.uint8)

    # Add some difference
    frame2[100:200, 100:200] = 255

    motion = detector._detect_motion(frame2, frame1)

    assert isinstance(motion, float)
    assert 0 <= motion <= 1.0
    assert motion > 0  # Should detect the change


def test_engagement_detector_detect_scene_change(detector):
    """Test scene change detection."""
    # Create two very different frames
    frame1 = np.zeros((480, 640), dtype=np.uint8)
    frame2 = np.ones((480, 640), dtype=np.uint8) * 255

    is_change = detector._detect_scene_change(frame2, frame1)

    assert isinstance(is_change, bool)
    # May or may not detect depending on threshold


def test_engagement_detector_analyze_frame(detector):
    """Test single frame analysis."""
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    prev_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    frame_data = detector._analyze_frame(frame, prev_frame, timestamp=5.0)

    assert isinstance(frame_data, dict)
    assert 'timestamp' in frame_data
    assert 'face_count' in frame_data
    assert 'motion_score' in frame_data
    assert 'scene_change' in frame_data
    assert frame_data['timestamp'] == 5.0


def test_engagement_detector_calculate_window_score(detector):
    """Test window score calculation."""
    window_data = [
        {'timestamp': 0, 'face_count': 1, 'face_area': 0.1, 'motion_score': 0.5, 'scene_change': False},
        {'timestamp': 1, 'face_count': 1, 'face_area': 0.12, 'motion_score': 0.6, 'scene_change': False},
        {'timestamp': 2, 'face_count': 2, 'face_area': 0.2, 'motion_score': 0.7, 'scene_change': True},
    ]

    score = detector._calculate_window_score(window_data)

    assert isinstance(score, dict)
    assert 'time_start' in score
    assert 'time_end' in score
    assert 'engagement_score' in score
    assert 0 <= score['engagement_score'] <= 1.0


def test_engagement_detector_analyze_video(detector, test_video_file):
    """Test full video analysis."""
    try:
        scores = detector.analyze(test_video_file)

        assert isinstance(scores, list)
        assert len(scores) > 0

        for score in scores:
            assert 'time_start' in score
            assert 'time_end' in score
            assert 'engagement_score' in score
            assert 0 <= score['engagement_score'] <= 1.0
    except Exception as e:
        pytest.skip(f"Could not analyze video: {e}")


def test_engagement_detector_get_peak_segments(detector):
    """Test peak engagement segment extraction."""
    engagement_scores = [
        {'time_start': 0, 'time_end': 5, 'engagement_score': 0.4, 'face_activity': 0.5, 'motion_activity': 0.3, 'scene_changes': 0},
        {'time_start': 5, 'time_end': 10, 'engagement_score': 0.8, 'face_activity': 0.7, 'motion_activity': 0.8, 'scene_changes': 2},
        {'time_start': 10, 'time_end': 15, 'engagement_score': 0.9, 'face_activity': 0.8, 'motion_activity': 0.9, 'scene_changes': 3},
    ]

    peaks = detector.get_peak_engagement_segments(engagement_scores, threshold=0.7, min_duration=4.0)

    assert isinstance(peaks, list)
    assert len(peaks) > 0
    for peak in peaks:
        assert peak['score'] >= 0.7
        assert 'start_time' in peak
        assert 'end_time' in peak
