import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("API_KEY")

# 일단 인기동영상을 불러와서 그걸 바탕으로 data를 만든다
def video_list():
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2Cstatistics&chart=mostPopular&maxResults=50&regionCode=kr&key={API_KEY}"

    res = requests.get(url).json()

    items = res["items"]
    data = []

    for video in items:
        snippet = video["snippet"]
        stats = video["statistics"]
        
        data.append({
            "제목": snippet["title"],
            "채널": snippet["channelTitle"],
            "카테고리 ID": snippet["categoryId"],
            "조회수": int(stats.get("viewCount", 0)),
            "좋아요": int(stats.get("likeCount", 0)),
            "댓글수": int(stats.get("commentCount", 0)),
        })

    df = pd.DataFrame(data)
    return df

# 카테고리 id를 바탕으로 카테고리명을 가져온다
def category_list():
    url = f"https://youtube.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=kr&key={API_KEY}"
    res = requests.get(url).json()
    items = res.get("items", [])
    return {item["id"]: item["snippet"]["title"] for item in items}


# 만들어진 data의 카테코리 id는 int형 변수이기 때문에 이것을 category 리스트랑 매핑해서 카테고리 별로 묶기 좋게 만든다.
def make_data():
    df = video_list()
    category_map = category_list()
    
    df["카테고리"] = df["카테고리 ID"].map(category_map)
    df = df.drop(columns=["카테고리 ID"])
    df = df[["제목", "채널", "카테고리", "조회수", "좋아요", "댓글수"]]
    return df
    