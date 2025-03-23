# 1. 베이스 이미지 선택 (원하는 Python 버전에 맞춰 조정)
FROM python:3.9-slim

# 2. 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 설치
#    requirements.txt 파일을 먼저 복사 후 pip install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY . /app

# 5. Flask가 사용할 포트 열기
EXPOSE 5001

# 6. 컨테이너 실행 시 Flask 서버를 실행
CMD ["python", "main.py"]
