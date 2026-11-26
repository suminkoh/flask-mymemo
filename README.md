# 📝 Flask MyMemo

Flask와 MySQL을 활용한 **개인 메모 관리 웹 애플리케이션**입니다.

Flask의 기본적인 웹 애플리케이션 구조와 REST API, 데이터베이스 연동, 사용자 인증 및 세션 관리 기능을 학습하기 위해 개발했습니다.

사용자는 회원가입과 로그인 후 자신만의 메모를 생성·조회·수정·삭제할 수 있습니다.

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.12 |
| Backend | Flask |
| Database | MySQL |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Password Security | Werkzeug |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Package Management | uv |
| Environment Variables | python-dotenv |

## ✨ 주요 기능

### 1. 사용자 인증

- 회원가입 및 로그인·로그아웃
- 사용자 이름과 이메일 중복 확인
- Werkzeug를 이용한 비밀번호 해시 저장 및 검증
- Flask-Login을 활용한 세션 기반 인증
- `@login_required`를 통한 비로그인 사용자 접근 제한

### 2. 메모 CRUD

| 기능 | HTTP Method | 설명 |
|------|-------------|------|
| Create | POST | 새로운 메모 생성 |
| Read | GET | 로그인한 사용자의 메모 조회 |
| Update | PUT | 기존 메모 수정 |
| Delete | DELETE | 기존 메모 삭제 |

- `current_user.id`를 활용한 사용자별 메모 관리
- 다른 사용자의 메모에 대한 수정·삭제 접근 제한
- JavaScript `fetch()`를 통한 비동기 API 요청

### 3. 웹 인터페이스

- Jinja2 템플릿을 활용한 HTML 렌더링
- 회원가입 및 로그인 폼
- 메모 생성·수정·삭제 인터페이스
- 사용자별 메모 목록 표시

## 📁 Project Structure

```text
flask_mymemo/
├── my_memo_app/
│   ├── app.py
│   ├── models.py
│   ├── login_manger.py
│   └── templates/
│       ├── home.html
│       ├── signup.html
│       └── memos.html
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

- `app.py`: Flask 애플리케이션 및 라우팅
- `models.py`: 데이터 모델 관련 파일
- `login_manger.py`: 로그인 관리 관련 파일
- `templates/`: HTML 템플릿
- `pyproject.toml`: 프로젝트 설정 및 의존성 관리
- `uv.lock`: 의존성 버전 고정
- `.env.example`: 환경변수 설정 예시

> `.env`와 `.venv`는 `.gitignore`를 통해 Git 관리 대상에서 제외했습니다.

## 🗄 Database Design

MySQL과 Flask-SQLAlchemy를 사용하여 사용자와 메모 간의 **1:N 관계**를 구현했습니다.

### User Table

| Column | Type | Constraint |
|--------|------|------------|
| id | Integer | PK, Auto Increment |
| username | String(80) | Unique, Not Null |
| email | String(120) | Unique, Not Null |
| password_hash | String(255) | Not Null |

### Memo Table

| Column | Type | Constraint |
|--------|------|------------|
| id | Integer | PK, Auto Increment |
| user_id | Integer | FK → user.id, Not Null |
| title | String(100) | Not Null |
| content | Text | Not Null |

**Relationship**

- 하나의 사용자는 여러 개의 메모를 작성할 수 있습니다.
- 각 메모는 하나의 사용자에게 속합니다.
- `memo.user_id`는 `user.id`를 참조합니다.

## 🔗 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | 메인 페이지 | X |
| GET | `/about` | 서비스 소개 | X |
| GET | `/signup` | 회원가입 페이지 | X |
| POST | `/signup` | 회원가입 처리 | X |
| POST | `/login` | 로그인 | X |
| GET | `/logout` | 로그아웃 | O |
| GET | `/memos` | 개인 메모 조회 | O |
| POST | `/memos/create` | 메모 생성 | O |
| PUT | `/memos/update/<int:id>` | 메모 수정 | O |
| DELETE | `/memos/delete/<int:id>` | 메모 삭제 | O |

### API 요청 예시

**메모 생성**

```http
POST /memos/create
Content-Type: application/json
```

```json
{
  "title": "Flask 공부",
  "content": "Flask-SQLAlchemy와 Flask-Login 학습"
}
```

**응답 예시**

```json
{
  "message": "메모가 성공적으로 생성되었습니다."
}
```

HTTP Status: `201 Created`

## 🚀 Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/suminkoh/flask-mymemo.git
cd flask-mymemo
```

### 2. Install Dependencies

Python 3.12 및 uv가 설치된 환경에서 실행합니다.

```bash
uv sync
```

### 3. Create Database

MySQL에서 데이터베이스를 생성합니다.

```sql
CREATE DATABASE IF NOT EXISTS flask_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 4. Environment Variables

프로젝트 루트 디렉터리에 `.env` 파일을 생성합니다.

```dotenv
DATABASE_URL=mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/flask_db
SECRET_KEY=YOUR_SECRET_KEY
```

시크릿 키는 다음 명령어로 생성할 수 있습니다.

```bash
uv run python -c "import secrets; print(secrets.token_hex(32))"
```

> DB 비밀번호 및 SECRET_KEY 등 민감한 정보는 GitHub에 업로드하지 않습니다.

### 5. Run Application

```bash
uv run flask --app my_memo_app.app run --debug
```

브라우저에서 다음 주소로 접속합니다.

http://127.0.0.1:5000

> `db.create_all()`은 존재하지 않는 테이블만 생성합니다. 기존 테이블의 컬럼 변경은 자동 반영되지 않으므로 별도 마이그레이션이 필요합니다.

## 🔐 Authentication Flow

1. 사용자가 회원가입 폼에 계정 정보 입력
2. Werkzeug를 통해 비밀번호 해시 생성
3. 사용자 정보를 MySQL에 저장
4. 로그인 요청 시 사용자 조회 및 비밀번호 검증
5. `login_user()`로 로그인 세션 생성
6. 세션 쿠키를 통해 사용자 인증 상태 유지
7. `@login_required`로 메모 페이지 접근 제한
8. `current_user.id`를 통해 메모 소유권 확인
9. `logout_user()`로 로그인 세션 종료

## 📚 What I Learned

### Flask & HTTP

- Flask 애플리케이션 구조 및 라우팅
- HTTP GET, POST, PUT, DELETE 메서드
- REST API 기반 CRUD 구현
- HTTP 상태 코드와 JSON 응답 처리
- `request.form`과 `request.get_json()`의 차이
- `redirect()`, `url_for()`, `render_template()` 활용

### Database & ORM

- MySQL과 Flask-SQLAlchemy 연동
- ORM을 활용한 데이터 생성·조회·수정·삭제
- `db.session.add()` 및 `db.session.commit()`의 역할
- Primary Key와 Foreign Key
- 사용자와 메모 간 1:N 관계 설계
- SQLAlchemy 모델과 실제 DB 스키마 동기화의 중요성

### Authentication & Security

- Flask-Login을 활용한 세션 인증
- Werkzeug 기반 비밀번호 해싱
- `UserMixin` 및 `user_loader` 구현
- `current_user`와 `login_required` 활용
- 인증(Authentication)과 인가(Authorization)의 차이
- `.env` 파일을 이용한 환경변수 관리

### Frontend Integration

- HTML Form을 통한 데이터 제출
- JavaScript `fetch()`를 이용한 HTTP 요청
- `JSON.stringify()`를 통한 JSON 데이터 변환
- `.then()`과 `.catch()`를 이용한 비동기 응답 처리
- Jinja2 템플릿을 통한 동적 데이터 렌더링

## 🔧 Troubleshooting

### 1. `Unknown column 'memo.user_id'`

**원인**

기존 MySQL 테이블에 `user_id` 컬럼이 없었지만, SQLAlchemy 모델에는 해당 컬럼이 추가되어 발생한 오류입니다.

**해결**

- MySQL 테이블에 `user_id` 컬럼 추가
- 기존 메모 데이터의 사용자 ID 연결
- `user.id`를 참조하는 Foreign Key 설정

**학습 내용**

`db.create_all()`은 기존 테이블의 컬럼을 자동으로 변경하지 않으며, 스키마 변경 시 별도의 마이그레이션이 필요합니다.

### 2. `401 Unauthorized`

**원인**

회원가입이 완료되지 않아 사용자 정보가 DB에 저장되지 않은 상태에서 로그인을 시도했습니다.

**해결**

- 회원가입 요청 및 HTTP 응답 확인
- MySQL `user` 테이블 데이터 확인
- 사용자 정보 저장 후 로그인 재시도

### 3. `405 Method Not Allowed`

**원인**

브라우저에서 `/signup` 링크를 클릭하면 GET 요청이 발생하지만, Flask 라우트에서는 POST 요청만 허용하고 있었습니다.

**해결**

GET 요청으로 회원가입 페이지를 렌더링하고, POST 요청으로 실제 회원가입을 처리하도록 수정했습니다.

### 4. Windows PowerShell의 JSON 요청 오류

**원인**

PowerShell에서 `curl.exe`로 JSON을 전송할 때 따옴표가 의도와 다르게 처리되어 올바르지 않은 요청이 발생했습니다.

**해결**

PowerShell의 `Invoke-RestMethod`와 `ConvertTo-Json`을 활용하여 API 요청을 테스트했습니다.

## 📌 Future Improvements

- Flask-Migrate를 활용한 데이터베이스 마이그레이션
- 회원가입 및 로그인 입력값 검증 강화
- CSRF 방어 및 인증 보안 개선
- 예외 처리와 사용자 피드백 개선
- API 자동화 테스트
- 배포 환경 구성

---

**Repository:** https://github.com/suminkoh/flask-mymemo

**Purpose:** Flask 기반 웹 애플리케이션의 CRUD, ORM, 사용자 인증 및 데이터베이스 연동 학습
