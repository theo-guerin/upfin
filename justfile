dev:
    concurrently "just frontend-watch" "just run"

run:
    export $(grep -v '^#' .env | xargs) && uv run -m app

frontend-build:
    bun run --cwd ./frontend build

frontend-watch:
    bun run --cwd ./frontend build --watch
