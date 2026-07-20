# syntax=docker/dockerfile:1

# ---- build stage -----------------------------------------------------------
FROM python:3.12-slim AS build
WORKDIR /src
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir build && python -m build --wheel --outdir /dist

# ---- runtime stage ---------------------------------------------------------
FROM python:3.12-slim AS runtime

# Non-root runtime user.
RUN useradd --create-home --uid 10001 fox
WORKDIR /app

COPY --from=build /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl "foxess-local[api,mqtt,prometheus]" \
    && rm -rf /tmp/*.whl

USER fox

ENV FOX_HOST=192.168.1.38 \
    FOX_CORS_ORIGINS=* \
    PORT=8080

EXPOSE 8080

# Read-only-filesystem compatible; no writable paths required at runtime.
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import os,urllib.request as u; \
u.urlopen(f\"http://localhost:{os.environ.get('PORT','8080')}/api/v1/health\").read()" || exit 1

# Serves REST API + /metrics + WebSocket. Override `command` for mqtt/exporter.
CMD ["sh", "-c", "uvicorn --factory foxess.api:create_app --host 0.0.0.0 --port ${PORT:-8080}"]
