FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app
WORKDIR /app
RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "python", "/app/__main__.py"]
# CMD ["uv", "run", "python", "/app/__main__.py"]
