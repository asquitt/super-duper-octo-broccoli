"""Visual engagement detection using computer vision."""

import cv2
import numpy as np
from typing import List, Dict, Optional
import os
from pathlib import Path


class EngagementDetector:
    """Detect visual engagement cues from video."""

    def __init__(self, config: dict):
        """Initialize engagement detector with configuration."""
        self.config = config
        self.face_cascade = None
        self.sampling_fps = config.get('sampling', {}).get('fps', 1)

        # Load face detection cascade if enabled
        if config.get('face_detection', {}).get('enabled', True):
            self._load_face_detector()

    def _load_face_detector(self):
        """Load Haar Cascade for face detection."""
        cascade_name = self.config.get('face_detection', {}).get(
            'cascade',
            'haarcascade_frontalface_default.xml'
        )

        # Try multiple locations
        cascade_paths = [
            cascade_name,
            os.path.join(cv2.data.haarcascades, cascade_name),
            f'/usr/share/opencv4/haarcascades/{cascade_name}',
            f'/usr/local/share/opencv4/haarcascades/{cascade_name}'
        ]

        for path in cascade_paths:
            if os.path.exists(path):
                self.face_cascade = cv2.CascadeClassifier(path)
                if not self.face_cascade.empty():
                    print(f"Loaded face detector from: {path}")
                    return

        print("Warning: Could not load face detector. Face detection disabled.")
        self.config['face_detection']['enabled'] = False

    def analyze(self, video_path: str) -> List[Dict]:
        """
        Analyze video for visual engagement cues.

        Args:
            video_path: Path to video file

        Returns:
            List of time-stamped engagement scores
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        print(f"Analyzing video: {duration:.1f}s, {fps:.1f} FPS, {total_frames} frames")

        # Calculate frame sampling
        frame_step = max(1, int(fps / self.sampling_fps))

        engagement_scores = []
        prev_frame = None
        frame_idx = 0

        window_size = int(self.sampling_fps * 5)  # 5-second windows
        window_data = []

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Sample frames
            if frame_idx % frame_step == 0:
                timestamp = frame_idx / fps

                # Analyze frame
                frame_data = self._analyze_frame(
                    frame,
                    prev_frame,
                    timestamp
                )

                window_data.append(frame_data)

                # Process window
                if len(window_data) >= window_size:
                    window_score = self._calculate_window_score(window_data)
                    engagement_scores.append(window_score)
                    # Slide window (50% overlap)
                    window_data = window_data[window_size // 2:]

                prev_frame = frame.copy()

            frame_idx += 1

        cap.release()

        # Process remaining window
        if window_data:
            window_score = self._calculate_window_score(window_data)
            engagement_scores.append(window_score)

        return engagement_scores

    def _analyze_frame(self, frame: np.ndarray, prev_frame: Optional[np.ndarray],
                      timestamp: float) -> Dict:
        """Analyze a single frame for engagement cues."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame_data = {
            'timestamp': timestamp,
            'face_count': 0,
            'face_area': 0.0,
            'motion_score': 0.0,
            'scene_change': False,
            'brightness': 0.0
        }

        # Face detection
        if self.config.get('face_detection', {}).get('enabled', False):
            faces = self._detect_faces(gray)
            frame_data['face_count'] = len(faces)

            if faces:
                total_area = sum(w * h for (x, y, w, h) in faces)
                frame_area = frame.shape[0] * frame.shape[1]
                frame_data['face_area'] = total_area / frame_area

        # Motion detection
        if prev_frame is not None and self.config.get('motion_detection', {}).get('enabled', True):
            motion_score = self._detect_motion(gray, prev_frame)
            frame_data['motion_score'] = motion_score

            # Scene change detection
            if self.config.get('scene_change', {}).get('enabled', True):
                scene_change = self._detect_scene_change(gray, prev_frame)
                frame_data['scene_change'] = scene_change

        # Brightness (can indicate spotlight moments)
        frame_data['brightness'] = np.mean(gray) / 255.0

        return frame_data

    def _detect_faces(self, gray_frame: np.ndarray) -> List:
        """Detect faces in frame."""
        if self.face_cascade is None or self.face_cascade.empty():
            return []

        scale_factor = self.config.get('face_detection', {}).get('scale_factor', 1.1)
        min_neighbors = self.config.get('face_detection', {}).get('min_neighbors', 5)

        faces = self.face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors
        )

        return faces

    def _detect_motion(self, current_gray: np.ndarray,
                      prev_frame: np.ndarray) -> float:
        """Detect motion between frames."""
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) if len(prev_frame.shape) == 3 else prev_frame

        # Resize if needed for speed
        if current_gray.shape[0] > 480:
            scale = 480 / current_gray.shape[0]
            current_gray = cv2.resize(current_gray, None, fx=scale, fy=scale)
            prev_gray = cv2.resize(prev_gray, None, fx=scale, fy=scale)

        # Calculate frame difference
        frame_diff = cv2.absdiff(current_gray, prev_gray)

        # Threshold
        threshold = self.config.get('motion_detection', {}).get('threshold', 25)
        _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)

        # Calculate motion score
        motion_pixels = np.sum(thresh > 0)
        total_pixels = thresh.shape[0] * thresh.shape[1]

        motion_score = motion_pixels / total_pixels

        return motion_score

    def _detect_scene_change(self, current_gray: np.ndarray,
                            prev_frame: np.ndarray) -> bool:
        """Detect scene changes (cuts, transitions)."""
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) if len(prev_frame.shape) == 3 else prev_frame

        # Calculate histogram difference
        hist1 = cv2.calcHist([current_gray], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([prev_gray], [0], None, [256], [0, 256])

        # Normalize
        hist1 = hist1 / hist1.sum()
        hist2 = hist2 / hist2.sum()

        # Compare histograms
        diff = np.sum(np.abs(hist1 - hist2))

        threshold = self.config.get('scene_change', {}).get('threshold', 30.0)

        return diff > threshold

    def _calculate_window_score(self, window_data: List[Dict]) -> Dict:
        """Calculate engagement score for a window of frames."""
        if not window_data:
            return {
                'time_start': 0.0,
                'time_end': 0.0,
                'engagement_score': 0.0
            }

        time_start = window_data[0]['timestamp']
        time_end = window_data[-1]['timestamp']

        # Extract metrics
        face_counts = [d['face_count'] for d in window_data]
        face_areas = [d['face_area'] for d in window_data]
        motion_scores = [d['motion_score'] for d in window_data]
        scene_changes = [d['scene_change'] for d in window_data]

        # Calculate component scores

        # 1. Face activity score
        face_activity = 0.0
        if self.config.get('face_detection', {}).get('enabled', False):
            avg_faces = np.mean(face_counts)
            face_variance = np.var(face_counts)
            avg_face_area = np.mean(face_areas)

            face_activity = min(1.0, (avg_faces * 0.3 + face_variance * 0.3 + avg_face_area * 0.4))

        # 2. Motion activity score
        motion_activity = 0.0
        if self.config.get('motion_detection', {}).get('enabled', True):
            avg_motion = np.mean(motion_scores)
            motion_variance = np.var(motion_scores)
            motion_peaks = sum(1 for m in motion_scores if m > np.mean(motion_scores) * 1.5)

            motion_activity = min(1.0, avg_motion * 0.5 + motion_variance * 2.0 + motion_peaks / len(motion_scores) * 0.3)

        # 3. Scene change score
        scene_change_score = 0.0
        if self.config.get('scene_change', {}).get('enabled', True):
            num_changes = sum(scene_changes)
            scene_change_score = min(1.0, num_changes * 0.3)

        # Combine scores
        thresholds = self.config.get('thresholds', {})
        face_weight = 0.4 if face_activity > 0 else 0.0
        motion_weight = 0.4
        scene_weight = 0.2

        # Normalize weights
        total_weight = face_weight + motion_weight + scene_weight
        if total_weight > 0:
            face_weight /= total_weight
            motion_weight /= total_weight
            scene_weight /= total_weight

        engagement_score = (
            face_activity * face_weight +
            motion_activity * motion_weight +
            scene_change_score * scene_weight
        )

        return {
            'time_start': time_start,
            'time_end': time_end,
            'engagement_score': engagement_score,
            'face_activity': face_activity,
            'motion_activity': motion_activity,
            'scene_changes': sum(scene_changes)
        }

    def get_peak_engagement_segments(self, engagement_scores: List[Dict],
                                    threshold: float = 0.7,
                                    min_duration: float = 5.0) -> List[Dict]:
        """Find segments with high visual engagement."""
        peaks = []

        for score_data in engagement_scores:
            if score_data['engagement_score'] >= threshold:
                duration = score_data['time_end'] - score_data['time_start']
                if duration >= min_duration:
                    peaks.append({
                        'start_time': score_data['time_start'],
                        'end_time': score_data['time_end'],
                        'score': score_data['engagement_score'],
                        'face_activity': score_data['face_activity'],
                        'motion_activity': score_data['motion_activity']
                    })

        # Sort by score
        peaks.sort(key=lambda x: x['score'], reverse=True)

        return peaks
