dev: _load-dotenv
    concurrently "just frontend-watch" "just run"

_load-dotenv:
    export $(grep -v '^#' .env | xargs)

run:
    uv run -m app

frontend-build:
    bun run --cwd ./frontend build

frontend-watch:
    bun run --cwd ./frontend build --watch

docker-build:
    docker build -t jellyfin-uploader:latest .

docker-setup-arm64:
    docker run --privileged --rm tonistiigi/binfmt --install arm64
    docker buildx create --name arm64builder --use 2>/dev/null || \
        docker buildx use arm64builder
    docker buildx inspect --bootstrap

docker-build-arm64: docker-setup-arm64
    docker buildx build --platform linux/arm64 -t jellyfin-uploader:latest .

docker-save-arm64: docker-build-arm64
    docker save jellyfin-uploader:latest | gzip > jellyfin-uploader-arm64.tar.gz
