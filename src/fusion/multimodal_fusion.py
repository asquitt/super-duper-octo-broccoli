"""Multimodal fusion agent to combine audio, text, and visual signals."""

import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict
import re


class MultimodalFusion:
    """Fuse multiple modality signals to identify engaging clips."""

    def __init__(self, config: dict):
        """Initialize fusion agent with configuration."""
        self.config = config
        self.strategy = config.get('strategy', 'weighted')
        self.weights = config.get('weights', {
            'audio': 0.35,
            'text': 0.40,
            'visual': 0.25
        })
        self.min_clip_duration = config.get('min_clip_duration', 30)
        self.max_clip_duration = config.get('max_clip_duration', 60)
        self.num_clips = config.get('num_clips', 5)

    def fuse_signals(self,
                    audio_scores: List[Dict],
                    text_scores: List[Dict],
                    visual_scores: List[Dict],
                    duration: float) -> List[Dict]:
        """
        Fuse audio, text, and visual signals to identify best clips.

        Args:
            audio_scores: Emotion scores from audio analysis
            text_scores: Topic scores from text analysis
            visual_scores: Engagement scores from visual analysis
            duration: Total video duration in seconds

        Returns:
            List of candidate clips with fused scores
        """
        # Create time grid (1-second resolution)
        time_grid = np.arange(0, duration, 1.0)

        # Interpolate each modality onto time grid
        audio_timeline = self._interpolate_scores(audio_scores, time_grid, 'emotion_score')
        text_timeline = self._interpolate_scores(text_scores, time_grid, 'topic_score')
        visual_timeline = self._interpolate_scores(visual_scores, time_grid, 'engagement_score')

        # Apply fusion strategy
        if self.strategy == 'weighted':
            fused_timeline = self._weighted_fusion(
                audio_timeline,
                text_timeline,
                visual_timeline
            )
        elif self.strategy == 'learned':
            fused_timeline = self._learned_fusion(
                audio_timeline,
                text_timeline,
                visual_timeline
            )
        else:  # llm-based
            fused_timeline = self._weighted_fusion(
                audio_timeline,
                text_timeline,
                visual_timeline
            )

        # Identify candidate clips
        candidates = self._identify_candidates(
            fused_timeline,
            time_grid,
            audio_scores,
            text_scores,
            visual_scores
        )

        return candidates

    def _interpolate_scores(self, scores: List[Dict], time_grid: np.ndarray,
                           score_key: str) -> np.ndarray:
        """Interpolate scores onto a uniform time grid."""
        timeline = np.zeros(len(time_grid))

        if not scores:
            return timeline

        for score_data in scores:
            start = score_data.get('time_start', score_data.get('start', 0))
            end = score_data.get('time_end', score_data.get('end', 0))
            score = score_data.get(score_key, 0.0)

            # Find indices in time grid
            start_idx = np.searchsorted(time_grid, start)
            end_idx = np.searchsorted(time_grid, end)

            # Fill timeline
            timeline[start_idx:end_idx] = np.maximum(
                timeline[start_idx:end_idx],
                score
            )

        # Smooth timeline (moving average)
        window_size = 3
        timeline = np.convolve(
            timeline,
            np.ones(window_size) / window_size,
            mode='same'
        )

        return timeline

    def _weighted_fusion(self, audio: np.ndarray, text: np.ndarray,
                        visual: np.ndarray) -> np.ndarray:
        """Simple weighted fusion of modalities."""
        # Normalize each modality
        audio = self._normalize(audio)
        text = self._normalize(text)
        visual = self._normalize(visual)

        # Apply weights
        fused = (
            audio * self.weights['audio'] +
            text * self.weights['text'] +
            visual * self.weights['visual']
        )

        # Boost where multiple signals align (synergy bonus)
        if self.config.get('ranking', {}).get('boost_combined_signals', True):
            # Calculate agreement (all modalities above threshold)
            threshold = 0.5
            audio_high = audio > threshold
            text_high = text > threshold
            visual_high = visual > threshold

            # Synergy: boost when 2+ modalities are high
            synergy = (audio_high.astype(int) +
                      text_high.astype(int) +
                      visual_high.astype(int))

            boost = np.where(synergy >= 2, 0.15, 0.0)
            fused = np.minimum(1.0, fused + boost)

        return fused

    def _learned_fusion(self, audio: np.ndarray, text: np.ndarray,
                       visual: np.ndarray) -> np.ndarray:
        """
        Learned fusion using simple heuristics (placeholder for ML model).

        In production, this could be replaced with a trained model.
        """
        # For now, use adaptive weights based on signal strength
        audio_strength = np.mean(audio)
        text_strength = np.mean(text)
        visual_strength = np.mean(visual)

        total_strength = audio_strength + text_strength + visual_strength

        if total_strength > 0:
            adaptive_weights = {
                'audio': audio_strength / total_strength,
                'text': text_strength / total_strength,
                'visual': visual_strength / total_strength
            }
        else:
            adaptive_weights = self.weights

        # Normalize
        audio = self._normalize(audio)
        text = self._normalize(text)
        visual = self._normalize(visual)

        # Fuse with adaptive weights
        fused = (
            audio * adaptive_weights['audio'] +
            text * adaptive_weights['text'] +
            visual * adaptive_weights['visual']
        )

        return fused

    def _normalize(self, arr: np.ndarray) -> np.ndarray:
        """Normalize array to [0, 1] range."""
        if arr.max() == arr.min():
            return arr

        return (arr - arr.min()) / (arr.max() - arr.min())

    def _identify_candidates(self, fused_timeline: np.ndarray,
                            time_grid: np.ndarray,
                            audio_scores: List[Dict],
                            text_scores: List[Dict],
                            visual_scores: List[Dict]) -> List[Dict]:
        """Identify candidate clips from fused timeline."""
        min_score = self.config.get('ranking', {}).get('min_score', 0.5)

        candidates = []

        # Find peaks in timeline
        peaks = self._find_peaks(fused_timeline, min_score)

        for peak_idx in peaks:
            peak_time = time_grid[peak_idx]

            # Determine clip boundaries
            start_time, end_time = self._determine_clip_boundaries(
                peak_idx,
                fused_timeline,
                time_grid
            )

            # Ensure duration constraints
            duration = end_time - start_time
            if duration < self.min_clip_duration:
                # Extend clip
                extension = (self.min_clip_duration - duration) / 2
                start_time = max(0, start_time - extension)
                end_time = min(time_grid[-1], end_time + extension)
            elif duration > self.max_clip_duration:
                # Trim clip around peak
                half_duration = self.max_clip_duration / 2
                start_time = max(0, peak_time - half_duration)
                end_time = min(time_grid[-1], peak_time + half_duration)

            # Calculate component scores
            audio_score = self._get_score_at_time(audio_scores, start_time, end_time, 'emotion_score')
            text_score = self._get_score_at_time(text_scores, start_time, end_time, 'topic_score')
            visual_score = self._get_score_at_time(visual_scores, start_time, end_time, 'engagement_score')

            # Calculate overall score
            overall_score = (
                audio_score * self.weights['audio'] +
                text_score * self.weights['text'] +
                visual_score * self.weights['visual']
            )

            # Get context (text snippets)
            text_context = self._get_text_context(text_scores, start_time, end_time)

            candidates.append({
                'start_time': start_time,
                'end_time': end_time,
                'duration': end_time - start_time,
                'score': overall_score,
                'audio_score': audio_score,
                'text_score': text_score,
                'visual_score': visual_score,
                'text_context': text_context
            })

        # Remove overlapping candidates (keep higher scored ones)
        candidates = self._remove_overlaps(candidates)

        # Sort by score
        candidates.sort(key=lambda x: x['score'], reverse=True)

        return candidates

    def _find_peaks(self, timeline: np.ndarray, min_score: float) -> List[int]:
        """Find peaks in timeline."""
        peaks = []

        # Simple peak detection: local maxima above threshold
        for i in range(1, len(timeline) - 1):
            if timeline[i] > min_score:
                if timeline[i] > timeline[i-1] and timeline[i] > timeline[i+1]:
                    peaks.append(i)

        return peaks

    def _determine_clip_boundaries(self, peak_idx: int,
                                   timeline: np.ndarray,
                                   time_grid: np.ndarray) -> Tuple[float, float]:
        """Determine clip start and end times around a peak."""
        # Find where score drops below threshold
        threshold = timeline[peak_idx] * 0.6

        # Search backwards for start
        start_idx = peak_idx
        for i in range(peak_idx - 1, -1, -1):
            if timeline[i] < threshold:
                break
            start_idx = i

        # Search forwards for end
        end_idx = peak_idx
        for i in range(peak_idx + 1, len(timeline)):
            if timeline[i] < threshold:
                break
            end_idx = i

        start_time = time_grid[start_idx]
        end_time = time_grid[min(end_idx + 1, len(time_grid) - 1)]

        return start_time, end_time

    def _get_score_at_time(self, scores: List[Dict], start_time: float,
                          end_time: float, score_key: str) -> float:
        """Get average score in time range."""
        if not scores:
            return 0.0

        relevant_scores = []

        for score_data in scores:
            score_start = score_data.get('time_start', score_data.get('start', 0))
            score_end = score_data.get('time_end', score_data.get('end', 0))

            # Check for overlap
            if score_end >= start_time and score_start <= end_time:
                relevant_scores.append(score_data.get(score_key, 0.0))

        return np.mean(relevant_scores) if relevant_scores else 0.0

    def _get_text_context(self, text_scores: List[Dict],
                         start_time: float, end_time: float) -> str:
        """Get text snippets in time range."""
        if not text_scores:
            return ""

        texts = []

        for score_data in text_scores:
            score_start = score_data.get('time_start', score_data.get('start', 0))
            score_end = score_data.get('time_end', score_data.get('end', 0))

            # Check for overlap
            if score_end >= start_time and score_start <= end_time:
                text = score_data.get('text', '')
                if text:
                    texts.append(text)

        return ' '.join(texts)

    def _remove_overlaps(self, candidates: List[Dict]) -> List[Dict]:
        """Remove overlapping candidates, keeping higher scored ones."""
        if not candidates:
            return []

        # Sort by score (descending)
        sorted_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)

        overlap_threshold = self.config.get('overlap_threshold', 0.3)

        keep = []

        for candidate in sorted_candidates:
            overlaps = False

            for kept in keep:
                if self._calculate_overlap(candidate, kept) > overlap_threshold:
                    overlaps = True
                    break

            if not overlaps:
                keep.append(candidate)

        return keep

    def _calculate_overlap(self, clip1: Dict, clip2: Dict) -> float:
        """Calculate overlap ratio between two clips."""
        start1, end1 = clip1['start_time'], clip1['end_time']
        start2, end2 = clip2['start_time'], clip2['end_time']

        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)

        if overlap_end <= overlap_start:
            return 0.0

        overlap_duration = overlap_end - overlap_start
        min_duration = min(end1 - start1, end2 - start2)

        return overlap_duration / min_duration
