#!/bin/bash
# Deploy to AWS Lambda

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
FUNCTION_NAME=${FUNCTION_NAME:-clip-extractor}
MEMORY_SIZE=${MEMORY_SIZE:-3008}
TIMEOUT=${TIMEOUT:-900}
ECR_REPO_NAME=${ECR_REPO_NAME:-clip-extractor}

echo "Deploying Clip Extractor to AWS Lambda..."
echo "Region: $AWS_REGION"
echo "Function: $FUNCTION_NAME"

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME"

echo "ECR URI: $ECR_URI"

# Create ECR repository if it doesn't exist
echo "Creating ECR repository..."
aws ecr create-repository \
    --repository-name $ECR_REPO_NAME \
    --region $AWS_REGION \
    2>/dev/null || echo "Repository already exists"

# Login to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $ECR_URI

# Build Docker image
echo "Building Docker image..."
cd ../..
docker build -f deployment/aws/Dockerfile.lambda -t $ECR_REPO_NAME:latest .

# Tag image
docker tag $ECR_REPO_NAME:latest $ECR_URI:latest

# Push to ECR
echo "Pushing image to ECR..."
docker push $ECR_URI:latest

# Create or update Lambda function
echo "Creating/updating Lambda function..."

# Check if function exists
if aws lambda get-function --function-name $FUNCTION_NAME --region $AWS_REGION 2>/dev/null; then
    echo "Updating existing function..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --image-uri $ECR_URI:latest \
        --region $AWS_REGION

    aws lambda update-function-configuration \
        --function-name $FUNCTION_NAME \
        --timeout $TIMEOUT \
        --memory-size $MEMORY_SIZE \
        --region $AWS_REGION
else
    echo "Creating new function..."

    # Create execution role if needed
    ROLE_NAME="${FUNCTION_NAME}-role"
    ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text 2>/dev/null || echo "")

    if [ -z "$ROLE_ARN" ]; then
        echo "Creating IAM role..."
        aws iam create-role \
            --role-name $ROLE_NAME \
            --assume-role-policy-document '{
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }]
            }'

        # Attach policies
        aws iam attach-role-policy \
            --role-name $ROLE_NAME \
            --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

        aws iam attach-role-policy \
            --role-name $ROLE_NAME \
            --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

        ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text)

        echo "Waiting for role to propagate..."
        sleep 10
    fi

    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --package-type Image \
        --code ImageUri=$ECR_URI:latest \
        --role $ROLE_ARN \
        --timeout $TIMEOUT \
        --memory-size $MEMORY_SIZE \
        --region $AWS_REGION
fi

echo "✓ Deployment complete!"
echo ""
echo "Test your function:"
echo "aws lambda invoke --function-name $FUNCTION_NAME --payload '{\"bucket\":\"my-bucket\",\"key\":\"video.mp4\"}' output.json"
