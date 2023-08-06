import requests
import pandas as pd
import json
import re


class Macroeconomic(object):

    def __init__(self):
        self.url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx'
        self.headers = {
            "Host": "datainterface.eastmoney.com",
            "Referer": "http://data.eastmoney.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42"}
        self.types = {
            '工业增加值增长': 'IAV',
            '海关进出口增减情况一览表': 'IE',
            '全国税收收入': 'NTR',
            '消费者信心指数': "CCI",
            '社会消费品零售总额': "TCC",
            '新增信贷数据': "NCD",
            '企业景气及企业家信心指数': "BCI",
            '企业商品价格指数': "CCP",
            '房价指数(08—10年)': "HPI",
            '货币供应量': "CS",
            '城镇固定资产投资': "FAI",
            '利率调整': 'IRA',
            '财政收入': 'FR',
            '外商直接投资数据': 'FDI',
            '外汇和黄金储备': 'FE',
            '外汇贷款数据': 'FEL',
            '本外币存款': 'CD',
            '居民消费者价格指数': 'CPI',
            '国内生产总值': 'GDP',
            '采购经理人指数': 'PMI',
            '工业品出厂价格指数': 'PPI',
            '存款准备金率': 'DRR',
        }

    def params(self, market=0):
        return {
            "type": "GJZB",
            "sty": "ZGZB",
            "ps": "10000",  # pages
            "mkt": str(market),  # market
        }

    def response(self, market=0):
        response = requests.get(
            self.url, headers=self.headers, params=self.params(market=market), timeout=5)
        response.encoding = response.apparent_encoding
        return pd.DataFrame([i.split(',') for i in eval(re.findall(r'\((.*)\)', response.text)[0])])

    def IAV(self):
        '''工业增加值
        '''
        df = self.response(0)
        df.columns = ['时间', '同比增长', '累计增长']
        return df

    def IE(self):
        '''海关进出口
        '''
        df = self.response(1)
        df.columns = ['时间', '出口额（亿美元）', '出口额同比', '出口额环比', '进口额（亿美元）',
                      '进口额同比', '进口额环比', '累计出口额（亿美元）', '累计出口额同比', '累计进口额（亿美元）', '累计进口额同比']
        return df

    def NTR(self):
        '''全国税收收入
        '''
        df = self.response(3)
        df.columns = ['时间', '税收收入合计(亿元)', '较上年同期(% )', '季度环比(%)']
        return df

    def CCI(self):
        '''消费者信心指数
        '''
        df = self.response(4)
        df.columns = ['时间', '消费者信心指数', '消费者信心指数（同比）', '消费者信心指数（环比）', '消费者满意指数',
                      '消费者满意指数（同比）', '消费者满意指数（环比）', '消费者预期指数', '消费者预期指数（同比）', '消费者预期指数（环比）', ]
        return df

    def TCC(self):
        '''社会消费品零售总额
        '''
        df = self.response(5)
        df.columns = ['时间', '当月(亿元)',	'当月同比增长',	'当月环比增长',	'累计(亿元)', '累计同比增长']
        return df

    def NCD(self):
        '''新增信贷数据
        '''
        df = self.response(7)
        df.columns = ['时间', '当月(亿元)',	'当月同比增长',	'当月环比增长',	'累计(亿元)', '累计同比增长']
        return df

    def BCI(self):
        '''企业景气及企业家信心指数
        '''
        df = self.response(8)
        df.columns = ['时间', '总指数', '总指数（同比）', '总指数（环比）', '农产品指数', '农产品指数（同比）', '农产品指数（环比）',
                      '矿产品指数', '矿产品指数（同比）', '矿产品指数（环比）', '煤油电指数', '煤油电指数（同比）', '煤油电指数（环比）', ]
        return df

    def CCP(self):
        '''企业商品价格指数
        '''
        df = self.response(9)
        df.columns = ['时间', '企业景气指数', '企业景气指数（同比）', '企业景气指数（环比）',
                      '企业家信心指数', '企业家信心指数（同比）', '企业家信心指数（环比）', ]
        return df

    def HPI(self):
        '''房价指数（08-10年）
        '''
        df = self.response(10)
        df.columns = ['时间', '国房指数', '国房指数（同比）', '土地开发面积指数',
                      '土地开发面积指数（同比）', '销售价格指数', '销售价格指数（同比）', ]
        return df

    def CS(self):
        '''货币供应量
        '''
        df = self.response(11)
        df.columns = ['时间', 'M2', 'M2同比增长', 'M2环比增长', 'M1',
                      'M1同比增长', 'M1环比增长', 'M0', 'M0同比增长', 'M0环比增长', ]
        return df

    def FAI(self):
        '''城镇固定资产投资
        '''
        df = self.response(12)
        df.columns = ['时间', '当月(亿元)', '同比增长', '环比增长', '自年初累计(亿元)']
        return df

    def IRA(self):
        '''利率调整
        '''
        df = self.response(13)
        df.columns = ['公布时间', '存款基准利率调整前', '存款基准利率调整后', '存款基准利率调整幅度', '货款基准利率调整前',
                      '货款基准利率调整后', '货款基准利率调整幅度', '上证消息公布次日指数涨跌', '深证消息公布次日指数涨跌', '生效时间']
        return df

    def FR(self):
        '''财政收入
        '''
        df = self.response(14)
        df.columns = ['时间', '当月(亿元)', '同比增长', '环比增长', '累计(亿元)', '累计同比']
        return df

    def FDI(self):
        '''外商直接投资
        '''
        df = self.response(15)
        df.columns = ['时间', '当月(亿元)', '同比增长', '环比增长', '累计(亿元)', '累计同比']
        return df

    def FE(self):
        '''外汇和黄金储备
        '''
        df = self.response(16)
        df.columns = ['时间', '国家外汇储备（亿元）', '国家外汇储备同比增长',
                      '国家外汇储备环比增长', '黄金储备（万盎司）', '黄金储备同比增长', '黄金储备环比增长']
        return df

    def FEL(self):
        '''外汇贷款
        '''
        df = self.response(17)
        df.columns = ['时间', '当月(亿元)', '同比增长', '环比增长', '累计(亿元)']
        return df

    def CD(self):
        '''本外币存款
        '''
        df = self.response(18)
        df.columns = ['时间', '当月(亿元)', '同比增长', '环比增长', '累计(亿元)']
        return df

    def CPI(self):
        '''居民消费者价格指数
        '''
        df = self.response(19)
        df.columns = ['时间', '全国当月', '全国同比增长', '全国环比增长', '全国累计', '城市当月',
                      '城市同比增长', '城市环比增长', '城市累计', '农村当月', '农村同比增长', '农村环比增长', '农村累计', ]
        return df

    def GDP(self):
        '''国内生产总值
        '''
        df = self.response(20)
        df.columns = ['时间', '全国生产总值绝对值(亿元)', '全国生产总值同比', '第一产业绝对值(亿元)',
                      '第一产业同比', '第二产业绝对值(亿元)', '第二产业同比', '第三产业绝对值(亿元)', '第三产业同比', ]
        return df

    def PMI(self):
        '''采购经理人指数
        '''
        df = self.response(21)
        df.columns = ['时间', '制造业指数', '制造业同比', '非制造业指数', '非制造业同比', ]
        return df

    def PPI(self):
        '''工业品出厂价格指数
        '''
        df = self.response(22)
        df.columns = ['时间', '当月', '同比', '累计']
        return df

    def DRR(self):
        '''存款准备金率
        '''
        df = self.response(23)
        df.columns = ['公布时间',  '生效时间', '大型金融机构调整前', '大型金融机构调整后', '大型金融机构调整幅度', '中小金融机构调整前',
                      '中小金融机构调整后', '中小金融机构调整幅度', '上证消息公布次日指数涨跌', '深证消息公布次日指数涨跌', '备注']
        return df


if __name__ == '__main__':
    mc = Macroeconomic()
    print(mc.types)
