#!/bin/bash
# Deploy to Azure Container Instances

set -e

# Configuration
RESOURCE_GROUP=${AZURE_RESOURCE_GROUP:-clip-extractor-rg}
LOCATION=${AZURE_LOCATION:-eastus}
CONTAINER_NAME=${CONTAINER_NAME:-clip-extractor}
REGISTRY_NAME=${REGISTRY_NAME:-clipextractorregistry}
IMAGE_NAME="$REGISTRY_NAME.azurecr.io/clip-extractor:latest"
MEMORY=${MEMORY:-4}
CPU=${CPU:-2}

echo "Deploying Clip Extractor to Azure Container Instances..."
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"

# Create resource group
echo "Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create container registry
echo "Creating container registry..."
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $REGISTRY_NAME \
    --sku Basic \
    2>/dev/null || echo "Registry already exists"

# Login to registry
echo "Logging in to registry..."
az acr login --name $REGISTRY_NAME

# Build and push image
echo "Building and pushing image..."
cd ../..
az acr build \
    --registry $REGISTRY_NAME \
    --image clip-extractor:latest \
    .

# Get registry credentials
REGISTRY_USERNAME=$(az acr credential show --name $REGISTRY_NAME --query username --output tsv)
REGISTRY_PASSWORD=$(az acr credential show --name $REGISTRY_NAME --query passwords[0].value --output tsv)

# Create storage account for data
STORAGE_ACCOUNT="${REGISTRY_NAME}storage"
echo "Creating storage account..."
az storage account create \
    --name $STORAGE_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku Standard_LRS \
    2>/dev/null || echo "Storage account already exists"

# Get storage account key
STORAGE_KEY=$(az storage account keys list \
    --resource-group $RESOURCE_GROUP \
    --account-name $STORAGE_ACCOUNT \
    --query '[0].value' \
    --output tsv)

# Create container instance
echo "Creating container instance..."
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --image $IMAGE_NAME \
    --cpu $CPU \
    --memory $MEMORY \
    --registry-login-server "$REGISTRY_NAME.azurecr.io" \
    --registry-username $REGISTRY_USERNAME \
    --registry-password $REGISTRY_PASSWORD \
    --environment-variables \
        AZURE_STORAGE_ACCOUNT=$STORAGE_ACCOUNT \
        AZURE_STORAGE_KEY=$STORAGE_KEY \
    --restart-policy OnFailure

echo "✓ Deployment complete!"
echo ""
echo "Container status:"
az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query instanceView.state
