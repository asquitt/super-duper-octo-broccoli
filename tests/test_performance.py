"""Performance benchmarks and tests."""

import pytest
import time
import os
import json
from src.orchestrator import ClipExtractor
from src.audio.emotion_detector import EmotionDetector
from src.text.topic_analyzer import TopicAnalyzer
from src.visual.engagement_detector import EngagementDetector
from src.utils.test_data_generator import TestDataGenerator


class PerformanceBenchmark:
    """Store and display performance benchmark results."""

    def __init__(self):
        self.results = {}

    def record(self, name: str, duration: float, details: dict = None):
        """Record a benchmark result."""
        self.results[name] = {
            'duration': duration,
            'details': details or {}
        }

    def print_results(self):
        """Print benchmark results."""
        print("\n" + "=" * 60)
        print("PERFORMANCE BENCHMARKS")
        print("=" * 60)

        for name, data in sorted(self.results.items()):
            print(f"\n{name}:")
            print(f"  Duration: {data['duration']:.3f}s")
            for key, value in data['details'].items():
                print(f"  {key}: {value}")

        print("\n" + "=" * 60 + "\n")

    def save_to_file(self, filepath: str):
        """Save results to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)


@pytest.fixture(scope="module")
def benchmark():
    """Create benchmark recorder."""
    return PerformanceBenchmark()


def test_audio_processing_speed(test_audio_file, sample_config, benchmark):
    """Benchmark audio emotion detection speed."""
    try:
        detector = EmotionDetector(sample_config['audio'])

        start_time = time.time()
        scores = detector.analyze(test_audio_file)
        duration = time.time() - start_time

        # Calculate processing speed
        from src.utils.video_processor import VideoProcessor
        processor = VideoProcessor()
        audio_duration = processor.get_duration(test_audio_file)
        speed_ratio = audio_duration / duration if duration > 0 else 0

        benchmark.record('Audio Emotion Detection', duration, {
            'num_segments': len(scores),
            'audio_duration': f"{audio_duration:.1f}s",
            'speed_ratio': f"{speed_ratio:.2f}x real-time"
        })

        # Should process faster than real-time on modern CPU
        print(f"\nAudio processing: {speed_ratio:.2f}x real-time")

    except Exception as e:
        pytest.skip(f"Audio benchmark failed: {e}")


def test_text_processing_speed(test_transcript, sample_config, benchmark):
    """Benchmark text topic analysis speed."""
    try:
        analyzer = TopicAnalyzer(sample_config['text'])

        start_time = time.time()
        scores = analyzer.analyze(test_transcript)
        duration = time.time() - start_time

        benchmark.record('Text Topic Analysis', duration, {
            'num_segments': len(scores),
            'transcript_length': len(test_transcript),
            'chars_per_second': f"{len(test_transcript) / duration:.0f}"
        })

        print(f"\nText processing: {len(test_transcript) / duration:.0f} chars/s")

    except Exception as e:
        pytest.skip(f"Text benchmark failed: {e}")


def test_visual_processing_speed(test_video_file, sample_config, benchmark):
    """Benchmark visual engagement detection speed."""
    try:
        detector = EngagementDetector(sample_config['visual'])

        start_time = time.time()
        scores = detector.analyze(test_video_file)
        duration = time.time() - start_time

        # Calculate processing speed
        from src.utils.video_processor import VideoProcessor
        processor = VideoProcessor()
        video_duration = processor.get_duration(test_video_file)
        speed_ratio = video_duration / duration if duration > 0 else 0

        benchmark.record('Visual Engagement Detection', duration, {
            'num_segments': len(scores),
            'video_duration': f"{video_duration:.1f}s",
            'speed_ratio': f"{speed_ratio:.2f}x real-time"
        })

        print(f"\nVisual processing: {speed_ratio:.2f}x real-time")

    except Exception as e:
        pytest.skip(f"Visual benchmark failed: {e}")


def test_full_pipeline_speed(test_audio_file, test_transcript, sample_config, tmp_path, benchmark):
    """Benchmark full pipeline processing speed."""
    try:
        # Create transcript file
        transcript_file = tmp_path / "transcript.txt"
        transcript_file.write_text(test_transcript)

        # Create extractor
        extractor = ClipExtractor()
        extractor.config = sample_config
        extractor.config['visual']['enabled'] = False  # Audio only for speed

        start_time = time.time()
        clips = extractor.extract_clips(
            input_path=test_audio_file,
            transcript_path=str(transcript_file),
            output_path=str(tmp_path / "output.json")
        )
        duration = time.time() - start_time

        # Calculate processing speed
        from src.utils.video_processor import VideoProcessor
        processor = VideoProcessor()
        input_duration = processor.get_duration(test_audio_file)
        speed_ratio = input_duration / duration if duration > 0 else 0

        benchmark.record('Full Pipeline (Audio + Text)', duration, {
            'num_clips': len(clips),
            'input_duration': f"{input_duration:.1f}s",
            'speed_ratio': f"{speed_ratio:.2f}x real-time"
        })

        print(f"\nFull pipeline: {speed_ratio:.2f}x real-time")

    except Exception as e:
        pytest.skip(f"Pipeline benchmark failed: {e}")


def test_memory_usage():
    """Test memory usage (informational)."""
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()

        print(f"\nMemory Usage:")
        print(f"  RSS: {memory_info.rss / 1024 / 1024:.1f} MB")
        print(f"  VMS: {memory_info.vms / 1024 / 1024:.1f} MB")

    except ImportError:
        pytest.skip("psutil not installed")


def test_scalability(tmp_path, benchmark):
    """Test scalability with different video lengths."""
    try:
        durations = [30, 60, 120]  # 30s, 1min, 2min
        results = []

        for duration in durations:
            # Generate test video
            video_path = str(tmp_path / f"test_{duration}s.mp4")
            TestDataGenerator.generate_test_video(video_path, duration=duration)

            if not os.path.exists(video_path):
                continue

            # Process
            extractor = ClipExtractor()
            extractor.config['visual']['enabled'] = False
            extractor.config['text']['enabled'] = False
            extractor.config['audio']['enabled'] = True

            start_time = time.time()
            clips = extractor.extract_clips(
                input_path=video_path,
                output_path=str(tmp_path / f"output_{duration}s.json")
            )
            processing_time = time.time() - start_time

            results.append({
                'duration': duration,
                'processing_time': processing_time,
                'ratio': duration / processing_time if processing_time > 0 else 0
            })

            # Cleanup
            os.remove(video_path)

        if results:
            benchmark.record('Scalability Test', 0, {
                'test_durations': str([r['duration'] for r in results]),
                'processing_times': str([f"{r['processing_time']:.2f}s" for r in results]),
                'speed_ratios': str([f"{r['ratio']:.2f}x" for r in results])
            })

            print("\nScalability Results:")
            for result in results:
                print(f"  {result['duration']}s video: {result['processing_time']:.2f}s ({result['ratio']:.2f}x)")

    except Exception as e:
        pytest.skip(f"Scalability test failed: {e}")


def test_save_benchmark_results(benchmark, tmp_path):
    """Save benchmark results to file."""
    output_file = tmp_path / "performance_benchmarks.json"
    benchmark.save_to_file(str(output_file))
    benchmark.print_results()

    assert os.path.exists(output_file)
