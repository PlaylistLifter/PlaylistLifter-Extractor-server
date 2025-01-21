# PlaylistLifter-Extractor-server

## 프로젝트 설명
Python 기반으로 유튜브 플레이리스트에서 노래 정보를 추출하고, Java 서버로 데이터를 전송하는 역할을 합니다.

## 주요 기능
- 유튜브 링크를 입력받아 영상 설명 및 자막에서 노래 정보 추출.
- 텍스트에서 노래 제목과 가수 정보를 파싱.
- REST API를 통해 데이터를 외부 Java 서버로 전달.

## 설치 및 실행
1. 가상환경 생성:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
