#!/bin/bash

# Variables
IMAGE_NAME="dalbodeule/runpod-classfication"
VERSION_TAG="latest"
DATE_TAG=$(date "+%Y%m%d")

# Build Dockerfile (CPU version)
DOCKER_BUILDKIT=1 docker buildx create --use || true
DOCKER_BUILDKIT=1 docker buildx build --file Dockerfile --platform linux/amd64,linux/arm64 -t ${IMAGE_NAME}:cpu-${VERSION_TAG} -t ${IMAGE_NAME}:cpu-${DATE_TAG} -t ${IMAGE_NAME}:cpu . --push

# Build Dockerfile.cuda (CUDA version)
DOCKER_BUILDKIT=1 docker buildx build --file Dockerfile.cuda --platform linux/amd64,linux/arm64 -t ${IMAGE_NAME}:cuda-${VERSION_TAG} -t ${IMAGE_NAME}:cuda-${DATE_TAG} -t ${IMAGE_NAME}:cuda . --push

# Create and push a multi-arch manifest for CPU version
DOCKER_CLI_EXPERIMENTAL=enabled docker manifest create ${IMAGE_NAME}:cpu-${VERSION_TAG} \
    ${IMAGE_NAME}:amd64-cpu-${VERSION_TAG} \
    ${IMAGE_NAME}:arm64-cpu-${VERSION_TAG}

DOCKER_CLI_EXPERIMENTAL=enabled docker manifest push ${IMAGE_NAME}:cpu-${VERSION_TAG}

# Create and push a multi-arch manifest for CUDA version
DOCKER_CLI_EXPERIMENTAL=enabled docker manifest create ${IMAGE_NAME}:cuda-${VERSION_TAG} \
    ${IMAGE_NAME}:amd64-cuda-${VERSION_TAG} \
    ${IMAGE_NAME}:arm64-cuda-${VERSION_TAG}

DOCKER_CLI_EXPERIMENTAL=enabled docker manifest push ${IMAGE_NAME}:cuda-${VERSION_TAG}

echo "Docker images for amd64 and arm64 (CPU and CUDA versions) have been built and pushed successfully."
