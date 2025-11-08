# OpenAI 翻译 API（兼容 DeepLX）

[English](README.md) | [中文](README_ZH.md)

本工具提供基于 OpenAI API 的翻译服务，使用 JSON 对象模式，同时完全兼容 DeepLX API 格式。专为沉浸式翻译工具设计，可以部署在本地（PC 或 Docker）或 VPS 上。

## 功能特点

- **OpenAI 驱动:** 利用 OpenAI 强大的语言模型提供高质量翻译
- **JSON 对象模式:** 使用 OpenAI 的结构化 JSON 输出，确保可靠解析
- **DeepLX 兼容:** 完全兼容现有的 DeepLX API 客户端
- **灵活配置:** 支持自定义基础 URL、模型和 API 密钥
- **高性能:** 使用 gevent 构建，高效处理并发请求
- **简易部署:** 可以部署在各种平台上，包括本地 PC、Docker 和 VPS

## 入门指南

### 1. 环境变量

需要以下环境变量：

- `OPENAI_API_KEY`（必填）：您的 OpenAI API 密钥
- `OPENAI_BASE_URL`（可选）：OpenAI API 基础 URL，默认为 `https://api.openai.com/v1`
- `OPENAI_MODEL`（可选）：使用的模型，默认为 `gpt-4o-mini`

### 2. 本地部署

#### 前置要求
- Python 3.9+
- pip

#### 步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_MODEL="gpt-4o-mini"  # 可选
export OPENAI_BASE_URL="https://api.openai.com/v1"  # 可选
```

3. 运行服务：
```bash
python deeplx-api.py
```

4. 配置您的沉浸式翻译服务以使用 DeepLX (Beta)，API 地址：`http://127.0.0.1:5000/translate`

### 3. Docker 部署

```bash
docker run \
  --name openai-translation-api \
  -p 5000:5000 \
  -e OPENAI_API_KEY="your-api-key-here" \
  -e OPENAI_MODEL="gpt-4o-mini" \
  -e OPENAI_BASE_URL="https://api.openai.com/v1" \
  --restart always \
  your-image-name
```

或从源代码构建：

```bash
docker build -t openai-translation-api .
docker run \
  --name openai-translation-api \
  -p 5000:5000 \
  -e OPENAI_API_KEY="your-api-key-here" \
  --restart always \
  openai-translation-api
```

您可以根据需要自定义端口映射。

配置您的沉浸式翻译服务以使用 DeepLX (Beta)，API 地址：`http://127.0.0.1:5000/translate` 或 `http://VPS_ip:5000/translate`。

## API 格式

该 API 完全兼容 DeepLX 格式：

**请求：**
```json
POST /translate
{
  "text": "Hello, world!",
  "source_lang": "EN",
  "target_lang": "ZH"
}
```

**响应：**
```json
{
  "code": 200,
  "data": "你好，世界！"
}
```

## 贡献
欢迎贡献！请随时提交问题或拉取请求。

## 许可证
本项目根据 [MIT 许可证](LICENSE.md) 开源。
