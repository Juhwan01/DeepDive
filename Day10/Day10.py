import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime

#load data
@st.cache
def load_data():
    '''
    pandas 버전별 차이:
        pandas 2.0 이상: format='mixed' 지원
        pandas 1.x 버전: format='mixed' 미지원
        
    '''
    
    # 첫 행은 total값이므로 버린다
    df_agg = pd.read_csv('Aggregated_Metrics_By_Video.csv').iloc[1:,:]

    # 컬럼 명이 이상하게 나올 수 있으니 그냥 재정의
    df_agg.columns = ['Video','Video title','Video publish time','Comments added','Shares','Dislikes','Likes',
                        'Subscribers lost','Subscribers gained','RPM(USD)','CPM(USD)','Average % viewed','Average view duration',
                        'Views','Watch time (hours)','Subscribers','Your estimated revenue (USD)','Impressions','Impressions ctr(%)']
    # string 값보다 유용한 datetime형으로 변환
    df_agg['Video publish time'] = pd.to_datetime(df_agg['Video publish time'],format='mixed')

    # 마찬가지로 평균 지속 시청 시간도 변환해준다
    df_agg['Average view duration'] = df_agg['Average view duration'].apply(lambda x:datetime.strptime(x,'%H:%M:%S'))

    # 임의로 만든 feature일뿐 이것이 좋은 인사이트를 주는지 안주는지는 해보면서 알아본다
    df_agg['Engagement_ratio'] =  (df_agg['Comments added'] + df_agg['Shares'] +df_agg['Dislikes'] + df_agg['Likes']) /df_agg.Views
    df_agg['Views / sub gained'] = df_agg['Views'] / df_agg['Subscribers gained']

    df_agg_sub = pd.read_csv('Aggregated_Metrics_By_Country_And_Subscriber_Status.csv')
    df_comments = pd.read_csv('Aggregated_Metrics_By_Video.csv')
    df_time = pd.read_csv('Video_Performance_Over_Time.csv')
    # 마찬가지로 변환
    df_time['Date'] = pd.to_datetime(df_time['Date'],format='mixed')
    
    return df_agg, df_agg_sub, df_comments, df_time

df_agg, df_agg_sub, df_comments, df_time = load_data()

df_agg_diff = df_agg.copy()
