#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import csv
import sys
import urllib.request
import urllib.parse


def get_data(word, page):
    url = 'http://www.pqdtcn.com/basic/basic_search'
    par_data = {"searchText": word,
                "pageSize": "100",
                "exactSearch": "0",
                "fullText": "0",
                "pageNumber": page,
                "facetsList": [],
                "sortOrder": "relevance"}
    result_data = json.dumps(par_data)
    post_data = bytes(result_data, 'utf-8')
    request = urllib.request.Request(url, post_data, headers={'Content-Type': 'application/json; charset=utf-8'})
    response = urllib.request.urlopen(request).read().decode('utf-8')
    page_result = []
    result_data = json.loads(response)['results']
    for p in result_data:
        result_data_key = (
            u'摘要', u'标题', u'作者', u'出版日期', u'大学/机构', u'文档URL', u'来源', u'ProQuest文档 ID', u'ISBN', u'导师')
        result_data_value = (
            p['thesisSummary'], p['thesisTitle'], p['thesisAuthor'], p['thesisYear'], p['thesisSchoolName'],
            u'http://www.pqdtcn.com/thesisDetails/' + p['thesisCodeEncrypt'], p['thesisSource'],
            p['thesisCode'], p['thesisIsbn'], p['thesisAdviser'])
        page_result.append(dict(zip(result_data_key, result_data_value)))
    print(page_result)
    return page_result


# 摘要、学科、标题、作者、页数、出版日期、学校代码、大学/机构、来源、出版地、出版国家/地区、ISBN、导师、委员会成员、学位、语言、ProQuest文档 ID、文档URL

def write_data(word, url_data):
    headers = ['摘要', '标题', '作者', '出版日期', '大学/机构', '文档URL', '来源', 'ProQuest文档 ID', 'ISBN', '导师']
    with open(word + '.csv', 'w', newline='', encoding='gb18030') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(url_data)


if __name__ == '__main__':
    print(sys.argv[1])
    result = []
    flag = 0
    for i in range(1, 100000):
        data = get_data(sys.argv[1], i)
        print(len(data))
        if len(data) == 0:
            flag = flag + 1
        print("flag=" + str(flag))
        if flag <= 10:
            result = result + data
        else:
            break
        result = result + data
    write_data(sys.argv[1], result)
