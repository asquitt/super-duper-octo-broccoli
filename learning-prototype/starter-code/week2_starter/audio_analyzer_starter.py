"""
Week 2 Starter Code: Audio Emotion Analyzer
File: audio_analyzer_starter.py

INSTRUCTIONS:
1. Read through the code structure
2. Fill in the TODO sections
3. Run the tests at the bottom
4. Compare with solution when done

TIPS:
- librosa.load() loads audio files
- librosa.feature.mfcc() extracts MFCC features
- Use numpy for array operations
- Normalize scores to 0-1 range
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Try to import librosa
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠ Warning: librosa not installed!")
    print("Install with: pip install librosa")


class AudioEmotionAnalyzer:
    """
    Analyze audio for emotional content.

    Features extracted:
    - MFCC (Mel-Frequency Cepstral Coefficients)
    - RMS Energy
    - Spectral Centroid (pitch/brightness)
    """

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize the audio analyzer.

        Args:
            sample_rate: Sample rate for audio processing
        """
        self.sample_rate = sample_rate

    def load_audio(self, audio_path: str) -> np.ndarray:
        """
        Load audio file.

        Args:
            audio_path: Path to audio file

        Returns:
            Audio time series as numpy array

        Example:
            >>> analyzer = AudioEmotionAnalyzer()
            >>> audio = analyzer.load_audio("audio.wav")
            >>> print(f"Loaded {len(audio)} samples")
        """
        if not LIBROSA_AVAILABLE:
            raise ImportError("librosa is required for audio processing")

        # TODO: Use librosa.load() to load audio
        # Hint: audio, sr = librosa.load(audio_path, sr=self.sample_rate)

        raise NotImplementedError("TODO: Implement load_audio()")

    def extract_mfcc(self, audio: np.ndarray, n_mfcc: int = 13) -> np.ndarray:
        """
        Extract MFCC features.

        MFCCs represent the spectral envelope of the audio signal.
        Higher values indicate more energy at certain frequencies.

        Args:
            audio: Audio time series
            n_mfcc: Number of MFCC coefficients to extract

        Returns:
            MFCC features, shape (n_mfcc, n_frames)

        Example:
            >>> mfcc = analyzer.extract_mfcc(audio)
            >>> print(f"MFCC shape: {mfcc.shape}")
        """
        if not LIBROSA_AVAILABLE:
            raise ImportError("librosa is required")

        # TODO: Use librosa.feature.mfcc() to extract MFCCs
        #
        # Steps:
        # 1. Call librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=n_mfcc)
        # 2. Return the result
        #
        # Hint: mfcc = librosa.feature.mfcc(...)

        raise NotImplementedError("TODO: Implement extract_mfcc()")

    def calculate_energy(self, audio: np.ndarray, frame_length: int = 2048) -> np.ndarray:
        """
        Calculate RMS (Root Mean Square) energy over time.

        High energy = Loud, intense moments
        Low energy = Quiet, calm moments

        Args:
            audio: Audio time series
            frame_length: Length of analysis frame

        Returns:
            RMS energy for each frame

        Example:
            >>> energy = analyzer.calculate_energy(audio)
            >>> print(f"Max energy: {energy.max():.3f}")
        """
        if not LIBROSA_AVAILABLE:
            raise ImportError("librosa is required")

        # TODO: Use librosa.feature.rms() to calculate energy
        #
        # Steps:
        # 1. Call librosa.feature.rms(y=audio, frame_length=frame_length)
        # 2. Flatten the result (it returns 2D array, we want 1D)
        # 3. Return the energy array
        #
        # Hint: rms = librosa.feature.rms(y=audio, frame_length=frame_length)
        # Hint: return rms.flatten()

        raise NotImplementedError("TODO: Implement calculate_energy()")

    def calculate_spectral_centroid(self, audio: np.ndarray) -> np.ndarray:
        """
        Calculate spectral centroid (brightness/pitch indicator).

        High centroid = Bright, high-pitched sounds
        Low centroid = Dark, low-pitched sounds

        Args:
            audio: Audio time series

        Returns:
            Spectral centroid for each frame

        Example:
            >>> centroid = analyzer.calculate_spectral_centroid(audio)
            >>> print(f"Avg centroid: {centroid.mean():.1f} Hz")
        """
        if not LIBROSA_AVAILABLE:
            raise ImportError("librosa is required")

        # TODO: Use librosa.feature.spectral_centroid()
        #
        # Hint: centroid = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)
        # Hint: return centroid.flatten()

        raise NotImplementedError("TODO: Implement calculate_spectral_centroid()")

    def calculate_emotion_score(self, audio: np.ndarray) -> float:
        """
        Calculate overall emotion/engagement score.

        Combines:
        - Energy (intensity)
        - MFCC variance (spectral dynamics)
        - Spectral centroid variance (pitch variation)

        Args:
            audio: Audio time series

        Returns:
            Emotion score (0.0 = calm/boring, 1.0 = exciting/engaging)

        Example:
            >>> score = analyzer.calculate_emotion_score(audio)
            >>> print(f"Emotion score: {score:.2f}")
        """
        # TODO: Combine features to calculate emotion score
        #
        # Steps:
        # 1. Extract energy
        # 2. Extract MFCCs
        # 3. Extract spectral centroid
        # 4. Calculate statistics (mean, variance, max)
        # 5. Combine into single score
        #
        # Suggested formula:
        # score = (
        #     normalized_energy_mean * 0.4 +
        #     mfcc_variance * 0.3 +
        #     centroid_variance * 0.3
        # )

        # Extract features
        energy = self.calculate_energy(audio)
        mfcc = self.extract_mfcc(audio)
        centroid = self.calculate_spectral_centroid(audio)

        # YOUR CODE HERE
        # Calculate statistics from features
        # energy_mean = ...
        # mfcc_var = ...
        # centroid_var = ...

        # Normalize and combine
        # score = ...

        raise NotImplementedError("TODO: Implement calculate_emotion_score()")

    def analyze_segments(self, audio: np.ndarray, segment_duration: float = 5.0):
        """
        Analyze audio in segments over time.

        Args:
            audio: Audio time series
            segment_duration: Length of each segment in seconds

        Returns:
            List of (time, score) tuples

        Example:
            >>> segments = analyzer.analyze_segments(audio)
            >>> for time, score in segments:
            >>>     print(f"{time:.1f}s: {score:.2f}")
        """
        # TODO: Split audio into segments and analyze each
        #
        # Steps:
        # 1. Calculate samples per segment
        # 2. Split audio into chunks
        # 3. Calculate score for each chunk
        # 4. Return list of (time, score)

        segment_samples = int(segment_duration * self.sample_rate)
        results = []

        # YOUR CODE HERE
        # Hint: Use a loop to process each segment
        # for i in range(0, len(audio), segment_samples):
        #     segment = audio[i:i+segment_samples]
        #     if len(segment) < segment_samples // 2:
        #         break  # Skip short segments at end
        #     score = self.calculate_emotion_score(segment)
        #     time = i / self.sample_rate
        #     results.append((time, score))

        raise NotImplementedError("TODO: Implement analyze_segments()")


# ============================================================
# TESTS - Run this file to test your implementation
# ============================================================

def run_tests():
    """Test the AudioEmotionAnalyzer implementation."""
    print("\n" + "="*60)
    print("TESTING AUDIO EMOTION ANALYZER")
    print("="*60 + "\n")

    if not LIBROSA_AVAILABLE:
        print("⚠ Cannot run tests: librosa not installed")
        print("Install with: pip install librosa soundfile")
        return

    analyzer = AudioEmotionAnalyzer()

    # Test 1: Generate synthetic audio
    print("Test 1: Synthetic Audio Generation")
    print("-" * 40)
    try:
        # Generate 5 seconds of test audio
        duration = 5.0
        t = np.linspace(0, duration, int(duration * analyzer.sample_rate))

        # Mix of frequencies (simulate speech/music)
        audio = (
            0.5 * np.sin(2 * np.pi * 440 * t) +  # A4 note
            0.3 * np.sin(2 * np.pi * 880 * t) +  # A5 note
            0.1 * np.random.randn(len(t))        # Noise
        )

        print(f"✓ Generated {duration}s of test audio")
        print(f"  Samples: {len(audio)}")
        print(f"  Sample rate: {analyzer.sample_rate} Hz")

    except Exception as e:
        print(f"✗ Error generating audio: {e}")
        return

    # Test 2: Feature Extraction
    print("\nTest 2: Feature Extraction")
    print("-" * 40)
    try:
        # MFCC
        mfcc = analyzer.extract_mfcc(audio)
        print(f"✓ MFCC shape: {mfcc.shape}")
        assert mfcc.shape[0] == 13, "Should have 13 MFCC coefficients"

        # Energy
        energy = analyzer.calculate_energy(audio)
        print(f"✓ Energy shape: {energy.shape}")
        print(f"  Max energy: {energy.max():.3f}")

        # Spectral centroid
        centroid = analyzer.calculate_spectral_centroid(audio)
        print(f"✓ Spectral centroid shape: {centroid.shape}")
        print(f"  Mean centroid: {centroid.mean():.1f} Hz")

    except NotImplementedError:
        print("⚠ Feature extraction not yet implemented")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 3: Emotion Scoring
    print("\nTest 3: Emotion Scoring")
    print("-" * 40)
    try:
        score = analyzer.calculate_emotion_score(audio)
        print(f"✓ Emotion score: {score:.3f}")
        assert 0.0 <= score <= 1.0, "Score should be in [0, 1] range"

        # Test with different audio types
        silent = np.zeros(len(audio))
        silent_score = analyzer.calculate_emotion_score(silent)
        print(f"✓ Silent audio score: {silent_score:.3f}")

        loud = np.ones(len(audio))
        loud_score = analyzer.calculate_emotion_score(loud)
        print(f"✓ Loud audio score: {loud_score:.3f}")

    except NotImplementedError:
        print("⚠ Emotion scoring not yet implemented")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 4: Segment Analysis
    print("\nTest 4: Segment Analysis")
    print("-" * 40)
    try:
        segments = analyzer.analyze_segments(audio, segment_duration=1.0)
        print(f"✓ Analyzed {len(segments)} segments")

        for time, score in segments:
            bar = '#' * int(score * 20)
            print(f"  {time:4.1f}s: {bar} ({score:.2f})")

    except NotImplementedError:
        print("⚠ Segment analysis not yet implemented")
    except Exception as e:
        print(f"✗ Error: {e}")

    print("\n" + "="*60)
    print("Testing complete!")
    print("Compare your implementation with the solution.")
    print("="*60 + "\n")


if __name__ == '__main__':
    run_tests()
