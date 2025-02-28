from flask import Blueprint, request, jsonify
from youtube import get_songs_from_youtube
import requests
import json

bp = Blueprint('receive', __name__)

@bp.route("/process-link", methods=["POST"])
def process_link():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid request format. Expected JSON"}), 400

        data = request.get_json()
        if not data or "youtubeUrl" not in data:
            return jsonify({"error": "Missing youtubeUrl in request."}), 400

        youtube_url = data["youtubeUrl"]
        print(f"Received YouTube URL: {youtube_url}")

        # 유튜브 댓글에서 노래, 유튜브 영상 제목목 추출
        youtubetitle, songs_list = get_songs_from_youtube(youtube_url)
        print(youtubetitle, songs_list)
        response_data = {
            "youtubeUrl": youtube_url,
            "title": youtubetitle,
            "songs": [{"artist": artist, "title": song} for artist, song in songs_list]
        }

        # JSON을 예쁘게 포맷팅하여 출력
        print("\n=== 🎵 추출된 노래 목록 ===")
        print(json.dumps(response_data, indent=4, ensure_ascii=False))  # 예쁘게 포맷팅

        # 보내는 코드
        send_response = requests.post("http://localhost:8080/api/playlist/add", json=response_data) 
        print(f"Spring Boot Response: {send_response.status_code}, {send_response.text}")

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
