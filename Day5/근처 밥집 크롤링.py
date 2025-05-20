from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import automail
import time


driver = webdriver.Chrome()
driver.get("https://www.naver.com/")
result = ""
# 명시적 대기: element가 로드될 때까지 최대 10초 기다림
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="query"]'))
)

search = driver.find_element(By.XPATH,'//*[@id="query"]')
search.send_keys('근처 밥집')
time.sleep(1)
search.send_keys(Keys.ENTER)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="place-main-section-root"]/section/div/div[5]/ul/li'))
)

restaurant_info = []

restaurants = driver.find_elements(By.XPATH,'//*[@id="place-main-section-root"]/section/div/div[5]/ul/li')

'''
restaurants 의 패턴

//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[1]/div[1]/div[1]/a/span[1]
//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[2]/div[1]/div[1]/a/span[1]
//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[3]/div[1]/div[1]/a/span[1]

'''

'''
restaurants_menu 의 패턴

//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[1]/div[1]/div[1]/a/span[5]
//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[2]/div[1]/div[1]/a/span[3]
//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[3]/div[1]/div[1]/a/span[2]
위에서 xpath를 이용한 방법은 사용 불가능 하다는 것을 알 수 있다 이제 클래스를 이용한 방식을 이용해보자

'''

'''
restaurants_menu 의 패턴

//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[1]/div[1]/div[1]/a/span[5]
//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[2]/div[1]/div[1]/a/span[3]
//*[@id="place-main-section-root"]/section/div/div[5]/ul/li[3]/div[1]/div[1]/a/span[2]
위에서 xpath를 이용한 방법은 사용 불가능 하다는 것을 알 수 있다 이제 클래스를 이용한 방식을 이용해보자

'''
# 기존 코드
'''
for restaurant in restaurants:
    try:
        name = restaurant.find_element(By.CLASS_NAME, 'TYaxT').text

        menu_elements = restaurant.find_element(By.CLASS_NAME, 'KCMnt')
        menus = list(map(str,menu_elements.text.split()))

        restaurant_info.append({
            'name': name,
            'menus': menus
        })

    except Exception as e:
        print(f"항목 처리 중 오류 발생: {e}")

for info in restaurant_info:
    print(f"식당명: {info['name']}")
    print(f"메뉴: {', '.join(info['menus']) if info['menus'] else '메뉴 정보 없음'}")
    print("-" * 50)
코드를 이렇게 작성했더니 되는 경우도 있지만 그렇지 않은 경우도 자주 발생 불확실성을 줄이고자 명시적 대기를 추가함
'''
# 수정 후 코드
if restaurants:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'TYaxT'))
        )
    except Exception as e:
        print(f"식당 이름 요소 로드 대기 중 오류: {e}")

for restaurant in restaurants:
    try:
        name = restaurant.find_element(By.CLASS_NAME, 'TYaxT').text
        try:
            WebDriverWait(restaurant, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'KCMnt'))
            )
        except:
            pass
        
        menu_elements = restaurant.find_element(By.CLASS_NAME, 'KCMnt')
        menus = list(map(str,menu_elements.text.split()))
        
        restaurant_info.append({
            'name': name,
            'menus': menus
        })
        
    except Exception as e:
        print(f"항목 처리 중 오류 발생: {e}")

for info in restaurant_info:
    result += f"식당명: {info['name']}\n"
    result += f"메뉴: {', '.join(info['menus']) if info['menus'] else '메뉴 정보 없음'}\n"
    result += "-" * 50 + "\n"
automail.send_restaurantList(result)
driver.quit()