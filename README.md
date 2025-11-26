# URL Shortener + Monitoring (Prometheus + Grafana)

## المتطلبات
- Docker
- Docker Compose

## ملفات مهمة
- prometheus.yml
- alert.rules.yml
- alertmanager.yml
- grafana/provisioning/... (datasource + dashboard)
- docker-compose.yml
- app.py (تأكد أنه يحتوي على /metrics ويمتدَّ بالكود الموجود)

## تشغيل الستاك
1. مكان المشروع، شغل:
   ```bash
   docker-compose up --build -d
