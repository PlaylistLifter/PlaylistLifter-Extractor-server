from selenium import webdriver
from bs4 import BeautifulSoup
import time

# 크롬드라이버 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 브라우저 UI 없이 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 유튜브 HTML 소스 가져오기 함수
def get_html_from_youtube(video_url):
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(video_url)
        time.sleep(3)  # 페이지 로딩 대기
        html_source = driver.page_source
    finally:
        driver.quit()
    return html_source

# 메인 실행
if __name__ == "__main__":
    video_url = input("url 입력 : ")
    html_source = get_html_from_youtube(video_url)
    soup = BeautifulSoup(html_source, 'html.parser')

    # 순차적으로 모든 노래 정보를 가져오기
    index = 1  # nth-child 시작점
    while True:
        selector = f"#items > yt-video-attribute-view-model:nth-child({index}) > div > a > div.yt-video-attribute-view-model__metadata"
        post = soup.select_one(selector)
        
        if post:
            # 노래 제목 추출
            song_title = post.find('h1', class_='yt-video-attribute-view-model__title').get_text(strip=True)
            
            # 가수 추출
            artist = post.find('h4', class_='yt-video-attribute-view-model__subtitle').get_text(strip=True)
            
            print(f"{index}. {song_title} - {artist}")
        else:
            # 정보가 없으면 반복 중단
            # print("더 이상 정보가 없습니다.")
            break
        
        index += 1  # 다음 child로 이동
