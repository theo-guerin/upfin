# syntax=docker/dockerfile:1

FROM dhi.io/python:3.14-debian13-sfw-dev AS builder
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
COPY --from=builder /app/.venv ./.venv
COPY app ./app
EXPOSE 8080
ENTRYPOINT ["python", "-m", "app"]
