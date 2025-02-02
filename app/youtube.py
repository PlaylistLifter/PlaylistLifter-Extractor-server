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

    # 고정 댓글 부분의 span 요소 찾기
    post = soup.select_one('#content-text > span')
    if post:
        lines = post.get_text().split("\n")  # 줄 단위로 분리 (strip=True 제거)
        for line in lines:
            if line.strip():  # 빈 줄 제거
                print(line.strip())
    else:
        print("고정 댓글을 찾을 수 없습니다.")
