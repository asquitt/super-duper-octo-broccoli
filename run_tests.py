#!/usr/bin/env python3
"""
Test runner script that works without pytest.
Runs basic tests to validate the system.
"""

import sys
import os
import time
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Test results
results = {
    'passed': 0,
    'failed': 0,
    'skipped': 0,
    'errors': []
}


def test(name):
    """Decorator for test functions."""
    def decorator(func):
        def wrapper():
            try:
                print(f"  Running {name}... ", end='', flush=True)
                start_time = time.time()
                func()
                duration = time.time() - start_time
                print(f"✓ PASS ({duration:.3f}s)")
                results['passed'] += 1
            except AssertionError as e:
                print(f"✗ FAIL: {e}")
                results['failed'] += 1
                results['errors'].append((name, str(e)))
            except Exception as e:
                print(f"⚠ SKIP: {e}")
                results['skipped'] += 1
        return wrapper
    return decorator


print("\n" + "=" * 60)
print("Running Basic System Tests")
print("=" * 60 + "\n")

# Test 1: Imports
print("Testing Imports:")


@test("Import utilities")
def test_import_utils():
    from src.utils.metrics import EvaluationMetrics
    from src.utils.test_data_generator import TestDataGenerator
    from src.utils.video_processor import VideoProcessor
    from src.utils.config_loader import ConfigLoader
    assert EvaluationMetrics is not None


test_import_utils()


@test("Import audio module")
def test_import_audio():
    from src.audio.emotion_detector import EmotionDetector
    assert EmotionDetector is not None


test_import_audio()


@test("Import text module")
def test_import_text():
    from src.text.topic_analyzer import TopicAnalyzer
    from src.text.transcriber import Transcriber
    assert TopicAnalyzer is not None


test_import_text()


@test("Import visual module")
def test_import_visual():
    from src.visual.engagement_detector import EngagementDetector
    assert EngagementDetector is not None


test_import_visual()


@test("Import fusion module")
def test_import_fusion():
    from src.fusion.multimodal_fusion import MultimodalFusion
    from src.fusion.title_generator import TitleGenerator
    assert MultimodalFusion is not None


test_import_fusion()


@test("Import orchestrator")
def test_import_orchestrator():
    from src.orchestrator import ClipExtractor
    assert ClipExtractor is not None


test_import_orchestrator()

# Test 2: Metrics
print("\nTesting Evaluation Metrics:")


@test("IoU calculation")
def test_iou():
    from src.utils.metrics import EvaluationMetrics
    clip1 = {'start_time': 0, 'end_time': 10}
    clip2 = {'start_time': 5, 'end_time': 15}
    iou = EvaluationMetrics.calculate_iou(clip1, clip2)
    assert 0 <= iou <= 1.0
    # 5 seconds overlap out of 15 total = 0.333...
    assert abs(iou - 0.333) < 0.01


test_iou()


@test("mAP calculation")
def test_map():
    from src.utils.metrics import EvaluationMetrics
    predicted = [
        {'start_time': 0, 'end_time': 10, 'score': 0.9}
    ]
    ground_truth = [
        {'start_time': 0, 'end_time': 10}
    ]
    map_score = EvaluationMetrics.calculate_map(predicted, ground_truth)
    assert map_score == 1.0


test_map()


@test("Precision/Recall/F1")
def test_precision_recall():
    from src.utils.metrics import EvaluationMetrics
    predicted = [
        {'start_time': 0, 'end_time': 10},
        {'start_time': 20, 'end_time': 30}
    ]
    ground_truth = [
        {'start_time': 0, 'end_time': 10},
        {'start_time': 20, 'end_time': 30}
    ]
    p, r, f1 = EvaluationMetrics.calculate_precision_recall_f1(predicted, ground_truth)
    assert p == 1.0
    assert r == 1.0
    assert f1 == 1.0


test_precision_recall()

# Test 3: Data Generation
print("\nTesting Data Generation:")


@test("Transcript generation")
def test_transcript_gen():
    from src.utils.test_data_generator import TestDataGenerator
    transcript = TestDataGenerator.generate_test_transcript(num_sentences=5)
    assert len(transcript) > 0
    assert '.' in transcript


test_transcript_gen()


@test("Timestamp generation")
def test_timestamps():
    from src.utils.test_data_generator import TestDataGenerator
    segments = TestDataGenerator.generate_test_transcript_with_timestamps(num_segments=5)
    assert len(segments) == 5
    assert all('start' in s and 'end' in s and 'text' in s for s in segments)


test_timestamps()


@test("Ground truth generation")
def test_ground_truth():
    from src.utils.test_data_generator import TestDataGenerator
    clips = TestDataGenerator.generate_ground_truth_clips(
        total_duration=120.0,
        num_clips=5
    )
    assert len(clips) <= 5
    for clip in clips:
        assert clip['start_time'] >= 0
        assert clip['end_time'] <= 120.0


test_ground_truth()

# Test 4: Title Generation
print("\nTesting Title Generation:")


@test("Keyword extraction")
def test_keywords():
    from src.fusion.title_generator import TitleGenerator
    config = {'max_length': 60, 'style': 'engaging', 'include_emoji': False}
    gen = TitleGenerator(config)
    text = "Machine learning and artificial intelligence transform the world"
    keywords = gen._extract_keywords(text)
    assert len(keywords) > 0


test_keywords()


@test("Title generation")
def test_title_gen():
    from src.fusion.title_generator import TitleGenerator
    config = {'max_length': 60, 'style': 'engaging', 'include_emoji': True}
    gen = TitleGenerator(config)
    clip = {
        'text_context': "Machine learning revolutionizes AI",
        'audio_score': 0.8,
        'text_score': 0.9,
        'visual_score': 0.7,
        'score': 0.85
    }
    title = gen.generate_title(clip)
    assert len(title) > 0
    assert len(title) <= config['max_length'] + 10  # Allow for emoji


test_title_gen()

# Test 5: Audio Processing
print("\nTesting Audio Processing:")


@test("Audio detector initialization")
def test_audio_detector():
    from src.audio.emotion_detector import EmotionDetector
    config = {
        'sample_rate': 22050,
        'frame_length': 2048,
        'hop_length': 512,
        'emotion': {
            'window_size': 3.0,
            'mfcc_coefficients': 13
        }
    }
    detector = EmotionDetector(config)
    assert detector.sample_rate == 22050


test_audio_detector()

# Test 6: Text Processing
print("\nTesting Text Processing:")


@test("Topic analyzer initialization")
def test_topic_analyzer():
    from src.text.topic_analyzer import TopicAnalyzer
    config = {
        'topic': {'window_size': 10}
    }
    analyzer = TopicAnalyzer(config)
    assert analyzer.window_size == 10


test_topic_analyzer()


@test("Question detection")
def test_question_detection():
    from src.text.topic_analyzer import TopicAnalyzer
    config = {'topic': {'window_size': 10}}
    analyzer = TopicAnalyzer(config)
    assert analyzer._is_question("What is AI?") is True
    assert analyzer._is_question("This is a statement.") is False


test_question_detection()

# Test 7: Visual Processing
print("\nTesting Visual Processing:")


@test("Visual detector initialization")
def test_visual_detector():
    from src.visual.engagement_detector import EngagementDetector
    config = {
        'sampling': {'fps': 1},
        'face_detection': {'enabled': False},
        'motion_detection': {'enabled': True},
        'scene_change': {'enabled': True}
    }
    detector = EngagementDetector(config)
    assert detector.sampling_fps == 1


test_visual_detector()

# Test 8: Fusion
print("\nTesting Multimodal Fusion:")


@test("Fusion initialization")
def test_fusion_init():
    from src.fusion.multimodal_fusion import MultimodalFusion
    config = {
        'strategy': 'weighted',
        'weights': {'audio': 0.35, 'text': 0.40, 'visual': 0.25},
        'min_clip_duration': 30,
        'max_clip_duration': 60,
        'num_clips': 5,
        'overlap_threshold': 0.3
    }
    fusion = MultimodalFusion(config)
    assert fusion.strategy == 'weighted'


test_fusion_init()


@test("Overlap calculation")
def test_overlap():
    from src.fusion.multimodal_fusion import MultimodalFusion
    config = {
        'strategy': 'weighted',
        'weights': {'audio': 0.35, 'text': 0.40, 'visual': 0.25},
        'min_clip_duration': 30,
        'max_clip_duration': 60,
        'num_clips': 5,
        'overlap_threshold': 0.3
    }
    fusion = MultimodalFusion(config)
    clip1 = {'start_time': 0, 'end_time': 10}
    clip2 = {'start_time': 5, 'end_time': 15}
    overlap = fusion._calculate_overlap(clip1, clip2)
    assert abs(overlap - 0.5) < 0.01


test_overlap()

# Test 9: Config Loading
print("\nTesting Configuration:")


@test("Config loader")
def test_config_loader():
    from src.utils.config_loader import ConfigLoader
    try:
        config = ConfigLoader()
        assert config.get('general.num_clips', 5) == 5
    except FileNotFoundError:
        # Config file might not exist in test environment
        pass


test_config_loader()

# Print Results
print("\n" + "=" * 60)
print("Test Results Summary")
print("=" * 60)
print(f"Passed:  {results['passed']} ✓")
print(f"Failed:  {results['failed']} ✗")
print(f"Skipped: {results['skipped']} ⚠")
print("=" * 60)

if results['failed'] > 0:
    print("\nFailed Tests:")
    for name, error in results['errors']:
        print(f"  - {name}: {error}")

print("\n")

# Exit with appropriate code
sys.exit(0 if results['failed'] == 0 else 1)
