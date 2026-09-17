from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/orders/<order_id>")
def get_order(order_id):
    # BOLA / IDOR: no check that this order belongs to the current user
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id = " + order_id)  # SQL injection
    return jsonify(cur.fetchone())

@app.route("/admin/delete_user")
def admin_delete_user():
    user_id = request.args.get("user_id")
    # Missing function-level authorization: no admin role check
    conn = sqlite3.connect("app.db")
    conn.execute("DELETE FROM users WHERE id = " + user_id)  # SQL injection
    conn.commit()
    return "ok"
