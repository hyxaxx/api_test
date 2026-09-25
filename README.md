# 接口自动化测试项目

基于 Python + requests + pytest 的接口自动化测试框架。测试用例通过 JSON 文件管理，实现**数据与代码分离**——新增用例只需改数据，不用动代码。

## 技术栈

| 工具 | 用途 |
|---|---|
| Python 3.11 | 开发语言 |
| requests | 发送 HTTP 请求 |
| pytest | 测试框架 |
| pytest-html | 生成 HTML 测试报告 |

## 目录结构

```
api_test/
├── config.py               配置：base_url、超时时间
├── conftest.py             全局 fixture（session）
├── pytest.ini              pytest 配置
├── requirements.txt        依赖清单
├── data/
│   └── cases.json          测试用例（JSON 数据驱动）
├── utils/
│   └── assertions.py       断言封装
└── tests/
    └── test_methods.py     接口测试用例
```

## 怎么运行

```bash
pip install -r requirements.txt
pytest
```

生成 HTML 测试报告：

```bash
pytest --html=report.html --self-contained-html
```

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
| 第三方接口 | jsonplaceholder |

## 断言设计

不只校验状态码，还校验**参数是否被服务端正确接收**：

| 发送的内容 | 校验方式 |
|---|---|
| URL 参数 | 比对回显的 `args` |
| JSON body | 比对回显的 `json` |
| 表单数据 | 比对回显的 `form` |
| 请求头 | 忽略大小写逐个比对 |

## 测试报告

```bash
pytest --html=report.html --self-contained-html
```

生成的 `report.html` 包含每条用例的名称、耗时、通过状态和失败详情。

## 后续计划

- [ ] 增加响应内容的业务断言（不只校验状态码和参数）
- [ ] 接入 GitHub Actions，实现提交后自动跑测试
- [ ] 尝试 Selenium / Playwright 做 UI 自动化