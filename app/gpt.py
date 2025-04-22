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
    다음은 유튜브 영상의 고정 댓글들입니다:

    {comment_text}

    이 댓글을 분석하여 **정확한 노래 제목과 가수 이름 쌍**을 추출해 주세요.

    중요 규칙:
    1. 가수 이름과 노래 제목 순서가 헷갈릴 경우, **실제 노래 제목과 아티스트 정보를 판단하여**, 반드시 "노래제목 - 가수" 순서로 출력해주세요.
    2. 댓글에 있는 형식이 "가수 - 노래제목"이라도, 실제 내용을 판단해서 "노래제목 - 가수" 순서로 수정해 주세요.
    3. 모든 결과는 다음 형식으로 출력해 주세요 (설명, 번호, 다른 문장 없이!):

    예시:
    가까운 듯 먼 그대여 - 카더가든  
    기다린 만큼, 더 - 검정치마  
    처음이니까 - 오왠  
    METEOR - 창모  
    새삥 - 지코

    이 형식 외의 출력은 허용되지 않습니다. 반드시 이 포맷을 지켜주세요.
    주의: 형식을 따르지 않거나 실제 정보를 바탕으로 판단하지 않은 결과는 무효 처리됩니다.

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
            song, artist = song_info.rsplit(" - ", 1)  # 마지막 `-` 기준으로 가수와 노래 제목 분리
            artists.append(artist.strip())
            songs.append(song.strip())

    return list(zip(artists, songs))  # (가수, 노래 제목) 형태의 리스트 반환