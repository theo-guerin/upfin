dev:
    concurrently "bun run --cwd ./frontend build --watch" "uv run -m app"

build-frontend:
    bun run --cwd ./frontend build

build-docker:
    docker build -t jellyfin-uploader:latest .

setup-arm64-builder:
    docker run --privileged --rm tonistiigi/binfmt --install arm64
    docker buildx create --name arm64builder --use 2>/dev/null || \
        docker buildx use arm64builder
    docker buildx inspect --bootstrap

build-docker-arm64: setup-arm64-builder
    docker buildx build --platform linux/arm64 -t jellyfin-uploader:latest .

export-docker-arm64: build-docker-arm64
    docker save jellyfin-uploader:latest | gzip > jellyfin-uploader-arm64.tar.gz
