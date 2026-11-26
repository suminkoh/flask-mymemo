from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin,
    login_user, logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#메모모델
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Memo {self.title}>'
    
#사용자모델
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#사용자로딩함수
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return '마이메모 소개 페이지입니다.'

with app.app_context():
    db.create_all()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    print("회원가입 요청 도착!")
    print("username:", repr(username))
    print("email:", repr(email))
    print("password 전달 여부:", bool(password))

    if not username or not email or not password:
        return jsonify({'message': '입력값이 누락되었습니다.'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': '이미 존재하는 아이디입니다.'}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({'message': '이미 사용 중인 이메일입니다.'}), 409

    try:
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        print("회원가입 DB 저장 성공! ID:", user.id)

        return jsonify({'message': '회원가입 성공'}), 201

    except Exception:
        db.session.rollback()
        app.logger.exception("회원가입 DB 저장 실패")
        return jsonify({'message': 'DB 저장 중 오류가 발생했습니다.'}), 500




@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and password and user.check_password(password):
        login_user(user)

        # 로그인 성공 → 메모 페이지로 이동
        return redirect(url_for('list_memos'))

    return jsonify({
        'message': '사용자 이름 또는 비밀번호가 잘못되었습니다.'
    }), 401


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': '로그아웃 성공'}), 200


#메모생성
@app.route('/memos/create', methods=['POST'])
@login_required
def create_memo():
    title = request.json['title']
    content = request.json['content']
    new_memo = Memo(title=title, content=content, user_id=current_user.id)
    db.session.add(new_memo)
    db.session.commit()
    return jsonify({'message': '메모가 성공적으로 생성되었습니다.'}), 201
#메모조회
@app.route('/memos', methods=['GET'])
@login_required
def list_memos():
    memos = Memo.query.filter_by(user_id=current_user.id).all()
    return render_template('memos.html', memos=memos, username=current_user.username)
#메모업데이트
@app.route('/memos/update/<int:id>', methods=['PUT'])
@login_required
def update_memo(id):
    memo = Memo.query.filter_by(id=id, user_id=current_user.id).first()
    if memo:
        memo.title = request.json['title']
        memo.content = request.json['content']
        db.session.commit()
        return jsonify({'message': '메모가 성공적으로 업데이트되었습니다.'}), 200
    else:
        abort(404, description="메모를 찾을 수 없습니다.")
#메모삭제
@app.route('/memos/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_memo(id):
    memo = Memo.query.filter_by(id=id, user_id=current_user.id).first()
    if memo:
        db.session.delete(memo)
        db.session.commit()
        return jsonify({'message': '메모가 성공적으로 삭제되었습니다.'}), 200
    else:
        abort(404, description="메모를 찾을 수 없습니다.")