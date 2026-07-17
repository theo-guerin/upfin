### Lint & type check

```sh
# Frontend (run from frontend/)
bun run lint           # oxlint + eslint
bun run format         # prettier (import sorting + tailwind)
bun run type-check     # vue-tsc

# Python
uv run ruff check .    # lint — import sorting only (I rule)
uv run pyrefly .       # type check (strict preset)
```
