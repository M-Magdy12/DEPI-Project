FROM python:3.9-slim as builder
WORKDIR /app

COPY kubernetes-cluster/ecommerce-app/requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local

COPY kubernetes-cluster/ecommerce-app/app.py .

COPY kubernetes-cluster/ecommerce-app/index.html .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
