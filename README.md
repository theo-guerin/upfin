# jellyfin-uploader

A small service that lets you upload movie files directly into a
[Jellyfin](https://jellyfin.org) library directory and match them against
existing Jellyfin entries via the API.

## Quick start

1. Setup the service into your Jellyfin Server:

```yaml
services:
  jellyfin-uploader:
    image: jellyfin-uploader:latest
    container_name: jellyfin-uploader
    ports:
      - "5080:8080" # left is the host port — change it if 5080 is taken
    logging:
      options:
        max-size: 10m
    env_file: .env
    restart: unless-stopped
```

2. Create a `.env` file with your settings (see [Configuration](#configuration)).

3. Run the service:

   ```sh
   docker compose up -d
   ```

## Configuration

Configuration is provided through environment variables in a `.env` file
(see [`.env.example`](.env.example)):

| Variable                      | Required | Default        | Description                                   |
| ----------------------------- | -------- | -------------- | --------------------------------------------- |
| `JELLYFIN_API_BASE_URL`       | yes      |                | Base URL of the Jellyfin server API            |
| `JELLYFIN_API_KEY`            | yes      |                | Jellyfin API key                               |
| `JELLYFIN_MOVIE_LIBRARY_PATH` | yes      |                | Filesystem path to the Jellyfin movie library |
| `ENVIRONMENT`                 | no       | `DEVELOPMENT`  | `DEVELOPMENT` or `PRODUCTION`                  |
| `PORT`                        | no       | `8080`         | Host port to expose the server on              |

## Local development

For hacking on the project without Docker, you'll need
[uv](https://docs.astral.sh/uv/), [bun](https://bun.sh), and
[just](https://just.systems):

```sh
uv sync
cp .env.example .env  # then fill in your values
just dev
```
