# =============================================================================
# 당뇨병 데이터 전처리 - Step by Step (Plotly 시각화)
# =============================================================================

# 1. 라이브러리 임포트
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Plotly 설정
import plotly.io as pio
pio.renderers.default = "notebook"  # Jupyter notebook에서 사용시

print("라이브러리 임포트 완료! 🎉")

# =============================================================================
# Step 1: 데이터 로드 및 기본 탐색
# =============================================================================

# 데이터 로드
df = pd.read_csv('diabetes_train.csv')

print("=== 데이터 기본 정보 ===")
print(f"데이터 크기: {df.shape}")
print(f"컬럼 수: {df.shape[1]}")
print(f"행 수: {df.shape[0]:,}")

# 첫 5행 확인
print("\n=== 첫 5행 미리보기 ===")
df.head()

# =============================================================================
# Step 2: 데이터 타입 및 결측값 확인
# =============================================================================

print("=== 데이터 타입 정보 ===")
print(df.dtypes)

print("\n=== 결측값 확인 ===")
missing_values = df.isnull().sum()
print(f"총 결측값: {missing_values.sum()}")

if missing_values.sum() == 0:
    print("✅ 결측값이 없습니다!")
else:
    print("결측값이 있는 컬럼:")
    print(missing_values[missing_values > 0])

print("\n=== 중복값 확인 ===")
duplicates = df.duplicated().sum()
print(f"중복 행 수: {duplicates}")

# =============================================================================
# Step 3: 타겟 변수 (당뇨병) 분포 확인
# =============================================================================

print("=== 타겟 변수 분포 ===")
target_dist = df['Diabetes_binary'].value_counts()
target_ratio = df['Diabetes_binary'].value_counts(normalize=True) * 100

print("당뇨병 없음 (0):", f"{target_dist[0]:,}개 ({target_ratio[0]:.1f}%)")
print("당뇨병 있음 (1):", f"{target_dist[1]:,}개 ({target_ratio[1]:.1f}%)")

# 클래스 불균형 시각화 - Plotly
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "pie"}, {"type": "bar"}]],
    subplot_titles=['당뇨병 분포 (파이차트)', '당뇨병 분포 (막대그래프)']
)

# 파이차트
fig.add_trace(
    go.Pie(
        labels=['정상', '당뇨'],
        values=target_dist.values,
        name="당뇨병 분포",
        textinfo='label+percent',
        marker=dict(colors=['lightblue', 'lightcoral'])
    ),
    row=1, col=1
)

# 막대그래프
fig.add_trace(
    go.Bar(
        x=['정상 (0)', '당뇨 (1)'],
        y=target_dist.values,
        name="개수",
        marker=dict(color=['lightblue', 'lightcoral']),
        text=target_dist.values,
        textposition='auto'
    ),
    row=1, col=2
)

fig.update_layout(
    title_text="당뇨병 타겟 변수 분포",
    height=400,
    showlegend=False
)

fig.show()

# =============================================================================
# Step 4: 각 변수 유형 분류 및 분포 확인
# =============================================================================

# 변수 유형별 분류
binary_cols = ['Diabetes_binary', 'HighBP', 'HighChol', 'CholCheck', 'Smoker', 
               'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 
               'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk']

continuous_cols = ['BMI', 'MentHlth', 'PhysHlth']

categorical_cols = ['Sex', 'Age', 'Education', 'Income', 'GenHlth']

other_cols = ['id']

print("=== 변수 유형 분류 ===")
print(f"이진 변수 ({len(binary_cols)}개): {binary_cols}")
print(f"연속형 변수 ({len(continuous_cols)}개): {continuous_cols}")
print(f"범주형 변수 ({len(categorical_cols)}개): {categorical_cols}")
print(f"기타 ({len(other_cols)}개): {other_cols}")

# 각 변수의 고유값 개수 확인
print("\n=== 각 변수의 고유값 개수 ===")
for col in df.columns:
    unique_count = df[col].nunique()
    unique_values = sorted(df[col].unique())
    print(f"{col}: {unique_count}개 고유값 - {unique_values}")

# =============================================================================
# Step 5: 연속형 변수 분포 및 이상치 확인
# =============================================================================

print("=== 연속형 변수 기술통계 ===")
continuous_stats = df[continuous_cols].describe()
print(continuous_stats)

# 연속형 변수 히스토그램 - Plotly
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=[f'{col} 분포' for col in continuous_cols]
)

colors = ['lightblue', 'lightgreen', 'lightcoral']

for i, (col, color) in enumerate(zip(continuous_cols, colors)):
    fig.add_trace(
        go.Histogram(
            x=df[col],
            name=col,
            nbinsx=50,
            marker=dict(color=color, line=dict(color='black', width=1)),
            opacity=0.7
        ),
        row=1, col=i+1
    )

fig.update_layout(
    title_text="연속형 변수 분포",
    height=400,
    showlegend=False
)

fig.update_xaxes(title_text="값")
fig.update_yaxes(title_text="빈도")

fig.show()

# 박스플롯으로 이상치 확인 - Plotly
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=[f'{col} 박스플롯' for col in continuous_cols]
)

for i, col in enumerate(continuous_cols):
    fig.add_trace(
        go.Box(
            y=df[col],
            name=col,
            boxpoints='outliers',  # 이상치만 표시
            marker=dict(color=colors[i])
        ),
        row=1, col=i+1
    )

fig.update_layout(
    title_text="연속형 변수 박스플롯 (이상치 확인)",
    height=400,
    showlegend=False
)

fig.show()

# =============================================================================
# Step 6: BMI 이상치 상세 분석
# =============================================================================

def detect_outliers_iqr(data, column):
    """IQR 방법으로 이상치 탐지"""
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    
    return {
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers_count': len(outliers),
        'outliers_percentage': len(outliers) / len(data) * 100
    }

print("=== BMI 이상치 분석 ===")
bmi_outliers = detect_outliers_iqr(df, 'BMI')

print(f"Q1: {bmi_outliers['Q1']:.2f}")
print(f"Q3: {bmi_outliers['Q3']:.2f}")
print(f"IQR: {bmi_outliers['IQR']:.2f}")
print(f"정상 범위: {bmi_outliers['lower_bound']:.2f} ~ {bmi_outliers['upper_bound']:.2f}")
print(f"이상치 개수: {bmi_outliers['outliers_count']:,}개 ({bmi_outliers['outliers_percentage']:.2f}%)")

# BMI 극값들 확인
print(f"\nBMI 최솟값: {df['BMI'].min()}")
print(f"BMI 최댓값: {df['BMI'].max()}")
print(f"BMI 평균: {df['BMI'].mean():.2f}")

# BMI 분포와 이상치 경계선 시각화
fig = go.Figure()

# 히스토그램
fig.add_trace(
    go.Histogram(
        x=df['BMI'],
        nbinsx=50,
        name='BMI 분포',
        marker=dict(color='lightblue', line=dict(color='black', width=1)),
        opacity=0.7
    )
)

# 이상치 경계선
fig.add_vline(
    x=bmi_outliers['lower_bound'], 
    line_dash="dash", 
    line_color="red",
    annotation_text=f"하한선: {bmi_outliers['lower_bound']:.1f}"
)

fig.add_vline(
    x=bmi_outliers['upper_bound'], 
    line_dash="dash", 
    line_color="red",
    annotation_text=f"상한선: {bmi_outliers['upper_bound']:.1f}"
)

fig.update_layout(
    title="BMI 분포와 이상치 경계선",
    xaxis_title="BMI",
    yaxis_title="빈도",
    height=500
)

fig.show()

# =============================================================================
# Step 7: 범주형 변수 분포 확인
# =============================================================================

print("=== 범주형 변수 분포 ===")

# 범주형 변수 막대그래프 - Plotly
fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=[f'{col} 분포' for col in categorical_cols] + [''],
    specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "bar"}, None]]
)

colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']

for i, (col, color) in enumerate(zip(categorical_cols, colors)):
    value_counts = df[col].value_counts().sort_index()
    
    row = (i // 3) + 1
    col_num = (i % 3) + 1
    
    fig.add_trace(
        go.Bar(
            x=value_counts.index,
            y=value_counts.values,
            name=col,
            marker=dict(color=color),
            text=value_counts.values,
            textposition='auto'
        ),
        row=row, col=col_num
    )

fig.update_layout(
    title_text="범주형 변수 분포",
    height=600,
    showlegend=False
)

fig.show()

# 범주형 변수별 상세 정보
category_info = {
    'Sex': {0: '여성', 1: '남성'},
    'Age': '연령대 (1: 18-24세 ~ 13: 80세 이상)',
    'Education': '교육수준 (1: 무학 ~ 6: 대학교 졸업 이상)',
    'Income': '소득수준 (1: <$10,000 ~ 8: ≥$75,000)',
    'GenHlth': '일반건강상태 (1: 우수 ~ 5: 나쁨)'
}

for col in categorical_cols:
    print(f"\n{col} 분포:")
    value_counts = df[col].value_counts().sort_index()
    for value, count in value_counts.items():
        percentage = count / len(df) * 100
        print(f"  {value}: {count:,}개 ({percentage:.1f}%)")

# =============================================================================
# Step 8: 당뇨병 여부에 따른 변수별 차이 분석
# =============================================================================

print("=== 당뇨병 여부에 따른 주요 변수 차이 ===")

# 연속형 변수들의 당뇨병 여부별 분포 비교
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=[f'{col} - 당뇨병 여부별 분포' for col in continuous_cols]
)

for i, col in enumerate(continuous_cols):
    # 정상군
    normal = df[df['Diabetes_binary'] == 0][col]
    # 당뇨군
    diabetes = df[df['Diabetes_binary'] == 1][col]
    
    fig.add_trace(
        go.Histogram(
            x=normal,
            name='정상',
            nbinsx=30,
            marker=dict(color='lightblue'),
            opacity=0.7,
            legendgroup="group1",
            showlegend=(i == 0)
        ),
        row=1, col=i+1
    )
    
    fig.add_trace(
        go.Histogram(
            x=diabetes,
            name='당뇨',
            nbinsx=30,
            marker=dict(color='lightcoral'),
            opacity=0.7,
            legendgroup="group2",
            showlegend=(i == 0)
        ),
        row=1, col=i+1
    )

fig.update_layout(
    title_text="당뇨병 여부에 따른 연속형 변수 분포 비교",
    height=400,
    barmode='overlay'
)

fig.show()

# 주요 건강 지표들의 당뇨병 발병률
health_indicators = ['HighBP', 'HighChol', 'Smoker', 'Stroke', 'HeartDiseaseorAttack']

diabetes_rates = []
indicator_names = []

for indicator in health_indicators:
    # 해당 지표가 있는 경우의 당뇨병 발병률
    rate_with = df[df[indicator] == 1]['Diabetes_binary'].mean() * 100
    # 해당 지표가 없는 경우의 당뇨병 발병률  
    rate_without = df[df[indicator] == 0]['Diabetes_binary'].mean() * 100
    
    diabetes_rates.extend([rate_with, rate_without])
    indicator_names.extend([f'{indicator}_있음', f'{indicator}_없음'])

# 건강 지표별 당뇨병 발병률 비교
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=indicator_names,
        y=diabetes_rates,
        marker=dict(color=['lightcoral' if '있음' in name else 'lightblue' for name in indicator_names]),
        text=[f'{rate:.1f}%' for rate in diabetes_rates],
        textposition='auto'
    )
)

fig.update_layout(
    title="건강 지표별 당뇨병 발병률 비교",
    xaxis_title="건강 지표",
    yaxis_title="당뇨병 발병률 (%)",
    height=500,
    xaxis_tickangle=-45
)

fig.show()

# =============================================================================
# Step 9: 전처리 준비 - 상관관계 분석
# =============================================================================

# 수치형 변수들 간의 상관관계 히트맵
numeric_cols = continuous_cols + categorical_cols + ['Diabetes_binary']
correlation_matrix = df[numeric_cols].corr()

fig = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='RdBu',
    zmid=0,
    text=correlation_matrix.round(2).values,
    texttemplate="%{text}",
    textfont={"size": 10},
    hoverongaps=False
))

fig.update_layout(
    title="주요 변수들 간의 상관관계",
    height=600,
    width=800
)

fig.show()

print("=== 전처리 계획 ===")
print("1. 결측값 처리: ✅ 필요 없음 (결측값 없음)")
print("2. 이상치 처리: 🤔 BMI 이상치 처리 여부 결정 필요")
print("3. 스케일링: 🔄 BMI, MentHlth, PhysHlth 표준화 예정")
print("4. 인코딩: ✅ 이미 수치형으로 인코딩됨")
print("5. 데이터 분할: 🔄 훈련/테스트 8:2 분할 예정")

print("\n다음 단계에서는 실제 전처리를 진행합니다!")
print("- 스케일링 방법 선택 (StandardScaler vs MinMaxScaler)")
print("- 이상치 처리 방법 결정") 
print("- 데이터 분할 실행")