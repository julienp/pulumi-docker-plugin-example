FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt-get update && apt-get install -qy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    tini \
    git
ADD . /app
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PULUMI_DOCKER=1
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen
ENTRYPOINT ["/usr/bin/tini", "--", "/app/entrypoint.sh"]
STOPSIGNAL SIGINT
