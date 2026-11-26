import os
from flask import Flask
from dotenv import load_dotenv

from .models import db
from .login_manager import login_manager
from .controllers import setup_routes

load_dotenv()

app = Flask(__name__)

# Flask 설정
app.json.ensure_ascii = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# DB 및 로그인 관리자 초기화
db.init_app(app)
login_manager.init_app(app)

# 로그인하지 않은 사용자는 홈으로 이동
login_manager.login_view = 'home'

# 라우트 등록
setup_routes(app)

# 테이블 생성
with app.app_context():
    db.create_all()