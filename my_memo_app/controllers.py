from flask import render_template, request, jsonify, abort, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError

from .models import db, User, Memo


def setup_routes(app):


    # 기본 페이지
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return '마이메모 소개 페이지입니다.'



    # 회원가입
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

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

            return jsonify({'message': '회원가입 성공'}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': '이미 사용 중인 사용자 정보입니다.'}), 409

        except Exception:
            db.session.rollback()
            app.logger.exception('회원가입 DB 저장 실패')
            return jsonify({'message': 'DB 저장 중 오류가 발생했습니다.'}), 500



    # 로그인
    @app.route('/login', methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({
                'message': '사용자 이름과 비밀번호를 입력해 주세요.'
            }), 400

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('list_memos'))

        return jsonify({
            'message': '사용자 이름 또는 비밀번호가 잘못되었습니다.'
        }), 401



    # 로그아웃
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))



    # 메모 생성
    @app.route('/memos/create', methods=['POST'])
    @login_required
    def create_memo():
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({'message': 'JSON 데이터를 전달해 주세요.'}), 400

        title = data.get('title')
        content = data.get('content')

        if not isinstance(title, str) or not 1 <= len(title.strip()) <= 100:
            return jsonify({'message': '제목은 1~100자로 입력해 주세요.'}), 400

        if not isinstance(content, str) or not content.strip():
            return jsonify({'message': '메모 내용을 입력해 주세요.'}), 400

        new_memo = Memo(
            title=title.strip(),
            content=content,
            user_id=current_user.id
        )

        db.session.add(new_memo)
        db.session.commit()

        return jsonify({'message': '메모가 성공적으로 생성되었습니다.'}), 201



    # 메모 조회
    @app.route('/memos', methods=['GET'])
    @login_required
    def list_memos():
        memos = Memo.query.filter_by(user_id=current_user.id).all()

        return render_template(
            'memos.html',
            memos=memos,
            username=current_user.username
        )


  
    # 메모 수정
    @app.route('/memos/update/<int:id>', methods=['PUT'])
    @login_required
    def update_memo(id):
        memo = Memo.query.filter_by(
            id=id,
            user_id=current_user.id
        ).first()

        if memo is None:
            abort(404, description='메모를 찾을 수 없습니다.')

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({'message': 'JSON 데이터를 전달해 주세요.'}), 400

        title = data.get('title')
        content = data.get('content')

        if not isinstance(title, str) or not 1 <= len(title.strip()) <= 100:
            return jsonify({'message': '제목은 1~100자로 입력해 주세요.'}), 400

        if not isinstance(content, str) or not content.strip():
            return jsonify({'message': '메모 내용을 입력해 주세요.'}), 400

        memo.title = title.strip()
        memo.content = content

        db.session.commit()

        return jsonify({'message': '메모가 성공적으로 업데이트되었습니다.'}), 200


  
    # 메모 삭제
    @app.route('/memos/delete/<int:id>', methods=['DELETE'])
    @login_required
    def delete_memo(id):
        memo = Memo.query.filter_by(
            id=id,
            user_id=current_user.id
        ).first()

        if memo is None:
            abort(404, description='메모를 찾을 수 없습니다.')

        db.session.delete(memo)
        db.session.commit()

        return jsonify({'message': '메모가 성공적으로 삭제되었습니다.'}), 200