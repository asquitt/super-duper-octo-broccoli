# Week 7: Testing & Optimization

**Goal**: Ensure code quality, write comprehensive tests, and optimize performance.

---

## 📚 Learning Objectives

By the end of this week, you will:
- ✅ Write unit tests with pytest
- ✅ Create integration tests
- ✅ Implement performance benchmarks
- ✅ Profile and optimize code
- ✅ Add error handling

---

## 🎯 What We're Building This Week

A testing suite that includes:
1. Unit tests for each module
2. Integration tests for full pipeline
3. Performance benchmarks
4. Test data generators
5. Continuous validation

---

## 📖 Key Concepts

### 1. Testing Pyramid

```
        /\
       /  \
      / UI \
     /------\
    /        \
   /Integration\
  /--------------\
 /                \
/   Unit Tests     \
--------------------

Unit Tests:        70% - Test individual functions
Integration Tests: 20% - Test components together
End-to-End Tests:  10% - Test full system
```

### 2. Test Structure (AAA Pattern)

```python
def test_emotion_detection():
    # Arrange: Set up test data
    audio_file = "test_audio.wav"
    detector = EmotionDetector()

    # Act: Perform action
    scores = detector.analyze(audio_file)

    # Assert: Check results
    assert len(scores) > 0
    assert all(0 <= s <= 1 for s in scores)
```

### 3. Test Coverage

What to test:
- **Happy path**: Normal usage
- **Edge cases**: Empty input, very large input
- **Error cases**: Invalid input, missing files
- **Boundary conditions**: Zero, negative, maximum values

### 4. Performance Testing

```python
import time

def benchmark_function(func, *args):
    start = time.time()
    result = func(*args)
    duration = time.time() - start
    return result, duration

# Usage
result, time_taken = benchmark_function(analyze_audio, "audio.wav")
print(f"Analysis took {time_taken:.2f}s")
```

---

## 💻 Starter Code

See `starter-code/week7_starter/test_suite.py`

### Unit Tests

```python
import pytest
import numpy as np
from src.audio.emotion_detector import EmotionDetector

class TestEmotionDetector:
    """Unit tests for EmotionDetector."""

    @pytest.fixture
    def detector(self):
        """Create detector instance for tests."""
        return EmotionDetector()

    @pytest.fixture
    def sample_audio(self):
        """Generate sample audio data."""
        # 1 second of random audio at 22050 Hz
        return np.random.randn(22050).astype(np.float32)

    def test_extract_mfcc(self, detector, sample_audio):
        """Test MFCC extraction."""
        mfccs = detector.extract_mfcc(sample_audio)

        # Check shape
        assert mfccs.shape[0] == 13  # 13 MFCC coefficients

        # Check values are reasonable
        assert np.isfinite(mfccs).all()  # No NaN or Inf

    def test_calculate_energy(self, detector, sample_audio):
        """Test energy calculation."""
        energy = detector.calculate_energy(sample_audio)

        # Energy should be positive
        assert energy > 0

        # Zero audio should have zero energy
        zero_audio = np.zeros_like(sample_audio)
        assert detector.calculate_energy(zero_audio) == 0

    def test_analyze_with_short_audio(self, detector):
        """Test with very short audio (edge case)."""
        short_audio = np.random.randn(100).astype(np.float32)

        # Should handle without crashing
        result = detector.analyze(short_audio)

        # May return empty or handle gracefully
        assert result is not None

    def test_analyze_with_invalid_input(self, detector):
        """Test with invalid input (error case)."""
        with pytest.raises(ValueError):
            detector.analyze(None)

        with pytest.raises(ValueError):
            detector.analyze([])  # Empty list
```

### Integration Tests

```python
class TestFullPipeline:
    """Integration tests for complete system."""

    @pytest.fixture
    def test_video(self):
        """Create test video file."""
        # Generate synthetic test video
        video_path = "test_data/integration_test.mp4"
        generate_test_video(video_path, duration=60)
        yield video_path
        # Cleanup
        os.remove(video_path)

    def test_end_to_end_processing(self, test_video):
        """Test complete pipeline from video to clips."""
        from src.orchestrator import ClipExtractor

        extractor = ClipExtractor()

        # Process video
        clips = extractor.process(
            video_path=test_video,
            num_clips=3
        )

        # Verify output
        assert len(clips) == 3
        assert all('start_time' in clip for clip in clips)
        assert all('end_time' in clip for clip in clips)
        assert all('score' in clip for clip in clips)

        # Clips should be sorted by score
        scores = [clip['score'] for clip in clips]
        assert scores == sorted(scores, reverse=True)

    def test_with_transcript(self, test_video):
        """Test with transcript input."""
        transcript = "This is a test transcript about AI."

        extractor = ClipExtractor()
        clips = extractor.process(
            video_path=test_video,
            transcript=transcript
        )

        assert len(clips) > 0
        # Should have metadata from text analysis
        assert 'keywords' in clips[0]['metadata']
```

### Performance Tests

```python
class TestPerformance:
    """Performance benchmarks."""

    def test_audio_processing_speed(self):
        """Audio processing should be fast enough."""
        detector = EmotionDetector()

        # 60 seconds of audio
        audio = np.random.randn(60 * 22050).astype(np.float32)

        start = time.time()
        detector.analyze(audio)
        duration = time.time() - start

        # Should process 60s audio in < 10s (6x realtime)
        assert duration < 10.0, f"Too slow: {duration:.2f}s"

    def test_memory_usage(self):
        """Check memory usage is reasonable."""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB

        # Process large video
        extractor = ClipExtractor()
        extractor.process("large_video.mp4")

        mem_after = process.memory_info().rss / 1024 / 1024

        mem_increase = mem_after - mem_before

        # Should not use more than 500 MB
        assert mem_increase < 500, f"Memory usage too high: {mem_increase:.1f} MB"
```

---

## ✏️ Exercises

### Exercise 1: Write Your First Test

```python
# test_utils.py
import pytest
from src.utils.video_processor import format_time

def test_format_time():
    """Test time formatting."""
    # Test cases
    assert format_time(0) == "00:00"
    assert format_time(65) == "01:05"
    assert format_time(3661) == "61:01"  # Over 60 minutes

def test_format_time_with_decimals():
    """Test with decimal seconds."""
    assert format_time(65.5) == "01:05"  # Rounds down
    assert format_time(65.9) == "01:05"
```

### Exercise 2: Test Edge Cases

```python
def test_edge_cases():
    detector = EmotionDetector()

    # Empty audio
    with pytest.raises(ValueError):
        detector.analyze(np.array([]))

    # Very long audio (stress test)
    long_audio = np.random.randn(10 * 60 * 22050)  # 10 minutes
    result = detector.analyze(long_audio)
    assert result is not None

    # All zeros
    silent = np.zeros(22050)
    result = detector.analyze(silent)
    assert all(s == 0 for s in result)  # No emotion in silence
```

### Exercise 3: Performance Benchmark

```python
import time

def benchmark_component(component_name, func, *args):
    """Benchmark a component."""
    print(f"\nBenchmarking {component_name}...")

    iterations = 10
    times = []

    for i in range(iterations):
        start = time.time()
        func(*args)
        duration = time.time() - start
        times.append(duration)

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"  Average: {avg_time:.3f}s")
    print(f"  Min: {min_time:.3f}s")
    print(f"  Max: {max_time:.3f}s")

    return avg_time

# Usage
benchmark_component("Audio Analysis",
                   detector.analyze,
                   audio_data)
```

---

## 🎯 Implementation Tasks

### Beginner
1. ✅ Install pytest: `pip install pytest`
2. ✅ Write first unit test
3. ✅ Run tests: `pytest`
4. ✅ Test time formatting functions

### Intermediate
5. ✅ Write tests for all modules
6. ✅ Add test fixtures
7. ✅ Test error handling
8. ✅ Create test data generators
9. ✅ Measure test coverage

### Advanced
10. ✅ Write integration tests
11. ✅ Add performance benchmarks
12. ✅ Set up continuous testing
13. ✅ Profile and optimize bottlenecks

---

## 🔍 Code Profiling

### Find Bottlenecks

```python
import cProfile
import pstats

def profile_function(func, *args):
    """Profile a function to find bottlenecks."""
    profiler = cProfile.Profile()
    profiler.enable()

    result = func(*args)

    profiler.disable()

    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 slowest

    return result

# Usage
profile_function(extractor.process, "video.mp4")
```

### Optimization Example

```python
# BEFORE: Slow
def calculate_scores_slow(data):
    scores = []
    for i in range(len(data)):
        score = expensive_operation(data[i])
        scores.append(score)
    return scores

# AFTER: Fast (using numpy)
def calculate_scores_fast(data):
    data_array = np.array(data)
    scores = vectorized_operation(data_array)
    return scores

# Result: 10x faster!
```

---

## 📊 Test Coverage

```bash
# Install coverage tool
pip install pytest-cov

# Run tests with coverage
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

**Coverage Goals**:
- Unit tests: 80%+ coverage
- Critical paths: 100% coverage
- Error handling: Test all exceptions

---

## 🐛 Common Issues

### Issue 1: Flaky tests
```python
# Problem: Test passes sometimes, fails other times
def test_flaky():
    result = random_function()
    assert result > 0  # Might fail randomly!

# Solution: Control randomness
def test_fixed():
    np.random.seed(42)  # Fixed seed
    result = random_function()
    assert result > 0
```

### Issue 2: Slow tests
```python
# Problem: Tests take too long
def test_slow():
    process_entire_video()  # Takes 5 minutes!

# Solution: Use smaller test data
def test_fast():
    process_video_segment(duration=5)  # Only 5 seconds
```

### Issue 3: External dependencies
```python
# Problem: Test requires internet/GPU/specific files
def test_requires_gpu():
    model = load_gpu_model()  # Fails without GPU

# Solution: Skip when not available
@pytest.mark.skipif(not has_gpu(), reason="Requires GPU")
def test_requires_gpu():
    model = load_gpu_model()
```

---

## 📈 Continuous Testing

```python
# conftest.py - Pytest configuration
import pytest

def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
    config.addinivalue_line(
        "markers", "integration: integration tests"
    )

# Run only fast tests
# pytest -m "not slow"

# Run only unit tests
# pytest -m "not integration"
```

---

## 🎓 What You'll Learn

- Test-driven development (TDD)
- pytest framework
- Performance profiling
- Code optimization
- Quality assurance

**These skills apply to**:
- Professional software development
- Maintaining large codebases
- Ensuring reliability
- Performance optimization
- DevOps/CI-CD

---

## 💡 Best Practices

1. **Write tests first**: TDD approach
2. **Test one thing**: Each test should be focused
3. **Use descriptive names**: `test_emotion_with_angry_audio()`
4. **Keep tests fast**: Use small test data
5. **Clean up**: Remove test files after tests
6. **Mock expensive operations**: Don't call real APIs in tests

---

**Next**: [Week 8 - Deployment](week8_deployment.md)
