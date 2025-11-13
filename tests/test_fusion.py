"""Tests for multimodal fusion."""

import pytest
import numpy as np
from src.fusion.multimodal_fusion import MultimodalFusion
from src.fusion.title_generator import TitleGenerator


@pytest.fixture
def fusion_agent(sample_config):
    """Create fusion agent with test config."""
    config = sample_config['fusion'].copy()
    config['min_clip_duration'] = sample_config['general']['min_clip_duration']
    config['max_clip_duration'] = sample_config['general']['max_clip_duration']
    config['num_clips'] = sample_config['general']['num_clips']
    config['overlap_threshold'] = sample_config['general']['overlap_threshold']
    return MultimodalFusion(config)


@pytest.fixture
def title_generator(sample_config):
    """Create title generator with test config."""
    return TitleGenerator(sample_config['fusion']['title_generation'])


def test_fusion_initialization(fusion_agent):
    """Test fusion agent initialization."""
    assert fusion_agent is not None
    assert fusion_agent.strategy == 'weighted'
    assert fusion_agent.weights['audio'] == 0.35
    assert fusion_agent.weights['text'] == 0.40
    assert fusion_agent.weights['visual'] == 0.25


def test_fusion_normalize(fusion_agent):
    """Test array normalization."""
    arr = np.array([1, 2, 3, 4, 5])
    normalized = fusion_agent._normalize(arr)
    assert normalized.min() >= 0
    assert normalized.max() <= 1.0
    assert np.allclose(normalized.max(), 1.0)
    assert np.allclose(normalized.min(), 0.0)


def test_fusion_interpolate_scores(fusion_agent):
    """Test score interpolation."""
    scores = [
        {'time_start': 0, 'time_end': 5, 'emotion_score': 0.8},
        {'time_start': 5, 'time_end': 10, 'emotion_score': 0.6},
    ]
    time_grid = np.arange(0, 11, 1.0)

    timeline = fusion_agent._interpolate_scores(scores, time_grid, 'emotion_score')

    assert isinstance(timeline, np.ndarray)
    assert len(timeline) == len(time_grid)
    assert np.all(timeline >= 0)
    assert np.all(timeline <= 1.0)


def test_fusion_weighted_fusion(fusion_agent):
    """Test weighted fusion strategy."""
    audio = np.array([0.8, 0.7, 0.6, 0.5])
    text = np.array([0.7, 0.8, 0.7, 0.6])
    visual = np.array([0.6, 0.7, 0.8, 0.7])

    fused = fusion_agent._weighted_fusion(audio, text, visual)

    assert isinstance(fused, np.ndarray)
    assert len(fused) == len(audio)
    assert np.all(fused >= 0)
    assert np.all(fused <= 1.0)


def test_fusion_calculate_overlap(fusion_agent):
    """Test overlap calculation."""
    clip1 = {'start_time': 0, 'end_time': 10}
    clip2 = {'start_time': 5, 'end_time': 15}

    overlap = fusion_agent._calculate_overlap(clip1, clip2)

    assert isinstance(overlap, float)
    assert 0 <= overlap <= 1.0
    # 5 seconds overlap out of 10 seconds min duration = 0.5
    assert np.isclose(overlap, 0.5)


def test_fusion_remove_overlaps(fusion_agent):
    """Test removing overlapping candidates."""
    candidates = [
        {'start_time': 0, 'end_time': 10, 'score': 0.9, 'duration': 10},
        {'start_time': 5, 'end_time': 15, 'score': 0.7, 'duration': 10},  # Overlaps with first
        {'start_time': 20, 'end_time': 30, 'score': 0.8, 'duration': 10},  # No overlap
    ]

    filtered = fusion_agent._remove_overlaps(candidates)

    assert isinstance(filtered, list)
    assert len(filtered) <= len(candidates)
    # Should keep highest scored clips
    assert any(c['score'] == 0.9 for c in filtered)


def test_fusion_fuse_signals(fusion_agent):
    """Test full signal fusion."""
    audio_scores = [
        {'time_start': 0, 'time_end': 10, 'emotion_score': 0.8},
        {'time_start': 10, 'time_end': 20, 'emotion_score': 0.6},
    ]
    text_scores = [
        {'start': 0, 'end': 10, 'topic_score': 0.7, 'text': "Important topic here"},
        {'start': 10, 'end': 20, 'topic_score': 0.9, 'text': "Another key point"},
    ]
    visual_scores = [
        {'time_start': 0, 'time_end': 10, 'engagement_score': 0.6},
        {'time_start': 10, 'time_end': 20, 'engagement_score': 0.8},
    ]

    candidates = fusion_agent.fuse_signals(audio_scores, text_scores, visual_scores, duration=30.0)

    assert isinstance(candidates, list)
    for candidate in candidates:
        assert 'start_time' in candidate
        assert 'end_time' in candidate
        assert 'score' in candidate
        assert 'audio_score' in candidate
        assert 'text_score' in candidate
        assert 'visual_score' in candidate
        assert 0 <= candidate['score'] <= 1.0


def test_title_generator_initialization(title_generator):
    """Test title generator initialization."""
    assert title_generator is not None
    assert title_generator.max_length == 60
    assert title_generator.style == 'engaging'


def test_title_generator_extract_keywords(title_generator):
    """Test keyword extraction."""
    text = "Machine learning and artificial intelligence are transforming the world"
    keywords = title_generator._extract_keywords(text)

    assert isinstance(keywords, list)
    assert len(keywords) > 0
    # Should extract meaningful words
    assert any(kw in ['machine', 'learning', 'artificial', 'intelligence'] for kw in keywords)


def test_title_generator_generate_title(title_generator):
    """Test title generation."""
    clip = {
        'text_context': "Machine learning is revolutionizing artificial intelligence and deep learning models",
        'audio_score': 0.8,
        'text_score': 0.9,
        'visual_score': 0.7,
        'score': 0.85
    }

    title = title_generator.generate_title(clip)

    assert isinstance(title, str)
    assert len(title) > 0
    assert len(title) <= title_generator.max_length + 10  # Some tolerance for emoji


def test_title_generator_truncate_title(title_generator):
    """Test title truncation."""
    long_title = "This is a very long title that definitely exceeds the maximum length and needs to be truncated"
    truncated = title_generator._truncate_title(long_title)

    assert len(truncated) <= title_generator.max_length
    # Should truncate at word boundary
    assert not truncated.endswith(' ')


def test_title_generator_add_emoji(title_generator):
    """Test emoji addition."""
    title = "The Secret to Machine Learning"
    characteristics = {
        'high_emotion': True,
        'high_topic': True,
        'high_visual': False,
        'dominant_modality': 'text'
    }

    title_with_emoji = title_generator._add_emoji(title, characteristics)

    assert len(title_with_emoji) > len(title)  # Should have emoji added
    # Check that emoji is at the end
    assert title in title_with_emoji


def test_title_generator_styles():
    """Test different title styles."""
    config = {'max_length': 60, 'include_emoji': False}

    # Professional style
    config_prof = config.copy()
    config_prof['style'] = 'professional'
    gen_prof = TitleGenerator(config_prof)
    assert gen_prof.style == 'professional'

    # Casual style
    config_casual = config.copy()
    config_casual['style'] = 'casual'
    gen_casual = TitleGenerator(config_casual)
    assert gen_casual.style == 'casual'
