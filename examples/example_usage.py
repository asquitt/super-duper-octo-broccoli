#!/usr/bin/env python3
"""
Example usage of the Multimodal Clip Extractor.

This script demonstrates various ways to use the clip extractor.
"""

from src.orchestrator import ClipExtractor


def example_basic():
    """Basic usage example."""
    print("Example 1: Basic video processing")
    print("-" * 50)

    # Initialize extractor with default config
    extractor = ClipExtractor()

    # Extract clips from a video
    clips = extractor.extract_clips(
        input_path="path/to/your/video.mp4",
        output_path="clips.json"
    )

    print(f"\nExtracted {len(clips)} clips:")
    for i, clip in enumerate(clips, 1):
        print(f"{i}. {clip['title']}")
        print(f"   Time: {clip['start_time']} - {clip['end_time']}")
        print(f"   Score: {clip['score']}")


def example_with_transcript():
    """Example with existing transcript."""
    print("\nExample 2: With existing transcript")
    print("-" * 50)

    extractor = ClipExtractor()

    clips = extractor.extract_clips(
        input_path="path/to/audio.mp3",
        transcript_path="path/to/transcript.txt",
        output_path="clips.json"
    )

    print(f"Extracted {len(clips)} clips")


def example_custom_config():
    """Example with custom configuration."""
    print("\nExample 3: Custom configuration")
    print("-" * 50)

    extractor = ClipExtractor()

    # Customize settings
    extractor.config['general']['num_clips'] = 3
    extractor.config['general']['min_clip_duration'] = 45
    extractor.config['general']['max_clip_duration'] = 90

    clips = extractor.extract_clips(
        input_path="path/to/video.mp4",
        output_path="clips.json"
    )

    print(f"Extracted {len(clips)} clips with custom settings")


def example_export_clips():
    """Example of extracting and exporting clips."""
    print("\nExample 4: Export video clips")
    print("-" * 50)

    extractor = ClipExtractor()

    # Extract clip metadata
    clips = extractor.extract_clips(
        input_path="path/to/video.mp4",
        output_path="clips.json"
    )

    # Export as separate video files
    extractor.export_clips(
        input_path="path/to/video.mp4",
        clips=clips,
        output_dir="./exported_clips"
    )

    print(f"Exported {len(clips)} video clips to ./exported_clips")


if __name__ == '__main__':
    print("Multimodal Clip Extractor - Usage Examples\n")
    print("Note: Replace 'path/to/your/video.mp4' with actual file paths\n")

    # Uncomment the examples you want to run:

    # example_basic()
    # example_with_transcript()
    # example_custom_config()
    # example_export_clips()

    print("\nEdit this file to uncomment and run specific examples.")
