import requests
import json
from pprint import pprint
import re
import pandas as pd
from tqdm import tqdm
from pypinyin import lazy_pinyin as pinyin


class China(object):
    def __init__(self):
        self.url = "https://gwpre.sina.cn/interface/news/ncp/data.d.json"
        self.provinces = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西',
                          '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾']

    def province(self):
        province_list = [''.join(pinyin(i)) for i in self.provinces]
        for p in province_list:
            yield p

    def response(self, province='hunan'):
        params = {'mod': 'province',
                  'province': province}
        response = requests.request("GET", self.url, params=params)
        data = json.loads(response.text)
        data = data['data']['historylist']
        return data

    def collect(self):
        lists = []
        j = 0
        for p in tqdm(self.province()):
            data = self.response(p)
            for i in data:
                conNum = i['conNum']
                conadd = i['conadd']
                date = i['ymd']
                lists.append([conNum, conadd, date, self.provinces[j]])
            j += 1
        return pd.DataFrame(lists, columns=['确诊', '新增确诊', '日期', '省份'])

    def save(self):
        self.collect().to_csv('corona.csv', index=False)


if __name__ == '__main__':
    Corona = China()
    print(Corona.collect())