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
learn_url = "http://%s/segment/learn/%s"


def perceptron_learn():
    corpus = [
    ]
    body = {
        'contents': corpus,
    }
    url = learn_url % (host, 'perceptron')
    resp = requests.post(url, json=body).json()
    #print(resp)
    return resp['data']


def perceptron(contents):
    url = ner_url % (host, 'perceptron')
    body = {
        'contents': contents,
        'return_segment': True,
    }
    resp = requests.post(url, json=body).json()
    #print(resp)
    return resp['data']


def ner_dict():
    url = "http://%s/dictionary/add" % host
    words = []
    with open("./name_dict.txt", encoding='utf-8') as r:
        for w in r.readlines():
            w = w.strip()
            if len(w) == 0:
                continue
            words.append([w, 'nr', 1000000*len(w)])
    resp = requests.post(url, json={"words": words}).json()
    return resp


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
        "AllNamedEntityRecognize": True,
    }
    body = {
        'contents': contents,
        'enable': enable,
        #'return_segment': True,
    }
    resp = requests.post(url, json=body).json()
    #print(resp)
    return resp['data']



if __name__ == '__main__':
    contents = []
    fname = "./pingfandeshijie.txt"
    with open(fname, encoding="utf-8") as r:
        content = r.read()
        content = html_clear.sub("", content)
        content = content.replace("#", ' ')
        content = content.replace("-", ' ')
        content = content.strip()
        if len(content) > 2:
            contents.append(content)

    start = time()
    #ner_dict()
    resp = ner(contents, segment="senior")
    #perceptron_learn()
    #resp = perceptron(contents)
    print("time: %.3f,  %d,  %d" % (time() - start, len(contents), len(resp[0])))

    names = {}
    for row in resp[0]:
        if row[1] == 'person':
            row[0] = row[0].strip()
            if row[0] not in names:
                names[row[0]] = 1
            else:
                names[row[0]] += 1

    i = 0
    persons = sorted(names.items(), key=lambda x: x[1], reverse=True)[:100]
    print("统计人物在书里出现的次数：")
    for row in persons:
        i += 1
        print("%03d   重要度: %3d    %s" % (i, row[1], row[0]))
