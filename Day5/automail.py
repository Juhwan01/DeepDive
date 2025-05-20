import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 정보 가져오기
sendEmail = os.getenv("EMAIL_SENDER")
recvEmail = os.getenv("EMAIL_RECEIVER")
password = os.getenv("EMAIL_PASSWORD")
smtpName = os.getenv("SMTP_SERVER")
smtpPort = int(os.getenv("SMTP_PORT"))

def send_restaurantList(string):
    text = string
    msg = MIMEText(text)

    msg['Subject'] = "음식점 리스트 입니다."
    msg['From'] = sendEmail
    msg['To'] = recvEmail
    print(msg.as_string())
    try:
        s = smtplib.SMTP(smtpName, smtpPort)
        s.starttls()
        s.login(sendEmail, password)
        s.sendmail(sendEmail, recvEmail, msg.as_string())
        s.close()
        print("이메일 전송 성공!")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")