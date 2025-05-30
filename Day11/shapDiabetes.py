import streamlit as st 
import shap  
import matplotlib.pyplot as plt  
from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split 
import pandas as pd  
import numpy as np  
from streamlit_shap import st_shap 

# @st.cache_resource: 
# - 이 부분은 시간이 오래 걸리는 작업을 저장해두는 기능
# - 한 번 실행한 결과를 저장해두고 다음에 필요할 때 다시 사용
@st.cache_resource
def load_model_and_data():
    # 당뇨병 환자의 데이터를 가져옵니다
    # X: 환자의 여러가지 정보(나이, 혈압 등)
    # y: 당뇨병의 진행 정도
    X, y = shap.datasets.diabetes()
    
    # 가져온 데이터를 두 부분으로 나눕니다
    # - X_train, y_train: AI를 학습시키는 데 사용할 데이터 (80%)
    # - X_test, y_test: AI가 얼마나 잘 학습했는지 테스트할 데이터 (20%)
    # - random_state=42: 항상 같은 방식으로 데이터가 나누어지도록 하는 설정
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # AI 모델(랜덤 포레스트)을 만들고 학습시킵니다
    # - n_estimators=100: 100개의 작은 판단 규칙들을 만들어서 사용합니다
    # - random_state=42: 항상 같은 방식으로 학습하도록 하는 설정
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)  # 실제로 AI가 데이터를 보고 학습하는 과정
    
    # AI의 판단 과정을 설명할 수 있는 도구를 준비합니다
    # - explainer: AI의 판단을 설명해주는 도구
    # - shap_values: 각각의 정보가 얼마나 중요했는지 계산한 값
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    return model, X_train, X_test, y_train, y_test, shap_values, explainer



model, X_train, X_test, y_train, y_test, shap_values, explainer = load_model_and_data()

st.title("streamlit-shap로 Streamlit 앱에서 SHAP 플롯 표시하기")

with st.expander('앱에 대하여'):
    st.markdown('''
                shap 사용해보기
                ''')

st.header('입력데이터')

with st.expander('데이터에 대하여'):
    st.write('예시 데이터셋으로 당뇨병 데이터 사용')

with st.expander('X'):
    # 학습 데이터의 특성(X_train)을 테이블 형태로 표시
    st.dataframe(X_train)   
with st.expander('Y'):
    # 학습 데이터의 타겟값(y_train)을 테이블 형태로 표시
    st.dataframe(y_train)
    
st.header('SHAP 출력')

# TreeExplainer를 사용하여 모델의 예측을 설명하는 도구를 생성
# RandomForest 모델이 당뇨병 진행 정도를 예측하는 방식을 해석
explainer = shap.TreeExplainer(model)

# 테스트 데이터에 대한 SHAP 값을 계산
# SHAP 값은 각 특성이 예측에 얼마나 기여했는지를 보여줌
shap_values = explainer(X_test)

# 워터폴 플롯
with st.expander('워터폴 플롯'):
    # - 한 환자의 예측값에 대해 각 특성이 어떻게 기여했는지 보여줌
    # - height=300은 플롯의 높이를 300픽셀로 설정
    st_shap(shap.plots.waterfall(shap_values[0]), height=300)

# 비스웜 플롯
with st.expander('비스웜 플롯'):
    # - 전체 테스트 데이터에 대한 SHAP 값의 분포를 보여줌
    # - 각 특성이 모델의 예측에 미치는 전반적인 영향을 시각화
    # - 빨간색은 특성값이 높음을, 파란색은 낮음을 의미함
    st_shap(shap.plots.beeswarm(shap_values), height=300)


































