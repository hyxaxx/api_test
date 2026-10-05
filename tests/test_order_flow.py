import pytest
import requests

BASE = "http://127.0.0.1:5000"


@pytest.fixture
def token():
    """登录一次，拿到 token"""
    r = requests.post(f"{BASE}/login",
                      json={"username": "admin", "password": "123456"},
                      timeout=5)
    assert r.status_code == 200
    return r.json()["token"]


@pytest.fixture
def auth_header(token):
    return {"Authorization": token}


def test_full_order_flow(auth_header):
    """完整业务流：创建订单 → 查询订单"""
    # 1. 创建订单
    r = requests.post(f"{BASE}/orders", json={"amount": 100},
                      headers=auth_header, timeout=5)
    assert r.status_code == 201
    order_id = r.json()["order_id"]

    # 2. 用上一步拿到的 id 查详情
    r = requests.get(f"{BASE}/orders/{order_id}",
                     headers=auth_header, timeout=5)
    assert r.status_code == 200
    assert r.json()["data"]["amount"] == 100      # ← 数据真的传对了吗

def test_login_wrong_password():
    r = requests.post(f"{BASE}/login",
                      json={"username": "admin", "password": "wrong"},
                      timeout=5)
    assert r.status_code == 401


def test_create_order_without_token():
    """不带 token 就下单 —— 应该被拒"""
    r = requests.post(f"{BASE}/orders", json={"amount": 100}, timeout=5)
    assert r.status_code == 401


def test_create_order_with_bad_token():
    """带假 token 就下单 —— 应该被拒"""
    r = requests.post(f"{BASE}/orders", json={"amount": 100},
                      headers={"Authorization": "fake-token"}, timeout=5)
    assert r.status_code == 401


def test_get_nonexistent_order(auth_header):
    """查一个不存在的订单"""
    r = requests.get(f"{BASE}/orders/99999",
                     headers=auth_header, timeout=5)
    assert r.status_code == 404