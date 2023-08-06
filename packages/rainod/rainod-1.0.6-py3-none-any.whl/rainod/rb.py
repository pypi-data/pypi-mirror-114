import pandas as pd
import numpy as np
from haversine import haversine

def test():
    print("곽운일, 심명진, 김도영, 편도준")

def test2():
    t = pd.DataFrame(data=[1,2,3])
    display(t)

def t_csv(x,y,z):
    if y==40:
        x.to_csv('land40_{}.csv'.format(z),encoding='cp949')
    if y==4070:
        x.to_csv('land40_70_{}.csv'.format(z),encoding='cp949')
    if y==70:
        x.to_csv('land70_{}.csv'.format(z),encoding='cp949')

def make_distance(x,y,name):
    df = pd.DataFrame()
    
    for i in range(len(x)):
        for j in range(len(y)):
            distance = haversine(x.loc[:,['위도','경도']].values[i],
                                 y.loc[:,['위도','경도']].values[j],
                                 unit = 'km')
            if distance <= 1:
                new_data ={'아파트' : x['주소'].values[i],
                           '거리' : distance}
                df = df.append(new_data,ignore_index=True)
                
    df = df.groupby(['아파트']).agg(['count', 'mean']).reset_index()
    df.columns=['주소', name+' 개수', name+' 평균거리']
    apt_df = pd.merge(x, df, left_on = '주소', right_on = '주소', how = 'left')
    return apt_df