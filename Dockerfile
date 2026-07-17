# syntax=docker/dockerfile:1

FROM dhi.io/bun:1-debian-dev AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/bun.lock ./
RUN --mount=type=cache,target=/root/.bun/install/cache,sharing=locked \
    bun install --frozen-lockfile
COPY frontend/ ./
RUN bun run build-only

FROM dhi.io/python:3.14-debian13-sfw-dev AS backend-builder
WORKDIR /app
ARG UV_EXCLUDE_NEWER="7 days"
COPY --from=dhi.io/uv:0 /uv /bin/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    sfw uv sync \
        --no-python-downloads \
        --no-editable \
        --link-mode=copy \
        --exclude-newer="${UV_EXCLUDE_NEWER}" \
        --locked \
        --no-dev

FROM dhi.io/python:3.14-debian13 AS runtime
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=PRODUCTION
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
COPY --from=backend-builder /app/.venv ./.venv
COPY app ./app
EXPOSE 8080
ENTRYPOINT ["python", "-m", "app"]
