from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import gpt

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

# 유튜브 댓글을 가져와서 GPT로 노래 추출
# 여기서 유튜브 영상 제목도 가져옴
def get_songs_from_youtube(video_url):
    html_source = get_html_from_youtube(video_url)
    soup = BeautifulSoup(html_source, 'html.parser')

    # 고정 댓글 부분의 span 요소 찾기
    post = soup.select_one('#content-text > span')
    
    # 유튜브 영상 제목 찾기
    youtubetitle = soup.select_one('#title > h1 > yt-formatted-string')
    youtubetitle = youtubetitle.get_text()

    if post:
        lines = post.get_text().split("\n")  # 줄 단위로 분리
        print(lines)
        # gpt.py의 `extract_songs` 함수 호출하여 노래 목록 추출
        songs_list = gpt.extract_songs(lines)  

        return youtubetitle, songs_list  # (가수, 노래 제목) 리스트 반환
    else:
        return youtubetitle, []  # 댓글에서 노래를 찾지 못한 경우 빈 리스트 반환
