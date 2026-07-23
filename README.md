# jellyfin-uploader

A web UI for uploading movies to your [Jellyfin](https://jellyfin.org) library. It auto-detects movie names from filenames and matches them against your Jellyfin catalog.

## Quick start

1. Add the service to your docker-compose.yml:

   ```yaml
   services:
     jellyfin-uploader:
       image: jellyfin-uploader:latest
       container_name: jellyfin-uploader
       ports:
         - "5080:8080" # left is the host port — change it if needed
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

All settings are read from environment variables (see [.env.example](.env.example)):

| Variable                      | Required | Default        | Description                                   |
| ----------------------------- | -------- | -------------- | --------------------------------------------- |
| `JELLYFIN_API_BASE_URL`       | yes      |                | Base URL of the Jellyfin server API            |
| `JELLYFIN_API_KEY`            | yes      |                | Jellyfin API key                               |
| `JELLYFIN_MOVIE_LIBRARY_PATH` | yes      |                | Filesystem path to the Jellyfin movie library |
| `ENVIRONMENT`                 | no       | `DEVELOPMENT`  | `DEVELOPMENT` or `PRODUCTION` (ignore for Docker) |

## Local development

To run the project locally without Docker, you'll need [uv](https://docs.astral.sh/uv/), [bun](https://bun.sh), and [just](https://just.systems):

```sh
uv sync
cp .env.example .env  # then fill in your values
just dev
```

## Disclaimer

**jellyfin-uploader does not support or condone piracy.** This tool is intended for managing media you personally own or have legal rights to. It does not include or distribute any media content.
