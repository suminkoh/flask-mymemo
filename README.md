# 📝 Flask MyMemo

Flask + MySQL 기반 개인 메모 관리 웹 앱 (회원가입/로그인 후 본인 메모 CRUD)

## 🛠 Tech Stack

Python 3.12 · Flask · MySQL · Flask-SQLAlchemy · Flask-Login · Werkzeug · Jinja2 · uv · python-dotenv

## ✨ 핵심 기능

- **인증**: 회원가입/로그인/로그아웃, 비밀번호 해시 저장(Werkzeug), 세션 인증(Flask-Login), `@login_required`
- **메모 CRUD**: 로그인 사용자별 메모 생성·조회·수정·삭제, 타인 메모 접근 차단
- **프론트**: Jinja2 렌더링 + JS `fetch()` 비동기 요청

## 🗄 DB 설계 (User 1 : N Memo)

| Table | Columns |
|-------|---------|
| User | id(PK), username(Unique), email(Unique), password_hash |
| Memo | id(PK), user_id(FK → user.id), title, content |

## 🔗 API Endpoints

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| GET | `/` | 메인 | X |
| GET/POST | `/signup` | 회원가입 | X |
| POST | `/login` | 로그인 | X |
| GET | `/logout` | 로그아웃 | O |
| GET | `/memos` | 내 메모 조회 | O |
| POST | `/memos/create` | 메모 생성 | O |
| PUT | `/memos/update/<id>` | 메모 수정 | O |
| DELETE | `/memos/delete/<id>` | 메모 삭제 | O |

## 🚀 실행 방법

```bash
# 1. 의존성 설치
uv sync

# 2. DB 생성 (MySQL)
CREATE DATABASE IF NOT EXISTS flask_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 3. .env 작성
DATABASE_URL=mysql+pymysql://USER:PASSWORD@localhost:3306/flask_db
SECRET_KEY=...   # uv run python -c "import secrets; print(secrets.token_hex(32))"

# 4. 실행
uv run flask --app my_memo_app.app run --debug
```

> ⚠️ `db.create_all()`은 **없는 테이블만** 생성합니다. 기존 테이블의 컬럼 변경은 반영되지 않으므로 마이그레이션(Flask-Migrate)이 필요합니다.

## 🔐 인증 흐름

회원가입(비밀번호 해시) → DB 저장 → 로그인 시 비밀번호 검증 → `login_user()`로 세션 생성 → `@login_required`로 접근 제한 → `current_user.id`로 소유권 확인 → `logout_user()`

## 📚 핵심 학습 포인트

- `request.form` vs `request.get_json()` 차이
- `db.session.add()` / `commit()`의 역할
- `UserMixin`, `user_loader`, `current_user`
- **인증(Authentication) vs 인가(Authorization)** 구분
- 모델과 실제 DB 스키마 동기화의 중요성

## 🔧 주요 트러블슈팅

| 오류 | 원인 | 해결 |
|------|------|------|
| `Unknown column 'memo.user_id'` | 모델엔 있으나 DB 테이블엔 컬럼 없음 | 컬럼·FK 직접 추가 (이후 마이그레이션 도입) |
| `401 Unauthorized` | 회원가입 미완료 상태에서 로그인 시도 | 가입 후 DB 저장 확인 |
| `405 Method Not Allowed` | `/signup` 라우트가 POST만 허용 | GET(페이지)·POST(처리) 모두 허용 |
| PowerShell JSON 오류 | `curl.exe`의 따옴표 처리 문제 | `Invoke-RestMethod` + `ConvertTo-Json` 사용 |

## 📌 개선 예정

Flask-Migrate 도입 · 입력값 검증 · CSRF 방어 · 예외 처리 · 자동화 테스트 · 배포 환경

---

**Repo:** https://github.com/suminkoh/flask-mymemo
