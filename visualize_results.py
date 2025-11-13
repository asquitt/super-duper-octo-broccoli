#!/usr/bin/env python3
"""
Visualization script for clip extraction results.
"""

import sys
import json
import argparse
from src.utils.visualizations import ResultVisualizer


def main():
    parser = argparse.ArgumentParser(description='Visualize clip extraction results')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file with clips')
    parser.add_argument('--duration', '-d', type=float, help='Total video duration in seconds')
    parser.add_argument('--html', help='Output HTML report file')
    parser.add_argument('--show-timeline', action='store_true', help='Show ASCII timeline')
    parser.add_argument('--show-scores', action='store_true', help='Show score comparison chart')
    parser.add_argument('--show-modalities', action='store_true', help='Show modality breakdown')

    args = parser.parse_args()

    # Load clips
    try:
        with open(args.input, 'r') as f:
            clips = json.load(f)
    except Exception as e:
        print(f"Error loading clips: {e}")
        sys.exit(1)

    if not clips:
        print("No clips found in input file.")
        sys.exit(0)

    # Estimate duration if not provided
    if not args.duration:
        # Try to estimate from clips
        max_end = max(
            (ResultVisualizer._time_to_seconds(c['end_time'])
             if isinstance(c.get('end_time'), str)
             else c.get('end_time', 0))
            for c in clips
        )
        args.duration = max_end + 10  # Add some buffer

    # Show visualizations
    if args.show_timeline or not any([args.show_scores, args.show_modalities, args.html]):
        print(ResultVisualizer.create_text_visualization(clips, args.duration))

    if args.show_scores:
        print(ResultVisualizer.create_comparison_chart(clips))

    if args.show_modalities:
        print(ResultVisualizer.create_modality_breakdown(clips))

    # Generate HTML report
    if args.html:
        ResultVisualizer.save_html_report(clips, args.html, args.duration)
        print(f"\nHTML report saved to: {args.html}")


if __name__ == '__main__':
    main()
