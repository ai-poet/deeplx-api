import random
import gevent
from gevent.pool import Pool
from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

import requests
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)
from flask import Flask, request
import json

app = Flask(__name__)

def load_urls():
    """加载所有URL"""
    with open(R"urls.txt", "r") as f:
        urls = f.read().splitlines()
    return list(set(urls))  # 去重

def translate_with_url(url, text, source_lang, target_lang):
    """使用指定URL进行翻译"""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        response = requests.post(url, verify=False, timeout=5, headers=headers,
                                data=json.dumps(payload))
        data = response.json()
        if data["code"] == 200:
            return response.text
    except Exception as e:
        print(f'{url}: {type(e).__name__}')
    return None

def get_translate_data(text, source_lang, target_lang):
    """并发请求所有URL，返回最先成功的结果"""
    urls = load_urls()
    
    # 创建所有翻译任务
    tasks = [gevent.spawn(translate_with_url, url, text, source_lang, target_lang) for url in urls]
    
    # 等待任意一个任务成功完成
    done = gevent.wait(tasks, count=1, timeout=10)
    
    # 终止所有其他任务
    for t in tasks:
        if not t.ready():
            t.kill()
    
    # 如果有成功的结果，返回第一个
    if done:
        result = done[0].value
        if result:
            return result
    
    # 如果没有成功的结果，返回错误信息
    return json.dumps({"code": 500, "message": "Translation failed"})

@app.route('/translate', methods=['POST'])
def translate():
    data = json.loads(request.get_data())
    text = data['text']
    source_lang = data['source_lang']
    target_lang = data['target_lang']
    return get_translate_data(text, source_lang, target_lang)

if __name__ == '__main__':
    # 启动 Flask 服务
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
