"""Main orchestrator for multimodal clip extraction."""

import os
import time
from pathlib import Path
from typing import Optional, Dict, List
import json

from src.utils.config_loader import ConfigLoader
from src.utils.video_processor import VideoProcessor
from src.audio.emotion_detector import EmotionDetector
from src.text.topic_analyzer import TopicAnalyzer
from src.text.transcriber import Transcriber
from src.visual.engagement_detector import EngagementDetector
from src.fusion.multimodal_fusion import MultimodalFusion
from src.fusion.title_generator import TitleGenerator


class ClipExtractor:
    """Main orchestrator for extracting engaging clips from videos."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the clip extractor."""
        # Load configuration
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.get_all()

        # Validate configuration
        self.config_loader.validate()

        # Initialize components
        self.video_processor = VideoProcessor()

        # Initialize analyzers based on config
        self.audio_analyzer = None
        self.text_analyzer = None
        self.visual_analyzer = None

        if self.config['audio']['enabled']:
            self.audio_analyzer = EmotionDetector(self.config['audio'])

        if self.config['text']['enabled']:
            self.text_analyzer = TopicAnalyzer(self.config['text'])
            self.transcriber = Transcriber(self.config['text'])

        if self.config['visual']['enabled']:
            self.visual_analyzer = EngagementDetector(self.config['visual'])

        # Initialize fusion agent
        self.fusion_agent = MultimodalFusion(self.config['fusion'])
        self.title_generator = TitleGenerator(
            self.config['fusion'].get('title_generation', {})
        )

        # Setup temp and cache directories
        self.temp_dir = Path(self.config['processing'].get('temp_dir', './temp'))
        self.cache_dir = Path(self.config['processing'].get('cache_dir', './cache'))
        self.temp_dir.mkdir(exist_ok=True, parents=True)
        self.cache_dir.mkdir(exist_ok=True, parents=True)

    def extract_clips(self, input_path: str,
                     transcript_path: Optional[str] = None,
                     output_path: Optional[str] = None) -> List[Dict]:
        """
        Extract engaging clips from video/audio file.

        Args:
            input_path: Path to video or audio file
            transcript_path: Optional path to transcript file
            output_path: Optional path to save results JSON

        Returns:
            List of extracted clips with metadata
        """
        print(f"\n{'='*60}")
        print(f"Multimodal Clip Extractor")
        print(f"{'='*60}\n")

        start_time = time.time()

        # Step 1: Validate input
        print("📁 Validating input file...")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        input_path = os.path.abspath(input_path)
        print(f"   Input: {input_path}")

        # Step 2: Get video duration and properties
        duration = self.video_processor.get_duration(input_path)
        has_video = self.video_processor.has_video_stream(input_path)

        print(f"   Duration: {duration:.1f}s ({duration/60:.1f} minutes)")
        print(f"   Has video: {'Yes' if has_video else 'No'}")

        # Step 3: Extract audio if needed
        audio_path = input_path
        if has_video and (self.audio_analyzer or self.text_analyzer):
            print("\n🎵 Extracting audio...")
            audio_path = str(self.temp_dir / f"audio_{Path(input_path).stem}.wav")
            self.video_processor.extract_audio(input_path, audio_path)
            print(f"   Saved to: {audio_path}")

        # Step 4: Analyze modalities
        audio_scores = []
        text_scores = []
        visual_scores = []
        transcript_data = None

        # Audio analysis
        if self.audio_analyzer:
            print("\n🎤 Analyzing audio emotion...")
            audio_scores = self.audio_analyzer.analyze(audio_path)
            print(f"   Extracted {len(audio_scores)} emotion segments")
            avg_emotion = sum(s['emotion_score'] for s in audio_scores) / len(audio_scores) if audio_scores else 0
            print(f"   Average emotion score: {avg_emotion:.2f}")

        # Text analysis
        if self.text_analyzer:
            print("\n📝 Analyzing text/topics...")

            # Get transcript
            if transcript_path:
                print(f"   Loading transcript from: {transcript_path}")
                transcript_data = self.transcriber.load_transcript_from_file(transcript_path)
            else:
                print("   Generating transcript (this may take a while)...")
                transcript_data = self.transcriber.transcribe(audio_path)

            if transcript_data and transcript_data.get('text'):
                print(f"   Transcript length: {len(transcript_data['text'])} characters")

                # Analyze topics
                text_scores = self.text_analyzer.analyze(
                    transcript_data['text'],
                    transcript_data.get('segments', [])
                )
                print(f"   Extracted {len(text_scores)} topic segments")
                avg_topic = sum(s['topic_score'] for s in text_scores) / len(text_scores) if text_scores else 0
                print(f"   Average topic score: {avg_topic:.2f}")
            else:
                print("   ⚠️  No transcript available, skipping text analysis")

        # Visual analysis
        if self.visual_analyzer and has_video:
            print("\n🎬 Analyzing visual engagement...")
            visual_scores = self.visual_analyzer.analyze(input_path)
            print(f"   Extracted {len(visual_scores)} engagement segments")
            avg_visual = sum(s['engagement_score'] for s in visual_scores) / len(visual_scores) if visual_scores else 0
            print(f"   Average engagement score: {avg_visual:.2f}")

        # Step 5: Fuse modalities
        print("\n🔮 Fusing multimodal signals...")
        candidates = self.fusion_agent.fuse_signals(
            audio_scores,
            text_scores,
            visual_scores,
            duration
        )
        print(f"   Found {len(candidates)} candidate clips")

        # Step 6: Select top clips
        num_clips = self.config['general']['num_clips']
        top_clips = candidates[:num_clips]

        print(f"   Selected top {len(top_clips)} clips")

        # Step 7: Generate titles
        print("\n✨ Generating titles...")
        results = []

        for i, clip in enumerate(top_clips, 1):
            title = self.title_generator.generate_title(clip)

            result = {
                'start_time': self._format_time(clip['start_time']),
                'end_time': self._format_time(clip['end_time']),
                'title': title,
                'score': round(clip['score'], 2),
                'audio_score': round(clip.get('audio_score', 0), 2),
                'text_score': round(clip.get('text_score', 0), 2),
                'visual_score': round(clip.get('visual_score', 0), 2),
                'duration': round(clip['duration'], 1)
            }

            results.append(result)

            print(f"   {i}. [{result['start_time']} - {result['end_time']}] {title}")
            print(f"      Score: {result['score']} (A:{result['audio_score']} T:{result['text_score']} V:{result['visual_score']})")

        # Step 8: Save results
        if output_path:
            print(f"\n💾 Saving results to: {output_path}")
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)

        # Cleanup
        if self.config['processing'].get('cleanup_temp', True):
            self._cleanup_temp_files()

        elapsed_time = time.time() - start_time
        print(f"\n✅ Processing complete in {elapsed_time:.1f}s ({elapsed_time/60:.1f} minutes)")
        print(f"{'='*60}\n")

        return results

    def _format_time(self, seconds: float) -> str:
        """Format seconds as MM:SS."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def _cleanup_temp_files(self):
        """Clean up temporary files."""
        try:
            for file in self.temp_dir.glob('*'):
                if file.is_file():
                    file.unlink()
        except Exception as e:
            print(f"Warning: Could not clean up temp files: {e}")

    def export_clips(self, input_path: str, clips: List[Dict],
                    output_dir: str):
        """
        Export extracted clips as separate video files.

        Args:
            input_path: Original video file path
            clips: List of clips from extract_clips()
            output_dir: Directory to save clip files
        """
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n🎬 Exporting clips to: {output_dir}")

        for i, clip in enumerate(clips, 1):
            # Parse time strings
            start = self.video_processor.time_to_seconds(clip['start_time'])
            end = self.video_processor.time_to_seconds(clip['end_time'])

            # Generate filename
            filename = f"clip_{i:02d}_{clip['start_time'].replace(':', '-')}.mp4"
            output_path = os.path.join(output_dir, filename)

            print(f"   Exporting clip {i}/{len(clips)}: {filename}")

            try:
                self.video_processor.extract_clip(
                    input_path,
                    start,
                    end,
                    output_path
                )
                print(f"   ✓ Saved: {output_path}")
            except Exception as e:
                print(f"   ✗ Error: {e}")

        print(f"\n✅ Exported {len(clips)} clips")
