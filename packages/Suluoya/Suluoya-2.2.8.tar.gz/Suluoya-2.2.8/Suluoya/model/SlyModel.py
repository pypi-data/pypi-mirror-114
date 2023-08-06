import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math



def normalize(x):
    '''
    Func:归一化\n
    In:dataframe\n
    Out:dataframe
    '''
    return x.apply(lambda x: ((x - np.min(x)) / (np.max(x) - np.min(x))))


def standarlize(df):
    '''
    Func:标准化->每一个元素/其所在列的元素的平方和的1/2次方\n
    IN:dataframe\n
    OUT:dataframe
    '''

    return df/((df**2).sum())


def entropy_weight(df):
    '''
    Func:熵权法计算权重\n
    In:dataframe各指标数据\n
    Out:series各指标权重
    '''
    df = normalize(df)
    # 求k
    k = 1 / math.log(df.index.size)
    # 信息熵
    df_p = df/df.sum()
    df_inf = -np.log(df_p).replace([np.inf, -np.inf], 0)*df_p*k
    # 计算冗余度
    redundancy = 1 - df_inf.sum()
    # 计算各指标的权重
    weights = redundancy/redundancy.sum()
    return weights


class Topsis(object):
    '''
    Func:Topsis\n
    IN:dataframe各指标数据\n
    OUT:dataframe
    '''

    def __init__(self, df):
        self.df = df

    def direction(self, col, type=1, best_value=0, range=(0, 1)):
        '''
        type=0 --> 极大型，越大越好\n
        type=1 --> 极小型，越小越好\n
        type=2 --> 中间型，接近某个值越好，需传入best_value\n
        type=3 --> 区域型，落在某个区间越好，需传入range
        '''
        def rgnl(x):
            min_value = range[0]
            max_value = range[1]
            M = max(min_value-np.min(self.df[col]),
                    np.max(self.df[col])-max_value)
            if x < min_value:
                return 1-(min_value-x)/M
            elif x > max_value:
                return 1-(x-max_value)/M
            else:
                return 1
        if type == 1:
            self.df[col] = np.max(self.df[col])-self.df[col]
        elif type == 2:
            self.df[col] = 1-abs(self.df[col]-best_value) / \
                np.max(abs(self.df[col]-best_value))
        elif type == 3:
            self.df[col] = self.df[col].map(lambda x: rgnl(x))

    def score(self, weights=[]):
        '''
        计算得分并归一化
        weights --> 按顺序传入指标权重
        OUT:series每个样本的分数
        '''
        self.df = standarlize(self.df)
        series_max = self.df.max()
        series_min = self.df.min()
        if weights == []:
            weights = np.ones(self.df.columns.size)/self.df.columns.size
        D_max = ((weights*((self.df-series_max)**2)).sum(axis=1))**(1/2)
        D_min = ((weights*((self.df-series_min)**2)).sum(axis=1))**(1/2)
        D = D_min/(D_min+D_max)
        return D/D.sum()


def entropy_weight_topsis(df):
    '''
    Func:基于熵权法修正的topsis评分\n
    IN:dataframe\n
    OUT:seires\n
    types --> list，每个指标的类型
    '''
    t = Topsis(df)
    i = 0
    types = list(entropy_weight(df))
    for column in t.df.columns:
        t.direction(column, types[i])
        i += 1
    return t.score(list(entropy_weight(df)))


def grey_relation(df, rho=0.05, mother_series=False):
    '''
    Func:灰色关联\n
    IN:dataframe原始数据\n
    OUT:series每个样本的评分\n
    rhp --> 关联度一般为0.05\n
    mother_series --> 母序列，默认为空
    '''
    df = df/df.mean()
    if mother_series==[]:
        seires_max = df.max()
    df = np.abs(df - seires_max)
    min = df.min()
    max = df.max()
    return ((min+rho*max)/(df+rho*max)).sum(axis=1)/df.columns.size


if __name__ == '__main__':
    test_dict = {'A': [9, 3, 2, 4], 'B': [
        3, 5, 7, 8], 'C': [10, 4, 8, 9], }
    test_df = pd.DataFrame(test_dict)
    t = grey_relation(test_df)
    print(t)
