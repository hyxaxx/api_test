def assert_ok(res, status=200):
    assert res.status_code == status, f"状态码错误，预期{status}，实际{res.status_code}"
    return res

def get_header(headers_dict, header_name):
    # 忽略大小写查找header
    for k, v in headers_dict.items():
        if k.lower() == header_name.lower():
            return v
    return None