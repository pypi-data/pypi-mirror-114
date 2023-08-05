import os
import pandas as pd
import numpy as np

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

import gensim
import lightgbm as lgb

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
from sklearn import preprocessing

from collections import Counter
from functools import reduce
import datetime


# 一些个人方法封装
class api():
    def __init__(self):
        pass
    
    def p(self, x):
        print(x)
        
    def os_analysis(self):
        from multiprocessing import cpu_count
        print("\nCPU的核数为：{}\n".format(cpu_count()))
    
    # 数据表情况观察
    def df_analysis(df):
        print("\n**************** DF Analysing ****************\n")
        print("shape of df is : {}".format(df.shape))
        print("")
        print("df memory : {:.2f} KB".format(df.memory_usage().sum()/(1024**1)))
        print("df memory : {:.2f} MB".format(df.memory_usage().sum()/(1024**2)))
        print("df memory : {:.2f} GB".format(df.memory_usage().sum()/(1024**3)))
        #print("info of df is :{}".format(df.info()))

        
        #print("\nhas null col : {}".format(x[x==True].index.tolist()))
        #print("notnull col : {}".format(x[x==False].index.tolist()))
        print("")
        tmp = pd.DataFrame({
            "null_ratio":df.isnull().sum(axis=0)/len(df),
            "null_num":df.isnull().sum(axis=0),
            "total_rows":df.shape[0],}).query('null_ratio > 0')  
        tmp["null_ratio"] = tmp["null_ratio"].apply(lambda x:str(round(100*x,2))+"%")
        print(tmp)
        print("")
        
        #print("\ndescribe of df is:\n{}\n".format(df.describe()))
        #print("head5 of df is :{}".format(df.head()))
        print("\n*************** Analysis Finished ************\n")

    # 做item2vec的序列处理，返回列表
    def get_item_query_list(self, df):
        def myreduce(list_input):
            return reduce(lambda x,y:str(x)+","+str(y), list_input)
        df["photo_id"] = df["photo_id"].astype(str)
        df = df.sort_values(by=["user_id","photo_rank"])
        item_query_df = df.groupby("user_id")["photo_id"].apply(myreduce)
        #print(item_query_df)
        query_list = []
        for i,c in item_query_df.items():
            if len(c) > 1:
                query_list.append(c.split(","))
            else:
                query_list.append(list(c))
        return query_list


    # 输入上述所出序列，输出物品向量模型和数据集
    def item2vec(self, list, min_count=1, size=3):
        model = gensim.models.Word2Vec(list, min_count=min_count, vector_size=size, seed=2021, workers=1)
        item2vec_df = pd.DataFrame(model.wv.vectors, index=model.wv.index_to_key)
        item2vec_df["photo_id"] = item2vec_df.index
        return model, item2vec_df


    # 最后的特征宽表中,photo_id换成item2vec，size是多少，就多几列
    def data_input_item2vec(self, data_input, item2vec_df):
        data_input["photo_id"] = data_input["photo_id"].astype(int)
        item2vec_df["photo_id"] = item2vec_df["photo_id"].astype(int)
        data_input = pd.merge(left=data_input, right=item2vec_df, how="left", on="photo_id")
        data_input.drop(columns="photo_id", inplace=True)
        return data_input

    '''
    # 为方便流式处理，定义模型方法
    def model_auto_load():
        import os
        if os.path.exists("lgb_model.txt"):
            # 模型加载
            gbm = lgb.Booster(model_file='lgb_model.txt')
        else:
            pass
    '''

    # 计算dtw值，没有除以k步
    def DTWDistance(self, s1, s2):
        DTW={}

        for i in range(len(s1)):
            DTW[(i, -1)] = float('inf')
        for i in range(len(s2)):
            DTW[(-1, i)] = float('inf')
        DTW[(-1, -1)] = 0

        for i in range(len(s1)):
            for j in range(len(s2)):
                dist= (s1[i]-s2[j])**2
                DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])

        return sqrt(DTW[len(s1)-1, len(s2)-1])

    # 建立目录
    def mkdir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
    # 清楚目录
    def rmdir(slef, directory):
        for root, dirs, files in os.walk(directory):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    # 网格搜索，参数优化
    def lgb_cv(self, x_train, y_train):
        cv_params = {
                'n_estimators':[100],
                'max_depth':range(2,15,1),
                'learning_rate':np.linspace(0.01,0.1,10),
                #'subsample':np.linspace(0.7,0.9,20),
                #'colsample_bytree':np.linspace(0.5,0.98,10),
                #'min_child_weight':range(1,9,1)
                }
        estimator = lgb.LGBMClassifier()

        gbm = GridSearchCV(estimator, cv_params, verbose=1, n_jobs=-1)
        gbm.fit(x_train, y_train.values.ravel(), verbose=2)
        print('Best parameters found by gr id search are:', gbm.best_params_)

    def plot(self, x, y, title="temp", label="deafault"):

        # 处理绘图格式
        plt.style.use("ggplot")
        # plt.style.use('fivethirtyeight')

        plt.figure(figsize=(20, 10))

        # 百分比处理
        def to_percent(temp, position):
            return "%.0f" % (100 * temp) + "%"

        plt.title(title)
        plt.plot(x, y, ls="-", color="darkorange", linewidth=1.5, label=label)

        plt.legend(loc="upper left", fontsize=12, frameon=False, ncol=1)
        plt.grid(axis="y", color="lightgray", linestyle="--", linewidth=0.5)

        extent = [
            mdates.date2num(min(x)), mdates.date2num(max(x)),
            #min(x), max(x),
            min(y), max(y),
        ]
        _, yv = np.meshgrid(np.linspace(0, 1, 210), np.linspace(0, 1, 90))
        plt.imshow(
            yv, cmap=plt.cm.Blues,
            origin="lower", alpha=0.6,
            aspect="auto", extent=extent,
        )
        plt.fill_between(x, y, max(y), color="white")
        plt.show() 




