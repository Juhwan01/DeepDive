from 시각화_데이터 import *

import matplotlib.pyplot as plt

'''
한글이 깨지는 문제로 영어로 작성
어제 배웠던 api사용을 바탕으로 유튜브 분석 자료를 만들고
분석자료 데이터를 바탕으로 오늘 배웠던 시각화 관련 간단한 예제 진행
'''

if __name__ == "__main__":
    df = make_data()
    category_counts = df["카테고리"].value_counts()
    plt.figure(figsize=(10, 5))
    category_counts.plot(kind="bar", color="skyblue")
    plt.title("Popular Videos by Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Videos")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
