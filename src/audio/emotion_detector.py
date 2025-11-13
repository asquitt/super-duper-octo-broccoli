"""Audio emotion detection using acoustic features."""

import numpy as np
import librosa
from typing import List, Tuple, Dict
from scipy import signal
from scipy.stats import skew, kurtosis
import warnings

warnings.filterwarnings('ignore')


class EmotionDetector:
    """Detect emotional intensity from audio using acoustic features."""

    def __init__(self, config: dict):
        """Initialize emotion detector with configuration."""
        self.config = config
        self.sample_rate = config.get('sample_rate', 22050)
        self.frame_length = config.get('frame_length', 2048)
        self.hop_length = config.get('hop_length', 512)
        self.window_size = config.get('emotion', {}).get('window_size', 3.0)

    def analyze(self, audio_path: str) -> List[Dict]:
        """
        Analyze audio file for emotional intensity.

        Returns:
            List of time-stamped emotion scores
        """
        # Load audio
        y, sr = librosa.load(audio_path, sr=self.sample_rate)

        # Extract features
        features = self._extract_features(y, sr)

        # Calculate emotion scores over time
        emotion_scores = self._calculate_emotion_scores(features, sr)

        return emotion_scores

    def _extract_features(self, y: np.ndarray, sr: int) -> Dict[str, np.ndarray]:
        """Extract acoustic features from audio signal."""
        features = {}

        # 1. MFCC (Mel-Frequency Cepstral Coefficients) - captures timbral texture
        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=self.config.get('emotion', {}).get('mfcc_coefficients', 13),
            n_fft=self.frame_length,
            hop_length=self.hop_length
        )
        features['mfcc'] = mfcc

        # 2. Spectral Centroid - brightness of sound
        spectral_centroid = librosa.feature.spectral_centroid(
            y=y,
            sr=sr,
            n_fft=self.frame_length,
            hop_length=self.hop_length
        )[0]
        features['spectral_centroid'] = spectral_centroid

        # 3. Zero Crossing Rate - noisiness/percussiveness
        zcr = librosa.feature.zero_crossing_rate(
            y=y,
            frame_length=self.frame_length,
            hop_length=self.hop_length
        )[0]
        features['zero_crossing_rate'] = zcr

        # 4. RMS Energy - loudness
        rms = librosa.feature.rms(
            y=y,
            frame_length=self.frame_length,
            hop_length=self.hop_length
        )[0]
        features['energy'] = rms

        # 5. Spectral Rolloff - shape of spectrum
        rolloff = librosa.feature.spectral_rolloff(
            y=y,
            sr=sr,
            n_fft=self.frame_length,
            hop_length=self.hop_length
        )[0]
        features['spectral_rolloff'] = rolloff

        # 6. Chroma features - harmonic content
        chroma = librosa.feature.chroma_stft(
            y=y,
            sr=sr,
            n_fft=self.frame_length,
            hop_length=self.hop_length
        )
        features['chroma'] = chroma

        # 7. Pitch (F0) using piptrack
        pitches, magnitudes = librosa.piptrack(
            y=y,
            sr=sr,
            n_fft=self.frame_length,
            hop_length=self.hop_length
        )
        # Get the pitch with highest magnitude at each frame
        pitch = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch.append(pitches[index, t])
        features['pitch'] = np.array(pitch)

        return features

    def _calculate_emotion_scores(self, features: Dict[str, np.ndarray],
                                  sr: int) -> List[Dict]:
        """Calculate emotion scores from features over time windows."""
        # Convert hop_length to time
        hop_time = self.hop_length / sr

        # Number of frames
        n_frames = features['energy'].shape[0]

        # Window size in frames
        window_frames = int(self.window_size / hop_time)

        emotion_scores = []

        for i in range(0, n_frames, window_frames // 2):  # 50% overlap
            end_idx = min(i + window_frames, n_frames)
            if end_idx - i < window_frames // 2:  # Skip incomplete windows
                break

            # Time stamp
            time_start = i * hop_time
            time_end = end_idx * hop_time

            # Extract window features
            window_features = {
                key: values[i:end_idx] if values.ndim == 1 else values[:, i:end_idx]
                for key, values in features.items()
            }

            # Calculate emotion indicators
            emotion_score = self._compute_emotion_score(window_features)

            emotion_scores.append({
                'time_start': time_start,
                'time_end': time_end,
                'emotion_score': emotion_score,
                'energy_score': self._compute_energy_score(window_features),
                'pitch_variation': self._compute_pitch_variation(window_features),
                'speech_activity': self._compute_speech_activity(window_features)
            })

        return emotion_scores

    def _compute_emotion_score(self, features: Dict[str, np.ndarray]) -> float:
        """Compute overall emotion score from features."""
        scores = []

        # 1. Energy variation (excitement, emphasis)
        energy = features['energy']
        energy_mean = np.mean(energy)
        energy_std = np.std(energy)
        energy_score = min(1.0, (energy_mean + energy_std) / 0.5)
        scores.append(energy_score * 0.3)

        # 2. Pitch variation (expressiveness)
        pitch = features['pitch']
        pitch_nonzero = pitch[pitch > 0]
        if len(pitch_nonzero) > 0:
            pitch_std = np.std(pitch_nonzero)
            pitch_score = min(1.0, pitch_std / 100.0)
            scores.append(pitch_score * 0.25)

        # 3. Spectral centroid variation (timbral changes)
        centroid = features['spectral_centroid']
        centroid_std = np.std(centroid)
        centroid_score = min(1.0, centroid_std / 1000.0)
        scores.append(centroid_score * 0.2)

        # 4. MFCC variation (voice quality changes)
        mfcc = features['mfcc']
        mfcc_var = np.var(mfcc, axis=1).mean()
        mfcc_score = min(1.0, mfcc_var / 50.0)
        scores.append(mfcc_score * 0.15)

        # 5. Zero crossing rate (emotion-related artifacts)
        zcr = features['zero_crossing_rate']
        zcr_mean = np.mean(zcr)
        zcr_score = min(1.0, zcr_mean / 0.2)
        scores.append(zcr_score * 0.1)

        return sum(scores)

    def _compute_energy_score(self, features: Dict[str, np.ndarray]) -> float:
        """Compute energy/loudness score."""
        energy = features['energy']
        energy_mean = np.mean(energy)
        energy_max = np.max(energy)

        # Combine mean and max
        score = (energy_mean * 0.6 + energy_max * 0.4)

        return min(1.0, score / 0.3)

    def _compute_pitch_variation(self, features: Dict[str, np.ndarray]) -> float:
        """Compute pitch variation score."""
        pitch = features['pitch']
        pitch_nonzero = pitch[pitch > 0]

        if len(pitch_nonzero) < 2:
            return 0.0

        # Calculate coefficient of variation
        pitch_mean = np.mean(pitch_nonzero)
        pitch_std = np.std(pitch_nonzero)

        if pitch_mean == 0:
            return 0.0

        cv = pitch_std / pitch_mean

        return min(1.0, cv * 2.0)

    def _compute_speech_activity(self, features: Dict[str, np.ndarray]) -> float:
        """Compute speech activity score (vs silence)."""
        energy = features['energy']

        # Voice activity detection using energy threshold
        energy_threshold = np.percentile(energy, 30)
        active_frames = np.sum(energy > energy_threshold)
        total_frames = len(energy)

        return active_frames / total_frames if total_frames > 0 else 0.0

    def get_peak_emotion_segments(self, emotion_scores: List[Dict],
                                  threshold: float = 0.7,
                                  min_duration: float = 5.0) -> List[Dict]:
        """
        Find segments with peak emotional intensity.

        Args:
            emotion_scores: List of emotion scores over time
            threshold: Minimum emotion score threshold
            min_duration: Minimum segment duration in seconds

        Returns:
            List of peak emotion segments
        """
        peaks = []

        for score_data in emotion_scores:
            if score_data['emotion_score'] >= threshold:
                duration = score_data['time_end'] - score_data['time_start']
                if duration >= min_duration:
                    peaks.append({
                        'start_time': score_data['time_start'],
                        'end_time': score_data['time_end'],
                        'score': score_data['emotion_score'],
                        'energy': score_data['energy_score'],
                        'pitch_var': score_data['pitch_variation']
                    })

        # Sort by score
        peaks.sort(key=lambda x: x['score'], reverse=True)

        return peaks
