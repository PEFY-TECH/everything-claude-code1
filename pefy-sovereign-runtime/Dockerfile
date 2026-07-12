FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
WORKDIR /app
RUN groupadd --system pefy && useradd --system --gid pefy --home /app pefy
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir .
COPY app ./app
COPY api ./api
COPY mcp_server ./mcp_server
USER pefy
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
