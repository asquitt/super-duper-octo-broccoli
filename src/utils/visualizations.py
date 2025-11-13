"""Visualization utilities for clip extraction results and performance."""

import json
from typing import List, Dict
import os


class ResultVisualizer:
    """Create visualizations and reports for clip extraction results."""

    @staticmethod
    def create_text_visualization(clips: List[Dict], duration: float) -> str:
        """
        Create ASCII text visualization of clips on timeline.

        Args:
            clips: List of extracted clips
            duration: Total video duration

        Returns:
            ASCII visualization string
        """
        if not clips:
            return "No clips found."

        # Create timeline
        timeline_width = 80
        timeline = [' '] * timeline_width

        # Mark clips on timeline
        for i, clip in enumerate(clips):
            start_pos = int((clip['start_time'] if isinstance(clip.get('start_time'), (int, float))
                           else ResultVisualizer._time_to_seconds(clip['start_time'])) / duration * timeline_width)
            end_pos = int((clip['end_time'] if isinstance(clip.get('end_time'), (int, float))
                         else ResultVisualizer._time_to_seconds(clip['end_time'])) / duration * timeline_width)

            start_pos = min(start_pos, timeline_width - 1)
            end_pos = min(end_pos, timeline_width - 1)

            # Mark clip with number
            for pos in range(start_pos, end_pos + 1):
                timeline[pos] = str(i + 1) if pos == start_pos else '='

        # Build visualization
        viz = []
        viz.append("\n" + "=" * 80)
        viz.append("CLIP EXTRACTION VISUALIZATION")
        viz.append("=" * 80)
        viz.append(f"\nTotal Duration: {duration:.1f}s ({duration/60:.1f} minutes)")
        viz.append(f"Number of Clips: {len(clips)}\n")

        # Timeline
        viz.append("Timeline:")
        viz.append("0s" + " " * (timeline_width - 10) + f"{duration:.0f}s")
        viz.append("".join(timeline))
        viz.append("")

        # Clip details
        viz.append("Clips:")
        for i, clip in enumerate(clips, 1):
            start = clip.get('start_time', '??:??')
            end = clip.get('end_time', '??:??')
            title = clip.get('title', 'Untitled')
            score = clip.get('score', 0)

            viz.append(f"{i}. [{start} - {end}] Score: {score:.2f}")
            viz.append(f"   {title}")
            viz.append("")

        viz.append("=" * 80 + "\n")

        return "\n".join(viz)

    @staticmethod
    def create_performance_report(results_file: str) -> str:
        """
        Create performance report from benchmark results.

        Args:
            results_file: Path to JSON file with benchmark results

        Returns:
            Formatted performance report
        """
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)

            report = []
            report.append("\n" + "=" * 80)
            report.append("PERFORMANCE BENCHMARK REPORT")
            report.append("=" * 80 + "\n")

            for name, data in sorted(results.items()):
                report.append(f"{name}:")
                report.append(f"  Duration: {data['duration']:.3f}s")
                for key, value in data.get('details', {}).items():
                    report.append(f"  {key}: {value}")
                report.append("")

            report.append("=" * 80 + "\n")

            return "\n".join(report)

        except Exception as e:
            return f"Error loading performance results: {e}"

    @staticmethod
    def create_metrics_report(metrics: Dict[str, float]) -> str:
        """
        Create formatted metrics report.

        Args:
            metrics: Dictionary of metric names and values

        Returns:
            Formatted report string
        """
        report = []
        report.append("\n" + "=" * 80)
        report.append("EVALUATION METRICS REPORT")
        report.append("=" * 80 + "\n")

        # Group metrics
        accuracy_metrics = {}
        other_metrics = {}

        for key, value in metrics.items():
            if any(k in key.lower() for k in ['map', 'hit', 'precision', 'recall', 'f1']):
                accuracy_metrics[key] = value
            else:
                other_metrics[key] = value

        if accuracy_metrics:
            report.append("Accuracy Metrics:")
            for key, value in sorted(accuracy_metrics.items()):
                bar = '█' * int(value * 20)
                report.append(f"  {key:.<25} {value:.4f} {bar}")
            report.append("")

        if other_metrics:
            report.append("Other Metrics:")
            for key, value in sorted(other_metrics.items()):
                report.append(f"  {key:.<25} {value:.4f}")
            report.append("")

        report.append("=" * 80 + "\n")

        return "\n".join(report)

    @staticmethod
    def create_comparison_chart(clips: List[Dict]) -> str:
        """
        Create ASCII bar chart comparing clip scores.

        Args:
            clips: List of clips with scores

        Returns:
            ASCII bar chart
        """
        if not clips:
            return "No clips to visualize."

        chart = []
        chart.append("\n" + "=" * 80)
        chart.append("CLIP SCORES COMPARISON")
        chart.append("=" * 80 + "\n")

        max_score = max(clip.get('score', 0) for clip in clips)

        for i, clip in enumerate(clips, 1):
            score = clip.get('score', 0)
            title = clip.get('title', 'Untitled')

            # Truncate title if too long
            if len(title) > 40:
                title = title[:37] + "..."

            # Create bar
            bar_length = int((score / max_score * 40)) if max_score > 0 else 0
            bar = '█' * bar_length

            chart.append(f"{i}. {score:.2f} {bar}")
            chart.append(f"   {title}")
            chart.append("")

        chart.append("=" * 80 + "\n")

        return "\n".join(chart)

    @staticmethod
    def create_modality_breakdown(clips: List[Dict]) -> str:
        """
        Create breakdown of modality scores.

        Args:
            clips: List of clips with modality scores

        Returns:
            Formatted breakdown
        """
        if not clips:
            return "No clips to analyze."

        breakdown = []
        breakdown.append("\n" + "=" * 80)
        breakdown.append("MODALITY SCORE BREAKDOWN")
        breakdown.append("=" * 80 + "\n")

        # Calculate averages
        audio_scores = [c.get('audio_score', 0) for c in clips]
        text_scores = [c.get('text_score', 0) for c in clips]
        visual_scores = [c.get('visual_score', 0) for c in clips]

        avg_audio = sum(audio_scores) / len(audio_scores) if audio_scores else 0
        avg_text = sum(text_scores) / len(text_scores) if text_scores else 0
        avg_visual = sum(visual_scores) / len(visual_scores) if visual_scores else 0

        breakdown.append("Average Scores by Modality:")
        breakdown.append(f"  Audio:  {avg_audio:.3f} {'█' * int(avg_audio * 30)}")
        breakdown.append(f"  Text:   {avg_text:.3f} {'█' * int(avg_text * 30)}")
        breakdown.append(f"  Visual: {avg_visual:.3f} {'█' * int(avg_visual * 30)}")
        breakdown.append("")

        breakdown.append("Individual Clip Breakdown:")
        for i, clip in enumerate(clips, 1):
            breakdown.append(f"\nClip {i}: {clip.get('title', 'Untitled')}")
            breakdown.append(f"  Audio:  {clip.get('audio_score', 0):.3f}")
            breakdown.append(f"  Text:   {clip.get('text_score', 0):.3f}")
            breakdown.append(f"  Visual: {clip.get('visual_score', 0):.3f}")
            breakdown.append(f"  Total:  {clip.get('score', 0):.3f}")

        breakdown.append("\n" + "=" * 80 + "\n")

        return "\n".join(breakdown)

    @staticmethod
    def save_html_report(clips: List[Dict], output_file: str, duration: float = None):
        """
        Save results as HTML report.

        Args:
            clips: List of extracted clips
            output_file: Path to save HTML file
            duration: Total video duration
        """
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("<title>Clip Extraction Report</title>")
        html.append("<style>")
        html.append("body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }")
        html.append("h1 { color: #333; }")
        html.append(".clip { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }")
        html.append(".score { display: inline-block; padding: 5px 10px; background: #4CAF50; color: white; border-radius: 4px; }")
        html.append(".time { color: #666; }")
        html.append(".title { font-size: 18px; font-weight: bold; margin: 10px 0; }")
        html.append(".bar { height: 20px; background: #4CAF50; border-radius: 4px; margin: 5px 0; }")
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        html.append("<h1>Clip Extraction Report</h1>")

        if duration:
            html.append(f"<p>Total Duration: {duration:.1f}s ({duration/60:.1f} minutes)</p>")

        html.append(f"<p>Number of Clips: {len(clips)}</p>")

        for i, clip in enumerate(clips, 1):
            score = clip.get('score', 0)
            start = clip.get('start_time', '??:??')
            end = clip.get('end_time', '??:??')
            title = clip.get('title', 'Untitled')

            html.append(f'<div class="clip">')
            html.append(f'<div><span class="score">{score:.2f}</span> <span class="time">{start} - {end}</span></div>')
            html.append(f'<div class="title">{i}. {title}</div>')

            # Score bars
            if 'audio_score' in clip:
                html.append(f'<div>Audio: <div class="bar" style="width: {clip["audio_score"]*100}%"></div></div>')
            if 'text_score' in clip:
                html.append(f'<div>Text: <div class="bar" style="width: {clip["text_score"]*100}%"></div></div>')
            if 'visual_score' in clip:
                html.append(f'<div>Visual: <div class="bar" style="width: {clip["visual_score"]*100}%"></div></div>')

            html.append('</div>')

        html.append("</body>")
        html.append("</html>")

        with open(output_file, 'w') as f:
            f.write('\n'.join(html))

    @staticmethod
    def _time_to_seconds(time_str: str) -> float:
        """Convert MM:SS or HH:MM:SS to seconds."""
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0.0
