echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

docker tag IMAGE_ID ghcr.io/OWNER/IMAGE_NAME:latest

docker push ghcr.io/OWNER/IMAGE_NAME:latest
