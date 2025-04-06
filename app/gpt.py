import os
from dotenv import load_dotenv
from openai import OpenAI  # OpenAI 라이브러리 임포트

# 환경 변수에서 API 키 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # OpenAI API 키 로드

# OpenAI API 클라이언트 생성
client = OpenAI(api_key=api_key)

def extract_songs(comments):
    if not comments:
        return []

    comment_text = "\n".join(comments)  # 여러 줄의 댓글을 하나의 문자열로 변환

    prompt = f"""
    다음은 유튜브 영상의 고정 댓글과 설명란에 있는 내용용입니다:

    {comment_text}

    이 내용을 분석하여 해당 유튜브 영상의 노래 제목과 가수 정보를 추출해 주세요.
    노래제목 - 가수 형식으로 추출해 주세요.
    출력 형식은 아무런 추가 설명 없이 다음 형식으로만 출력하세요.
    노래 전부 정확하게 추출해 주세요. 검토도 해주세요.

    예시:
    가까운 듯 먼 그대여 - 카더가든
    기다린 만큼, 더 - 검정치마
    처음이니까 - 오왠

    이 형식을 따르지 않은 답변은 올바르지 않습니다.
    """

    # OpenAI API 호출
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 gpt-4o 사용 가능
        messages=[{"role": "user", "content": prompt}]
    )

    # 결과 받아오기
    response_text = completion.choices[0].message.content

    # 노래 제목과 가수 분리하여 리스트에 저장
    extracted_songs = response_text.strip().split("\n")
    artists, songs = [], []

    for song_info in extracted_songs:
        if " - " in song_info:
            song, artist = song_info.rsplit(" - ", 1)  # 마지막 - 기준으로 가수와 노래 제목 분리
            artists.append(artist.strip())
            songs.append(song.strip())

    return list(zip(artists, songs))  # (가수, 노래 제목) 형태의 리스트 반환