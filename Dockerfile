FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt-get update && apt-get install tini
ADD . /app
WORKDIR /app
RUN uv sync --frozen
ENTRYPOINT ["/usr/bin/tini", "--", "/app/entrypoint.sh"]
