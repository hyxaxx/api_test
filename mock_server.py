from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

USERS = {"admin": "123456"}
tokens = {}      # token -> username
orders = {}      # order_id -> {...}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if USERS.get(data.get("username")) == data.get("password"):
        token = str(uuid.uuid4())
        tokens[token] = data["username"]
        return jsonify({"code": 0, "token": token})
    return jsonify({"code": 1, "msg": "用户名或密码错误"}), 401

@app.route("/orders", methods=["POST"])
@app.route("/orders", methods=["POST"])
def create_order():
    token = request.headers.get("Authorization")
    if token not in tokens:
        return jsonify({"code": 401, "msg": "未登录"}), 401
    oid = len(orders) + 1
    orders[oid] = {"id": oid, "amount": request.json.get("amount")}
    return jsonify({"code": 0, "order_id": oid}), 201

@app.route("/orders/<int:oid>", methods=["GET"])
def get_order(oid):
    token = request.headers.get("Authorization")
    if token not in tokens:
        return jsonify({"code": 401, "msg": "未登录"}), 401
    if oid not in orders:
        return jsonify({"code": 404, "msg": "订单不存在"}), 404
    return jsonify({"code": 0, "data": orders[oid]})

#故意写错mock服务引入bug测试
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     # if USERS.get(data.get("username")) == data.get("password"):     ← 注释掉
#     token = str(uuid.uuid4())                                         # ← 总是发 token
#     tokens[token] = data["username"]
#     return jsonify({"code": 0, "token": token})
#     # return jsonify({"code": 1, "msg": "用户名或密码错误"}), 401

if __name__ == "__main__":
    app.run(port=5000)