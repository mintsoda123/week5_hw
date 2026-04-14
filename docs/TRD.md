# TRD (Technical Requirements Document)
# Week 5 딥러닝 학습 플랫폼

---

## 1. 시스템 아키텍처

```
[사용자 브라우저]
       │
       ▼
[Frontend: React + Tailwind] ← Vercel CDN
       │  REST API 호출
       ▼
[Backend: FastAPI] ← Railway / Render (or Local)
       │
       ▼
[SQLite DB] ← 로컬 파일 (개발) / 별도 스토리지 (프로덕션)

[Google OAuth 2.0] ← 인증 서버
[Polar.sh Webhook] ← 결제 이벤트
```

### 기술 스택 요약
| 레이어 | 기술 | 버전 |
|--------|------|------|
| Frontend | React | 18.x |
| UI 프레임워크 | Tailwind CSS | 3.x |
| 빌드 도구 | Vite | 5.x |
| Backend | FastAPI | 0.111.x |
| DB ORM | SQLAlchemy | 2.x |
| DB | SQLite | 3.x |
| 인증 | Google OAuth 2.0 + JWT | - |
| 결제 | Polar.sh | latest |
| 배포 (Frontend) | Vercel | - |
| 배포 (Backend) | Railway 또는 Render | - |

---

## 2. 백엔드 설계 (FastAPI)

### 2.1 디렉토리 구조
```
backend/
├── main.py              # FastAPI 앱 진입점
├── database.py          # SQLAlchemy 설정
├── models.py            # DB 모델
├── schemas.py           # Pydantic 스키마
├── auth.py              # JWT 유틸리티
├── routers/
│   ├── auth.py          # Google OAuth 라우터
│   ├── content.py       # 컨텐츠 + 사용량 라우터
│   └── payment.py       # Polar.sh Webhook 라우터
└── requirements.txt
```

### 2.2 데이터베이스 모델

**users 테이블**
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | 자동 증가 |
| email | VARCHAR UNIQUE | Gmail 주소 |
| name | VARCHAR | 이름 |
| google_id | VARCHAR UNIQUE | Google sub |
| picture | VARCHAR | 프로필 이미지 URL |
| is_premium | BOOLEAN | 유료 여부 |
| usage_count | INTEGER | 총 사용 횟수 |
| created_at | DATETIME | 가입일 |

**usage_logs 테이블**
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | - |
| user_id | INTEGER FK | users.id |
| section_id | VARCHAR | 섹션 식별자 |
| accessed_at | DATETIME | 접근 시각 |

### 2.3 API 엔드포인트

| 메서드 | 경로 | 설명 | 인증 |
|--------|------|------|------|
| GET | /auth/google/login | OAuth 리다이렉트 URL 반환 | ❌ |
| GET | /auth/google/callback | 토큰 교환 + JWT 발급 | ❌ |
| GET | /auth/me | 현재 사용자 정보 | ✅ |
| POST | /auth/logout | 로그아웃 | ✅ |
| GET | /content/ | 컨텐츠 목록 | ✅ |
| GET | /content/{section_id} | 섹션 열람 (사용량 차감) | ✅ |
| GET | /usage/status | 사용량 현황 | ✅ |
| POST | /payment/webhook | Polar.sh 이벤트 수신 | 서명 검증 |
| GET | /payment/checkout | Polar.sh 결제 링크 | ✅ |

### 2.4 인증 흐름 (Google OAuth 2.0 PKCE)
```
1. Frontend → GET /auth/google/login
2. Backend → Google OAuth URL 반환
3. Frontend → Google 로그인 페이지로 리다이렉트
4. Google → /auth/google/callback?code=xxx 콜백
5. Backend → code를 access_token으로 교환
6. Backend → Google Userinfo API 호출 (email, name, picture)
7. Backend → DB에 사용자 저장 or 조회
8. Backend → JWT 발급 후 Frontend로 리다이렉트
9. Frontend → JWT를 localStorage에 저장
```

### 2.5 사용량 제한 로직
```python
FREE_LIMIT = 5

def check_usage(user, section_id):
    if user.is_premium:
        return True  # 프리미엄: 무제한
    if user.usage_count >= FREE_LIMIT:
        # 이미 본 섹션인지 확인
        existing = db.query(UsageLog).filter(
            user_id=user.id, section_id=section_id
        ).first()
        if existing:
            return True  # 이미 본 섹션: 재방문 허용
        raise HTTPException(402, "무료 한도 초과")
    return True
```

---

## 3. 프론트엔드 설계 (React + Tailwind)

### 3.1 디렉토리 구조
```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          # 상단 네비게이션
│   │   ├── ContentCard.jsx     # 섹션 카드
│   │   ├── PaywallModal.jsx    # 결제 유도 모달
│   │   ├── UsageBar.jsx        # 사용량 표시 바
│   │   └── CodeBlock.jsx       # 코드 하이라이팅
│   ├── pages/
│   │   ├── HomePage.jsx        # 메인 페이지
│   │   └── ContentPage.jsx     # 섹션 상세 페이지
│   ├── context/
│   │   └── AuthContext.jsx     # 인증 상태 관리
│   ├── api/
│   │   └── client.js           # Axios 인스턴스
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── package.json
├── tailwind.config.js
└── vite.config.js
```

### 3.2 상태 관리
- **AuthContext**: 사용자 정보, JWT 토큰, 로그인 상태
- **로컬 상태**: 각 페이지의 로딩/에러 상태

### 3.3 컴포넌트 설명
- **Navbar**: 로그인 버튼 / 사용자 프로필 / 사용량 카운터
- **ContentCard**: 섹션 제목, 설명, "학습하기" 버튼
- **PaywallModal**: 결제 유도, Polar.sh 링크 연결
- **UsageBar**: "5회 중 N회 사용" 시각적 표시

---

## 4. 결제 설계 (Polar.sh)

### 4.1 흐름
```
1. 사용자 → "결제하기" 클릭
2. Frontend → GET /payment/checkout
3. Backend → Polar.sh Checkout URL 반환
4. 사용자 → Polar.sh 결제 페이지에서 결제
5. Polar.sh → POST /payment/webhook (이벤트: order.created)
6. Backend → 서명 검증 후 user.is_premium = True 업데이트
7. 사용자 → 다음 로그인 시 프리미엄 상태 반영
```

### 4.2 Webhook 이벤트
```json
{
  "type": "order.created",
  "data": {
    "customer_email": "user@gmail.com",
    "product_id": "polar_product_id",
    "status": "paid"
  }
}
```

---

## 5. 환경 변수

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# JWT
SECRET_KEY=your_super_secret_jwt_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7

# Polar.sh
POLAR_ACCESS_TOKEN=your_polar_access_token
POLAR_PRODUCT_ID=your_polar_product_id
POLAR_WEBHOOK_SECRET=your_polar_webhook_secret

# App
FRONTEND_URL=http://localhost:5173
DATABASE_URL=sqlite:///./app.db
FREE_USAGE_LIMIT=5
```

---

## 6. 배포 아키텍처

### 개발 환경
- Backend: `uvicorn main:app --reload` (포트 8000)
- Frontend: `npm run dev` (포트 5173)

### 프로덕션
- **Frontend** → Vercel (자동 빌드, CDN)
- **Backend** → Railway 또는 Render (무료 티어 가능)
- **DB** → SQLite (단일 인스턴스) → 스케일 필요 시 PostgreSQL 전환

### Vercel 설정 (vercel.json)
```json
{
  "builds": [
    { "src": "frontend/package.json", "use": "@vercel/static-build" }
  ]
}
```

---

## 7. 보안 고려사항

| 항목 | 구현 방법 |
|------|---------|
| JWT 검증 | 모든 보호된 엔드포인트에 Bearer 토큰 검증 |
| CORS | 허용된 origin만 설정 |
| Webhook 검증 | Polar.sh 서명(HMAC-SHA256) 검증 |
| SQL Injection | SQLAlchemy ORM 사용 (파라미터화 쿼리) |
| HTTPS | Vercel/Railway 기본 제공 |
