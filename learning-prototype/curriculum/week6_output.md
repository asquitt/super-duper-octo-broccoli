# Week 6: Output Generation & CLI

**Goal**: Create engaging titles, format output, and build a command-line interface.

---

## 📚 Learning Objectives

By the end of this week, you will:
- ✅ Generate descriptive clip titles
- ✅ Format output as JSON
- ✅ Build a CLI with argparse
- ✅ Create visualizations of results
- ✅ Export clips using FFmpeg

---

## 🎯 What We're Building This Week

An output system that:
1. Generates titles for clips
2. Exports results as JSON
3. Creates HTML reports
4. Provides a CLI interface
5. (Optional) Extracts actual video clips

---

## 📖 Key Concepts

### 1. Title Generation

Good titles are:
- **Descriptive**: Tell what happens
- **Engaging**: Create curiosity
- **Short**: 5-10 words

**Template-Based Generation**:
```python
templates = [
    "Exciting moment at {time}",
    "Key discussion about {topic}",
    "{emotion} scene from {speaker}",
    "Watch this {adjective} part!"
]

# Fill in template
title = "Key discussion about AI at 2:35"
```

**Context-Based Generation**:
```python
# Use transcript + scores
if has_question:
    title = f"Q&A: {question_text[:50]}"
elif emotion_score > 0.8:
    title = f"Exciting moment at {timestamp}"
elif topic_changed:
    title = f"New topic: {top_keyword}"
else:
    title = f"Highlight at {timestamp}"
```

### 2. JSON Output Format

```json
{
  "video_info": {
    "input_file": "lecture.mp4",
    "duration": 3600.0,
    "processed_at": "2024-01-15T10:30:00"
  },
  "clips": [
    {
      "id": 1,
      "start_time": 125.5,
      "end_time": 155.5,
      "duration": 30.0,
      "score": 0.87,
      "title": "Key discussion about neural networks",
      "metadata": {
        "audio_score": 0.85,
        "text_score": 0.90,
        "visual_score": 0.86,
        "keywords": ["neural networks", "AI", "deep learning"],
        "has_question": true
      }
    }
  ],
  "summary": {
    "total_clips": 5,
    "total_duration": 150.0,
    "avg_score": 0.82
  }
}
```

### 3. CLI Design

Good CLI:
- Clear help messages
- Sensible defaults
- Flexible options
- Progress feedback

```bash
# Simple usage
python main.py --input video.mp4

# Advanced usage
python main.py \
    --input video.mp4 \
    --transcript transcript.txt \
    --output clips.json \
    --num-clips 5 \
    --min-score 0.7 \
    --clip-length 45 \
    --no-visual
```

---

## 💻 Starter Code

See `starter-code/week6_starter/output_generator.py`

### Key Functions

```python
def generate_title(clip: Dict, transcript: str = None) -> str:
    """
    Generate engaging title for clip.

    Args:
        clip: Clip dictionary with metadata
        transcript: Full transcript text

    Returns:
        Title string
    """
    # TODO:
    # 1. Extract clip metadata (scores, keywords, time)
    # 2. Check if transcript available for this time range
    # 3. Select appropriate template
    # 4. Fill in template with context
    pass

def export_json(clips: List[Dict], output_path: str, video_info: Dict = None):
    """
    Export clips to JSON file.

    Args:
        clips: List of clip dictionaries
        output_path: Where to save JSON
        video_info: Optional video metadata
    """
    # TODO:
    # 1. Create output structure
    # 2. Add video info
    # 3. Add clips with all metadata
    # 4. Calculate summary stats
    # 5. Write to file with pretty formatting
    pass

def create_html_report(clips: List[Dict], output_path: str):
    """
    Create HTML visualization of results.

    Args:
        clips: List of clip dictionaries
        output_path: Where to save HTML file
    """
    # TODO:
    # 1. Create HTML template
    # 2. Add timeline visualization
    # 3. Add clip cards with details
    # 4. Add interactive elements
    # 5. Write to file
    pass

def build_cli() -> argparse.ArgumentParser:
    """
    Build command-line interface.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='Extract engaging clips from long videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python main.py --input lecture.mp4

  # With transcript
  python main.py --input video.mp4 --transcript transcript.txt

  # Custom settings
  python main.py --input video.mp4 --num-clips 10 --clip-length 45
        """
    )

    # TODO: Add all arguments
    # - input file (required)
    # - transcript (optional)
    # - output path
    # - number of clips
    # - minimum score
    # - clip length
    # - weights for fusion
    # - enable/disable modalities

    return parser
```

---

## ✏️ Exercises

### Exercise 1: Template System
```python
# Create title templates
templates = {
    'question': "Q&A: {question}",
    'topic_change': "New topic: {topic}",
    'high_emotion': "{emotion} moment at {time}",
    'default': "Highlight at {time}"
}

def select_template(clip):
    if clip['metadata']['has_question']:
        return 'question'
    elif clip['metadata']['topic_changed']:
        return 'topic_change'
    elif clip['score'] > 0.85:
        return 'high_emotion'
    else:
        return 'default'

# Generate title
template_key = select_template(clip)
template = templates[template_key]
title = template.format(
    question=clip['metadata'].get('question', ''),
    topic=clip['metadata'].get('topic', ''),
    emotion='Exciting',
    time=format_time(clip['start_time'])
)
```

### Exercise 2: JSON Export
```python
import json
from datetime import datetime

def export_results(clips, output_path, video_file):
    output = {
        'video_info': {
            'input_file': video_file,
            'processed_at': datetime.now().isoformat(),
            'duration': clips[-1]['end_time'] if clips else 0
        },
        'clips': clips,
        'summary': {
            'total_clips': len(clips),
            'avg_score': sum(c['score'] for c in clips) / len(clips) if clips else 0,
            'total_duration': sum(c['end_time'] - c['start_time'] for c in clips)
        }
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✓ Saved {len(clips)} clips to {output_path}")
```

### Exercise 3: Simple CLI
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description='Video clip extractor')

    # Required arguments
    parser.add_argument('--input', required=True, help='Input video file')

    # Optional arguments
    parser.add_argument('--output', default='clips.json', help='Output JSON file')
    parser.add_argument('--num-clips', type=int, default=5, help='Number of clips')
    parser.add_argument('--clip-length', type=float, default=30.0, help='Clip length in seconds')

    # Flags
    parser.add_argument('--no-visual', action='store_true', help='Skip visual analysis')

    args = parser.parse_args()

    print(f"Processing: {args.input}")
    print(f"Output: {args.output}")
    print(f"Clips: {args.num_clips} × {args.clip_length}s")

    # Process video...

if __name__ == '__main__':
    main()
```

---

## 🎯 Implementation Tasks

### Beginner
1. ✅ Create title templates
2. ✅ Write JSON output
3. ✅ Format timestamps (MM:SS)
4. ✅ Build basic CLI

### Intermediate
5. ✅ Context-aware title generation
6. ✅ HTML report generation
7. ✅ Progress indicators
8. ✅ Error handling

### Advanced
9. ✅ Extract video clips with FFmpeg
10. ✅ Thumbnail generation
11. ✅ Interactive HTML with JavaScript
12. ✅ Batch processing multiple videos

---

## 💻 Extracting Video Clips (Optional)

```python
def extract_clip(video_path: str, start_time: float, end_time: float,
                output_path: str) -> str:
    """
    Extract video clip using FFmpeg.

    Args:
        video_path: Input video
        start_time: Start time in seconds
        end_time: End time in seconds
        output_path: Output clip file

    Returns:
        Path to extracted clip
    """
    import subprocess

    duration = end_time - start_time

    cmd = [
        'ffmpeg',
        '-ss', str(start_time),      # Start time
        '-i', video_path,             # Input
        '-t', str(duration),          # Duration
        '-c', 'copy',                 # Copy codecs (fast!)
        '-y',                         # Overwrite
        output_path
    ]

    subprocess.run(cmd, capture_output=True, check=True)

    return output_path

# Usage
for i, clip in enumerate(clips):
    output = f"clip_{i+1}.mp4"
    extract_clip(
        'video.mp4',
        clip['start_time'],
        clip['end_time'],
        output
    )
    print(f"✓ Extracted {output}")
```

---

## 📊 HTML Report Template

```python
def create_html_report(clips, output_path):
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Video Highlights Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .clip {{ border: 1px solid #ddd; margin: 20px 0; padding: 15px; }}
        .score {{ color: #0066cc; font-weight: bold; }}
        .timeline {{ background: #f0f0f0; height: 30px; margin: 10px 0; position: relative; }}
        .clip-bar {{ background: #0066cc; height: 100%; position: absolute; }}
    </style>
</head>
<body>
    <h1>Video Highlights Report</h1>
    <p>Found {len(clips)} highlights</p>

    <div class="timeline">
        <!-- Timeline visualization -->
    </div>

    <div class="clips">
"""

    for i, clip in enumerate(clips, 1):
        html += f"""
        <div class="clip">
            <h3>Clip {i}: {clip['title']}</h3>
            <p>Time: {format_time(clip['start_time'])} - {format_time(clip['end_time'])}</p>
            <p>Score: <span class="score">{clip['score']:.2f}</span></p>
            <p>Keywords: {', '.join(clip['metadata'].get('keywords', []))}</p>
        </div>
"""

    html += """
    </div>
</body>
</html>
"""

    with open(output_path, 'w') as f:
        f.write(html)
```

---

## 🐛 Common Issues

### Issue 1: Unicode in titles
```python
# Problem: Transcript has special characters
title = "Discussion about AI's future"  # Apostrophe causes issues

# Solution: Escape for JSON
import json
title = json.dumps(title)  # Properly escaped
```

### Issue 2: Large JSON files
```python
# Problem: Many clips create huge JSON

# Solution: Compress output
import gzip
import json

with gzip.open('clips.json.gz', 'wt') as f:
    json.dump(output, f)
```

### Issue 3: CLI argument validation
```python
def validate_args(args):
    """Validate CLI arguments."""
    if not os.path.exists(args.input):
        parser.error(f"Input file not found: {args.input}")

    if args.num_clips < 1:
        parser.error("--num-clips must be >= 1")

    if args.clip_length < 5:
        parser.error("--clip-length must be >= 5 seconds")

    return args
```

---

## 📈 Testing

```python
def test_output_generator():
    # Test title generation
    clip = {
        'start_time': 125.5,
        'score': 0.87,
        'metadata': {'keywords': ['AI', 'neural networks']}
    }

    title = generate_title(clip)
    assert len(title) > 0
    assert len(title) < 100  # Not too long
    print(f"✓ Generated title: {title}")

    # Test JSON export
    clips = [clip]
    export_json(clips, 'test_output.json')
    assert os.path.exists('test_output.json')

    # Validate JSON
    with open('test_output.json') as f:
        data = json.load(f)
        assert 'clips' in data
        assert len(data['clips']) == 1

    print("✓ All output tests passed")
```

---

## 🎓 What You'll Learn

- Template-based text generation
- JSON data formatting
- CLI design with argparse
- HTML/CSS basics
- FFmpeg video processing

**These skills apply to**:
- Building command-line tools
- Data export/reporting
- Web development
- Automation scripts
- Data pipelines

---

**Next**: [Week 7 - Testing & Optimization](week7_testing.md)
