from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)
API_KEY = "sk-live-9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c"  # 硬编码密钥(演示 Gitleaks/ocr)


def current_user_id(req):
    uid = req.headers.get("X-User-Id")
    if not uid:
        abort(401)
    return uid


@app.route("/orders/<order_id>")
def get_order(order_id):
    uid = current_user_id(request)
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    # 字符串拼接 SQLi + 无 owner_id 校验(BOLA/越权)
    cur.execute(f"SELECT * FROM orders WHERE id = '{order_id}'")
    return jsonify(cur.fetchone())
