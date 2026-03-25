# little_WMS
it's a small scale WMS.

:warning: this is in early alpha. changes may brake your saved data :warning:

This is a WMS(Warehouse Managment System) for personal use. It's vision is to be so simple to use that you use it.

Learn more in [Docs](docs/main.md)

## Development setup

Copy ´.env.example' to ´.env´.
In .env set DEBUG=1 and DJANGO_SUPERUSER_PASSWORD=1.
Mount the development entrypoint and src directory directly into the container and run in it via ´docker compose up´.

´´´ docker-compose.yml
services:
  web:
    image: nilskrau/little_wms:latest
    ports:
      - 8567:8567
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./src:/app/wms
      - ./scripts/entrypoint-dev.sh:/app/entrypoint.sh
´´´

