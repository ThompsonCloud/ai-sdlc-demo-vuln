from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)


def current_user_id(req):
    # 由网关注入的已认证身份；缺失即未认证
    uid = req.headers.get("X-User-Id")
    if not uid:
        abort(401)
    return uid


def require_admin(req):
    if req.headers.get("X-User-Role") != "admin":
        abort(403)  # 功能级授权校验


@app.route("/orders/<order_id>")
def get_order(order_id):
    uid = current_user_id(request)
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    # v2: 用字符串拼接 + 去掉 owner_id 归属校验（演示：故意引入 SQLi + BOLA/越权）
    cur.execute(f"SELECT * FROM orders WHERE id = '{order_id}'")
    row = cur.fetchone()
    if row is None:
        abort(404)
    return jsonify(row)


@app.route("/admin/delete_user", methods=["POST"])
def admin_delete_user():
    require_admin(request)  # 功能级授权
    user_id = request.args.get("user_id")
    conn = sqlite3.connect("app.db")
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))  # 参数化
    conn.commit()
    return "ok"
