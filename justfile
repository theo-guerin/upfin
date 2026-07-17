dev:
    concurrently "bun run --cwd ./frontend build --watch" "uv run -m app"

build:
    bun run --cwd ./frontend build
