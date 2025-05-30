# -*- coding: utf-8 -*-

import plotly.express as px
import pandas as pd
import json
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from streamlit_elements import(
    elements,
    dashboard,
    mui,
    editor,
    media,
    lazy,
    sync,
    nivo
    )

st.set_page_config(layout="wide")

# 각 지역의 중심 좌표 (위도, 경도) - 임시로 넣은 값(각 지역의 중앙 좌표값을 기준으로 함)
region_data = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '대구광역시': [35.8714, 128.6014],
    '인천광역시': [37.4563, 126.7052],
    '광주광역시': [35.1595, 126.8526],
    '대전광역시': [36.3504, 127.3845],
    '울산광역시': [35.5384, 129.3114],
    '세종특별자치시': [36.4800, 127.2890],
    '경기도': [37.4138, 127.5183],
    '강원특별자치도': [37.8228, 128.1555],
    '충청북도': [36.6357, 127.4914],
    '충청남도': [36.5184, 126.8000],
    '전북특별자치도': [35.7175, 127.1530],
    '전라남도': [34.8679, 126.9910],
    '경상북도': [36.4919, 128.8889],
    '경상남도': [35.4606, 128.2132],
    '제주특별자치도': [33.4996, 126.5312]
}

@st.cache_data
def load_data():
    # 필요 없는 헤더 컬럼 지우기
    df = pd.read_csv('인구수데이터.csv')[1:]
    # 전국 컬럼 버리고 reset_index로 인덱스 정리
    df = df[df['행정구역(시군구)별']!='전국'].reset_index(drop=True)
    return df


def create_map(df, selected_year,select_sex):
    population_col=''
    selected_year = selected_year+'.01'
    # 선택된 월에 따른 데이터 컬럼 매핑 사용 입력 값을 사이드바에서 받아올 것이기 때문에
    if select_sex == "남성":
        population_col = selected_year + '.1'  
    elif select_sex == "여성":
        population_col = selected_year + '.2'
    elif select_sex == "남성+여성":
        population_col = selected_year
    st.write("찾으려는 컬럼명:", population_col)
    st.dataframe(df[['행정구역(시군구)별', population_col]].head())
    # 사이드바에서 선택된(ex.2월) 컬럼에 맞는 인구수 값을 int로 형변환
    df['population'] = df[population_col].astype(int)  # 인구수 정수형 변환(필수->나중에 이걸로 계산해야함)
    # 각 지역의 위도/경도 매핑 사용
    # x값은 행정구역(시군구)별로 해서 map함수 사용 -> 각각 region에 맞는 좌표 값을 위도,경도에 매핑해 줌
    df['lat'] = df['행정구역(시군구)별'].map(lambda x: region_data.get(x, [0, 0])[0])  
    df['lon'] = df['행정구역(시군구)별'].map(lambda x: region_data.get(x, [0, 0])[1])
    
    # 인구수에 따른 상대적 버블 크기 계산 사용 - 버블 사이즈를 구하는 공식(Min-Max 정규화 사용함)
    # 공식: 10 + (현재인구 - 최소인구) / (최대인구 - 최소인구) * 50
    # ├─ 10: 최소 버블 크기 (가장 작은 지역도 보이도록)
    # ├─ (현재인구 - 최소인구): 최소값 기준으로 조정 (0부터 시작)
    # ├─ / (최대인구 - 최소인구): 전체 범위로 나누기 (0~1 정규화)
    # ├─ * 50: 0~50 범위로 확장
    # └─ 결과: 10~60 크기 (최소 10, 최대 60)
    max_pop, min_pop = df['population'].max(), df['population'].min()
    df['bubble_size'] = 10 + (df['population'] - min_pop) / (max_pop - min_pop) * 100
    # 근데 이게 비율 값이라 그런지 남성 여성 나눠서 해도 그렇게 큰차이를 보이는거 같지는 않습니다
    
    # Plotly를 활용한 지도 시각화 생성
    fig = go.Figure(go.Scattermapbox(
    lat=df['lat'],
    lon=df['lon'],
    mode='markers',
    marker=dict(
            size=df['bubble_size'],
            color='#FF6B6B',
            opacity=0.7
        ),
        text=df['행정구역(시군구)별']
    ))
        
    # 지도 레이아웃 설정
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',  # 지도 스타일 설정
            center=dict(lat=36.5, lon=127.5),  # 지도 중심점 설정
            zoom=6.8  # 줌 레벨 설정
        ),
        height=600,  # 지도 높이 설정
        margin=dict(t=0, b=0, l=0, r=0)  # 여백 설정
    )
    return fig  # 생성된 지도 반환


with st.sidebar:
    st.title("행정구역별 인구수 시각화")
    st.header("설정값")
    st.write("STreamlit Elements를 사용하여 드래그 가능하고 크기 조절 가능한 대시보드 만들기")
    st.write("---")
    select_year = st.selectbox("연도 선택",["2016","2017","2018","2019","2020","2021","2022","2023","2024","2025"])
    select_sex = st.selectbox("성별",["남성+여성","남성","여성"])
    
df = load_data()
fig=create_map(df, select_year, select_sex)
st.plotly_chart(fig)