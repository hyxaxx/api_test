import json
from pathlib import Path
from openpyxl import load_workbook
from config import BASE_URL, TIMEOUT

# 项目根目录（utils 的上一级）
ROOT = Path(__file__).resolve().parent.parent


def load_cases_from_excel(path=None):
    """从 Excel 读取测试用例"""
    if path is None:
        path = ROOT / "data" / "cases.xlsx"

    wb = load_workbook(path)
    ws = wb.active
    headers = [c.value for c in ws[1]]

    cases = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:              # 跳过空行
            continue
        case = dict(zip(headers, row))

        # 关键：JSON 字符串 → 字典
        for field in ("params", "json", "headers", "data","auth"):
            val = case.get(field)
            if isinstance(val, str) and val.strip():
                case[field] = json.loads(val)
            else:
                case[field] = None
        # 布尔字段特殊处理：Excel 里存的是字符串
        for field in ("allow_redirects",):
            val = case.get(field)
            if isinstance(val, str):
                case[field] = val.strip().lower() in ("true", "1", "yes")
            elif val is None:
                case[field] = None      # send() 里用 .get(..., True) 兜底
        cases.append(case)
    return cases


def send(session, case):
    """根据一条用例的描述发请求"""
    full_url = case["path"]
    if not full_url.startswith("http"):
        full_url = BASE_URL + full_url

    auth = case.get("auth")
    auth = tuple(auth) if auth else None

    return session.request(
        method=case["method"],
        url=full_url,
        params=case.get("params"),
        json=case.get("json"),
        data=case.get("data"),
        headers=case.get("headers"),
        auth=auth,
        allow_redirects=case.get("allow_redirects", True),
        timeout=TIMEOUT,
    )