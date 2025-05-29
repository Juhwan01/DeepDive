# -*- coding: utf-8 -*-

import json
import streamlit as st
from pathlib import Path

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

with st.sidebar:
    st.title("#30DaysOfStreamlit")
    st.header("Day 27 - streamlit Elements")
    st.write("STreamlit Elements를 사용하여 드래그 가능하고 크기 조절 가능한 대시보드 만들기")
    st.write("---")
    
    media_url = st.text_input("미디어 URL",value="https://www.youtube.com/watch?v=zMWaQ-D0g3oL")

# data라는 key값이 없을 경우 
if "data" not in st.session_state:
    # st.sessionstate는 상태 관리 시스템(세션 동안 데이터를 저장하고 유지하는데 사용)
    # data라는 키 값이 없기에 새로운 key,value를 할당(Path모듈을 이용해서 data.json파일에서 읽어온걸 text로 저장)
    st.session_state.data = Path("data.json").read_text()

# 미리 레이아웃의 구조를 정의한다
layout = [
    dashboard.Item("editor", 0,0,6,3),
    dashboard.Item("chart", 6,0,6,3),
    dashboard.Item("media", 0,2,12,4)
    ]

# elements를 계층구조로 만든다 elements->dashboard->mui.Card->mui.CardHeader->mui.CardContent(구조는 유동적으로 변할 수 있음)
with elements("demo"):
    # draggable을 허용할 객체를 설정하는 파라미터 .은 클래스를 의미하고 draggable은 클래스의 이름을 의미한다
    with dashboard.Grid(layout, draggableHandle=".draggable"):
            # 여기서 key=editor에서 editor는 아까 위에서 만든 dashboard.Item의 키이다.
            # flexbox 레이아웃 사용, 자식 요소들 세로로 배치
            with mui.Card(key="editor",sx={"display":"flex", "flexDirection":"column"}):
                # 여기서 클래스 이름을 draggable로 지정하면서 드래그 가능 영역으로 지정한다
                mui.CardHeader(title="Editor", className="draggable")
                # flex=남은 공간을 모두 차지(1), 최소높이 0
                with mui.CardContent(sx={"flex":1,"minHeight":0}):
                    # VS Code와 같은 코드 에디터
                    editor.Monaco(
                        defaultValue=st.session_state.data,
                        language="json",
                        # 내용이 변경될 때마다 실행되는 콜백 - 성능 최적화를 위해 실제 호출까지 지연
                        # lazy("data")는 변경된 내용을 session_state.data에 자동으로 저장 - 컴포넌트의 상태 변화를 Streamlit의 session_state와 자동으로 동기화해주는 역할
                        #lazy: 이벤트 발생 시 비동기로 상태만 업데이트, Streamlit 재실행 안함
                        #sync: 이벤트 발생 시 즉시 전체 Streamlit 스크립트를 재실행
                        onChange=sync("data")
                        )
                with mui.CardActions:
                    # 
                    mui.Button("변경 사항 적용",onClick=sync())
                    
            with mui.Card(key="chart",sx={"display":"flex","flexDirection":"column"}):
                mui.CardHeader(title="Chart", className="draggable")
                # 그래프 할때는 content사용 안했음
                #           CardContent의 역할
                # 패딩과 여백 추가 (기본적으로 16px 내부 여백)
                # 텍스트 스타일링 (Typography 컴포넌트들에 기본 스타일 적용)
                # 레이아웃 구조화 (flex 속성 등으로 공간 분할)
                nivo.Bump(
                    data=json.loads(st.session_state.data),
                    colors={"scheme": "spectral"},
                    lineWidth=3,
                    activeLineWidth=6,
                    inactiveLineWidth=3,
                    inactiveOpacity=0.15,
                    pointSize=10,
                    activePointSize=16,
                    inactivePointSize=0,
                    pointColor={"theme": "background"},
                    pointBorderWidth=3,
                    activePointBorderWidth=3,
                    pointBorderColor={"from": "serie.color"},
                    axisTop={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": -36
                    },
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": 32
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "ranking",
                        "legendPosition": "middle",
                        "legendOffset": -40
                    },
                    margin={"top": 40, "right": 100, "bottom": 40, "left": 60},
                    axisRight=None
                )
            with mui.Card(key="media",sx={"display":"flex", "flexDirection":"column"}):
                mui.CardHeader(title="Media", className="draggable")
                with mui.CardContent(sx={"flex":1,"minHeight":0}):
                    # controls=True 파라미터는 미디어 플레이어의 컨트롤 버튼들을 표시할지 여부를 결정
                    media.Player(url=media_url, width="100%",height="100%",controls=True)
                                