import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots


fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=('총 확진자', '일일 신규 확진자', '총 사망자', '백신 접종률', '확진자 vs 백신접종률 비교', ''),
    specs=[[{}, {}],
           [{}, {}],
           [{"colspan": 2, "secondary_y": True}, None]],  
    vertical_spacing=0.1
)

df = pd.read_csv("owid-covid-data.csv")
korea_data = df[df['location']=='South Korea']


fig.add_trace(go.Scatter(x=korea_data['date'],y=korea_data['total_cases']), row=1,col=1)
fig.add_trace(go.Scatter(x=korea_data['date'],y=korea_data['new_cases']), row=1,col=2)
fig.add_trace(go.Scatter(x=korea_data['date'],y=korea_data['total_deaths']), row=2,col=1)
fig.add_trace(go.Scatter(x=korea_data['date'],y=korea_data['people_vaccinated_per_hundred']), row=2,col=2)


fig.add_trace(
    go.Scatter(
        x=korea_data['date'],
        y=korea_data['new_cases'],
        mode='lines',
        name='일일 확진자',
        line=dict(color='red', width=3)
    ), 
    row=3, col=1
)


fig.add_trace(
    go.Scatter(
        x=korea_data['date'],
        y=korea_data['people_vaccinated_per_hundred'],
        mode='lines',
        name='백신 접종률',
        line=dict(color='purple', width=3)
    ), 
    row=3, col=1, secondary_y=True
)


variant_info = [
    ('2020-12-01', '알파 변이', 'orange'),
    ('2021-07-01', '델타 변이', 'green'), 
    ('2021-12-01', '오미크론 변이', 'red')
]


for date_str, name, color in variant_info:
    fig.add_vline(x=date_str, line_dash="dash", line_color=color, line_width=2)


for date_str, name, color in variant_info:
    fig.add_trace(
        go.Scatter(
            x=[None], y=[None],  
            mode='lines',
            line=dict(color=color, width=2, dash='dash'),
            name=name,
            showlegend=True
        )
    )


fig.update_yaxes(title_text="확진자 수", secondary_y=False, row=3, col=1)
fig.update_yaxes(title_text="접종률 (%)", secondary_y=True, row=3, col=1)

fig.update_layout(
    height=800,  
    showlegend=True,  
    title_text="한국 코로나19 종합 현황 + 변이 바이러스 시점 분석"
)

fig.show()