# LTChallenge
Coding test challenge using Twitter data for an airline company


## Start Development
docker build -f docker/Dockerfile.dev -t ltchallenge_env .
docker run --name ltchallenge -it -p 8080:8080 -v $(pwd):/app ltchallenge_env
