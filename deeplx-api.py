import logging
# 配置日志，将 gevent 和 urllib3 的日志级别设置为 CRITICAL，避免打印无关的清理异常
logging.getLogger('gevent').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

import random
import gevent
from gevent.pool import Pool
from gevent import monkey
from gevent.pywsgi import WSGIServer
from gevent import queue  # 导入队列模块

monkey.patch_all()

import requests
# 禁用 urllib3 的安全警告
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)
from flask import Flask, request
import json

app = Flask(__name__)

def load_urls():
    """加载所有URL"""
    with open(r"urls.txt", "r") as f:
        urls = f.read().splitlines()
    return list(set(urls))  # 去重

def translate_with_url(url, text, source_lang, target_lang, result_queue):
    """使用指定URL进行翻译，若成功则将结果放入队列"""
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
            # 将成功结果放入队列
            result_queue.put(response.text)
    except Exception as e:
        print(f'{url}: {type(e).__name__}')

def get_translate_data(text, source_lang, target_lang):
    """
    并发请求所有URL，返回最先成功的结果，使用队列同步。
    若在10秒内没有任何成功结果，则返回错误信息。
    """
    urls = load_urls()
    result_queue = queue.Queue()  # 用于获取第一个正确的翻译结果
    tasks = []
    for url in urls:
        t = gevent.spawn(translate_with_url, url, text, source_lang, target_lang, result_queue)
        tasks.append(t)
    
    try:
        # 等待队列中有结果，超时时间为10秒
        result = result_queue.get(timeout=10)
        return result
    except queue.Empty:
        return json.dumps({"code": 500, "message": "Translation failed"})
    finally:
        # 杀死所有仍在运行的任务
        for t in tasks:
            if not t.ready():
                t.kill()

@app.route('/translate', methods=['POST'])
def translate():
    """
    接收POST请求，解析翻译参数，并调用 get_translate_data 返回翻译结果，
    同时统一设置响应头为 application/json。
    """
    data = json.loads(request.get_data())
    text = data['text']
    source_lang = data['source_lang']
    target_lang = data['target_lang']
    result = get_translate_data(text, source_lang, target_lang)
    # 使用 Flask 的 response_class 强制设置 MIME 类型为 application/json
    return app.response_class(response=result, mimetype='application/json')

if __name__ == '__main__':
    # 启动 Flask 服务，使用 gevent 的 WSGIServer
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
