FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN python -m pip install --no-cache-dir -e .

ENV PYTHONPATH=/app/src
EXPOSE 8030
CMD ["uvicorn", "deepresearch.api:app", "--host", "0.0.0.0", "--port", "8030"]
