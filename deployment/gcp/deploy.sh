#!/bin/bash
# Deploy to Google Cloud Run

set -e

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-$(gcloud config get-value project)}
REGION=${GCP_REGION:-us-central1}
SERVICE_NAME=${SERVICE_NAME:-clip-extractor}
MEMORY=${MEMORY:-4Gi}
TIMEOUT=${TIMEOUT:-900}
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "Deploying Clip Extractor to Google Cloud Run..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com

# Build and push image
echo "Building Docker image..."
cd ../..
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --memory $MEMORY \
    --timeout $TIMEOUT \
    --max-instances 10 \
    --no-allow-unauthenticated

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo "✓ Deployment complete!"
echo ""
echo "Service URL: $SERVICE_URL"
echo ""
echo "Test your service:"
echo "curl -X POST $SERVICE_URL -H \"Authorization: Bearer \$(gcloud auth print-identity-token)\" -H \"Content-Type: application/json\" -d '{\"bucket\":\"my-bucket\",\"key\":\"video.mp4\"}'"
