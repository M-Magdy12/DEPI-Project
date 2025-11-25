from flask import Flask, request, jsonify, redirect, render_template
import string, random, time
import os
import sqlite3
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

DB_PATH = "/app/data/urls.db"

# ==========================
# DATABASE INITIALIZATION
# ==========================
def init_db():
    os.makedirs("/app/data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            short_code TEXT PRIMARY KEY,
            long_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ==========================
# PROMETHEUS METRICS
# ==========================
URLS_SHORTENED = Counter('urls_shortened_total', 'Total shortened URLs')
URLS_REDIRECTED = Counter('urls_redirected_total', 'Total redirects')
URLS_NOT_FOUND = Counter('urls_not_found_total', 'Not found URLs')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')

# ==========================
# HELPERS
# ==========================
def gen_code(n=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

# ==========================
# ROUTES
# ==========================

# الصفحة الرئيسية للـ ecommerce
@app.route("/")
def home():
    return render_template("ecommerce.html")

# URL shortener API (اختياري لو حابب تحافظ عليه)
@app.route("/shorten", methods=["POST"])
def shorten():
    start = time.time()
    data = request.get_json() or {}
    long_url = data.get("url")
    if not long_url:
        return jsonify({"error": "missing url"}), 400

    short_code = gen_code()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO urls (short_code, long_url) VALUES (?, ?)", (short_code, long_url))
    conn.commit()
    conn.close()

    URLS_SHORTENED.inc()
    REQUEST_LATENCY.observe(time.time() - start)

    return jsonify({
        "short_code": short_code,
        "short_url": f"/{short_code}"
    })


@app.route("/<short_code>")
def redirect_short(short_code):
    start = time.time()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT long_url FROM urls WHERE short_code=?", (short_code,))
    row = cur.fetchone()
    conn.close()

    if not row:
        URLS_NOT_FOUND.inc()
        REQUEST_LATENCY.observe(time.time() - start)
        return "Not Found", 404

    URLS_REDIRECTED.inc()
    REQUEST_LATENCY.observe(time.time() - start)

    return redirect(row[0], code=302)


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
