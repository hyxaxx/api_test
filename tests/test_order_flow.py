import pytest
import requests
import allure
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


@allure.feature("订单业务流")
@allure.story("完整下单流程")
def test_full_order_flow(auth_header):
    with allure.step("创建订单"):
        r = requests.post(f"{BASE}/orders", json={"amount": 100},
                          headers=auth_header, timeout=5)
        assert r.status_code == 201
        order_id = r.json()["order_id"]

    with allure.step(f"查询订单 {order_id}"):
        r = requests.get(f"{BASE}/orders/{order_id}",
                         headers=auth_header, timeout=5)
        assert r.status_code == 200
        assert r.json()["data"]["amount"] == 100

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