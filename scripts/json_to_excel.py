import json
from pathlib import Path
from openpyxl import Workbook

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "data" / "cases.json", encoding="utf-8") as f:
    cases = json.load(f)

# ---- 关键改动：收集所有用例里出现过的字段 ----
all_keys = set()
for c in cases:
    all_keys.update(c.keys())

fixed = ["name", "method", "path", "expected_status"]
other = sorted(all_keys - set(fixed))
columns = fixed + other
print("导出列:", columns)

# ---- 写 Excel ----
wb = Workbook()
ws = wb.active
ws.append(columns)

for c in cases:
    row = []
    for col in columns:
        val = c.get(col)
        if isinstance(val, (dict, list)):
            row.append(json.dumps(val, ensure_ascii=False))   # 字典/列表 → JSON 字符串
        elif val is None:
            row.append("")
        else:
            row.append(val)
    ws.append(row)

wb.save(ROOT / "data" / "cases.xlsx")
print(f"已生成 {ROOT / 'data' / 'cases.xlsx'}，共 {len(cases)} 条用例")