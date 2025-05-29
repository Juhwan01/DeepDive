import streamlit as st 
import shap  
import matplotlib.pyplot as plt  
from sklearn.ensemble import RandomForestRegressor 
from sklearn.model_selection import train_test_split 
import pandas as pd  
import numpy as np  

# @st.cache_resource: 
# - 이 부분은 시간이 오래 걸리는 작업을 저장해두는 기능입니다
# - 한 번 실행한 결과를 저장해두고 다음에 필요할 때 다시 사용합니다
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

# @st.cache_data:
# - 계산 결과를 저장해두는 기능입니다
# - 같은 입력값으로 다시 계산하지 않도록 해줍니다
# - 앱의 속도를 빠르게 해주는 역할을 합니다
@st.cache_data
def evaluate_model(_model, X_test, y_test):
    # _model 앞에 _를 붙인 이유:
    # - AI 모델은 너무 복잡해서 그대로 저장하기 어렵습니다
    # - _를 붙여서 이 정보는 저장하지 말라고 알려주는 것입니다
    
    # AI 모델로 예측을 수행합니다
    predictions = _model.predict(X_test)
    
    # AI가 얼마나 정확하게 예측했는지 계산합니다
    # MSE: 예측한 값과 실제 값의 차이를 제곱한 평균
    mse = np.mean((predictions - y_test) ** 2)
    
    # RMSE: MSE의 제곱근 값
    # - MSE를 조금 더 이해하기 쉬운 숫자로 바꾼 것입니다
    rmse = np.sqrt(mse)
    
    # R²: AI의 예측이 얼마나 정확한지 나타내는 점수 (0~1점)
    # - 1점에 가까울수록 정확하다는 의미입니다
    r2 = _model.score(X_test, y_test)
    
    return predictions, mse, rmse, r2


st.title('당뇨병 진행도 예측 모델 분석')

model, X_train, X_test, y_train, y_test, shap_values, explainer = load_model_and_data()


predictions, mse, rmse, r2 = evaluate_model(model, X_test, y_test)