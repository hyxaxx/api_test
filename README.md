# 接口自动化测试项目

基于 Python + requests + pytest 的接口自动化测试框架。测试用例通过 JSON 文件管理，实现**数据与代码分离**——新增用例只需改数据，不用动代码。

项目包含两部分：
1. **基础接口测试**：针对 httpbin.org 的各类 HTTP 场景
2. **业务流测试**：针对项目自带的本地 Mock 服务，覆盖登录鉴权 → 下单 → 查单的完整链路

## 技术栈

| 工具 | 用途 |
|---|---|
| Python 3.11 | 开发语言 |
| requests | 发送 HTTP 请求 |
| pytest | 测试框架 |
| Flask | 搭建本地 Mock 服务 |
| pytest-html | 生成 HTML 测试报告 |

## 目录结构

```
api_test/
├── config.py               配置：base_url、超时时间
├── conftest.py             全局 fixture（session）
├── pytest.ini              pytest 配置
├── requirements.txt        依赖清单
├── mock_server.py          本地 Mock 服务（被测对象）
├── data/
│   └── cases.json          测试用例（JSON 数据驱动）
├── utils/
│   └── assertions.py       断言封装
└── tests/
    ├── test_methods.py     基础接口用例（15 条）
    └── test_order_flow.py  业务流 + 异常用例（5 条）
```

## 怎么运行

**① 安装依赖**

```bash
pip install -r requirements.txt
```

**② 启动 Mock 服务**（单独开一个终端，保持运行）

```bash
python mock_server.py
```

服务跑在 `http://127.0.0.1:5000`。

**③ 跑测试**

```bash
pytest
```

生成 HTML 报告：

```bash
pytest --html=report.html --self-contained-html
```

## Mock 服务

`mock_server.py` 用 Flask 实现了一个带鉴权的最小业务系统，用来模拟真实业务中的**接口依赖链**（公共 API 如 httpbin 是无状态的，无法覆盖这类场景）。

| 接口 | 方法 | 说明 |
|---|---|---|
| `/login` | POST | 登录，成功返回 token |
| `/orders` | POST | 创建订单（需 token） |
| `/orders/<id>` | GET | 查询订单（需 token） |

默认账号：`admin` / `123456`

## 用例设计

测试用例存放在 `data/cases.json`，每条用例描述「发什么请求 + 期望什么结果」：

```json
{
  "name": "GET 带 URL 参数",
  "method": "GET",
  "path": "/get",
  "params": {"name": "hyx"},
  "expected_status": 200
}
```

**新增用例 = 往 JSON 里加一个对象**，测试代码零改动。

### 覆盖场景

| 场景 | 覆盖内容 |
|---|---|
| 请求方法 | GET / POST / PUT / DELETE |
| 状态码 | 200 / 301 / 302 / 401 / 404 / 500 |
| 传参方式 | URL 参数、JSON body、表单 data |
| 请求头 | 自定义 header |
| 认证 | Basic Auth（成功 + 失败两种） |
| 重定向 | 跟随 / 不跟随（`allow_redirects`） |
| **业务流** | **登录 → 创建订单 → 查询订单** |
| **异常场景** | **未登录下单、假 token 下单、订单不存在、密码错误** |

## 断言设计

不只校验状态码，还校验**参数是否被服务端正确接收**：

| 发送的内容 | 校验方式 |
|---|---|
| URL 参数 | 比对回显的 `args` |
| JSON body | 比对回显的 `json` |
| 表单数据 | 比对回显的 `form` |
| 请求头 | 忽略大小写逐个比对 |

业务流测试则直接校验**数据是否真的写进去了**（创建订单后再查询，验证金额一致）。

## 测试报告

```bash
pytest --html=report.html --self-contained-html
```

生成的 `report.html` 包含每条用例的名称、耗时、通过状态和失败详情。

## 后续计划

- [ ] 用例数据改用 Excel 维护，便于非技术人员参与
- [ ] 接入 GitHub Actions，实现提交后自动跑测试
- [ ] 增加参数化与并发执行