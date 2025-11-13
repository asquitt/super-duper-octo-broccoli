"""Tests for evaluation metrics."""

import pytest
import numpy as np
from src.utils.metrics import EvaluationMetrics


def test_calculate_iou_no_overlap():
    """Test IoU with no overlap."""
    clip1 = {'start_time': 0, 'end_time': 10}
    clip2 = {'start_time': 20, 'end_time': 30}
    iou = EvaluationMetrics.calculate_iou(clip1, clip2)
    assert iou == 0.0


def test_calculate_iou_perfect_overlap():
    """Test IoU with perfect overlap."""
    clip1 = {'start_time': 0, 'end_time': 10}
    clip2 = {'start_time': 0, 'end_time': 10}
    iou = EvaluationMetrics.calculate_iou(clip1, clip2)
    assert iou == 1.0


def test_calculate_iou_partial_overlap():
    """Test IoU with partial overlap."""
    clip1 = {'start_time': 0, 'end_time': 10}
    clip2 = {'start_time': 5, 'end_time': 15}
    iou = EvaluationMetrics.calculate_iou(clip1, clip2)
    # Intersection: 5 seconds (5-10)
    # Union: 15 seconds (0-15)
    expected_iou = 5.0 / 15.0
    assert abs(iou - expected_iou) < 0.01


def test_calculate_map_perfect_predictions():
    """Test mAP with perfect predictions."""
    predicted = [
        {'start_time': 0, 'end_time': 10, 'score': 0.9},
        {'start_time': 20, 'end_time': 30, 'score': 0.8}
    ]
    ground_truth = [
        {'start_time': 0, 'end_time': 10},
        {'start_time': 20, 'end_time': 30}
    ]
    map_score = EvaluationMetrics.calculate_map(predicted, ground_truth)
    assert map_score == 1.0


def test_calculate_map_no_matches():
    """Test mAP with no matches."""
    predicted = [
        {'start_time': 0, 'end_time': 10, 'score': 0.9}
    ]
    ground_truth = [
        {'start_time': 50, 'end_time': 60}
    ]
    map_score = EvaluationMetrics.calculate_map(predicted, ground_truth)
    assert map_score == 0.0


def test_hit_at_k():
    """Test HIT@K metric."""
    predicted = [
        {'start_time': 0, 'end_time': 10, 'score': 0.9},
        {'start_time': 50, 'end_time': 60, 'score': 0.7}
    ]
    ground_truth = [
        {'start_time': 0, 'end_time': 10}
    ]

    # Should hit at k=1
    hit1 = EvaluationMetrics.calculate_hit_at_k(predicted, ground_truth, k=1)
    assert hit1 == 1.0

    # Should not hit if ground truth is different
    ground_truth2 = [
        {'start_time': 100, 'end_time': 110}
    ]
    hit2 = EvaluationMetrics.calculate_hit_at_k(predicted, ground_truth2, k=1)
    assert hit2 == 0.0


def test_precision_recall_f1():
    """Test precision, recall, and F1 score."""
    predicted = [
        {'start_time': 0, 'end_time': 10},
        {'start_time': 20, 'end_time': 30},
        {'start_time': 50, 'end_time': 60}
    ]
    ground_truth = [
        {'start_time': 0, 'end_time': 10},
        {'start_time': 20, 'end_time': 30}
    ]

    precision, recall, f1 = EvaluationMetrics.calculate_precision_recall_f1(
        predicted, ground_truth
    )

    # 2 true positives, 3 predictions, 2 ground truths
    expected_precision = 2.0 / 3.0
    expected_recall = 2.0 / 2.0
    expected_f1 = 2 * (expected_precision * expected_recall) / (expected_precision + expected_recall)

    assert abs(precision - expected_precision) < 0.01
    assert abs(recall - expected_recall) < 0.01
    assert abs(f1 - expected_f1) < 0.01


def test_coverage():
    """Test temporal coverage calculation."""
    predicted = [
        {'start_time': 0, 'end_time': 10},
        {'start_time': 20, 'end_time': 30}
    ]
    total_duration = 100.0

    coverage = EvaluationMetrics.calculate_coverage(predicted, total_duration)

    # Total coverage: 20 seconds out of 100
    expected_coverage = 20.0 / 100.0
    assert abs(coverage - expected_coverage) < 0.01


def test_coverage_with_overlap():
    """Test coverage with overlapping clips."""
    predicted = [
        {'start_time': 0, 'end_time': 15},
        {'start_time': 10, 'end_time': 20}
    ]
    total_duration = 100.0

    coverage = EvaluationMetrics.calculate_coverage(predicted, total_duration)

    # Merged coverage: 0-20 = 20 seconds out of 100
    expected_coverage = 20.0 / 100.0
    assert abs(coverage - expected_coverage) < 0.01


def test_calculate_all_metrics():
    """Test calculating all metrics together."""
    predicted = [
        {'start_time': 0, 'end_time': 10, 'score': 0.9},
        {'start_time': 20, 'end_time': 30, 'score': 0.8}
    ]
    ground_truth = [
        {'start_time': 0, 'end_time': 10},
        {'start_time': 20, 'end_time': 30}
    ]
    total_duration = 100.0

    metrics = EvaluationMetrics.calculate_all_metrics(
        predicted, ground_truth, total_duration
    )

    assert 'mAP' in metrics
    assert 'HIT@1' in metrics
    assert 'HIT@5' in metrics
    assert 'precision' in metrics
    assert 'recall' in metrics
    assert 'f1_score' in metrics
    assert 'coverage' in metrics

    # Perfect match
    assert metrics['mAP'] == 1.0
    assert metrics['HIT@1'] == 1.0
    assert metrics['precision'] == 1.0
    assert metrics['recall'] == 1.0
