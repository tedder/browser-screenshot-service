#!/bin/bash
#
set -x

[[ "$1" != "" ]] && BRANCH="$1" || BRANCH=main
[[ "$BRANCH" == "main" ]] && TAG="latest" || TAG="$BRANCH"
[[ -z "$ARCHS" ]] && ARCHS="linux/armhf,linux/arm64,linux/amd64"
# rebuild the container
git checkout $BRANCH || exit 2

git pull

#DOCKER_BUILDKIT=1 docker buildx build --progress=plain --compress --push $2 --platform linux/armhf,linux/arm64,linux/amd64,linux/i386 --tag kx1t/screenshot:$TAG .
DOCKER_BUILDKIT=1 docker buildx build --compress --push $2 --platform $ARCHS --tag kx1t/screenshot:$TAG .
