#!/usr/bin/env python3
"""
Multimodal Clip Extractor - CLI Interface

Extract engaging clips from long-form video/audio content using
multimodal AI analysis (audio emotion, text topics, visual engagement).
"""

import argparse
import sys
import os
from pathlib import Path

from src.orchestrator import ClipExtractor


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Extract engaging clips from long-form video/audio',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a video file
  python main.py --input video.mp4 --output clips.json

  # Process audio with transcript
  python main.py --input audio.mp3 --transcript transcript.txt

  # Export clips as separate video files
  python main.py --input video.mp4 --output clips.json --export-clips ./output

  # Customize clip duration
  python main.py --input video.mp4 --min-duration 30 --max-duration 60 --num-clips 5

  # Use custom config
  python main.py --input video.mp4 --config my_config.yaml
        """
    )

    # Required arguments
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input video or audio file path'
    )

    # Optional arguments
    parser.add_argument(
        '--output', '-o',
        help='Output JSON file path (default: clips.json)'
    )

    parser.add_argument(
        '--transcript', '-t',
        help='Path to transcript file (txt, srt, or vtt format)'
    )

    parser.add_argument(
        '--config', '-c',
        help='Path to custom config YAML file'
    )

    parser.add_argument(
        '--export-clips', '-e',
        help='Export clips as separate video files to this directory'
    )

    # Customization arguments
    parser.add_argument(
        '--num-clips', '-n',
        type=int,
        help='Number of clips to extract (default: 5)'
    )

    parser.add_argument(
        '--min-duration',
        type=int,
        help='Minimum clip duration in seconds (default: 30)'
    )

    parser.add_argument(
        '--max-duration',
        type=int,
        help='Maximum clip duration in seconds (default: 60)'
    )

    parser.add_argument(
        '--no-audio',
        action='store_true',
        help='Disable audio emotion analysis'
    )

    parser.add_argument(
        '--no-text',
        action='store_true',
        help='Disable text topic analysis'
    )

    parser.add_argument(
        '--no-visual',
        action='store_true',
        help='Disable visual engagement analysis'
    )

    args = parser.parse_args()

    # Validate input
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    # Set default output
    if not args.output:
        input_stem = Path(args.input).stem
        args.output = f"{input_stem}_clips.json"

    # Initialize extractor
    try:
        extractor = ClipExtractor(config_path=args.config)

        # Apply CLI overrides
        if args.num_clips:
            extractor.config['general']['num_clips'] = args.num_clips
        if args.min_duration:
            extractor.config['general']['min_clip_duration'] = args.min_duration
        if args.max_duration:
            extractor.config['general']['max_clip_duration'] = args.max_duration
        if args.no_audio:
            extractor.config['audio']['enabled'] = False
        if args.no_text:
            extractor.config['text']['enabled'] = False
        if args.no_visual:
            extractor.config['visual']['enabled'] = False

    except Exception as e:
        print(f"Error initializing extractor: {e}")
        sys.exit(1)

    # Extract clips
    try:
        clips = extractor.extract_clips(
            input_path=args.input,
            transcript_path=args.transcript,
            output_path=args.output
        )

        print(f"\n✓ Results saved to: {args.output}")

        # Export clips if requested
        if args.export_clips:
            extractor.export_clips(
                input_path=args.input,
                clips=clips,
                output_dir=args.export_clips
            )

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
