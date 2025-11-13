"""Audio transcription using Whisper or other speech-to-text models."""

from typing import List, Dict, Optional
import warnings

warnings.filterwarnings('ignore')

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("Warning: whisper not available")


class Transcriber:
    """Transcribe audio to text with timestamps."""

    def __init__(self, config: dict):
        """Initialize transcriber with configuration."""
        self.config = config
        self.model_name = config.get('transcription', {}).get('model', 'base')
        self.language = config.get('transcription', {}).get('language', 'en')
        self.model = None

        if WHISPER_AVAILABLE:
            try:
                # Load Whisper model (lazy loading)
                print(f"Loading Whisper model: {self.model_name}")
                self.model = whisper.load_model(self.model_name)
                print("Whisper model loaded successfully")
            except Exception as e:
                print(f"Warning: Could not load Whisper model: {e}")

    def transcribe(self, audio_path: str) -> Dict:
        """
        Transcribe audio file to text with timestamps.

        Args:
            audio_path: Path to audio file

        Returns:
            Dictionary with 'text' and 'segments' (timestamped chunks)
        """
        if not WHISPER_AVAILABLE or self.model is None:
            return self._fallback_transcription(audio_path)

        try:
            result = self.model.transcribe(
                audio_path,
                language=self.language,
                task='transcribe',
                verbose=False
            )

            # Format segments
            segments = []
            for segment in result.get('segments', []):
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip()
                })

            return {
                'text': result.get('text', ''),
                'segments': segments,
                'language': result.get('language', self.language)
            }

        except Exception as e:
            print(f"Transcription error: {e}")
            return self._fallback_transcription(audio_path)

    def _fallback_transcription(self, audio_path: str) -> Dict:
        """Fallback when Whisper is not available."""
        return {
            'text': '',
            'segments': [],
            'language': self.language,
            'error': 'Transcription not available. Please provide a transcript file.'
        }

    def load_transcript_from_file(self, transcript_path: str) -> Dict:
        """
        Load transcript from a text file.

        Supports formats:
        - Plain text
        - SRT format
        - VTT format
        """
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Detect format
        if '-->' in content:
            # SRT or VTT format
            return self._parse_srt_vtt(content)
        else:
            # Plain text
            return {
                'text': content,
                'segments': [],
                'language': self.language
            }

    def _parse_srt_vtt(self, content: str) -> Dict:
        """Parse SRT or VTT subtitle format."""
        import re

        segments = []
        full_text = []

        # Remove VTT header if present
        if content.startswith('WEBVTT'):
            content = re.sub(r'^WEBVTT.*?\n\n', '', content, flags=re.DOTALL)

        # Split into blocks
        blocks = re.split(r'\n\n+', content.strip())

        for block in blocks:
            lines = block.strip().split('\n')

            if len(lines) < 2:
                continue

            # Find timestamp line
            timestamp_line = None
            text_lines = []

            for line in lines:
                if '-->' in line:
                    timestamp_line = line
                elif not line.isdigit():  # Skip sequence numbers
                    text_lines.append(line)

            if timestamp_line and text_lines:
                # Parse timestamps
                times = re.findall(r'(\d{1,2}):(\d{2}):(\d{2})[.,](\d{3})', timestamp_line)

                if len(times) >= 2:
                    # Start time
                    h1, m1, s1, ms1 = map(int, times[0])
                    start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000.0

                    # End time
                    h2, m2, s2, ms2 = map(int, times[1])
                    end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000.0

                    text = ' '.join(text_lines)
                    full_text.append(text)

                    segments.append({
                        'start': start,
                        'end': end,
                        'text': text
                    })

        return {
            'text': ' '.join(full_text),
            'segments': segments,
            'language': self.language
        }
