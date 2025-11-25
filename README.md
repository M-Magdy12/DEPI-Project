# URL Shortener - DevOps Project (Week 1)

Run:
  docker compose up --build

API:
  POST /shorten   (JSON body: { "url": "https://example.com" })
  GET  /<short_code>
  GET  /metrics   (Prometheus format)
