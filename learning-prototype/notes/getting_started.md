# Getting Started with the Learning Prototype

Welcome! This guide will help you begin your journey to building a multimodal AI system.

---

## 🎯 Your Learning Journey

You'll build the system **step by step** over 8 weeks, learning:
- Audio signal processing
- Natural language processing
- Computer vision
- Machine learning
- System architecture

**No prior AI experience needed!** We start from the basics.

---

## 📋 Prerequisites

### What You Need:

✅ **Python 3.8+** - Download from python.org
✅ **FFmpeg** - Media processing tool
✅ **4GB RAM** - Minimum (8GB recommended)
✅ **Text Editor** - VS Code, PyCharm, or any editor
✅ **Curiosity** - Willingness to learn!

### What You DON'T Need:

❌ GPU - Everything runs on CPU
❌ Prior AI knowledge - We teach you!
❌ Expensive tools - Everything is free/open-source

---

## 🚀 Quick Start (5 minutes)

### Step 1: Setup Environment

```bash
# Navigate to learning prototype
cd learning-prototype

# Run setup script
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh

# Activate virtual environment
source venv/bin/activate
```

This will:
- Create a Python virtual environment
- Install required packages
- Generate sample test files
- Set up project structure

### Step 2: Start Week 1

```bash
# Read the curriculum
cat curriculum/week1_foundations.md

# Go to starter code
cd starter-code/week1_starter

# Open in your editor
code media_processor_starter.py  # or use your editor
```

### Step 3: Start Coding!

1. Read the instructions in the file
2. Fill in the `TODO` sections
3. Run the tests: `python media_processor_starter.py`
4. Compare with solution when done

---

## 📚 How to Use This Learning Path

### Weekly Workflow:

```
Monday-Tuesday:     Read curriculum, understand concepts
Wednesday-Thursday: Complete exercises, implement code
Friday:            Test your implementation
Weekend:           Review, compare with solution, prepare for next week
```

### For Each Week:

1. **📖 Read Curriculum** (`curriculum/weekN_*.md`)
   - Understand the goals
   - Review key concepts
   - Check prerequisites

2. **💻 Review Starter Code** (`starter-code/weekN_starter/`)
   - Read the structure
   - Understand what to build
   - Note the TODOs

3. **✏️ Complete Exercises**
   - Hands-on practice
   - Test understanding
   - Build components

4. **🔨 Implement Solution**
   - Fill in starter code
   - Run tests frequently
   - Debug and iterate

5. **✅ Validate**
   - Run test suite
   - Compare with solution
   - Understand differences

6. **📝 Take Notes** (`notes/`)
   - Document learnings
   - Save examples
   - Note gotchas

---

## 🎓 Learning Tips

### For Beginners:

1. **Take Your Time** - Don't rush
2. **Type Code** - Don't just copy-paste
3. **Experiment** - Try different values
4. **Ask Questions** - Use comments to document
5. **Review Often** - Revisit previous weeks

### For Experienced Programmers:

1. **Read Theory** - Understand the "why"
2. **Try Optimizations** - Make it faster
3. **Add Features** - Extend functionality
4. **Refactor** - Improve code quality
5. **Challenge Yourself** - Skip to harder exercises

### General Tips:

```python
# Good: Understand before implementing
def extract_audio(video_path):
    """I understand this extracts audio from video using FFmpeg"""
    # Implementation...

# Bad: Copy without understanding
def extract_audio(video_path):
    # Some code I copied
```

**Learning > Completing**

---

## 🐛 Debugging Guide

### Common Issues:

**1. "ModuleNotFoundError: No module named 'librosa'"**
```bash
# Solution: Install dependencies
source venv/bin/activate
pip install -r requirements-learning.txt
```

**2. "FFmpeg command not found"**
```bash
# Solution: Install FFmpeg
# Ubuntu: sudo apt-get install ffmpeg
# macOS: brew install ffmpeg
# Windows: Download from ffmpeg.org
```

**3. "File not found" errors**
```bash
# Solution: Check your paths
# Use absolute paths or check current directory
import os
print(os.getcwd())  # Where am I?
print(os.listdir('.'))  # What's here?
```

**4. Code runs but wrong output**
```python
# Solution: Add debug prints
def my_function(x):
    print(f"DEBUG: Input x = {x}")  # See what's coming in
    result = x * 2
    print(f"DEBUG: Result = {result}")  # See what's going out
    return result
```

---

## 📂 Project Structure

```
learning-prototype/
│
├── curriculum/          # What to learn each week
│   ├── week1_foundations.md
│   ├── week2_audio.md
│   └── ...
│
├── starter-code/        # Code templates to fill in
│   ├── week1_starter/
│   ├── week2_starter/
│   └── ...
│
├── solutions/           # Complete solutions (check after trying!)
│   ├── week1_solution/
│   └── ...
│
├── exercises/           # Practice exercises
│   ├── exercise1_audio.py
│   └── ...
│
├── notes/              # Learning resources
│   ├── audio_processing_101.md
│   ├── nlp_basics.md
│   └── ...
│
├── sample_data/        # Test files (generated)
│   ├── sample_audio.wav
│   ├── sample_video.mp4
│   └── sample_transcript.txt
│
├── my_solutions/       # YOUR work goes here
│   ├── week1/
│   ├── week2/
│   └── ...
│
└── outputs/            # Test outputs
```

---

## 🎯 What You'll Build

### Week 1: Media Processor
Extract audio from video, get metadata

### Week 2: Emotion Detector
Analyze audio for emotional moments

### Week 3: Topic Analyzer
Find important topics in text

### Week 4: Visual Tracker
Detect movement and changes in video

### Week 5: Fusion Engine
Combine all signals intelligently

### Week 6: Output Generator
Create clips and titles

### Week 7: Testing Suite
Validate and optimize

### Week 8: Deployment
Package and deploy

**Final Result**: Complete AI system that finds video highlights!

---

## 💡 Success Strategies

### 1. Set a Schedule

```
Mon/Wed/Fri: 1-2 hours coding
Tue/Thu: 30 min reading/planning
Weekend: Review and catch up
```

### 2. Track Progress

Create a checklist:
- [ ] Week 1 curriculum read
- [ ] Week 1 exercises done
- [ ] Week 1 tests passing
- [ ] Week 1 solution compared

### 3. Build Portfolio

- Save your code to GitHub
- Document your learnings
- Create a blog post
- Show friends/colleagues

### 4. Get Help

- Check solutions folder
- Review main project code
- Read the notes
- Search online for concepts

---

## 🎊 Ready to Start?

### Your First Task:

```bash
# 1. Run setup
./scripts/setup_environment.sh

# 2. Read Week 1
cat curriculum/week1_foundations.md

# 3. Start coding!
cd starter-code/week1_starter
python media_processor_starter.py
```

---

## 📞 Need Help?

- **Stuck on code?** Check the solution
- **Don't understand concept?** Read notes
- **Want to see it working?** Check main project
- **Tests failing?** Read error messages carefully

---

**Let's build something amazing!** 🚀

**Next Step**: [Week 1: Foundations](curriculum/week1_foundations.md)
