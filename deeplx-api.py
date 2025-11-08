import logging
logging.getLogger('gevent').setLevel(logging.CRITICAL)

import os
from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

from flask import Flask, request
import json
from openai import OpenAI

app = Flask(__name__)

OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

def get_translate_data(text, source_lang, target_lang):
    """
    使用 OpenAI API 进行翻译，返回 DeepLX 兼容格式的结果
    """
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": 'You are a professional translator. Translate the given text accurately and naturally. Return only a JSON object with a single field "translation" containing the translated text.'
                },
                {
                    "role": "user",
                    "content": f'Translate the following text from {source_lang} to {target_lang}:\n\n{text}'
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        translated_text = result.get('translation', '')
        
        return json.dumps({
            "code": 200,
            "data": translated_text
        })
    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        return json.dumps({
            "code": 500,
            "message": f"Translation failed: {str(e)}"
        })

@app.route('/translate', methods=['POST'])
def translate():
    """
    接收POST请求，解析翻译参数，并调用 OpenAI API 返回翻译结果
    兼容 DeepLX API 格式
    """
    try:
        data = json.loads(request.get_data())
        text = data['text']
        source_lang = data.get('source_lang', 'auto')
        target_lang = data['target_lang']
        result = get_translate_data(text, source_lang, target_lang)
        return app.response_class(response=result, mimetype='application/json')
    except Exception as e:
        error_response = json.dumps({
            "code": 400,
            "message": f"Invalid request: {str(e)}"
        })
        return app.response_class(response=error_response, mimetype='application/json', status=400)

if __name__ == '__main__':
    print(f"Starting OpenAI Translation API Server")
    print(f"Model: {OPENAI_MODEL}")
    print(f"Base URL: {OPENAI_BASE_URL}")
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
