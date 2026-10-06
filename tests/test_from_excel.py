import pytest

from utils.loader import load_cases_from_excel, send
from utils.assertions import assert_ok


@pytest.mark.parametrize("case",
    load_cases_from_excel(),
    ids=lambda c: c["name"])
def test_api_from_excel(session, case):
    res = send(session, case)
    assert_ok(res, status=case["expected_status"])