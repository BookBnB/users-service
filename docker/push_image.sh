#!/bin/bash
docker/build_production_image.sh
docker tag users-service:latest $IMAGE_NAME:$IMAGE_VERSION
docker tag users-service:latest $IMAGE_NAME:latest
echo "$REGISTRY_PASSWORD" | docker login $REGISTRY_URL -u $REGISTRY_USERNAME --password-stdin
docker push $IMAGE_NAME:$IMAGE_VERSION
docker push $IMAGE_NAME:latest
