# Installation Guide

Complete installation instructions for the Multimodal Clip Extractor.

## Prerequisites

- Python 3.8 or higher
- FFmpeg 4.0 or higher
- 4GB RAM minimum (8GB recommended)
- No GPU required (CPU-optimized)

## Quick Install (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/asquitt/super-duper-octo-broccoli.git
cd super-duper-octo-broccoli
```

### 2. Install FFmpeg

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### macOS

```bash
brew install ffmpeg
```

#### Windows

Download from https://ffmpeg.org/download.html and add to PATH.

### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Python Dependencies

#### Minimal Installation (Recommended for testing)

```bash
pip install -r requirements-minimal.txt
```

#### Full Installation

```bash
pip install -r requirements.txt
```

### 5. Verify Installation

```bash
python main.py --help
```

## Docker Installation

### Build Docker Image

```bash
docker build -t clip-extractor .
```

### Run with Docker

```bash
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  clip-extractor --input /input/video.mp4 --output /output/clips.json
```

### Use Docker Compose

```bash
docker-compose up
```

## Cloud Deployment

### AWS Lambda

```bash
cd deployment/aws
chmod +x deploy.sh
./deploy.sh
```

Requirements:
- AWS CLI configured
- Docker installed
- IAM permissions for Lambda, ECR, and S3

### Google Cloud Run

```bash
cd deployment/gcp
chmod +x deploy.sh
./deploy.sh
```

Requirements:
- gcloud CLI configured
- Docker installed
- GCP project with billing enabled

### Azure Container Instances

```bash
cd deployment/azure
chmod +x deploy.sh
./deploy.sh
```

Requirements:
- Azure CLI configured
- Docker installed
- Azure subscription

## Troubleshooting

### FFmpeg Not Found

Ensure FFmpeg is installed and in your PATH:

```bash
ffmpeg -version
```

### Out of Memory

Reduce processing load by disabling some modalities:

```bash
python main.py --input video.mp4 --no-visual
```

Or increase Docker memory limits in docker-compose.yml.

### Model Download Issues

Models are downloaded automatically on first run. Ensure you have internet connectivity.

To pre-download models:

```python
from transformers import AutoModel, AutoTokenizer
model = AutoModel.from_pretrained('distilbert-base-uncased')
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
```

### Slow Processing

Processing time is typically 1-2x real-time on modern CPUs. To speed up:

1. Reduce sampling rate in config.yaml
2. Use audio-only analysis (--no-visual)
3. Use shorter input files for testing
4. Deploy to cloud with more CPU cores

## Development Setup

For development and testing:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Format code
black src/

# Type checking
mypy src/
```

## Uninstallation

```bash
# Remove virtual environment
deactivate
rm -rf venv/

# Remove Docker images
docker rmi clip-extractor

# Remove temporary files
rm -rf temp/ cache/ output/
```

## Getting Help

- GitHub Issues: https://github.com/asquitt/super-duper-octo-broccoli/issues
- Documentation: See README.md
- Examples: See examples/ directory
