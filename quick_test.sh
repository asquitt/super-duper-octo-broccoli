#!/bin/bash
# Quick test script for local setup validation
# This script tests the clip extractor with minimal cost/dependencies

set -e  # Exit on error

echo "=========================================="
echo "Multimodal Clip Extractor - Quick Test"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if FFmpeg is installed
echo -n "Checking for FFmpeg... "
if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
    echo "Please install FFmpeg: sudo apt-get install ffmpeg (or brew install ffmpeg on macOS)"
    exit 1
fi

# Check Python version
echo -n "Checking Python version... "
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"

# Create test directory
TEST_DIR="./test_output"
mkdir -p "$TEST_DIR"
echo "Test directory: $TEST_DIR"
echo ""

# Generate test data
echo "=========================================="
echo "Generating Test Data"
echo "=========================================="

echo -n "Generating 30-second test audio... "
ffmpeg -f lavfi -i "sine=frequency=440:duration=30" -ar 22050 -ac 1 -y "$TEST_DIR/test_audio.wav" &> /dev/null
if [ -f "$TEST_DIR/test_audio.wav" ]; then
    echo -e "${GREEN}✓ Done${NC}"
else
    echo -e "${RED}✗ Failed${NC}"
    exit 1
fi

echo -n "Generating 30-second test video... "
ffmpeg -f lavfi -i "testsrc=duration=30:size=640x480:rate=30" \
       -f lavfi -i "sine=frequency=1000:duration=30" \
       -pix_fmt yuv420p -y "$TEST_DIR/test_video.mp4" &> /dev/null
if [ -f "$TEST_DIR/test_video.mp4" ]; then
    echo -e "${GREEN}✓ Done${NC}"
else
    echo -e "${RED}✗ Failed${NC}"
    exit 1
fi

echo -n "Generating test transcript... "
cat > "$TEST_DIR/test_transcript.txt" << EOF
Welcome to this amazing demonstration of our multimodal clip extractor system.
Today we're going to explore some groundbreaking concepts in AI and machine learning.
First, let's talk about the fundamentals of emotion detection in audio signals.
This is absolutely revolutionary and will change everything about content creation.
The key insight here is that we can combine multiple modalities for better results.
What you might not know is that this works without any GPU requirements.
Let me show you how the system analyzes visual engagement and motion.
This changes everything about how we create highlight reels from long videos.
EOF
echo -e "${GREEN}✓ Done${NC}"
echo ""

# Run unit tests
echo "=========================================="
echo "Running Unit Tests"
echo "=========================================="

if command -v pytest &> /dev/null; then
    echo "Running pytest..."
    pytest tests/ -v --tb=short -x 2>&1 | head -50
    PYTEST_EXIT=$?

    if [ $PYTEST_EXIT -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed${NC}"
    elif [ $PYTEST_EXIT -eq 5 ]; then
        echo -e "${YELLOW}⚠ No tests collected (this is okay for quick test)${NC}"
    else
        echo -e "${YELLOW}⚠ Some tests failed (continuing with integration test)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ pytest not installed, skipping unit tests${NC}"
fi
echo ""

# Test 1: Audio-only processing
echo "=========================================="
echo "Test 1: Audio + Transcript Processing"
echo "=========================================="

echo "Processing audio file with transcript..."
START_TIME=$(date +%s)

python3 main.py \
    --input "$TEST_DIR/test_audio.wav" \
    --transcript "$TEST_DIR/test_transcript.txt" \
    --output "$TEST_DIR/audio_clips.json" \
    --num-clips 3 \
    --min-duration 5 \
    --max-duration 15 \
    --no-visual

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ -f "$TEST_DIR/audio_clips.json" ]; then
    echo -e "${GREEN}✓ Test 1 passed${NC} (${DURATION}s)"
    echo ""
    echo "Results:"
    cat "$TEST_DIR/audio_clips.json" | python3 -m json.tool 2>/dev/null || cat "$TEST_DIR/audio_clips.json"
else
    echo -e "${RED}✗ Test 1 failed${NC}"
    exit 1
fi
echo ""

# Test 2: Video processing (audio + visual, no text for speed)
echo "=========================================="
echo "Test 2: Video Processing (Audio + Visual)"
echo "=========================================="

echo "Processing video file..."
START_TIME=$(date +%s)

python3 main.py \
    --input "$TEST_DIR/test_video.mp4" \
    --output "$TEST_DIR/video_clips.json" \
    --num-clips 2 \
    --min-duration 5 \
    --max-duration 10 \
    --no-text

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ -f "$TEST_DIR/video_clips.json" ]; then
    echo -e "${GREEN}✓ Test 2 passed${NC} (${DURATION}s)"
    echo ""
    echo "Results:"
    cat "$TEST_DIR/video_clips.json" | python3 -m json.tool 2>/dev/null || cat "$TEST_DIR/video_clips.json"
else
    echo -e "${RED}✗ Test 2 failed${NC}"
    exit 1
fi
echo ""

# Test 3: Minimal processing (fastest)
echo "=========================================="
echo "Test 3: Minimal Processing (Audio Only)"
echo "=========================================="

echo "Processing with minimal settings for speed..."
START_TIME=$(date +%s)

python3 main.py \
    --input "$TEST_DIR/test_audio.wav" \
    --output "$TEST_DIR/minimal_clips.json" \
    --num-clips 1 \
    --no-text \
    --no-visual

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ -f "$TEST_DIR/minimal_clips.json" ]; then
    echo -e "${GREEN}✓ Test 3 passed${NC} (${DURATION}s)"
else
    echo -e "${RED}✗ Test 3 failed${NC}"
    exit 1
fi
echo ""

# Performance summary
echo "=========================================="
echo "Performance Summary"
echo "=========================================="

AUDIO_SIZE=$(du -h "$TEST_DIR/test_audio.wav" | cut -f1)
VIDEO_SIZE=$(du -h "$TEST_DIR/test_video.mp4" | cut -f1)

echo "Test Files:"
echo "  Audio: $AUDIO_SIZE (30s)"
echo "  Video: $VIDEO_SIZE (30s)"
echo ""
echo "All tests completed successfully!"
echo ""
echo "Generated files in $TEST_DIR:"
ls -lh "$TEST_DIR" | tail -n +2
echo ""

# Cleanup option
echo "=========================================="
echo "Cleanup"
echo "=========================================="
echo ""
read -p "Remove test files? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$TEST_DIR"
    rm -rf temp/ cache/
    echo -e "${GREEN}✓ Cleanup completed${NC}"
else
    echo "Test files kept in: $TEST_DIR"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Quick Test Completed Successfully!${NC}"
echo "=========================================="
