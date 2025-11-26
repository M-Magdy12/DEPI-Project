#E-commerce backend.py
from flask import Flask, request, jsonify, render_template
import os
import sqlite3
import time
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

DB_PATH = "/app/data/ecommerce.db"

# ==========================
# DATABASE INITIALIZATION
# ==========================
def init_db():
    os.makedirs("/app/data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Products table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            icon TEXT,
            stock INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Orders table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Order items table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # Check if products exist, if not add sample data
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        sample_products = [
            ("iPhone 15 Pro", "Smartphones", 999, "Latest flagship with A17 Pro chip and titanium design", "📱"),
            ("MacBook Pro 16\"", "Laptops", 2499, "Powerful M3 Max chip for professionals", "💻"),
            ("AirPods Pro", "Audio", 249, "Active noise cancellation with spatial audio", "🎧"),
            ("Apple Watch Ultra", "Wearables", 799, "Rugged titanium case with advanced health features", "⌚"),
            ("iPad Pro 12.9\"", "Tablets", 1099, "M2 chip with Liquid Retina XDR display", "📲"),
            ("Sony WH-1000XM5", "Audio", 399, "Industry-leading noise cancellation", "🎵"),
            ("Samsung Galaxy S24", "Smartphones", 899, "AI-powered photography and performance", "📱"),
            ("Dell XPS 15", "Laptops", 1799, "InfinityEdge display with powerful specs", "💻"),
        ]
        cur.executemany(
            "INSERT INTO products (name, category, price, description, icon) VALUES (?, ?, ?, ?, ?)",
            sample_products
        )
    
    conn.commit()
    conn.close()

init_db()

# ==========================
# PROMETHEUS METRICS
# ==========================
PRODUCTS_VIEWED = Counter('products_viewed_total', 'Total product views')
ORDERS_PLACED = Counter('orders_placed_total', 'Total orders placed')
CART_ADDITIONS = Counter('cart_additions_total', 'Total items added to cart')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds')

# ==========================
# ROUTES
# ==========================

# Homepage - E-commerce
@app.route("/")
def home():
    return render_template("ecommerce.html")

# Get all products
@app.route("/api/products", methods=["GET"])
def get_products():
    start = time.time()
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    category = request.args.get('category')
    
    if category:
        cur.execute("SELECT * FROM products WHERE category = ?", (category,))
    else:
        cur.execute("SELECT * FROM products")
    
    products = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    PRODUCTS_VIEWED.inc()
    REQUEST_LATENCY.observe(time.time() - start)
    
    return jsonify(products)

# Get single product
@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    start = time.time()
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cur.fetchone()
    conn.close()
    
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    REQUEST_LATENCY.observe(time.time() - start)
    return jsonify(dict(product))

# Place order
@app.route("/api/orders", methods=["POST"])
def place_order():
    start = time.time()
    data = request.get_json() or {}
    
    # Validate required fields
    customer_name = data.get("customer_name")
    customer_email = data.get("customer_email")
    customer_phone = data.get("customer_phone", "")
    items = data.get("items", [])
    
    if not customer_name or not customer_email or not items:
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Calculate total
    total_amount = 0
    for item in items:
        cur.execute("SELECT price FROM products WHERE id = ?", (item['product_id'],))
        product = cur.fetchone()
        if product:
            total_amount += product[0] * item.get('quantity', 1)
    
    # Create order
    cur.execute(
        "INSERT INTO orders (customer_name, customer_email, customer_phone, total_amount) VALUES (?, ?, ?, ?)",
        (customer_name, customer_email, customer_phone, total_amount)
    )
    order_id = cur.lastrowid
    
    # Add order items
    for item in items:
        cur.execute("SELECT name, price FROM products WHERE id = ?", (item['product_id'],))
        product = cur.fetchone()
        if product:
            cur.execute(
                "INSERT INTO order_items (order_id, product_id, product_name, price, quantity) VALUES (?, ?, ?, ?, ?)",
                (order_id, item['product_id'], product[0], product[1], item.get('quantity', 1))
            )
    
    conn.commit()
    conn.close()
    
    ORDERS_PLACED.inc()
    REQUEST_LATENCY.observe(time.time() - start)
    
    return jsonify({
        "success": True,
        "order_id": order_id,
        "total_amount": total_amount,
        "message": "Order placed successfully!"
    }), 201

# Get order by ID
@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    start = time.time()
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # Get order
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cur.fetchone()
    
    if not order:
        conn.close()
        return jsonify({"error": "Order not found"}), 404
    
    # Get order items
    cur.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    items = [dict(row) for row in cur.fetchall()]
    
    conn.close()
    
    order_data = dict(order)
    order_data['items'] = items
    
    REQUEST_LATENCY.observe(time.time() - start)
    return jsonify(order_data)

# Get all orders (admin)
@app.route("/api/orders", methods=["GET"])
def get_all_orders():
    start = time.time()
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    REQUEST_LATENCY.observe(time.time() - start)
    return jsonify(orders)

# Add to cart tracking (optional - for analytics)
@app.route("/api/cart/add", methods=["POST"])
def track_cart_addition():
    CART_ADDITIONS.inc()
    return jsonify({"success": True})

# Prometheus metrics
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Health check
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)