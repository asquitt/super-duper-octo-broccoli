#!/bin/bash
# Setup Script for Learning Prototype
# This installs all dependencies and prepares the environment

set -e

echo "=========================================="
echo "Multimodal Clip Extractor - Setup"
echo "Learning Prototype Environment"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python
echo -n "Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check FFmpeg
echo -n "Checking FFmpeg... "
if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}✓ Found FFmpeg${NC}"
else
    echo -e "${YELLOW}⚠ FFmpeg not found${NC}"
    echo ""
    echo "Please install FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org"
    echo ""
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install minimal dependencies
echo ""
echo "Installing dependencies..."
cat > requirements-learning.txt << EOF
# Minimal dependencies for learning prototype
numpy>=1.21.0
scipy>=1.7.0

# Audio processing
librosa>=0.9.0
soundfile>=0.11.0

# Video processing
opencv-python>=4.5.0

# Text processing (optional - start without)
# transformers>=4.30.0
# torch>=2.0.0

# Utilities
pyyaml>=6.0
matplotlib>=3.5.0  # For visualization
EOF

pip install --quiet -r requirements-learning.txt

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create project structure
echo ""
echo "Creating project structure..."

mkdir -p sample_data
mkdir -p outputs
mkdir -p my_solutions/{week1,week2,week3,week4,week5,week6,week7,week8}

# Generate sample test data
echo ""
echo "Generating sample test data..."

# Sample audio
if command -v ffmpeg &> /dev/null; then
    ffmpeg -f lavfi -i "sine=frequency=440:duration=10" \
           -ar 22050 -ac 1 -y sample_data/sample_audio.wav &>/dev/null
    echo -e "${GREEN}✓ Generated sample_audio.wav${NC}"

    ffmpeg -f lavfi -i "testsrc=duration=10:size=640x480:rate=30" \
           -f lavfi -i "sine=frequency=1000:duration=10" \
           -pix_fmt yuv420p -y sample_data/sample_video.mp4 &>/dev/null
    echo -e "${GREEN}✓ Generated sample_video.mp4${NC}"
fi

# Sample transcript
cat > sample_data/sample_transcript.txt << 'EOF'
Welcome to this amazing presentation about artificial intelligence.
Today we're going to explore some groundbreaking concepts.
First, let's talk about machine learning and how it works.
Machine learning is a subset of AI that learns from data.
Now here's the really exciting part about neural networks.
Neural networks are inspired by the human brain.
You might be wondering, how do neural networks learn?
They learn by adjusting weights based on errors.
This is absolutely revolutionary for technology.
Let me show you a real example of this in action.
EOF

echo -e "${GREEN}✓ Generated sample_transcript.txt${NC}"

# Create welcome message
echo ""
echo "=========================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Your learning environment is ready!"
echo ""
echo "Getting Started:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Go to Week 1: cd curriculum && cat week1_foundations.md"
echo "  3. Start coding: cd ../starter-code/week1_starter"
echo ""
echo "Sample Data:"
echo "  - sample_data/sample_audio.wav (10s audio)"
echo "  - sample_data/sample_video.mp4 (10s video)"
echo "  - sample_data/sample_transcript.txt"
echo ""
echo "Your Work:"
echo "  - Save your solutions in: my_solutions/weekN/"
echo "  - Test outputs go in: outputs/"
echo ""
echo "Happy learning! 🚀"
echo ""
