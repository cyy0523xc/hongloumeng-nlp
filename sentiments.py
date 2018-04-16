# -*- coding: utf-8 -*-
#
# 实体识别
# Author: alex
# Created Time: 2018年04月14日 星期六 15时07分34秒
import re
import requests
from time import time
from config import host

html_clear = re.compile("<[^>]*>")
sentiments_url = "http://%s/sentiments/predict/default"


def sentiments(contents):
    url = sentiments_url % host
    body = {
        'contents': contents,
    }
    resp = requests.post(url, json=body).json()
    return resp['data']


if __name__ == '__main__':
    contents = []
    for i in range(120):
        fname = "./text/%03d.md" % (i+1)
        with open(fname, encoding="utf-8") as r:
            content = r.read()
            content = html_clear.sub("", content)
            content = content.replace("#", ' ')
            content = content.replace("-", ' ')
            content = content.strip()
            if len(content) > 2:
                contents.append(content)

    start = time()
    resp = sentiments(contents)
    print("time: %.3f" % (time() - start))

    i = 0
    print("情感变化：")
    for row in resp:
        i += 1
        print("%03d   情感值: %.3f" % (i, row))
