import json
import os
import sys

import pandas as pd
import requests
from tqdm import tqdm

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..log.SlyLog import slog, sprint
    from .GetData import StockData
except:
    from log.SlyLog import slog, sprint

    from GetData import StockData


class CompanyInfo(object):

    def __init__(self, names=['贵州茅台', '隆基股份']):
        self.names = names
        self.codes = list(StockData(names=self.names).stock_pair.values())
        self.sprint = sprint()
        self.main_url = 'http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax'
        self.headers = {
            "Host": "f10.eastmoney.com",
            "Referer": "http://f10.eastmoney.com/CompanySurvey/Index?type=web&code=SZ300059",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
            "X-Requested-With": "XMLHttpRequest"
        }

    def params_list(self, codes):
        for code in codes:
            yield {'code': code[0:2].upper()+code[3:]}

    def request(self, params):
        response = requests.get(
            self.main_url, headers=self.headers, params=params, timeout=5)
        response.encoding = response.apparent_encoding
        return json.loads(response.text)

    def get_data(self,):
        for params in self.params_list(codes=self.codes):
            yield self.request(params=params)

    def info(self):
        info = []
        self.sprint.blue('getting company information...')
        for json_data in self.get_data():
            info.append(
                (list(json_data['jbzl'].values())+list(json_data['fxxg'].values())))
        columns = ['公司名称', '英文名称', '曾用名', 'A股代码', 'A股简称', 'B股代码', 'B股简称', 'H股代码', 'H股简称', '证券类别', '所属行业', '上市交易所', '所属证监会行业', '总经理', '法人代表', '董秘', '董事长', '证券事务代表', '独立董事', '联系电话', '电子信箱', '传真', '公司网址', '办公地址', '注册地址', '区域', '邮政编码',
                   '注册资本(元)', '工商登记', '雇员人数', '管理人员人数', '律师事务所', '会计师事务所', '公司简介', '经营范围', '成立日期', '上市日期', '发行市盈率(倍)', '网上发行日期', '发行方式', '每股面值(元)', '发行量(股)', '每股发行价(元)', '发行费用(元)', '发行总市值(元)', '募集资金净额(元)', '首日开盘价(元)', '首日收盘价(元)', '首日换手率', '首日最高价(元)', '网下配售中签率', '定价中签率']
        return pd.DataFrame(info, columns=columns)


class IndustryAnalysis(object):

    def __init__(self, names=['贵州茅台', '隆基股份']):
        self.names = names
        self.codes = list(StockData(names=self.names).stock_pair.values())
        self.sprint = sprint()
        self.url = 'http://f10.eastmoney.com/IndustryAnalysis/IndustryAnalysisAjax?'
        self.headers = {
            "Host": "f10.eastmoney.com",
            "Referer": "http://f10.eastmoney.com/IndustryAnalysis/Index?type=web&code=SZ300059",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
            "X-Requested-With": "XMLHttpRequest"
        }

    def params_list(self, codes):
        params_list = []
        for code in codes:
            params_list.append({"code": code[0:2].upper()+code[3:],
                                "icode": "447"})
        return params_list

    def request(self, params):
        response = requests.get(
            self.url, headers=self.headers, params=params, timeout=5)
        response.encoding = response.apparent_encoding
        return json.loads(response.text)

    def get_data(self):
        data_list = []
        for params in tqdm(self.params_list(codes=self.codes)):
            data_list.append(self.request(params=params))
        return data_list

    @property
    def info(self):
        self.sprint.blue('getting industry analysis data...')
        industry_info = []
        growth_info = []
        valuation_info = []
        dupont_info = []
        market_size = []
        i = 0
        for data in self.get_data():
            industry_info.append({self.names[i]: data['hyzx']})  # 行业资讯
            growth_info.append(data['czxbj']['data'])  # 成长性比较
            valuation_info.append({self.names[i]: data['gzbj']['data']})  # 估值
            dupont_info.append({self.names[i]: data['dbfxbj']['data']})  # 杜邦
            market_size.append(
                {self.names[i]+'——'+'按总市值排名': data['gsgmzsz']})  # 总市值
            market_size.append(
                {self.names[i]+'——'+'按流通市值排名': data['gsgmltsz']})  # 流通市值
            market_size.append(
                {self.names[i]+'——'+'按营业收入排名': data['gsgmyysr']})  # 营业收入
            market_size.append(
                {self.names[i]+'——'+'按净利润排名': data['gsgmjlr']})  # 净利润
            i += 1
        return {
            'industry_info': industry_info,
            'growth_info': growth_info,
            'valuation_info': valuation_info,
            'dupont_info': dupont_info,
            'market_size': market_size,
        }

    def industry_info(self, info=None):
        if info == None:
            info = self.info
        lists = []
        for i in info['industry_info']:
            for j, k in i.items():
                for l in k:
                    lists.append([j, l['date'], l['title']])
        return pd.DataFrame(lists, columns=['stock', 'date', 'advisory'])

    def growth_info(self, info=None):
        if info == None:
            info = self.info
        lists = []
        for i in info['growth_info']:
            lists.append([i[0]['jc']])
            for j in i:
                lists.append(j.values())
        T1 = ['基本每股收益增长率(%)', '营业收入增长率(%)', '净利润增长率(%)']
        T2 = ['3年复合', '19A', 'TTM', '20E', '21E', '22E']
        columns = ['排名', '代码', '简称']
        for t1 in T1:
            for t2 in T2:
                columns.append(t2+'--'+t1)
        return pd.DataFrame(lists, columns=columns)

    def valuation_info(self, info=None):
        '''
        (1)MRQ市净率=上一交易日收盘价/最新每股净资产
        (2)市现率①=总市值/现金及现金等价物净增加额
        (3)市现率②=总市值/经营活动产生的现金流量净额
        '''
        if info == None:
            info = self.info
        columns = ['排名', '代码', '简称', 'PEG']
        T = {'市盈率': ['19A', 'TTM', '20E', '21E', '22E'],
             '市销率': ['19A', 'TTM', '20E', '21E', '22E'],
             '市净率': ['19A', 'MRQ'],
             '市现率①': ['19A', 'TTM'],
             '市现率②': ['19A', 'TTM'],
             'EV/EBITDA': ['19A', 'TTM']}
        for i, j in T.items():
            for k in j:
                columns.append(k+'--'+i)
        lists = []
        for i in info['valuation_info']:
            lists.append(i.keys())
            for j in i.values():
                for k in j:
                    lists.append(k.values())
        return pd.DataFrame(lists, columns=columns)

    def dupont_info(self, info=None):
        if info == None:
            info = self.info
        T1 = ['ROE(%)', '净利率(%)', '总资产周转率(%)', '权益乘数(%)']
        T2 = ['3年平均', '17A', '18A', '19A']
        columns = ['排名', '代码', '简称']
        for t1 in T1:
            for t2 in T2:
                columns.append(t2+'--'+t1)
        lists = []
        for i in info['dupont_info']:
            lists.append(i.keys())
            for j in i.values():
                for k in j:
                    lists.append(k.values())
        return pd.DataFrame(lists, columns=columns)

    def market_size(self, info=None):
        if info == None:
            info = self.info
        columns = ['排名', '代码', '简称',
                   '总市值(元)', '流通市值(元)', '营业收入(元)', '净利润(元)', '报告期']
        lists = []
        for i in info['market_size']:
            lists.append(i.keys())
            for j in i.values():
                for k in j:
                    lists.append(k.values())
        return pd.DataFrame(lists, columns=columns)


class ManagementHoldings(object):
    '''公司高管持股(不能用)
    '''

    def __init__(self, names=['贵州茅台', '隆基股份']):
        self.names = names
        self.codes = list(StockData(names=self.names).stock_pair.values())
        import tushare as ts
        ts.set_token(
            '287812b9098691320f49c5a31cd241d341b8bdb052de60fd8e20d262')
        self.pro = ts.pro_api()

    def holdings(self):
        return self.pro.stk_rewards(ts_code='000001.SZ,600000.SH')


if __name__ == '__main__':
    ia = IndustryAnalysis()
    df = ia.market_size()
