"""Evaluation metrics for clip extraction quality."""

import numpy as np
from typing import List, Dict, Tuple


class EvaluationMetrics:
    """Calculate evaluation metrics for clip extraction."""

    @staticmethod
    def calculate_iou(clip1: Dict, clip2: Dict) -> float:
        """
        Calculate Intersection over Union (IoU) for two clips.

        Args:
            clip1: {'start_time': float, 'end_time': float}
            clip2: {'start_time': float, 'end_time': float}

        Returns:
            IoU score (0-1)
        """
        start1, end1 = clip1['start_time'], clip1['end_time']
        start2, end2 = clip2['start_time'], clip2['end_time']

        # Calculate intersection
        intersection_start = max(start1, start2)
        intersection_end = min(end1, end2)
        intersection = max(0, intersection_end - intersection_start)

        # Calculate union
        union_start = min(start1, start2)
        union_end = max(end1, end2)
        union = union_end - union_start

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def calculate_map(predicted_clips: List[Dict], ground_truth_clips: List[Dict],
                     iou_threshold: float = 0.5) -> float:
        """
        Calculate mean Average Precision (mAP).

        Args:
            predicted_clips: List of predicted clips with scores
            ground_truth_clips: List of ground truth clips
            iou_threshold: IoU threshold for considering a match

        Returns:
            mAP score (0-1)
        """
        if not predicted_clips or not ground_truth_clips:
            return 0.0

        # Sort predictions by score (descending)
        sorted_preds = sorted(predicted_clips, key=lambda x: x.get('score', 0), reverse=True)

        # Track which ground truth clips have been matched
        matched_gt = set()
        precisions = []
        num_correct = 0

        for i, pred_clip in enumerate(sorted_preds):
            # Find best matching ground truth clip
            best_iou = 0.0
            best_gt_idx = -1

            for gt_idx, gt_clip in enumerate(ground_truth_clips):
                if gt_idx in matched_gt:
                    continue

                iou = EvaluationMetrics.calculate_iou(pred_clip, gt_clip)
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = gt_idx

            # Check if match is valid
            if best_iou >= iou_threshold and best_gt_idx != -1:
                matched_gt.add(best_gt_idx)
                num_correct += 1

            # Calculate precision at this rank
            precision = num_correct / (i + 1)
            precisions.append(precision)

        # Calculate average precision
        ap = np.mean(precisions) if precisions else 0.0
        return ap

    @staticmethod
    def calculate_hit_at_k(predicted_clips: List[Dict], ground_truth_clips: List[Dict],
                          k: int = 1, iou_threshold: float = 0.5) -> float:
        """
        Calculate HIT@K metric.

        Args:
            predicted_clips: List of predicted clips with scores
            ground_truth_clips: List of ground truth clips
            k: Number of top predictions to consider
            iou_threshold: IoU threshold for considering a match

        Returns:
            HIT@K score (0-1)
        """
        if not predicted_clips or not ground_truth_clips:
            return 0.0

        # Sort predictions by score (descending)
        sorted_preds = sorted(predicted_clips, key=lambda x: x.get('score', 0), reverse=True)
        top_k_preds = sorted_preds[:k]

        # Check if any top-k prediction matches any ground truth
        for pred_clip in top_k_preds:
            for gt_clip in ground_truth_clips:
                iou = EvaluationMetrics.calculate_iou(pred_clip, gt_clip)
                if iou >= iou_threshold:
                    return 1.0

        return 0.0

    @staticmethod
    def calculate_precision_recall_f1(predicted_clips: List[Dict],
                                     ground_truth_clips: List[Dict],
                                     iou_threshold: float = 0.5) -> Tuple[float, float, float]:
        """
        Calculate Precision, Recall, and F1-score.

        Args:
            predicted_clips: List of predicted clips
            ground_truth_clips: List of ground truth clips
            iou_threshold: IoU threshold for considering a match

        Returns:
            Tuple of (precision, recall, f1_score)
        """
        if not predicted_clips:
            return 0.0, 0.0, 0.0

        if not ground_truth_clips:
            return 0.0, 0.0, 0.0

        # Find true positives
        matched_gt = set()
        true_positives = 0

        for pred_clip in predicted_clips:
            for gt_idx, gt_clip in enumerate(ground_truth_clips):
                if gt_idx in matched_gt:
                    continue

                iou = EvaluationMetrics.calculate_iou(pred_clip, gt_clip)
                if iou >= iou_threshold:
                    matched_gt.add(gt_idx)
                    true_positives += 1
                    break

        # Calculate metrics
        precision = true_positives / len(predicted_clips)
        recall = true_positives / len(ground_truth_clips)
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return precision, recall, f1_score

    @staticmethod
    def calculate_coverage(predicted_clips: List[Dict], total_duration: float) -> float:
        """
        Calculate temporal coverage of predicted clips.

        Args:
            predicted_clips: List of predicted clips
            total_duration: Total video duration in seconds

        Returns:
            Coverage ratio (0-1)
        """
        if not predicted_clips or total_duration <= 0:
            return 0.0

        # Merge overlapping clips
        sorted_clips = sorted(predicted_clips, key=lambda x: x['start_time'])
        merged_duration = 0.0
        current_start = sorted_clips[0]['start_time']
        current_end = sorted_clips[0]['end_time']

        for clip in sorted_clips[1:]:
            if clip['start_time'] <= current_end:
                # Overlapping, extend current interval
                current_end = max(current_end, clip['end_time'])
            else:
                # Non-overlapping, add current interval and start new one
                merged_duration += (current_end - current_start)
                current_start = clip['start_time']
                current_end = clip['end_time']

        # Add last interval
        merged_duration += (current_end - current_start)

        return merged_duration / total_duration

    @staticmethod
    def calculate_all_metrics(predicted_clips: List[Dict],
                            ground_truth_clips: List[Dict] = None,
                            total_duration: float = None) -> Dict[str, float]:
        """
        Calculate all evaluation metrics.

        Args:
            predicted_clips: List of predicted clips with scores
            ground_truth_clips: Optional list of ground truth clips
            total_duration: Optional total video duration

        Returns:
            Dictionary of all metrics
        """
        metrics = {}

        # Always calculate coverage if duration provided
        if total_duration:
            metrics['coverage'] = EvaluationMetrics.calculate_coverage(
                predicted_clips, total_duration
            )

        # Calculate metrics requiring ground truth
        if ground_truth_clips:
            metrics['mAP'] = EvaluationMetrics.calculate_map(
                predicted_clips, ground_truth_clips
            )
            metrics['HIT@1'] = EvaluationMetrics.calculate_hit_at_k(
                predicted_clips, ground_truth_clips, k=1
            )
            metrics['HIT@5'] = EvaluationMetrics.calculate_hit_at_k(
                predicted_clips, ground_truth_clips, k=5
            )

            precision, recall, f1 = EvaluationMetrics.calculate_precision_recall_f1(
                predicted_clips, ground_truth_clips
            )
            metrics['precision'] = precision
            metrics['recall'] = recall
            metrics['f1_score'] = f1

        return metrics

    @staticmethod
    def print_metrics(metrics: Dict[str, float]):
        """Pretty print metrics."""
        print("\n" + "="*50)
        print("EVALUATION METRICS")
        print("="*50)

        for metric_name, value in sorted(metrics.items()):
            print(f"{metric_name:.<30} {value:.4f}")

        print("="*50 + "\n")
