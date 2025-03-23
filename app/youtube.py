from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import gpt

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube API 빌드
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)

# 유튜브 영상 ID 추출
def get_video_id(video_url):
    if "watch?v=" not in video_url:
        return None
    start = video_url.find("watch?v=") + len("watch?v=")
    return video_url[start:start+11]

# 고정 댓글 가져오기
def get_pinned_comment(video_id):
    request = YOUTUBE.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=1,
        order="relevance"
    )
    response = request.execute()
    items = response.get("items", [])
    if not items:
        return None

    raw_comment = items[0]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
    clean_comment = BeautifulSoup(raw_comment, "html.parser").get_text()
    return clean_comment

# 영상 제목 가져오기
def get_video_title(video_id):
    request = YOUTUBE.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    items = response.get("items", [])
    if not items:
        return "제목 없음"
    return items[0]["snippet"]["title"]

# 통합 함수: 영상 제목 + 고정 댓글 기반 노래 리스트 추출
def get_songs_from_youtube(video_url):
    video_id = get_video_id(video_url)
    if not video_id:
        return "영상 ID 없음", []

    title = get_video_title(video_id)
    comment = get_pinned_comment(video_id)

    if comment:
        lines = comment.split("\n")
        print(lines)  # 디버깅 용도
        songs_list = gpt.extract_songs(lines)
        return title, songs_list
    else:
        return title, []
