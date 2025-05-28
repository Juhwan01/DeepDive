import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime


#Define Functions 
#데이터 프레임 스타일링을 위한 함수들/try-except 블록은 숫자가 아닌 값(문자열, NaN 등)에 대해 비교 연산이 실패할 경우를 대비한 에러 처리입니다.
def style_negative(v, props=''):
    """ 
    음수 값을 가진 셀에 스타일을 적용
    v < 0이면 지정된 props (CSS 속성) 반환
    양수이거나 0이면 None 반환 (스타일 적용 안함)
    """
    try: 
        return props if v < 0 else None
    except:
        pass
    
def style_positive(v, props=''):
    """
    양수 값을 가진 셀에 스타일을 적용
    v > 0이면 지정된 props (CSS 속성) 반환
    음수이거나 0이면 None 반환 (스타일 적용 안함)
    """
    try: 
        return props if v > 0 else None
    except:
        pass

#load data
# streamlit 문법 변경
@st.cache_data
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
    # 판다스 버전 변경에 따른 문법 변경
    df_agg['Video publish time'] = pd.to_datetime(df_agg['Video publish time'],format='mixed')

    # 마찬가지로 평균 지속 시청 시간도 변환해준다
    df_agg['Average view duration'] = df_agg['Average view duration'].apply(lambda x:datetime.strptime(x,'%H:%M:%S'))

    # 임의로 만든 feature일뿐 이것이 좋은 인사이트를 주는지 안주는지는 해보면서 알아본다
    df_agg['Avg_duration_sec'] = df_agg['Average view duration'].apply(lambda x: x.second + x.minute*60 + x.hour*3600)
    df_agg['Engagement_ratio'] =  (df_agg['Comments added'] + df_agg['Shares'] +df_agg['Dislikes'] + df_agg['Likes']) /df_agg.Views
    df_agg['Views / sub gained'] = df_agg['Views'] / df_agg['Subscribers gained']

    df_agg_sub = pd.read_csv('Aggregated_Metrics_By_Country_And_Subscriber_Status.csv')
    df_comments = pd.read_csv('Aggregated_Metrics_By_Video.csv')
    df_time = pd.read_csv('Video_Performance_Over_Time.csv')
    
    # 마찬가지로 변환
    # 판다스 버전 변경에 따른 문법 변경
    df_time['Date'] = pd.to_datetime(df_time['Date'],format='mixed')
    
    return df_agg, df_agg_sub, df_comments, df_time

df_agg, df_agg_sub, df_comments, df_time = load_data()

df_agg_diff = df_agg.copy()

metric_date_12mo = df_agg_diff['Video publish time'].max() - pd.DateOffset(months=12)

# 판다스 버전 변경에 따른 문법 변경 numeric_only=True 작성해야함
median_agg = df_agg_diff[df_agg_diff['Video publish time'] >= metric_date_12mo].median(numeric_only=True)

# 판다스 버전 변경에 따른 문법 변경
# (값 - 중앙값) / 중앙값 = 상대 변화율 (relative change)
numeric_df = df_agg_diff.select_dtypes(include=['float64', 'int64'])
df_agg_diff[numeric_df.columns] = (numeric_df - median_agg).div(median_agg)


add_sidebar = st.sidebar.selectbox('Aggregate or Individual Video', ('Aggregate Metrics','Individual Video Analysis'))

# df_agg_metrics에서 'Video publish time' 제거 - 숫자 컬럼만 median 계산에 사용, median() 함수는 datetime 컬럼에 대해 Timestamp를 반환하는데, delta를 계산할 때 Timedelta를 Timestamp로 나누려고 해서 지원되지 않는 연산이 됩니다.
if add_sidebar == 'Aggregate Metrics':
    # 제일 최근날짜(max값 날짜)에서 DateOff
    df_agg_metrics = df_agg[['Video publish time','Views','Likes','Subscribers','Shares','Comments added','RPM(USD)','Average % viewed',
                             'Avg_duration_sec', 'Engagement_ratio','Views / sub gained']]
    metric_date_6mo = df_agg_metrics['Video publish time'].max() - pd.DateOffset(months=6)
    metric_date_12mo = df_agg_metrics['Video publish time'].max() - pd.DateOffset(months=12)
    metric_medians6mo = df_agg_metrics[df_agg_metrics['Video publish time'] >= metric_date_6mo].median()
    metric_medians12mo = df_agg_metrics[df_agg_metrics['Video publish time'] >= metric_date_12mo].median()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    # 행에 따른 각 열을 다시 생성하지 않고도 그 위에 쌓는 식으로 로직을 작성
    count = 0
    # 원본 코드에는 계산이 불가능한 컬럼 까지 포함되어 있음 슬라이싱을통한 컬럼 삭제
    for i in metric_medians6mo.index[1:]:
        with columns[count]:
            delta = (metric_medians6mo[i] - metric_medians12mo[i])/metric_medians12mo[i]
            st.metric(label= i, value = round(metric_medians6mo[i],1), delta = "{:.2%}".format(delta))
            count += 1
            if count >= 5:
                count = 0
    # lambda 함수로 date()변환을 간단히 시켜줌
    df_agg_diff['Publish_date'] = df_agg_diff['Video publish time'].apply(lambda x:x.date())
    df_agg_diff_final = df_agg_diff.loc[:,['Video title','Publish_date','Views','Likes','Subscribers','Shares','Comments added','RPM(USD)','Average % viewed',
                             'Avg_duration_sec', 'Engagement_ratio','Views / sub gained']]
    
    # df_agg_diff_final에서 median을 계산할 수 있는 숫자 컬럼들의 이름을 리스트로 가져옴
    df_agg_numeric_lst = df_agg_diff_final.median(numeric_only=True).index.tolist()
    df_to_pct = {}
    for i in df_agg_numeric_lst:
        # '{:.1%}'.format는 소수점 1자리 퍼센트 형식으로 변환하는 함수
        # 각 숫자 컬럼명을 키로, 포맷 함수를 값으로 저장 '{:.1%}'.format는 함수 객체 자체를 저장 (호출하지 않음)
        df_to_pct[i] = '{:.1%}'.format
        
        
    # 함수정의 define위에 되어 있는거 사용하는 방법(applymap은 데이터프레임의 각 셀에 함수를 적용할 때 사용하는 방법)
    # pandas가 알아서 매칭해서 적용(딕셔너리 안에 컬럼별 함수들)
    st.dataframe(df_agg_diff_final.style.hide().applymap(style_negative, props='color:red;').applymap(style_positive, props='color:green;').format(df_to_pct))
if add_sidebar == 'Individual Video Analysis':
    st.write('제작중')







































