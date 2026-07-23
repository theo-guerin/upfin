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
    docker build -t upfin:latest .

docker-setup-arm64:
    docker run --privileged --rm tonistiigi/binfmt --install arm64
    docker buildx create --name arm64builder --use 2>/dev/null || \
        docker buildx use arm64builder
    docker buildx inspect --bootstrap

docker-build-arm64: docker-setup-arm64
    docker buildx build --platform linux/arm64 -t upfin:latest .
