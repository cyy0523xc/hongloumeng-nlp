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
ner_url = "http://%s/ner/%s"


def ner(contents, segment='senior'):
    """"""
    url = ner_url % (host, segment)
    enable = {
            "NameRecognize": True,
            "PlaceRecognize": False,
            "OrganizationRecognize": False,
            "CustomDictionary": False,
            "TranslatedNameRecognize": False,
            "JapaneseNameRecognize": False,
        }
    body = {
        'contents': contents,
        #'enable': enable,
    }
    resp = requests.post(url, json=body).json()
    return resp['data']



if __name__ == '__main__':
    contents = []
    for i in range(120):
        fname = "./text/%03d.md" % (i+1)
        with open(fname, encoding="utf-8") as r:
            content = r.read()
            contents.append(html_clear.sub("", content))

    start = time()
    resp = ner(contents, segment="nshort")
    print("time: %.3f" % (time() - start))

    names = {}
    for i in range(len(contents)):
        for row in resp[i]:
            if row[1] == 'person':
                if row[0] not in names:
                    names[row[0]] = 1
                else:
                    names[row[0]] += 1

    i = 0
    persons = sorted(names.items(), key=lambda x: x[1], reverse=True)[:50]
    print("统计人物在各回里出现的次数：")
    for row in persons:
        i += 1
        print("%03d   重要度: %3d    %s" % (i, row[1], row[0]))
