#废弃 臃肿 所有功能合并到 test_method
"""
#tests/test_status.py — 测 200 / 404 / 500 等状态码
import pytest

from config import BASE_URL
from utils.assertions import assert_ok
#测试文件之间互相 import 是坏味道
from tests.test_methods import load_cases

all_cases = load_cases()

@pytest.mark.parametrize(
    "case",
    all_cases,
    ids=lambda x:x["name"]
)
def test_status_code(session,case):
    full_url = BASE_URL + case["path"]
    res = session.request(url=full_url,method=case["method"])

    assert_ok(res,status=case["expected_status"])

    """
