from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

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

# 댓글에서 가수와 노래 제목을 추출하는 함수
def extract_songs_from_comments(comments):
    artists = []
    songs = []

    for line in comments:
        # 정규식을 이용하여 시간 포맷 제거 (00:00 or 00:00:00)
        line = re.sub(r'\d{2}:\d{2}(:\d{2})?', '', line).strip()

        if line:
            try:
                if "_" in line:  # 가수와 노래 구분자가 `_` 인 경우
                    song, artist = line.split("_", 1)
                elif "-" in line:  # 가수와 노래 구분자가 `-` 인 경우
                    song, artist = line.split("-", 1)
                else:
                    continue  # `_`, `-`가 없는 경우(잡글) 무시
                
                # 리스트에 추가
                artists.append(artist.strip())
                songs.append(song.strip())

            except ValueError:  # 예외 처리
                print(f"파싱 오류 발생: {line}")

    return list(zip(artists, songs))

# 유튜브 링크를 받아서 가수와 노래 제목을 추출하는 메인 함수
def get_songs_from_youtube(video_url):
    html_source = get_html_from_youtube(video_url)
    soup = BeautifulSoup(html_source, 'html.parser')

    # 고정 댓글 부분의 span 요소 찾기
    post = soup.select_one('#content-text > span')

    if post:
        lines = post.get_text().split("\n")  # 줄 단위로 분리
        songs_list = extract_songs_from_comments(lines)

        return songs_list  # (가수, 노래 제목) 리스트 반환
    else:
        return []  # 댓글에서 노래를 찾지 못한 경우 빈 리스트 반환
