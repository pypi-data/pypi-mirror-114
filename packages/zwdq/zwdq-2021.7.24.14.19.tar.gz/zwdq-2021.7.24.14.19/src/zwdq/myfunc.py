import numpy as np
import pandas as pd
from math import sqrt
import os
import datetime

# 百分数脱敏
def ratio_tuomin(x):
    # x是百分比的数字部分,即比例*100,比如是54.3%的,即为54.3,要把它脱敏变成55
    # 精度这里我建议我们按照2、5、7、10 进行分割，选择绝对止值距离较近的那一档，举个🌰，
    # 1.13% ➡️12%、9.12% ➡️10%、43.53% ➡️45%。你看看可以吗～
    # 非个位数的
    def mymap(x):
        if 0 <= x < 1: x = 0
        elif 1 <= x < 3.5: x = 2
        elif 3.5 <= x < 6: x = 5
        elif 6 <= x < 8.5: x = 7
        else : x = 10
        return x
    flag = -1 if x < 0 else 1
    x = abs(x)
    if x > 10:
        first_num = x // 10
        second_num = x % 10 
        return flag * (first_num * 10 + mymap(second_num))
    else:
        return flag * mymap(x)

# 根据起始、终止时间切分df表的，返回的是历史时期某一列的nparray数组
def get_his_y_values(mydata,x,y,time_begin,time_end):
    y_his = mydata[ (mydata[ x ] >= time_begin) & (mydata[ x ] <= time_end) ][ y ].values
    return y_his

# 这个是算两个列表绝对差异的 返回的第一个值是平均绝对差异，第二个值是最大绝对差异
def gap_func(list1,list2):
    n1 = len(list1)
    n2 = len(list2)
    # 一般起点一样终点不一样，切掉后面不一样的
    if n1 > n2:
        list1 = list1[:n2]
    else:
        list2 = list2[:n1]
    mygap_tmp = []
    for i in range(len(list1)):
        if list2[i] > 0:
            if abs((list1[i] - list2[i])/list2[i]) < 100:
                mygap_tmp.append((list1[i] - list2[i])/list2[i])
    # 计算绝对差异
    mygap = abs(np.array(mygap_tmp)).mean()
    # 计算极端差异
    try:
        mygap_max = abs(np.array(mygap_tmp)).max()
    except:
        print("极端差异计算报错，记为负1")
        mygap_max = -1
    return mygap,mygap_max

def getYesterday(): 
    today = datetime.date.today() 
    oneday = datetime.timedelta(days=1) 
    yesterday = today-oneday  
    tmp = str(yesterday)
    ans = tmp[:4] + tmp[5:7] + tmp[8:10]
    return ans


def get_holiday_qujian_date(myholiday_name):
    if myholiday_name == "同期国庆":
        h_begin = np.datetime64(datetime.datetime.strptime(str('2020-09-25'),'%Y-%m-%d').date())
        h_end   = np.datetime64(datetime.datetime.strptime(str('2020-10-10'),'%Y-%m-%d').date())
        a_begin = np.datetime64(datetime.datetime.strptime(str('2020-10-01'),'%Y-%m-%d').date())
        a_end   = np.datetime64(datetime.datetime.strptime(str('2020-10-07'),'%Y-%m-%d').date())
        b_begin = np.datetime64(datetime.datetime.strptime(str('2020-09-24'),'%Y-%m-%d').date())
        b_end   = np.datetime64(datetime.datetime.strptime(str('2020-09-30'),'%Y-%m-%d').date())
    if myholiday_name == "同期五一":
        h_begin = np.datetime64(datetime.datetime.strptime(str('2020-04-24'),'%Y-%m-%d').date())
        h_end   = np.datetime64(datetime.datetime.strptime(str('2020-05-09'),'%Y-%m-%d').date())
        a_begin = np.datetime64(datetime.datetime.strptime(str('2020-05-01'),'%Y-%m-%d').date())
        a_end   = np.datetime64(datetime.datetime.strptime(str('2020-05-05'),'%Y-%m-%d').date())
        b_begin = np.datetime64(datetime.datetime.strptime(str('2020-04-24'),'%Y-%m-%d').date())
        b_end   = np.datetime64(datetime.datetime.strptime(str('2020-04-30'),'%Y-%m-%d').date())
    if myholiday_name == "同期元旦":
        h_begin = np.datetime64(datetime.datetime.strptime(str('2020-12-24'),'%Y-%m-%d').date())
        h_end   = np.datetime64(datetime.datetime.strptime(str('2021-01-09'),'%Y-%m-%d').date())
        a_begin = np.datetime64(datetime.datetime.strptime(str('2021-01-01'),'%Y-%m-%d').date())
        a_end   = np.datetime64(datetime.datetime.strptime(str('2021-01-03'),'%Y-%m-%d').date())
        b_begin = np.datetime64(datetime.datetime.strptime(str('2020-12-25'),'%Y-%m-%d').date())
        b_end   = np.datetime64(datetime.datetime.strptime(str('2020-12-31'),'%Y-%m-%d').date())
    if myholiday_name == "同期618":
        h_begin = np.datetime64(datetime.datetime.strptime(str('2020-06-01'),'%Y-%m-%d').date())
        h_end   = np.datetime64(datetime.datetime.strptime(str('2020-06-20'),'%Y-%m-%d').date())
        a_begin = np.datetime64(datetime.datetime.strptime(str('2020-06-16'),'%Y-%m-%d').date())
        a_end   = np.datetime64(datetime.datetime.strptime(str('2020-06-18'),'%Y-%m-%d').date())
        b_begin = np.datetime64(datetime.datetime.strptime(str('2020-06-09'),'%Y-%m-%d').date())
        b_end   = np.datetime64(datetime.datetime.strptime(str('2020-06-15'),'%Y-%m-%d').date())
    if myholiday_name == "同期双11":
        h_begin = np.datetime64(datetime.datetime.strptime(str('2020-11-01'),'%Y-%m-%d').date())
        h_end   = np.datetime64(datetime.datetime.strptime(str('2020-11-20'),'%Y-%m-%d').date())
        a_begin = np.datetime64(datetime.datetime.strptime(str('2020-11-09'),'%Y-%m-%d').date())
        a_end   = np.datetime64(datetime.datetime.strptime(str('2020-11-11'),'%Y-%m-%d').date())
        b_begin = np.datetime64(datetime.datetime.strptime(str('2020-11-04'),'%Y-%m-%d').date())
        b_end   = np.datetime64(datetime.datetime.strptime(str('2020-11-10'),'%Y-%m-%d').date())
    if myholiday_name == "同期春节":
        h_begin = np.datetime64(datetime.datetime.strptime(str('2021-01-20'),'%Y-%m-%d').date())
        h_end   = np.datetime64(datetime.datetime.strptime(str('2021-02-25'),'%Y-%m-%d').date())
        a_begin = np.datetime64(datetime.datetime.strptime(str('2020-05-01'),'%Y-%m-%d').date())
        a_end   = np.datetime64(datetime.datetime.strptime(str('2020-05-05'),'%Y-%m-%d').date())
        b_begin = np.datetime64(datetime.datetime.strptime(str('2020-04-24'),'%Y-%m-%d').date())
        b_end   = np.datetime64(datetime.datetime.strptime(str('2020-04-30'),'%Y-%m-%d').date())
    return h_begin,h_end,a_begin,a_end,b_begin,b_end
