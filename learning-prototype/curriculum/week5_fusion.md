# Week 5: Multimodal Fusion

**Goal**: Combine audio, text, and visual signals to find the best clips.

---

## 📚 Learning Objectives

By the end of this week, you will:
- ✅ Understand multimodal fusion strategies
- ✅ Align signals from different sources
- ✅ Implement weighted combination
- ✅ Detect signal synergy
- ✅ Rank and select top clips

---

## 🎯 What We're Building This Week

A fusion engine that:
1. Aligns audio, text, and visual signals in time
2. Combines scores using weighted strategies
3. Detects moments where all signals agree (synergy)
4. Ranks candidate clips
5. Removes overlapping clips

This is the **heart** of the system!

---

## 📖 Key Concepts

### 1. The Multimodal Fusion Problem

```
You have three signals:

Audio:   [0.2, 0.8, 0.9, 0.3, 0.1] (emotion scores over time)
Text:    [0.1, 0.7, 0.6, 0.2, 0.0] (topic importance)
Visual:  [0.3, 0.9, 0.8, 0.4, 0.2] (engagement scores)

Question: Which moments are most important?

Answer: Where multiple signals are HIGH!
         Time 1-2: All three are high → HIGHLIGHT!
```

### 2. Fusion Strategies

**Early Fusion**: Combine features before analysis
```
Audio features + Text features + Visual features
           ↓
    Single classifier
           ↓
        Output
```

**Late Fusion**: Combine decisions after analysis (we use this!)
```
Audio → Emotion score ────┐
Text  → Topic score   ────┼──→ Weighted Sum → Final Score
Visual → Engagement ──────┘
```

**Weighted Combination**:
```python
final_score = (
    audio_score  * 0.4 +  # Audio is important for emotion
    text_score   * 0.3 +  # Text shows topics
    visual_score * 0.3    # Visual shows engagement
)
```

### 3. Signal Alignment

Problem: Signals might be at different time intervals
```
Audio:  Analyzed every 1 second   → 60 scores for 1 minute
Text:   Analyzed every 5 seconds  → 12 scores for 1 minute
Visual: Analyzed every 2 seconds  → 30 scores for 1 minute

Need: All aligned to same timeline!
```

Solution: **Interpolation**
```python
# Resample all signals to common timeline (e.g., every 1 second)
audio_aligned  = interpolate(audio_times, audio_scores, common_times)
text_aligned   = interpolate(text_times, text_scores, common_times)
visual_aligned = interpolate(visual_times, visual_scores, common_times)
```

### 4. Peak Detection

Find moments where score is locally maximum:
```
Scores: [0.3, 0.5, 0.9, 0.6, 0.2, 0.4, 0.8, 0.5, 0.1]
                     ↑                    ↑
                   Peak 1              Peak 2

Peaks are potential highlight moments!
```

**Algorithm**:
```python
1. Find local maxima (higher than neighbors)
2. Filter by minimum height (e.g., > 0.6)
3. Filter by minimum distance (e.g., 5 seconds apart)
4. Sort by score
5. Take top N peaks
```

### 5. Clip Generation

Convert peaks to clips:
```
Peak at time T with score S
↓
Clip: [T - 15s, T + 15s] (30-second clip centered on peak)

Adjust if:
- Clip goes before start → Shift to [0, 30]
- Clip goes past end → Shift to [end-30, end]
```

---

## 💻 Fusion Algorithm

### Step-by-Step Process

```
INPUT:
- audio_scores: List[(time, score)]
- text_scores:  List[(time, score)]
- visual_scores: List[(time, score)]
- duration: Total video duration

STEP 1: Align signals
common_timeline = [0, 1, 2, 3, ..., duration]
audio_aligned  = interpolate(audio_scores, common_timeline)
text_aligned   = interpolate(text_scores, common_timeline)
visual_aligned = interpolate(visual_scores, common_timeline)

STEP 2: Combine scores
combined = []
for t in common_timeline:
    score = (
        audio_aligned[t] * 0.4 +
        text_aligned[t]  * 0.3 +
        visual_aligned[t] * 0.3
    )
    combined.append((t, score))

STEP 3: Find peaks
peaks = find_peaks(combined, min_height=0.6, min_distance=5)

STEP 4: Generate clips
clips = []
for peak_time, peak_score in peaks:
    start = max(0, peak_time - 15)
    end = min(duration, peak_time + 15)
    clips.append({
        'start_time': start,
        'end_time': end,
        'score': peak_score
    })

STEP 5: Remove overlaps
final_clips = remove_overlapping_clips(clips)

STEP 6: Sort by score
final_clips.sort(key=lambda c: c['score'], reverse=True)

OUTPUT: Top N clips
return final_clips[:5]  # Return top 5
```

---

## 💻 Starter Code

See `starter-code/week5_starter/fusion_engine.py`

### Key Functions to Implement

```python
def align_signals(signals: List[List[Tuple[float, float]]],
                 duration: float,
                 resolution: float = 1.0) -> np.ndarray:
    """
    Align multiple signals to common timeline.

    Args:
        signals: List of [(time, score)] for each modality
        duration: Total duration
        resolution: Time step for common timeline

    Returns:
        Array of shape (n_signals, n_timesteps)
    """
    # TODO:
    # 1. Create common timeline: [0, resolution, 2*resolution, ...]
    # 2. For each signal, interpolate to common timeline
    # 3. Stack into 2D array
    pass

def weighted_fusion(aligned_signals: np.ndarray,
                   weights: List[float] = [0.4, 0.3, 0.3]) -> np.ndarray:
    """
    Combine aligned signals using weighted sum.

    Args:
        aligned_signals: Shape (n_signals, n_timesteps)
        weights: Weight for each signal

    Returns:
        Combined score for each timestep
    """
    # TODO:
    # 1. Normalize weights to sum to 1.0
    # 2. Multiply each signal by its weight
    # 3. Sum across signals
    pass

def find_peaks(scores: np.ndarray,
              min_height: float = 0.6,
              min_distance: int = 5) -> List[Tuple[int, float]]:
    """
    Find peak moments in score timeline.

    Args:
        scores: Score for each timestep
        min_height: Minimum score to be peak
        min_distance: Minimum timesteps between peaks

    Returns:
        List of (peak_index, peak_score)
    """
    # TODO:
    # 1. Find local maxima (score[i] > score[i-1] and score[i] > score[i+1])
    # 2. Filter by min_height
    # 3. Filter by min_distance (keep highest in each window)
    # 4. Sort by score
    pass

def generate_clips(peaks: List[Tuple[int, float]],
                  duration: float,
                  clip_length: float = 30.0) -> List[Dict]:
    """
    Generate clips centered on peaks.

    Args:
        peaks: List of (time, score)
        duration: Total video duration
        clip_length: Desired clip length

    Returns:
        List of clip dictionaries
    """
    # TODO:
    # 1. For each peak, create clip [peak - length/2, peak + length/2]
    # 2. Adjust boundaries if they go outside [0, duration]
    # 3. Create clip dict with start_time, end_time, score
    pass
```

---

## ✏️ Exercises

### Exercise 1: Signal Interpolation
```python
import numpy as np

# Original signal (sparse)
times = [0, 5, 10, 15, 20]
scores = [0.2, 0.8, 0.9, 0.5, 0.1]

# New timeline (dense)
new_times = np.arange(0, 21, 1)  # Every second

# Interpolate
new_scores = np.interp(new_times, times, scores)

# Visualize
for t, s in zip(new_times, new_scores):
    bar = '#' * int(s * 20)
    print(f"{t:2d}s: {bar} {s:.2f}")
```

### Exercise 2: Weighted Fusion
```python
# Three signals
audio  = [0.2, 0.8, 0.9, 0.3]
text   = [0.1, 0.7, 0.6, 0.2]
visual = [0.3, 0.9, 0.8, 0.4]

# Weights
w_audio, w_text, w_visual = 0.4, 0.3, 0.3

# Combine
combined = []
for a, t, v in zip(audio, text, visual):
    score = a * w_audio + t * w_text + v * w_visual
    combined.append(score)

print("Combined:", [f"{s:.2f}" for s in combined])
# Output: [0.23, 0.80, 0.83, 0.31]
```

### Exercise 3: Peak Detection
```python
scores = [0.2, 0.5, 0.9, 0.6, 0.3, 0.4, 0.8, 0.5, 0.2]

peaks = []
for i in range(1, len(scores) - 1):
    if scores[i] > scores[i-1] and scores[i] > scores[i+1]:
        if scores[i] > 0.6:  # Minimum height
            peaks.append((i, scores[i]))

print("Peaks:", peaks)
# Output: [(2, 0.9), (6, 0.8)]
```

---

## 🎯 Implementation Tasks

### Beginner Tasks
1. ✅ Understand numpy arrays
2. ✅ Implement linear interpolation
3. ✅ Implement weighted sum
4. ✅ Find local maxima

### Intermediate Tasks
5. ✅ Align multiple signals
6. ✅ Implement peak detection with constraints
7. ✅ Generate clips from peaks
8. ✅ Remove overlapping clips
9. ✅ Visualize fusion results

### Advanced Tasks
10. ✅ Implement adaptive weighting
11. ✅ Add signal synergy detection
12. ✅ Implement non-maximum suppression
13. ✅ Add confidence intervals

---

## 📊 Understanding Overlap Removal

```python
def remove_overlapping_clips(clips: List[Dict]) -> List[Dict]:
    """
    Remove overlapping clips, keeping highest scored ones.

    Algorithm: Non-Maximum Suppression (NMS)
    1. Sort clips by score (descending)
    2. Keep first clip
    3. Remove any clips that overlap with it
    4. Repeat with remaining clips
    """
    # Sort by score
    sorted_clips = sorted(clips, key=lambda c: c['score'], reverse=True)

    result = []
    for clip in sorted_clips:
        # Check if overlaps with any kept clip
        overlaps = False
        for kept_clip in result:
            if clips_overlap(clip, kept_clip):
                overlaps = True
                break

        if not overlaps:
            result.append(clip)

    return result

def clips_overlap(clip1: Dict, clip2: Dict, threshold: float = 0.3) -> bool:
    """Check if two clips overlap significantly."""
    # Calculate intersection
    start = max(clip1['start_time'], clip2['start_time'])
    end = min(clip1['end_time'], clip2['end_time'])
    intersection = max(0, end - start)

    # Calculate union
    union = (clip1['end_time'] - clip1['start_time'] +
             clip2['end_time'] - clip2['start_time'] -
             intersection)

    # IoU (Intersection over Union)
    iou = intersection / union if union > 0 else 0

    return iou > threshold
```

---

## 🐛 Common Issues

### Issue 1: Different array lengths
```python
# Problem: Signals have different lengths
audio  = [0.2, 0.8, 0.9]  # 3 elements
text   = [0.1, 0.7]       # 2 elements

# Solution: Interpolate to same length first
common_times = np.linspace(0, duration, 100)
audio_interp = np.interp(common_times, audio_times, audio)
text_interp = np.interp(common_times, text_times, text)
```

### Issue 2: Peaks too close together
```python
# Problem: Multiple peaks within 5 seconds
# Solution: Implement minimum distance constraint

def filter_peaks_by_distance(peaks, min_distance=5):
    filtered = []
    for time, score in sorted(peaks, key=lambda p: p[1], reverse=True):
        # Check distance to all kept peaks
        too_close = any(abs(time - t) < min_distance for t, _ in filtered)
        if not too_close:
            filtered.append((time, score))
    return filtered
```

### Issue 3: Clips extend beyond video duration
```python
# Problem: Clip is [295s, 325s] but video ends at 300s
# Solution: Clamp to valid range

start = max(0, peak_time - clip_length / 2)
end = min(duration, peak_time + clip_length / 2)

# Ensure minimum length
if end - start < clip_length:
    if start == 0:
        end = min(duration, clip_length)
    elif end == duration:
        start = max(0, duration - clip_length)
```

---

## 📈 Testing Your Fusion Engine

```python
def test_fusion_engine():
    # Create test data
    audio_scores = [(0, 0.2), (5, 0.8), (10, 0.9), (15, 0.3)]
    text_scores = [(0, 0.1), (5, 0.7), (10, 0.6), (15, 0.2)]
    visual_scores = [(0, 0.3), (5, 0.9), (10, 0.8), (15, 0.4)]

    fusion = FusionEngine()

    # Test alignment
    aligned = fusion.align_signals(
        [audio_scores, text_scores, visual_scores],
        duration=15.0,
        resolution=1.0
    )
    assert aligned.shape[0] == 3, "Should have 3 signals"
    assert aligned.shape[1] == 16, "Should have 16 timesteps (0-15)"
    print("✓ Signal alignment works")

    # Test fusion
    combined = fusion.weighted_fusion(aligned)
    assert len(combined) == 16, "Combined should match timeline"
    print(f"✓ Fusion works, peak score: {max(combined):.2f}")

    # Test peak detection
    peaks = fusion.find_peaks(combined, min_height=0.6)
    assert len(peaks) > 0, "Should find at least one peak"
    print(f"✓ Found {len(peaks)} peaks")

    # Test clip generation
    clips = fusion.generate_clips(peaks, duration=15.0, clip_length=10.0)
    assert len(clips) > 0, "Should generate clips"
    print(f"✓ Generated {len(clips)} clips")

    print("\nAll tests passed!")

if __name__ == '__main__':
    test_fusion_engine()
```

---

## 🎓 What You'll Learn

After this week, you will understand:
- How to combine multiple data sources
- Signal processing and alignment
- Peak detection algorithms
- Non-maximum suppression
- Algorithm design and optimization

**These skills apply to**:
- Sensor fusion (robotics, autonomous vehicles)
- Multi-modal machine learning
- Time-series analysis
- Recommendation systems
- Data integration

---

## 💡 Extension Ideas

1. **Adaptive Weighting**: Learn weights from data
2. **Synergy Detection**: Bonus when all signals agree
3. **Temporal Smoothing**: Smooth scores before peak detection
4. **Multi-Scale Fusion**: Generate clips of different lengths
5. **Confidence Scoring**: Estimate clip quality confidence

---

**Next**: [Week 6 - Output Generation](week6_output.md)
