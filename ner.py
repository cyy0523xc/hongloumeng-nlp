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
        "贾母/nr 便/d 留下/v 文官/nr 自使/v ，/w 将/p 正旦/n 芳官/nr 指与/v 宝玉/nr ，/w 将/p 小旦/n 蕊官/nr 送/v 了/u 宝钗/nr ，/w 将/p 小生/n 藕官/nr 指与/v 了/u  黛玉/nr ，/w 将/d 大花面/n 葵官/nr 送/v 了/u 湘云/nr ，/w 将/p 小花面/n 豆官/nr 送/v 了/u 宝琴/nr ，/w 将/p 老外/n 艾官/nr 送/v 了/u 探春/nr ，/w 尤氏/nr 便/d 讨/v 了/u 老旦/n 茄官/nr 去/v 。/w",
        "宝玉/nr 听/v 了/y ，/w 心下/n 纳闷/vn ，/w 只得/d 踱到/v 潇湘馆/ns ，/w 瞧/v 黛玉/nr 益发/vd 瘦/a 的/u 可怜/a ，/w 问/v 起来/v ，/w 比/p 往日/t 已/d 算/v 大愈/l 了/y 。/w",
        "是/v 日/j 也/d 定/v 了/u 一/m 本/q 小戏/n 请/v 贾母/nr 王夫人/nr 等/u",
        "这里/r 宝玉/nr 问/v 他/r ：/w “/w 到底/d 是/v 为/v 谁/r 烧纸/v ？/w 我/r 想来/v 若是/v 为/p 父母/n 兄弟/n ，/w 你们/r 皆/d 烦/a 人/n 外头/f 烧/v 过/v 了/y ，/w 这里/r 烧/v 这/r 几/m 张/q ，/w 必/d 有/v 私自/Ng 的/u 情理/n 。/w ”/w 藕官/nr 因/p 方才/t 护庇/v 之/u 情/n 感激/v 于衷/nr ，/w 便/d 知/v 他/r 是/v 自己/r 一流/b 的/u 人物/n ，/w 便/d 含泪/v 说/v 道/v ：/w “/w 我/r 这/r 事/n ，/w 除了/p 你/r 屋里/s 的/u 芳官/nr 并/c 宝姑娘/nr 的/u 蕊官/nr ，/w 并/d 没/v 第三/m 个/q 人/n 知道/v 。/w 今日/t 被/p 你/r 遇见/v ，/w 又/d 有/v 这/r 段/q 意思/n ，/w 少/ad 不得/v 也/d 告诉/v 了/u 你/r ，/w 只/d 不/d 许再/Vg 对/p 人/n 言讲/v 。/w ”/w 又/d 哭道/v ：/w “/w 我/r 也/d 不便/a 和/c 你/r 面说/v ，/w 你/r 只/d 回去/v 背人/vd 悄问/vd 芳官/nr 就/d 知道/v 了/y 。/w ”/w 说/v 毕/Vg ，/w 佯常/d 而/c 去/v 。/w",
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
            words.append([w, 'nr', 1000*len(w)])
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
    }
    resp = requests.post(url, json=body).json()
    #print(resp)
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
    ner_dict()
    resp = ner(contents, segment="nshort")
    #perceptron_learn()
    #resp = perceptron(contents)
    print("time: %.3f" % (time() - start))

    names = {}
    for i in range(len(contents)):
        for row in resp[i]:
            if row[1] == 'person':
                row[0] = row[0].strip()
                if row[0] not in names:
                    names[row[0]] = 1
                else:
                    names[row[0]] += 1

    i = 0
    persons = sorted(names.items(), key=lambda x: x[1], reverse=True)[:100]
    print("统计人物在各回里出现的次数：")
    for row in persons:
        i += 1
        print("%03d   重要度: %3d    %s" % (i, row[1], row[0]))
