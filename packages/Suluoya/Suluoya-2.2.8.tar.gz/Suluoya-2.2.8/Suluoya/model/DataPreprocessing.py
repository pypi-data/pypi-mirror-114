import pandas as pd
import numpy as np
import math
from scipy.stats import kstest
from pprint import pprint as print

import os
import sys

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..log.SlyLog import slog, sprint
except:
    from log.SlyLog import slog, sprint

sprint = sprint()


df = pd.DataFrame([[1, 2, 3, '是'], [np.nan, 5, '6', '否'], [
                  '7', None, 'h', None]], columns=['a', 'b', 'c', 'd'])


class type_class(object):
    def __init__(self):
        con_ = 1  # 连续
        bool_ = 2  # 布尔
        cat_ = 3  # 分类
        date_ = 4  # 日期
        object_ = 5  # 未知或混杂
        self.detype_dict = {'float64': con_, 'int64': con_,
                            'bool': bool_, 'category': cat_, 'object': object_,
                            'date': date_  # 没写完
                            }


class Series(object):
    def __init__(self,series,name):
        self.values = series.values
        self.name = name
        


class DataPreprocessing(type_class):
    def __init__(self, df):
        self.df = df
        self.columns = list(df.columns)  # ['a', 'b', 'c']
        type_class.__init__(self)

        self.types = dict(
            zip(self.columns, [self.detype_dict[str(i)] for i in df.dtypes.values]))

    def retype(self, type_dict={}):
        if not type_dict:
            pass
        # for column, type_ in type_dict.items():
        #    self.types[column] = type_
        
    # def num_(self,name):
    #     self.types[name] = con_
    #     self.df[name] = self.df[name].astype('float')
        
    # def bool_(self,name,bool_dict={'是':True,'否':False}):
    #     self.types[name] = bool_
    #     self.df[name] = self.df[name].replace(bool_dict)#.astype('bool')
        


if __name__ == '__main__':
    #dp = DataPreprocessing(df=df)
    #dp.bool_('d')
    s=Series(df.a,'a')
    print(s.values)


class dataPreprocessing(object):
    def __init__(self, df=pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                       columns=['a', 'b', 'c'])):
        self.df = df
        self.columns = df.columns
        self.df_type = dict(zip(df.columns, ['None'] * len(self.columns)))
        self.order_dict = dict(zip(df.columns, [] * len(self.columns)))

    def var_type(self, name='a', type=1):
        # 连续变量
        type_dict = {1: '连续变量', 2: '是否变量', 3: '有序分类', 4: '无序分类'}
        if type not in type_dict:
            raise ValueError('请输入正确的参数（1-4）')
        if name not in self.columns:
            raise ValueError(f'输入的变量名不在数据中\n变量名：{list(self.columns)}')
        self.df_type[name] = type

    def cat_missing(self, series):
        na_count = len(series)-series.count()  # 缺失值个数
        var_count = series.value_counts()
        if int(na_count) > math.ceil(0.05*var_count.min()):
            print('缺失值过多，用“None”填充')
            return series.fillna('None')
        elif int(na_count) == 0:
            print('无缺失值')
            return series
        else:
            print('缺失值用众数填充')
            print(str(series.mode()[0]))
            return series.fillna(str(series.mode()[0]))

    def con_missing(self, series):
        series = series.astype('float')
        if series.count() <= 0.95*len(series):
            print('该连续变量缺失值个数超过5%，但仍然填充平均值')
        return series.fillna(series.mean())

    def missing(self, names=[]):
        if not names:
            print('未输入任何变量名，对所有变量进行缺失值处理')
            names = list(self.columns)
        for name in names:
            t = self.df_type[name]
            print(name)
            if t == 1:
                self.df[name] = self.con_missing(self.df[name])
            elif t == 2 or t == 3 or t == 4:
                self.df[name] = self.cat_missing(self.df[name])
            else:
                print('该变量没有定义数据类型，暂不处理')

    def con_extreme(self, series):
        '''连续变量极端值
        '''
        # 正态分布数据
        series = series.astype('float')
        if kstest(series.dropna(), 'norm')[1] > 0.05:
            print('正态分布数值变量')
            mean = series.mean()
            std = series.std()
            max = mean+3*std
            min = mean-3*std
        # 非正态分布数据
        else:
            print('非正态分布数值变量')
            Q1 = series.quantile(q=0.25)
            Q3 = series.quantile(q=0.75)
            max = Q1 + 1.5 * (Q3 - Q1)
            min = Q1 - 1.5 * (Q3 - Q1)
        s = series[series.map(lambda x:min <= x <= max)]
        max = s.max()
        min = s.min()
        return series.map(lambda x: x if min <= x <= max else max if x > max else min)

    def extreme(self, names=[]):
        if not names:
            print('未输入任何变量名，对所有连续变量进行极端值处理')
            names = [i[0] for i in self.df_type.items() if i[1] == 1]
        for name in names:
            t = self.df_type[name]
            if t == 1:
                print(name)
                self.df[name] = self.con_extreme(self.df[name])
            elif t == 2 or t == 3 or t == 4:
                pass
            else:
                print(name)
                print('该变量没有定义数据类型，暂不处理')

    def order(self, name='', order_list=[]):
        self.order_dict[name] = order_list

    def recode(self, names=[]):
        '''重新编码
        '''
        if not names:
            print('未输入任何变量名，对所有分类变量重编码')
            names = [i[0] for i in self.df_type.items() if i[1] ==
                     2 or i[1] == 3 or i[1] == 4]
        for name in names:
            t = self.df_type[name]
            print(name)
            if t == 2:
                j = 0
                print('是否变量')
                index_dict = {}
                orders = self.order_dict[name]
                orders.append('None')
                for o in self.order_dict[name]:
                    index_dict[o] = j
                    j += 1
                self.df[name] = self.df[name].map(
                    lambda x: index_dict[x]).astype('str')
            if t == 3:
                j = 1
                print('有序分类变量')
                index_dict = {}
                orders = self.order_dict[name]
                orders.append('None')
                for o in self.order_dict[name]:
                    index_dict[o] = j
                    j += 1
                self.df[name] = self.df[name].map(
                    lambda x: index_dict[x]).astype('str')
            if t == 4:
                print('无序分类变量')
                self.df[name] = self.df[name].astype(
                    'category').cat.codes.astype('str')

    def dummy(self, names=[]):
        if not names:
            print('未输入任何变量名，所有分类变量生成哑变量')
            names = [i[0] for i in self.df_type.items() if i[1] ==
                     2 or i[1] == 3 or i[1] == 4]
        else:
            if not set(names).issubset(set(self.columns)):
                raise ValueError(f'输入的变量名不在数据中\n变量名：{list(self.columns)}')
        self.df = pd.get_dummies(self.df)

    def dirty(self, dirty_dict={}):
        for name, value in dirty_dict.items():
            self.df = self.df[self.df[name] != value]

    def deal(self):
        self.missing()
        self.extreme()
        self.recode()
        self.dummy()
