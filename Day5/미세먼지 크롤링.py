from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests

html = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&pkid=227&qvt=0&query=%EA%B2%BD%EC%83%81%EB%82%A8%EB%8F%84%20%EA%B9%80%ED%95%B4%EC%8B%9C%20%ED%99%9C%EC%B2%9C%EB%8F%99%20%EC%B4%88%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80')
soup = bs(html.text,'html.parser')
html.close()
data_list = []
datas = soup.find_all('div',{'class' : 'grade level1'})

for data in datas:
    title = data.find('span',{'class' : 'title'})
    value = data.find('span',{'class' : 'num'})
    print(f'오늘 {title.text}먼지 농도는 {value.text} 입니다')
