FROM python:3.11-slim as builder

WORKDIR /app


COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim

WORKDIR /app


RUN groupadd -r appuser && useradd -r -g appuser appuser


COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


COPY --chown=appuser:appuser . .


RUN mkdir -p /app/data && chown -R appuser:appuser /app/data


USER appuser

EXPOSE 5000


CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2"]
