import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
user_flag=True

headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/x-www-form-urlencoded"
}

def translate(lang,query):
    global user_flag
    data = {
        "source":"auto",
        "target":lang,
        "text":query
        }
    url = "https://papago.apigw.ntruss.com/nmt/v1/translation"
    response = requests.post(url,headers=headers,data=data)

    rescode = response.status_code

    if rescode == 200:
        result = response.json()
        translated_text = result['message']['result']['translatedText']
        src_lang = result['message']['result']['srcLangType']
        if user_flag:
            user_flag =  not user_flag
            print(f"user 1 : {translated_text}")
        else:
            user_flag =  not user_flag
            print(f"user 2 : {translated_text}")
        return translated_text, src_lang
    else:
        print(f"Error Code:: {rescode}")
        

while True:
    string = input()
    translate_text,srcLang=translate("ko",string)
    string = input()
    translate(srcLang,string)
    