# main.py
from flask import Flask
from communication import bp as communication_bp

app = Flask(__name__)
# 테스트
# Blueprint 등록
app.register_blueprint(communication_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
