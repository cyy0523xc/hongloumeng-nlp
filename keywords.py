# -*- coding: utf-8 -*-
#
# 关键词分析
# Author: alex
# Created Time: 2018年04月14日 星期六 14时10分52秒
import requests
from time import time
from config import host

kw_url = "http://%s/article/keywords/%d"


def keywords(contents, size=10):
    body = {
        "contents": contents,
        "output_rank": True,
    }
    url = kw_url % (host, size)
    resp = requests.post(url, json=body).json()
    return resp['data']


if __name__ == '__main__':
    with open('./hongloumeng_80.md', encoding="utf-8") as r80, \
        open('./hongloumeng_120.md', encoding="utf-8") as r120:
        contents = [r80.read(), r120.read()]
        start = time()
        size = 50
        resp = keywords(contents, size=size)
        print("time %.3f" % (time() - start))

        i = 0
        print("\n前80回关键词TOP%d:" % size)
        for row in resp[0]:
            print("%2d  %5s: %10.3f" % (i, row[0], row[1]))
            i += 1

        i = 0
        print("\n全本关键词TOP%d:" % size)
        for row in resp[1]:
            print("%2d  %5s: %10.3f" % (i, row[0], row[1]))
            i += 1
