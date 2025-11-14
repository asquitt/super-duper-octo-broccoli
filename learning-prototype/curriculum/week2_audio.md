# Week 2: Audio Emotion Detection

**Goal**: Extract emotion and engagement signals from audio using signal processing.

---

## 📚 Learning Objectives

By the end of this week, you will:
- ✅ Understand audio signal processing basics
- ✅ Extract MFCC (Mel-Frequency Cepstral Coefficients)
- ✅ Calculate energy, pitch, and spectral features
- ✅ Build an emotion scoring algorithm
- ✅ Detect high-energy moments in audio

---

## 🎯 What We're Building This Week

An audio emotion detector that can:
1. Load audio files and extract features
2. Calculate MFCCs (voice characteristics)
3. Detect energy spikes (excitement, emphasis)
4. Track pitch variation (expressiveness)
5. Score emotional intensity over time

---

## 📖 Concepts to Understand

### 1. Audio as a Signal

```
Audio Waveform:
     ^
  A  |    ╱╲    ╱╲
  m  |   ╱  ╲  ╱  ╲
  p  |  ╱    ╲╱    ╲
  l  | ╱            ╲
  i  |╱              ╲
  t  +──────────────────────> Time
  u  |
  d  |
  e  |
```

**Key Properties:**
- **Amplitude**: Loudness (higher = louder)
- **Frequency**: Pitch (higher = higher pitch)
- **Duration**: Length of sound

### 2. Features We Extract

**MFCC (Mel-Frequency Cepstral Coefficients)**:
- Represents the voice/sound characteristics
- Used in speech recognition
- Captures timbral texture
- We use 13 coefficients

**Energy/RMS**:
- Root Mean Square energy
- Indicates loudness
- High energy = excitement, emphasis

**Pitch (F0)**:
- Fundamental frequency
- Variation indicates expressiveness
- Speech: 85-180 Hz (male), 165-255 Hz (female)

**Spectral Centroid**:
- "Brightness" of sound
- Where the center of mass of spectrum is
- Higher = brighter sound

**Zero Crossing Rate**:
- How often signal crosses zero
- Indicates noisiness
- Useful for detecting certain sounds

### 3. Emotion Detection Strategy

```
High Energy + High Pitch Variation = Excitement/Emphasis
Low Energy + Low Variation = Calm/Boring
High Energy + Scene Change = Important Moment
```

---

## 💻 Starter Code

### File: `audio_emotion_detector.py`

```python
"""
Week 2 Starter Code: Audio Emotion Detector
Your task: Implement the TODO sections
"""

import numpy as np
import librosa
from typing import List, Dict


class EmotionDetector:
    """Detect emotional intensity from audio."""

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize detector.

        Args:
            sample_rate: Audio sample rate (Hz)
        """
        self.sample_rate = sample_rate
        self.frame_length = 2048  # Window size for analysis
        self.hop_length = 512     # Step size between windows
        self.window_size = 3.0    # Analyze in 3-second windows

    def load_audio(self, file_path: str) -> np.ndarray:
        """
        Load audio file.

        Args:
            file_path: Path to audio file

        Returns:
            Audio signal as numpy array

        Example:
            >>> detector = EmotionDetector()
            >>> audio = detector.load_audio("audio.wav")
        """
        # TODO: Use librosa to load audio
        # Hint: librosa.load(file_path, sr=self.sample_rate)

        # YOUR CODE HERE
        y, sr = librosa.load(file_path, sr=self.sample_rate)
        return y

    def extract_mfcc(self, audio: np.ndarray, n_mfcc: int = 13) -> np.ndarray:
        """
        Extract MFCC features.

        Args:
            audio: Audio signal
            n_mfcc: Number of MFCC coefficients

        Returns:
            MFCC features (n_mfcc x time_frames)

        Example:
            >>> detector = EmotionDetector()
            >>> audio = detector.load_audio("audio.wav")
            >>> mfcc = detector.extract_mfcc(audio)
            >>> print(f"MFCC shape: {mfcc.shape}")
        """
        # TODO: Extract MFCC using librosa
        # Hint: librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=n_mfcc)

        # YOUR CODE HERE
        pass

    def extract_energy(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract RMS energy.

        Args:
            audio: Audio signal

        Returns:
            Energy values over time
        """
        # TODO: Extract RMS energy
        # Hint: librosa.feature.rms(y=audio, frame_length=self.frame_length)

        # YOUR CODE HERE
        pass

    def extract_pitch(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract pitch (fundamental frequency).

        Args:
            audio: Audio signal

        Returns:
            Pitch values over time (Hz)
        """
        # TODO: Extract pitch using librosa.piptrack
        # Hint:
        #   pitches, magnitudes = librosa.piptrack(y=audio, sr=self.sample_rate)
        #   For each time frame, select pitch with highest magnitude

        # YOUR CODE HERE
        pass

    def calculate_emotion_score(self, audio: np.ndarray) -> List[Dict]:
        """
        Calculate emotion scores over time windows.

        Args:
            audio: Audio signal

        Returns:
            List of scores with timestamps

        Example:
            >>> detector = EmotionDetector()
            >>> audio = detector.load_audio("audio.wav")
            >>> scores = detector.calculate_emotion_score(audio)
            >>> for score in scores:
            >>>     print(f"{score['time']:.1f}s: {score['emotion']:.2f}")
        """
        # Extract all features
        mfcc = self.extract_mfcc(audio)
        energy = self.extract_energy(audio)
        pitch = self.extract_pitch(audio)

        # TODO: Divide into time windows and calculate scores
        # For each window:
        #   1. Get window features
        #   2. Calculate energy score (mean + std)
        #   3. Calculate pitch variation (std of pitch)
        #   4. Combine into emotion score

        # Hints:
        # - Convert frame index to time: frame * hop_length / sample_rate
        # - Window size in frames: window_size * sample_rate / hop_length
        # - Normalize scores to 0-1 range

        scores = []

        # YOUR CODE HERE
        # This is the main algorithm - combine all features intelligently

        return scores

    def get_peak_moments(self, scores: List[Dict], threshold: float = 0.7) -> List[Dict]:
        """
        Find peak emotional moments.

        Args:
            scores: List of emotion scores
            threshold: Minimum score to be considered a peak

        Returns:
            List of peak moments
        """
        # TODO: Filter scores above threshold
        # Return peaks sorted by score (highest first)

        # YOUR CODE HERE
        pass


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_array(arr: np.ndarray) -> np.ndarray:
    """Normalize array to 0-1 range."""
    # TODO: Implement normalization
    # Formula: (value - min) / (max - min)
    # Handle case where max == min

    # YOUR CODE HERE
    pass


def plot_emotion_timeline(scores: List[Dict]):
    """
    Plot emotion scores over time (optional - requires matplotlib).

    Args:
        scores: List of emotion scores
    """
    try:
        import matplotlib.pyplot as plt

        times = [s['time'] for s in scores]
        emotions = [s['emotion'] for s in scores]

        plt.figure(figsize=(12, 4))
        plt.plot(times, emotions, linewidth=2)
        plt.xlabel('Time (s)')
        plt.ylabel('Emotion Score')
        plt.title('Emotion Timeline')
        plt.grid(True, alpha=0.3)
        plt.ylim([0, 1])
        plt.show()
    except ImportError:
        print("matplotlib not installed - skipping plot")


# ============================================================
# TEST YOUR CODE
# ============================================================

def test_emotion_detector():
    """Test the emotion detector."""
    print("Testing EmotionDetector...")

    detector = EmotionDetector()

    # Test 1: Load audio
    print("\nTest 1: Load Audio")
    # TODO: Add path to your test audio file
    test_audio = "path/to/test/audio.wav"

    if os.path.exists(test_audio):
        audio = detector.load_audio(test_audio)
        print(f"✓ Loaded audio: {len(audio)} samples")
        print(f"  Duration: {len(audio)/detector.sample_rate:.2f}s")

    # Test 2: Extract features
    print("\nTest 2: Extract Features")
    if os.path.exists(test_audio):
        mfcc = detector.extract_mfcc(audio)
        energy = detector.extract_energy(audio)
        pitch = detector.extract_pitch(audio)

        print(f"✓ MFCC shape: {mfcc.shape}")
        print(f"✓ Energy shape: {energy.shape}")
        print(f"✓ Pitch shape: {pitch.shape}")

    # Test 3: Calculate emotions
    print("\nTest 3: Calculate Emotion Scores")
    if os.path.exists(test_audio):
        scores = detector.calculate_emotion_score(audio)
        print(f"✓ Calculated {len(scores)} emotion scores")

        # Show top 3 peaks
        peaks = detector.get_peak_moments(scores, threshold=0.6)
        print(f"✓ Found {len(peaks)} peak moments")
        for i, peak in enumerate(peaks[:3], 1):
            print(f"  {i}. Time: {peak['time']:.1f}s, Score: {peak['emotion']:.2f}")

    print("\n✓ Tests complete!")


if __name__ == '__main__':
    import os
    test_emotion_detector()
```

---

## ✏️ Exercises

### Exercise 1: Feature Visualization

```python
"""
Exercise 1: Visualize audio features
Understand what each feature looks like
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def visualize_audio_features(audio_file):
    """
    Create a visualization of all audio features.

    TODO: Complete this function to show:
    1. Waveform
    2. MFCC
    3. Energy
    4. Spectral Centroid
    5. Zero Crossing Rate
    """
    # Load audio
    y, sr = librosa.load(audio_file, sr=22050)

    # Create subplots
    fig, axes = plt.subplots(5, 1, figsize=(12, 10))

    # Plot 1: Waveform
    # TODO: Plot the raw waveform

    # Plot 2: MFCC
    # TODO: Plot MFCC heatmap

    # Plot 3: Energy
    # TODO: Plot RMS energy

    # Plot 4: Spectral Centroid
    # TODO: Plot spectral centroid

    # Plot 5: Zero Crossing Rate
    # TODO: Plot ZCR

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    visualize_audio_features("path/to/audio.wav")
```

### Exercise 2: Emotion Detection Algorithm

```python
"""
Exercise 2: Build your own emotion detection algorithm
Experiment with different approaches
"""

def simple_emotion_detector(energy, pitch):
    """
    Simple emotion detection using just energy and pitch.

    TODO: Implement a simple algorithm:
    - High energy + high pitch variation = high emotion
    - Low energy + low variation = low emotion

    Args:
        energy: Energy values over time
        pitch: Pitch values over time

    Returns:
        Emotion scores over time
    """
    # YOUR CODE HERE
    pass


def advanced_emotion_detector(mfcc, energy, pitch, zcr):
    """
    Advanced emotion detection using all features.

    TODO: Combine all features intelligently:
    - Weight each feature (e.g., energy: 40%, pitch: 30%, etc.)
    - Detect patterns (sustained high energy, sudden changes)
    - Consider speech activity (using ZCR)

    Returns:
        Emotion scores over time
    """
    # YOUR CODE HERE
    pass
```

---

## 🎯 Tasks for This Week

### Beginner Tasks
1. ✅ Install librosa (`pip install librosa`)
2. ✅ Implement `load_audio()`
3. ✅ Implement `extract_mfcc()`
4. ✅ Implement `extract_energy()`

### Intermediate Tasks
5. ✅ Implement `extract_pitch()`
6. ✅ Implement `normalize_array()`
7. ✅ Complete Exercise 1 (visualization)
8. ✅ Test with sample audio files

### Advanced Tasks
9. ✅ Implement `calculate_emotion_score()`
10. ✅ Implement `get_peak_moments()`
11. ✅ Complete Exercise 2 (algorithm design)
12. ✅ Optimize for speed

---

## 📝 Notes

### Understanding MFCC

MFCCs capture the spectral envelope of sound:
- Based on human hearing (mel scale)
- 13 coefficients capture most information
- Used in speech recognition
- Lower coefficients = overall spectrum shape
- Higher coefficients = fine details

### Energy vs Loudness

- **RMS Energy**: Mathematical measure
- **Loudness**: Perceived intensity (psychoacoustic)
- High energy often correlates with emotion
- Sudden changes are important

### Pitch Detection Challenges

- Works best with voice/single instruments
- Fails with multiple sources (polyphonic)
- Background noise causes issues
- Use magnitude to filter weak pitches

### Performance Tips

```python
# Slow: Process entire file
features = extract_features(full_audio)

# Fast: Process in chunks
for chunk in audio_chunks:
    features = extract_features(chunk)

# Faster: Use librosa's optimizations
features = librosa.feature.mfcc(y, sr, n_fft=2048, hop_length=512)
```

---

## 🔍 Testing Your Solution

```python
"""Week 2 Test Suite"""

def test_feature_extraction():
    """Test feature extraction."""
    detector = EmotionDetector()

    # Create test signal (sine wave)
    t = np.linspace(0, 1, 22050)
    test_signal = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave

    # Extract features
    mfcc = detector.extract_mfcc(test_signal)
    energy = detector.extract_energy(test_signal)

    # Validate shapes
    assert mfcc.shape[0] == 13, "MFCC should have 13 coefficients"
    assert len(energy) > 0, "Energy should be extracted"

    print("✓ Feature extraction tests passed")


def test_emotion_scoring():
    """Test emotion scoring algorithm."""
    detector = EmotionDetector()

    # Test with generated audio
    # High energy = high emotion
    # Low energy = low emotion

    # TODO: Add your tests

    print("✓ Emotion scoring tests passed")
```

---

## 📚 Resources

### Learn More:

1. **Librosa Tutorial**: https://librosa.org/doc/latest/tutorial.html
2. **MFCC Explained**: https://www.youtube.com/watch?v=4_SH2nfbQZ8
3. **Audio Signal Processing**: https://www.coursera.org/learn/audio-signal-processing

### Quick Reference:

```python
# Load audio
y, sr = librosa.load('audio.wav', sr=22050)

# Extract MFCC
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# Extract energy
rms = librosa.feature.rms(y=y)

# Extract spectral features
spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
zcr = librosa.feature.zero_crossing_rate(y)

# Extract pitch
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
```

---

## ✅ Completion Checklist

Before moving to Week 3:

- [ ] Understand what MFCCs represent
- [ ] Can extract energy from audio
- [ ] Can detect pitch
- [ ] Implemented emotion scoring algorithm
- [ ] Tested with real audio files
- [ ] Can identify peak moments
- [ ] Understand normalization

---

## 🎓 Next Steps

**Week 3: Text Topic Analysis** → Extract important topics from transcripts

---

**Questions?** Review the notes or check the solution code.
