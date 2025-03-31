FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ADD . /app
WORKDIR /app
RUN uv sync --frozen
ENTRYPOINT ["/tini", "--", "/app/entrypoint.sh"]
