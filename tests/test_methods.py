#tests/test_methods.py — 测 GET/POST 各种传参方式

#day 11 新增json 提交

import json
import pytest
from config import BASE_URL,TIMEOUT
from utils.assertions import assert_ok,get_header

def load_cases():
    with open("data/cases.json","r",encoding="utf-8") as f :
        return json.load(f)

all_cases = load_cases()

@pytest.mark.parametrize("case", all_cases, ids=lambda x: x["name"])
def test_api_methods(session, case):
    if case["path"].startswith("http"):
        full_url = case["path"]
    else:
        full_url = BASE_URL + case["path"]

    auth = case.get("auth")
    auth = tuple(auth) if auth else None

    response = session.request(
        method=case["method"],
        url=full_url,
        params=case.get("params"),
        json=case.get("json"),
        data=case.get("data"),
        headers=case.get("headers"),
        auth=auth,
        allow_redirects=case.get("allow_redirects",True),
        timeout=TIMEOUT
    )

    # ① 状态码
    assert_ok(response, status=case["expected_status"])

    # ② 只有带参数的用例，才去解析 JSON
    # ② 验证参数确实被收到
    if case.get("params") or case.get("json") or case.get("data") or case.get("headers"):
        data = response.json()

        if case.get("params"):
            assert data["args"] == case["params"], f"URL参数丢失：{data.get('args')}"

        if case.get("json"):
            assert data["json"] == case["json"], f"请求体丢失：{data.get('json')}"

        if case.get("data"):
            assert data["form"] == case["data"], f"表单数据丢失：{data.get('form')}"

        if case.get("headers"):
            for key, expected in case["headers"].items():
                actual = get_header(data["headers"], key)
                assert actual == expected, f"header [{key}] 丢失：期望{expected}，实际{actual}"
