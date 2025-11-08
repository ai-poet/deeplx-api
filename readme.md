# OpenAI Translation API (DeepLX Compatible)

[English](README.md) | [中文](README_ZH.md)

This tool provides a translation service powered by OpenAI API with JSON object mode, while maintaining full compatibility with DeepLX API format. It's designed for immersive translation tools and can be deployed locally (PC or Docker) or on a VPS.

## Features

- **OpenAI Powered:** Leverages OpenAI's powerful language models for high-quality translation
- **JSON Object Mode:** Uses OpenAI's structured JSON output for reliable parsing
- **DeepLX Compatible:** Fully compatible with existing DeepLX API clients
- **Flexible Configuration:** Support for custom base URLs, models, and API keys
- **High Performance:** Built with gevent for efficient concurrent request handling
- **Easy Deployment:** Can be deployed on various platforms, including local PCs, Docker, and VPS

## Getting Started

### 1. Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `OPENAI_BASE_URL` (optional): OpenAI API base URL, defaults to `https://api.openai.com/v1`
- `OPENAI_MODEL` (optional): Model to use, defaults to `gpt-4o-mini`

### 2. Local Deployment

#### Prerequisites
- Python 3.9+
- pip

#### Steps

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_MODEL="gpt-4o-mini"  # optional
export OPENAI_BASE_URL="https://api.openai.com/v1"  # optional
```

3. Run the service:
```bash
python deeplx-api.py
```

4. Configure your immersive translation service to use DeepLX (Beta) with API address: `http://127.0.0.1:5000/translate`

### 3. Docker Deployment

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

Or build from source:

```bash
docker build -t openai-translation-api .
docker run \
  --name openai-translation-api \
  -p 5000:5000 \
  -e OPENAI_API_KEY="your-api-key-here" \
  --restart always \
  openai-translation-api
```

You can customize the port mapping as needed.

Configure your immersive translation service to use DeepLX (Beta) with API address: `http://127.0.0.1:5000/translate` or `http://VPS_ip:5000/translate`.

## API Format

The API is fully compatible with DeepLX format:

**Request:**
```json
POST /translate
{
  "text": "Hello, world!",
  "source_lang": "EN",
  "target_lang": "ZH"
}
```

**Response:**
```json
{
  "code": 200,
  "data": "你好，世界！"
}
```

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the [MIT License](LICENSE.md).
