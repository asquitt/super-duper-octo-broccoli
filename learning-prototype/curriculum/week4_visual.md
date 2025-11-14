# Week 4: Visual Engagement Detection

**Goal**: Detect motion, scene changes, and visual engagement in video.

---

## 📚 Learning Objectives

By the end of this week, you will:
- ✅ Understand computer vision basics
- ✅ Extract frames from video
- ✅ Detect motion between frames
- ✅ Identify scene changes
- ✅ Calculate visual engagement scores

---

## 🎯 What We're Building This Week

A visual analyzer that can:
1. Extract frames from video at intervals
2. Detect motion using frame differencing
3. Identify scene changes using histograms
4. Track faces (optional)
5. Score visual engagement over time

---

## 📖 Key Concepts

### 1. Video as Frame Sequence

```
Video (30 fps):
Frame 0  Frame 1  Frame 2  ... Frame 899 (for 30s video)
   |        |        |              |
   └────────┴────────┴──────────────┘
         Extract every Nth frame

Sample at 1 fps:
Frame 0, Frame 30, Frame 60, ...
```

### 2. Motion Detection

**Frame Differencing**: Compare consecutive frames
```
Frame N     Frame N+1
[image1] - [image2] = Difference

High difference = Motion detected
Low difference  = Static scene
```

**Algorithm**:
```python
1. Convert frames to grayscale
2. Calculate absolute difference
3. Threshold to get motion mask
4. Count non-zero pixels
5. Normalize to get motion score
```

### 3. Scene Change Detection

**Histogram Comparison**: Different scenes have different color distributions

```
Scene 1 (outdoors):   Lots of blue (sky), green (grass)
Scene 2 (indoors):    Lots of beige (walls), brown (furniture)

Compare histograms → Large difference = Scene change
```

**Chi-Square Distance**: Measures histogram similarity
```
Low value  = Similar scenes
High value = Different scenes (scene change!)
```

### 4. Face Detection (Optional)

Uses Haar Cascades or DNN:
```
Presence of faces = Higher engagement
Multiple faces = Group discussion (interesting!)
Face movements = Speaker gesturing (engaging!)
```

---

## 💻 How It Works

### Frame Extraction Pipeline

```
Input: video.mp4
↓
Extract frames every 1 second
↓
Frame 0    Frame 30   Frame 60   Frame 90
  |          |          |          |
Save as: frame_0000.jpg, frame_0030.jpg, ...
```

### Motion Detection Pipeline

```
Frame N                 Frame N+1
  |                        |
  └────── Difference ──────┘
            |
     Threshold (> 25)
            |
     Count pixels
            |
  Motion Score: 0.0-1.0
```

### Engagement Calculation

```
Engagement Score = weighted_sum(
    motion_score    * 0.4,    # Movement is engaging
    scene_changes   * 0.3,    # New scenes are interesting
    face_presence   * 0.3     # People are engaging
)
```

---

## 💻 Starter Code

See `starter-code/week4_starter/visual_analyzer.py`

### Key Functions to Implement

```python
def extract_frames(video_path: str, sample_rate: float = 1.0) -> List[np.ndarray]:
    """
    Extract frames from video.

    Args:
        video_path: Path to video file
        sample_rate: Frames per second to extract

    Returns:
        List of frame images (numpy arrays)
    """
    # TODO: Use OpenCV to read video and extract frames
    pass

def calculate_motion(frame1: np.ndarray, frame2: np.ndarray) -> float:
    """
    Calculate motion between two frames.

    Args:
        frame1, frame2: Consecutive frames

    Returns:
        Motion score (0.0 = no motion, 1.0 = high motion)
    """
    # TODO:
    # 1. Convert to grayscale
    # 2. Calculate absolute difference
    # 3. Apply threshold
    # 4. Count non-zero pixels
    # 5. Normalize by total pixels
    pass

def detect_scene_change(frame1: np.ndarray, frame2: np.ndarray,
                       threshold: float = 0.7) -> bool:
    """
    Detect if scene changed between frames.

    Args:
        frame1, frame2: Consecutive frames
        threshold: Similarity threshold

    Returns:
        True if scene changed
    """
    # TODO:
    # 1. Calculate histograms for each channel
    # 2. Compare using chi-square or correlation
    # 3. Return True if difference > threshold
    pass
```

---

## ✏️ Exercises

### Exercise 1: Frame Extraction
```python
# Extract 1 frame per second from a video
frames = extract_frames("video.mp4", sample_rate=1.0)
print(f"Extracted {len(frames)} frames")

# Save first frame
cv2.imwrite("first_frame.jpg", frames[0])
```

### Exercise 2: Motion Detection
```python
# Calculate motion between consecutive frames
for i in range(len(frames) - 1):
    motion = calculate_motion(frames[i], frames[i+1])
    print(f"Motion between frame {i} and {i+1}: {motion:.3f}")
```

### Exercise 3: Scene Changes
```python
# Detect all scene changes
scene_changes = []
for i in range(len(frames) - 1):
    if detect_scene_change(frames[i], frames[i+1]):
        scene_changes.append(i)
        print(f"Scene change detected at frame {i}")
```

---

## 🎯 Implementation Tasks

### Beginner Tasks
1. ✅ Install OpenCV: `pip install opencv-python`
2. ✅ Load video and get frame count
3. ✅ Extract single frame
4. ✅ Convert frame to grayscale
5. ✅ Calculate frame difference

### Intermediate Tasks
6. ✅ Extract frames at specific intervals
7. ✅ Implement motion detection
8. ✅ Implement scene change detection
9. ✅ Calculate engagement scores
10. ✅ Visualize motion over time

### Advanced Tasks
11. ✅ Add face detection
12. ✅ Implement optical flow (advanced motion)
13. ✅ Detect camera movements (pan, zoom)
14. ✅ Create video timeline visualization

---

## 📊 Understanding the Code

### OpenCV Basics

```python
import cv2
import numpy as np

# Read video
cap = cv2.VideoCapture("video.mp4")

# Get properties
fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

print(f"Video: {duration:.1f}s, {fps} fps, {frame_count} frames")

# Read a frame
ret, frame = cap.read()  # ret = success boolean, frame = image
if ret:
    print(f"Frame shape: {frame.shape}")  # (height, width, channels)

# Always release
cap.release()
```

### Frame Differencing

```python
# Convert to grayscale
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

# Calculate absolute difference
diff = cv2.absdiff(gray1, gray2)

# Apply threshold (values > 25 are motion)
_, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

# Count motion pixels
motion_pixels = np.count_nonzero(thresh)
total_pixels = thresh.shape[0] * thresh.shape[1]

# Motion score
motion_score = motion_pixels / total_pixels
```

### Histogram Comparison

```python
# Calculate histogram for each channel
hist1_b = cv2.calcHist([frame1], [0], None, [256], [0, 256])
hist1_g = cv2.calcHist([frame1], [1], None, [256], [0, 256])
hist1_r = cv2.calcHist([frame1], [2], None, [256], [0, 256])

hist2_b = cv2.calcHist([frame2], [0], None, [256], [0, 256])
hist2_g = cv2.calcHist([frame2], [1], None, [256], [0, 256])
hist2_r = cv2.calcHist([frame2], [2], None, [256], [0, 256])

# Compare using correlation (returns 0-1, where 1 = identical)
corr_b = cv2.compareHist(hist1_b, hist2_b, cv2.HISTCMP_CORREL)
corr_g = cv2.compareHist(hist1_g, hist2_g, cv2.HISTCMP_CORREL)
corr_r = cv2.compareHist(hist1_r, hist2_r, cv2.HISTCMP_CORREL)

# Average correlation
avg_corr = (corr_b + corr_g + corr_r) / 3

# If correlation < 0.7, scenes are different
if avg_corr < 0.7:
    print("Scene change detected!")
```

---

## 🐛 Common Issues

### Issue 1: "ModuleNotFoundError: No module named 'cv2'"
```bash
# Solution: Install OpenCV
pip install opencv-python
```

### Issue 2: "Video file not found"
```python
# Solution: Check file path
import os
print(os.path.exists("video.mp4"))  # Should print True

# Use absolute path if needed
video_path = os.path.abspath("video.mp4")
```

### Issue 3: "cap.read() returns False"
```python
# Solution: Check if video opened successfully
cap = cv2.VideoCapture("video.mp4")
if not cap.isOpened():
    print("Error: Could not open video")
else:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
```

### Issue 4: High memory usage
```python
# Solution: Don't load all frames at once
# Process frames one by one

cap = cv2.VideoCapture("video.mp4")
prev_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if prev_frame is not None:
        motion = calculate_motion(prev_frame, frame)
        # Process motion score

    prev_frame = frame

cap.release()
```

---

## 📈 Testing Your Code

```python
# Test with sample video
def test_visual_analyzer():
    analyzer = VisualAnalyzer()

    # Test frame extraction
    frames = analyzer.extract_frames("sample_video.mp4", sample_rate=1.0)
    assert len(frames) > 0, "No frames extracted"
    print(f"✓ Extracted {len(frames)} frames")

    # Test motion detection
    if len(frames) >= 2:
        motion = analyzer.calculate_motion(frames[0], frames[1])
        assert 0.0 <= motion <= 1.0, "Motion score out of range"
        print(f"✓ Motion detection works: {motion:.3f}")

    # Test scene detection
    scene_change = analyzer.detect_scene_change(frames[0], frames[-1])
    print(f"✓ Scene detection works: {scene_change}")

    print("\nAll tests passed!")

if __name__ == '__main__':
    test_visual_analyzer()
```

---

## 🎓 What You'll Learn

After this week, you will understand:
- How video is stored as frame sequences
- How to process images with OpenCV
- Motion detection algorithms
- Scene segmentation techniques
- Visual feature extraction

**These skills apply to**:
- Video surveillance systems
- Action recognition
- Video summarization
- Sports analytics
- Content moderation

---

## 📚 Additional Resources

- [OpenCV Python Tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Image Processing Basics](https://www.pyimagesearch.com/)
- [Computer Vision Fundamentals](https://opencv.org/)

---

**Next**: [Week 5 - Multimodal Fusion](week5_fusion.md)
