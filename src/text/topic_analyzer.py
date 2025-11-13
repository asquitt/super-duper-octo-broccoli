"""Text topic and keyword analysis using NLP."""

import re
from typing import List, Dict, Tuple
import numpy as np
from collections import Counter
import warnings

warnings.filterwarnings('ignore')

try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    from sklearn.metrics.pairwise import cosine_similarity
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers not available. Using fallback method.")


class TopicAnalyzer:
    """Analyze text for topic changes and keyword density."""

    def __init__(self, config: dict):
        """Initialize topic analyzer with configuration."""
        self.config = config
        self.window_size = config.get('topic', {}).get('window_size', 10)

        # Initialize model if available
        self.model = None
        self.tokenizer = None

        if TRANSFORMERS_AVAILABLE:
            try:
                model_name = config.get('model', 'distilbert-base-uncased')
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModel.from_pretrained(model_name)
                self.model.eval()
            except Exception as e:
                print(f"Warning: Could not load transformer model: {e}")
                print("Falling back to simple keyword-based analysis")

        # Common filler words to ignore
        self.stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what',
            'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
            'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
            'about', 'after', 'before', 'between', 'during', 'into', 'through',
            'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
            'up', 'down', 'out', 'off', 'above', 'below', 'any', 'because', 'if',
            'while', 'their', 'them', 'your', 'our', 'his', 'her', 'its', 'my',
            'me', 'him', 'us', 'yeah', 'oh', 'um', 'uh', 'like', 'know', 'think',
            'mean', 'really', 'actually', 'basically', 'literally', 'okay', 'right'
        ])

    def analyze(self, transcript: str, timestamps: List[Dict] = None) -> List[Dict]:
        """
        Analyze transcript for topic changes and keyword density.

        Args:
            transcript: Full transcript text
            timestamps: Optional list of {'text': str, 'start': float, 'end': float}

        Returns:
            List of time-stamped topic scores
        """
        # Parse transcript into sentences with timestamps
        sentences = self._parse_transcript(transcript, timestamps)

        if not sentences:
            return []

        # Calculate embeddings or features for each sentence
        if self.model is not None:
            embeddings = self._get_embeddings(sentences)
            topic_scores = self._calculate_topic_scores_transformer(
                sentences, embeddings
            )
        else:
            topic_scores = self._calculate_topic_scores_simple(sentences)

        # Detect questions and answers
        qa_scores = self._detect_qa_patterns(sentences)

        # Combine scores
        combined_scores = self._combine_scores(topic_scores, qa_scores)

        return combined_scores

    def _parse_transcript(self, transcript: str,
                         timestamps: List[Dict] = None) -> List[Dict]:
        """Parse transcript into sentences with timestamps."""
        # Split into sentences
        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if s.strip()]

        if timestamps:
            # Match sentences to timestamps
            return self._align_sentences_to_timestamps(sentences, timestamps)
        else:
            # Estimate timestamps based on word count
            return self._estimate_timestamps(sentences)

    def _align_sentences_to_timestamps(self, sentences: List[str],
                                      timestamps: List[Dict]) -> List[Dict]:
        """Align sentences to provided timestamps."""
        result = []
        current_time = 0.0

        for i, sentence in enumerate(sentences):
            # Find corresponding timestamp
            if i < len(timestamps):
                ts = timestamps[i]
                result.append({
                    'text': sentence,
                    'start': ts.get('start', current_time),
                    'end': ts.get('end', current_time + 5.0)
                })
                current_time = ts.get('end', current_time + 5.0)
            else:
                # Estimate if no more timestamps
                duration = len(sentence.split()) * 0.4  # ~0.4s per word
                result.append({
                    'text': sentence,
                    'start': current_time,
                    'end': current_time + duration
                })
                current_time += duration

        return result

    def _estimate_timestamps(self, sentences: List[str]) -> List[Dict]:
        """Estimate timestamps based on word count."""
        result = []
        current_time = 0.0

        for sentence in sentences:
            words = sentence.split()
            duration = len(words) * 0.4  # Assume ~0.4 seconds per word
            result.append({
                'text': sentence,
                'start': current_time,
                'end': current_time + duration
            })
            current_time += duration

        return result

    def _get_embeddings(self, sentences: List[Dict]) -> np.ndarray:
        """Get sentence embeddings using transformer model."""
        texts = [s['text'] for s in sentences]

        embeddings = []
        batch_size = 8

        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                inputs = self.tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=128,
                    return_tensors='pt'
                )

                outputs = self.model(**inputs)
                # Use [CLS] token embedding
                batch_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
                embeddings.append(batch_embeddings)

        return np.vstack(embeddings)

    def _calculate_topic_scores_transformer(self, sentences: List[Dict],
                                           embeddings: np.ndarray) -> List[Dict]:
        """Calculate topic scores using transformer embeddings."""
        scores = []

        for i in range(len(sentences)):
            # Define window around current sentence
            start_idx = max(0, i - self.window_size // 2)
            end_idx = min(len(sentences), i + self.window_size // 2 + 1)

            window_sentences = sentences[start_idx:end_idx]
            window_embeddings = embeddings[start_idx:end_idx]

            # Calculate topic change score
            if i > 0:
                similarity = cosine_similarity(
                    embeddings[i:i+1],
                    embeddings[i-1:i]
                )[0][0]
                topic_change_score = 1.0 - similarity
            else:
                topic_change_score = 0.0

            # Calculate keyword density in window
            keyword_score = self._calculate_keyword_density(window_sentences)

            # Calculate semantic density (variance in embeddings)
            semantic_density = np.var(
                cosine_similarity(window_embeddings)
            )

            scores.append({
                'sentence_idx': i,
                'start': sentences[i]['start'],
                'end': sentences[i]['end'],
                'topic_change': topic_change_score,
                'keyword_density': keyword_score,
                'semantic_density': min(1.0, semantic_density * 10),
                'text': sentences[i]['text']
            })

        return scores

    def _calculate_topic_scores_simple(self, sentences: List[Dict]) -> List[Dict]:
        """Calculate topic scores using simple keyword-based method."""
        scores = []

        for i in range(len(sentences)):
            # Define window
            start_idx = max(0, i - self.window_size // 2)
            end_idx = min(len(sentences), i + self.window_size // 2 + 1)

            window_sentences = sentences[start_idx:end_idx]

            # Calculate keyword density
            keyword_score = self._calculate_keyword_density(window_sentences)

            # Calculate word overlap (topic continuity)
            if i > 0:
                overlap = self._calculate_word_overlap(
                    sentences[i-1]['text'],
                    sentences[i]['text']
                )
                topic_change_score = 1.0 - overlap
            else:
                topic_change_score = 0.0

            scores.append({
                'sentence_idx': i,
                'start': sentences[i]['start'],
                'end': sentences[i]['end'],
                'topic_change': topic_change_score,
                'keyword_density': keyword_score,
                'semantic_density': keyword_score,  # Fallback
                'text': sentences[i]['text']
            })

        return scores

    def _calculate_keyword_density(self, sentences: List[Dict]) -> float:
        """Calculate keyword density in a window of sentences."""
        # Combine all text
        text = ' '.join(s['text'].lower() for s in sentences)

        # Extract words
        words = re.findall(r'\b[a-z]+\b', text)

        # Filter stop words
        keywords = [w for w in words if w not in self.stop_words and len(w) > 3]

        if not words:
            return 0.0

        # Calculate density
        density = len(keywords) / len(words)

        # Boost if there are repeated keywords (emphasis)
        if keywords:
            keyword_counts = Counter(keywords)
            repetition_boost = sum(1 for count in keyword_counts.values() if count > 1)
            repetition_boost = min(0.3, repetition_boost * 0.1)
            density += repetition_boost

        return min(1.0, density)

    def _calculate_word_overlap(self, text1: str, text2: str) -> float:
        """Calculate word overlap between two texts."""
        words1 = set(re.findall(r'\b[a-z]+\b', text1.lower()))
        words2 = set(re.findall(r'\b[a-z]+\b', text2.lower()))

        words1 = words1 - self.stop_words
        words2 = words2 - self.stop_words

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def _detect_qa_patterns(self, sentences: List[Dict]) -> List[Dict]:
        """Detect question-answer patterns."""
        qa_scores = []

        for i, sentence in enumerate(sentences):
            text = sentence['text']

            # Check if sentence is a question
            is_question = self._is_question(text)

            # Check if followed by an answer
            has_answer = False
            if is_question and i + 1 < len(sentences):
                # Simple heuristic: next sentence is longer
                next_text = sentences[i + 1]['text']
                if len(next_text.split()) > len(text.split()):
                    has_answer = True

            qa_score = 0.0
            if is_question:
                qa_score = 0.7 if has_answer else 0.4

            qa_scores.append({
                'sentence_idx': i,
                'start': sentence['start'],
                'end': sentence['end'],
                'qa_score': qa_score,
                'is_question': is_question
            })

        return qa_scores

    def _is_question(self, text: str) -> bool:
        """Check if text is a question."""
        text = text.strip()

        # Ends with question mark
        if text.endswith('?'):
            return True

        # Starts with question word
        question_words = ['what', 'where', 'when', 'why', 'who', 'whom', 'whose',
                         'which', 'how', 'can', 'could', 'would', 'should', 'do',
                         'does', 'did', 'is', 'are', 'was', 'were']

        first_word = text.lower().split()[0] if text.split() else ''
        return first_word in question_words

    def _combine_scores(self, topic_scores: List[Dict],
                       qa_scores: List[Dict]) -> List[Dict]:
        """Combine topic and QA scores."""
        combined = []

        for i in range(len(topic_scores)):
            topic = topic_scores[i]
            qa = qa_scores[i] if i < len(qa_scores) else {'qa_score': 0.0}

            # Weighted combination
            overall_score = (
                topic['topic_change'] * 0.3 +
                topic['keyword_density'] * 0.4 +
                topic['semantic_density'] * 0.2 +
                qa['qa_score'] * 0.1
            )

            combined.append({
                'start': topic['start'],
                'end': topic['end'],
                'topic_score': overall_score,
                'topic_change': topic['topic_change'],
                'keyword_density': topic['keyword_density'],
                'qa_score': qa['qa_score'],
                'text': topic['text']
            })

        return combined

    def get_peak_topic_segments(self, topic_scores: List[Dict],
                               threshold: float = 0.7,
                               min_duration: float = 5.0) -> List[Dict]:
        """Find segments with high topic importance."""
        peaks = []

        # Group consecutive high-scoring sentences
        current_segment = None

        for score_data in topic_scores:
            if score_data['topic_score'] >= threshold:
                if current_segment is None:
                    current_segment = {
                        'start_time': score_data['start'],
                        'end_time': score_data['end'],
                        'score': score_data['topic_score'],
                        'texts': [score_data['text']]
                    }
                else:
                    # Extend current segment
                    current_segment['end_time'] = score_data['end']
                    current_segment['score'] = max(
                        current_segment['score'],
                        score_data['topic_score']
                    )
                    current_segment['texts'].append(score_data['text'])
            else:
                if current_segment is not None:
                    duration = current_segment['end_time'] - current_segment['start_time']
                    if duration >= min_duration:
                        peaks.append(current_segment)
                    current_segment = None

        # Add last segment
        if current_segment is not None:
            duration = current_segment['end_time'] - current_segment['start_time']
            if duration >= min_duration:
                peaks.append(current_segment)

        return peaks
