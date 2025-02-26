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

valid_urls = []


def check_url_availability(url):
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "text": "Hello, world!",
            "source_lang": "EN",
            "target_lang": "ZH"
        }
        response = requests.post(url, verify=False, timeout=5, headers=headers,
                                 data=json.dumps(payload))
        if "你好，世界" in response.text:
            return url  # 返回可用的 URL
    except Exception as e:
        print('%s: %s' % (url, type(e).__name__))
    return None  # 不可用的 URL 返回 None


def get_valid_urls():
    global valid_urls
    with open(R"urls.txt", "r") as f:
        urls = f.read().splitlines()

    urls = list(set(urls))  # 去重
    p = Pool(200)
    jobs = [p.spawn(check_url_availability, _url) for _url in urls]

    # 等待所有任务完成
    gevent.joinall(jobs)

    # 构建新的 valid_urls 列表
    new_valid_urls = [job.value for job in jobs if job.value is not None]

    # 全局替换 valid_urls
    valid_urls[:] = new_valid_urls  # 使用切片赋值实现原子操作

    print("Updated valid_urls. Available URLs count: {}".format(len(valid_urls)))


def periodic_update(interval):
    """定期更新 valid_urls"""
    while True:
        get_valid_urls()
        gevent.sleep(interval)  # 每隔 interval 秒更新一次


# 启动定期更新任务
gevent.spawn(periodic_update, 86400)  # 每隔 1天更新一次


def single_translate(text, source_lang, target_lang):
    for i in range(10):
        urls = random.choice(valid_urls)
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "text": text,
                "source_lang": source_lang,
                "target_lang": target_lang
            }
            response = requests.post(urls, verify=False, timeout=5, headers=headers,
                                     data=json.dumps(payload))
            data = response.json()
            if data["code"] == 200:
                return response.text
        except Exception as e:
            print('%s' % (type(e).__name__))


def get_translate_data(text, source_lang, target_lang):
    tasks = [gevent.spawn(single_translate, text, source_lang, target_lang) for _ in range(3)]
    done = gevent.wait(tasks, count=1)
    for t in tasks:
        t.kill()
    return done.pop().value


@app.route('/translate', methods=['POST'])
def translate():
    data = json.loads(request.get_data())
    text = data['text']
    source_lang = data['source_lang']
    target_lang = data['target_lang']
    return get_translate_data(text, source_lang, target_lang)


if __name__ == '__main__':
    # 启动时先获取一次 valid_urls
    get_valid_urls()
    # 启动 Flask 服务
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
