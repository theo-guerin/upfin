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
