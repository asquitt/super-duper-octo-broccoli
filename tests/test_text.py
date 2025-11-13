"""Tests for text topic analysis."""

import pytest
from src.text.topic_analyzer import TopicAnalyzer
from src.text.transcriber import Transcriber


@pytest.fixture
def analyzer(sample_config):
    """Create topic analyzer with test config."""
    return TopicAnalyzer(sample_config['text'])


def test_topic_analyzer_initialization(analyzer):
    """Test analyzer initialization."""
    assert analyzer is not None
    assert analyzer.window_size == 10


def test_topic_analyzer_extract_keywords(analyzer):
    """Test keyword extraction."""
    sentences = [
        {'text': "The machine learning model works well.", 'start': 0, 'end': 5},
        {'text': "Machine learning and deep learning are important.", 'start': 5, 'end': 10}
    ]
    keywords = analyzer._extract_keywords(' '.join(s['text'] for s in sentences))
    assert isinstance(keywords, list)
    assert len(keywords) > 0
    # Should extract words like 'machine', 'learning', 'model', etc.
    assert any('machine' in kw or 'learning' in kw for kw in keywords)


def test_topic_analyzer_calculate_keyword_density(analyzer):
    """Test keyword density calculation."""
    sentences = [
        {'text': "This is a test sentence with some keywords.", 'start': 0, 'end': 5},
        {'text': "Another test with more keywords here.", 'start': 5, 'end': 10}
    ]
    density = analyzer._calculate_keyword_density(sentences)
    assert isinstance(density, float)
    assert 0 <= density <= 1.3  # Can exceed 1 with boost


def test_topic_analyzer_is_question(analyzer):
    """Test question detection."""
    assert analyzer._is_question("What is machine learning?") is True
    assert analyzer._is_question("How does this work?") is True
    assert analyzer._is_question("Can we improve this?") is True
    assert analyzer._is_question("This is a statement.") is False
    assert analyzer._is_question("Machine learning is great.") is False


def test_topic_analyzer_detect_qa_patterns(analyzer):
    """Test Q&A pattern detection."""
    sentences = [
        {'text': "What is machine learning?", 'start': 0, 'end': 3},
        {'text': "Machine learning is a subset of AI.", 'start': 3, 'end': 6},
        {'text': "This is another statement.", 'start': 6, 'end': 9}
    ]
    qa_scores = analyzer._detect_qa_patterns(sentences)
    assert isinstance(qa_scores, list)
    assert len(qa_scores) == len(sentences)
    # First sentence is a question followed by answer
    assert qa_scores[0]['is_question'] is True
    assert qa_scores[0]['qa_score'] > 0


def test_topic_analyzer_analyze(analyzer, test_transcript):
    """Test full transcript analysis."""
    scores = analyzer.analyze(test_transcript)
    assert isinstance(scores, list)
    assert len(scores) > 0

    for score in scores:
        assert 'start' in score
        assert 'end' in score
        assert 'topic_score' in score
        assert 0 <= score['topic_score'] <= 1.1  # Slightly above 1 possible with bonuses
        assert 'text' in score


def test_topic_analyzer_get_peak_segments(analyzer):
    """Test peak topic segment extraction."""
    topic_scores = [
        {'start': 0, 'end': 5, 'topic_score': 0.5, 'text': "Low score segment"},
        {'start': 5, 'end': 10, 'topic_score': 0.8, 'text': "High score segment"},
        {'start': 10, 'end': 15, 'topic_score': 0.9, 'text': "Very high score"},
        {'start': 15, 'end': 20, 'topic_score': 0.4, 'text': "Another low segment"},
    ]

    peaks = analyzer.get_peak_topic_segments(topic_scores, threshold=0.7, min_duration=4.0)

    assert isinstance(peaks, list)
    assert len(peaks) > 0
    for peak in peaks:
        assert peak['score'] >= 0.7
        assert 'start_time' in peak
        assert 'end_time' in peak
        assert peak['end_time'] - peak['start_time'] >= 4.0


def test_transcriber_load_plain_text(tmp_path):
    """Test loading plain text transcript."""
    transcriber = Transcriber({'transcription': {}})

    # Create test transcript file
    transcript_file = tmp_path / "transcript.txt"
    transcript_file.write_text("This is a test transcript. It has multiple sentences.")

    result = transcriber.load_transcript_from_file(str(transcript_file))

    assert 'text' in result
    assert len(result['text']) > 0
    assert 'test transcript' in result['text']


def test_transcriber_parse_srt(tmp_path):
    """Test parsing SRT format."""
    transcriber = Transcriber({'transcription': {}})

    # Create test SRT file
    srt_content = """1
00:00:00,000 --> 00:00:05,000
First subtitle line.

2
00:00:05,000 --> 00:00:10,000
Second subtitle line.
"""
    srt_file = tmp_path / "transcript.srt"
    srt_file.write_text(srt_content)

    result = transcriber.load_transcript_from_file(str(srt_file))

    assert 'text' in result
    assert 'segments' in result
    assert len(result['segments']) == 2
    assert result['segments'][0]['start'] == 0.0
    assert result['segments'][0]['end'] == 5.0
    assert 'First subtitle' in result['segments'][0]['text']
