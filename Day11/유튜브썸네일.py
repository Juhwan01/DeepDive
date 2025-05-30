# -*- coding: utf-8 -*-

import streamlit as st

def get_ytid(input_url):
    if 'youtu.be' in input_url:
        ytid = input_url.split('/')[-1]
    if 'youtube.com' in input_url:
        ytid = input_url.split('=')[-1]
    return ytid


st.title("yt-image-app")
st.header("유튜브 썸네일 이미지 추출기")

with st.expander('이 앱에 대하여'):
    st.write('이 앱은 YouTube 동영상의 썸네일 이미지를 검색합니다')
    

st.sidebar.header("설정")
img_dict = {'Max': 'maxresdefault', 'High': 'hqdefault', 'Medium': 'mqdefault', 'Standard': 'sddefault'}
selected_img_quality = st.sidebar.selectbox('이미지 품질 선택', ['Max', 'High', 'Medium', 'Standard'])
img_quality = img_dict[selected_img_quality]

yt_url = st.text_input('YouTube URL 붙여넣기', 'https://www.youtube.com/watch?v=WBeEfnLxEYw')

if yt_url != '':
    ytid = get_ytid(yt_url)

    yt_img = f'http://img.youtube.com/vi/{ytid}/{img_quality}.jpg'
    st.image(yt_img)
    st.write('YouTube 동영상 썸네일 이미지 URL: ', yt_img)
else:
    st.write(' URL을 입력해 제출하세요 ...')