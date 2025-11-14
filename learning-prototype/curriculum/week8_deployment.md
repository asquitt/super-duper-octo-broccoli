# Week 8: Deployment & Distribution

**Goal**: Package your system for deployment and share it with the world.

---

## 📚 Learning Objectives

By the end of this week, you will:
- ✅ Create a Docker container
- ✅ Write deployment scripts
- ✅ Set up cloud deployment (optional)
- ✅ Create user documentation
- ✅ Build a demo

---

## 🎯 What We're Building This Week

Deployment infrastructure:
1. Dockerfile for containerization
2. docker-compose for local deployment
3. Cloud deployment scripts (AWS/GCP/Azure)
4. User documentation
5. Demo/showcase

---

## 📖 Key Concepts

### 1. Containerization with Docker

**Why Docker?**
- Consistent environment everywhere
- Easy to share and deploy
- Isolates dependencies
- Works on any platform

**Docker Basics**:
```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY src/ /app/src/
WORKDIR /app

# Run application
CMD ["python", "main.py"]
```

### 2. Deployment Options

```
Local:
- Run directly on machine
- Good for: Development, personal use

Docker:
- Containerized application
- Good for: Consistent deployment, sharing

Cloud:
- AWS Lambda, Google Cloud Run, Azure Functions
- Good for: Scalability, production use

Serverless:
- Function-as-a-Service (FaaS)
- Good for: Event-driven, pay-per-use
```

### 3. Configuration Management

**Environment Variables**:
```bash
# .env file
VIDEO_INPUT_PATH=/data/videos
OUTPUT_PATH=/data/outputs
NUM_CLIPS=5
CLIP_LENGTH=30
```

**Config Files**:
```yaml
# config.yaml
processing:
  num_clips: 5
  clip_length: 30.0
  min_score: 0.6

weights:
  audio: 0.4
  text: 0.3
  visual: 0.3

output:
  format: json
  create_html: true
```

---

## 💻 Starter Code

See `starter-code/week8_starter/`

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY main.py .

# Create directories for data
RUN mkdir -p /data/input /data/output

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run application
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  clip-extractor:
    build: .
    image: multimodal-clip-extractor:latest
    volumes:
      - ./data:/data
      - ./config:/config
    environment:
      - CONFIG_PATH=/config/config.yaml
    command: >
      --input /data/input/video.mp4
      --output /data/output/clips.json
      --num-clips 5
```

### Deploy Script

```bash
#!/bin/bash
# deploy.sh - Deploy to cloud

echo "Deploying Multimodal Clip Extractor..."

# Build Docker image
echo "Building Docker image..."
docker build -t clip-extractor:latest .

# Tag for registry
docker tag clip-extractor:latest myregistry/clip-extractor:latest

# Push to registry
echo "Pushing to registry..."
docker push myregistry/clip-extractor:latest

# Deploy to cloud (example: AWS)
echo "Deploying to cloud..."
# Add cloud-specific deployment commands here

echo "✓ Deployment complete!"
```

---

## ✏️ Exercises

### Exercise 1: Build Docker Image

```bash
# Build the image
docker build -t clip-extractor .

# Run container
docker run -v $(pwd)/data:/data clip-extractor \
    --input /data/video.mp4 \
    --output /data/clips.json

# Check output
ls data/clips.json
```

### Exercise 2: Docker Compose

```bash
# Create docker-compose.yml (see above)

# Start services
docker-compose up

# Run in detached mode
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Exercise 3: Cloud Deployment (AWS Example)

```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure

# Create ECR repository
aws ecr create-repository --repository-name clip-extractor

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin \
    <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag clip-extractor:latest \
    <account-id>.dkr.ecr.us-east-1.amazonaws.com/clip-extractor:latest

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/clip-extractor:latest

# Deploy to ECS/Lambda/etc.
# (Use AWS console or CloudFormation)
```

---

## 🎯 Implementation Tasks

### Beginner
1. ✅ Install Docker
2. ✅ Create basic Dockerfile
3. ✅ Build Docker image
4. ✅ Run container locally
5. ✅ Write user documentation

### Intermediate
6. ✅ Create docker-compose.yml
7. ✅ Add environment variables
8. ✅ Create deployment script
9. ✅ Set up volumes for data
10. ✅ Add health checks

### Advanced
11. ✅ Deploy to cloud (AWS/GCP/Azure)
12. ✅ Set up CI/CD pipeline
13. ✅ Add monitoring/logging
14. ✅ Implement auto-scaling
15. ✅ Create Kubernetes deployment

---

## 📦 Distribution

### PyPI Package (Optional)

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name='multimodal-clip-extractor',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'librosa>=0.9.0',
        'opencv-python>=4.5.0',
        'transformers>=4.30.0',
    ],
    entry_points={
        'console_scripts': [
            'clip-extractor=src.main:main',
        ],
    },
    author='Your Name',
    description='Extract engaging clips from long videos',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/clip-extractor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
```

### Installation

```bash
# Install from source
pip install -e .

# Or build distribution
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*
```

---

## 📚 Documentation

### README.md

```markdown
# Multimodal Clip Extractor

Extract engaging 30-60 second clips from long videos using AI.

## Features

- 🎵 Audio emotion detection
- 📝 Text topic analysis
- 🎬 Visual engagement detection
- 🤖 Multimodal fusion
- ⚡ CPU-optimized (no GPU needed)

## Quick Start

### Docker (Recommended)

\`\`\`bash
docker run -v $(pwd)/data:/data clip-extractor \
    --input /data/video.mp4 \
    --output /data/clips.json
\`\`\`

### Local Installation

\`\`\`bash
pip install multimodal-clip-extractor
clip-extractor --input video.mp4
\`\`\`

## Usage

\`\`\`bash
# Basic usage
clip-extractor --input lecture.mp4

# With transcript
clip-extractor --input video.mp4 --transcript transcript.txt

# Custom settings
clip-extractor --input video.mp4 --num-clips 10 --clip-length 45
\`\`\`

## Documentation

See [docs/](docs/) for detailed documentation.

## License

MIT License
```

### User Guide

Create `docs/USER_GUIDE.md` with:
- Installation instructions
- Usage examples
- Configuration options
- Troubleshooting
- FAQ

---

## 🐛 Common Issues

### Issue 1: Large Docker images
```dockerfile
# Problem: Image is 2GB+

# Solution: Use slim base, multi-stage build
FROM python:3.9-slim as builder
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
# Result: 500MB image
```

### Issue 2: Permission issues in Docker
```dockerfile
# Problem: Files created by container are owned by root

# Solution: Run as non-root user
RUN useradd -m appuser
USER appuser
```

### Issue 3: Slow builds
```dockerfile
# Problem: Rebuilds install all packages every time

# Solution: Copy requirements first
COPY requirements.txt .
RUN pip install -r requirements.txt
# These layers are cached

COPY src/ ./src/
# Only this rebuilds when code changes
```

---

## 🚀 Production Checklist

### Before Deployment:
- [ ] All tests pass
- [ ] Security vulnerabilities checked
- [ ] Documentation complete
- [ ] Environment variables configured
- [ ] Logging set up
- [ ] Error handling robust
- [ ] Performance tested
- [ ] Docker image optimized

### After Deployment:
- [ ] Monitor logs
- [ ] Check performance metrics
- [ ] Set up alerts
- [ ] Document runbook
- [ ] Plan rollback strategy

---

## 📊 Monitoring

```python
# Add logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def process_video(video_path):
    logger.info(f"Processing video: {video_path}")

    try:
        clips = extract_clips(video_path)
        logger.info(f"Extracted {len(clips)} clips")
        return clips
    except Exception as e:
        logger.error(f"Failed to process video: {e}", exc_info=True)
        raise
```

---

## 🎓 What You'll Learn

- Docker containerization
- Cloud deployment
- DevOps practices
- Configuration management
- Production-ready systems

**These skills apply to**:
- Deploying any application
- MLOps and ML deployment
- Cloud engineering
- Site reliability engineering (SRE)
- Full-stack development

---

## 💡 Next Steps

After Week 8, you can:

1. **Deploy to Production**
   - Set up cloud infrastructure
   - Add monitoring and alerts
   - Implement CI/CD

2. **Extend Functionality**
   - Add more modalities (subtitle analysis, etc.)
   - Fine-tune ML models
   - Add batch processing

3. **Build Your Own Project**
   - Apply to your domain
   - Customize for specific use cases
   - Share with community

4. **Contribute**
   - Add features to main project
   - Help other learners
   - Create tutorials

---

## 🎊 Congratulations!

You've completed the 8-week learning path! You now have:

✅ A complete multimodal AI system
✅ Deep understanding of audio, text, and visual processing
✅ Production-ready deployment skills
✅ A portfolio project to showcase

**You're ready to build AI systems!** 🚀

---

## 📞 Resources

- Docker Documentation: https://docs.docker.com
- AWS Documentation: https://docs.aws.amazon.com
- Kubernetes Tutorial: https://kubernetes.io/docs/tutorials/

---

**Congratulations on completing the course!** 🎓

Now go build amazing things! 🌟
