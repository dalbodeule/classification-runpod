#!/bin/bash

# Variables
IMAGE_NAME="dalbodeule/runpod-classification"
VERSION_TAG="latest"
DATE_TAG="$(date "+%Y%m%d")"

# Create buildx instance only if not already existing
if ! docker buildx inspect > /dev/null 2>&1; then
    DOCKER_BUILDKIT=1 docker buildx create --use
fi

# Build Dockerfile (CPU version)
DOCKER_BUILDKIT=1 docker buildx build --file Dockerfile --platform linux/amd64,linux/arm64 -t ${IMAGE_NAME}:cpu-${VERSION_TAG} -t ${IMAGE_NAME}:cpu-${DATE_TAG} -t ${IMAGE_NAME}:cpu . --push

# Build Dockerfile.cuda (CUDA version)
DOCKER_BUILDKIT=1 docker buildx build --file Dockerfile.cuda --platform linux/amd64 -t ${IMAGE_NAME}:cuda-${VERSION_TAG} -t ${IMAGE_NAME}:cuda-${DATE_TAG} -t ${IMAGE_NAME}:cuda . --push

echo "Docker images for amd64 and arm64 (CPU and CUDA versions) have been built and pushed successfully."

