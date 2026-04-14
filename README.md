# Week 5 딥러닝 학습 플랫폼

딥러닝 5주차 핵심 개념(Regularization, Overfitting, Data Augmentation, Transfer Learning, CNN 등)을 학습할 수 있는 Freemium 웹 애플리케이션입니다.

## 배포 주소

- **프론트엔드**: https://week5-hw.vercel.app
- **백엔드 API**: https://week5hw-production.up.railway.app
- **API 문서**: https://week5hw-production.up.railway.app/docs

---

## 주요 기능

- Google OAuth 2.0 소셜 로그인
- 딥러닝 8개 섹션 (개념 설명 + 코드 예시 + 결과 해석)
- Freemium 모델: 5개 섹션 무료, 6번째부터 결제 필요
- 실시간 사용량 카운터
- 결제 팝업(Paywall) 및 Polar.sh 결제 페이지 연동
- 프리미엄 결제 완료 시 자동 권한 업그레이드 (Webhook)

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | React 18 + Tailwind CSS + Vite |
| Backend | FastAPI + SQLAlchemy + SQLite |
| 인증 | Google OAuth 2.0 + JWT |
| 결제 | Polar.sh |
| 프론트 배포 | Vercel |
| 백엔드 배포 | Railway (Docker) |

---

## 프로젝트 구조

```
week5-webapp/
├── frontend/                  # React 프론트엔드
│   ├── src/
│   │   ├── api/client.js      # Axios 인스턴스
│   │   ├── context/
│   │   │   └── AuthContext.jsx  # 인증 상태 관리
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ContentCard.jsx
│   │   │   ├── PaywallModal.jsx
│   │   │   ├── UsageBar.jsx
│   │   │   └── CodeBlock.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ContentPage.jsx
│   │   │   ├── AuthCallbackPage.jsx
│   │   │   └── PaymentSuccessPage.jsx
│   │   └── main.jsx
│   ├── public/_redirects       # SPA 라우팅
│   └── vercel.json             # Vercel SPA 라우팅 설정
│
├── backend/                   # FastAPI 백엔드
│   ├── routers/
│   │   ├── auth.py            # Google OAuth 라우터
│   │   ├── content.py         # 콘텐츠 + 사용량 추적
│   │   └── payment.py         # Polar.sh Webhook 처리
│   ├── main.py                # FastAPI 앱 엔트리포인트
│   ├── database.py            # SQLAlchemy SQLite 설정
│   ├── models.py              # User, UsageLog 모델
│   ├── schemas.py             # Pydantic 스키마
│   ├── auth.py                # JWT 유틸리티
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── run.py                 # Railway 실행 파일
│   └── railway.json
│
├── docs/                      # 문서
│   ├── PRD.md                 # 제품 요구사항
│   ├── TRD.md                 # 기술 요구사항
│   ├── SETUP_GUIDE.md         # OAuth, Polar.sh 설정 가이드
│   └── DEPLOY_GUIDE.md        # 배포 가이드
│
├── install.bat                # Windows 자동 설치 스크립트
└── .env.example               # 환경변수 예시
```

---

## 학습 콘텐츠 (8개 섹션)

| 섹션 | 주제 | 접근 |
|------|------|------|
| 1 | 🛡️ Regularization (규제) | 무료 |
| 2 | ⚖️ Overfitting vs Underfitting | 무료 |
| 3 | 🖼️ Data Augmentation (데이터 증강) | 무료 |
| 4 | 🧠 Transfer Learning (전이 학습) | 무료 |
| 5 | ✍️ MNIST CNN 실습 | 무료 |
| 6 | ⏹️ Early Stopping (조기 종료) | 프리미엄 |
| 7 | 🔧 Hyperparameter Tuning | 프리미엄 |
| 8 | 📊 Model Evaluation (모델 평가 지표) | 프리미엄 |

---

## 로컬 실행 방법

### 자동 설치 (Windows)
```
install.bat 더블클릭
```

### 수동 설치

**백엔드:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# .env 파일 설정 후
uvicorn main:app --reload
```

**프론트엔드:**
```bash
cd frontend
npm install
# .env.local 설정 후
npm run dev
```

접속 주소:
- 프론트엔드: http://localhost:5173
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs

---

## 환경변수

### 백엔드 (backend/.env)

```env
SECRET_KEY=your_jwt_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
FRONTEND_URL=http://localhost:5173
FREE_USAGE_LIMIT=5
POLAR_ACCESS_TOKEN=your_polar_access_token
POLAR_PRODUCT_ID=your_polar_product_id
POLAR_WEBHOOK_SECRET=your_polar_webhook_secret
```

### 프론트엔드 (frontend/.env.local)

```env
VITE_API_URL=http://localhost:8000
```

---

## 인증 흐름

```
사용자 → Google 로그인 버튼 클릭
→ 백엔드 /auth/google/login (Google OAuth URL 반환)
→ Google 동의 화면
→ 백엔드 /auth/google/callback (JWT 발급)
→ 프론트엔드 /auth/callback?token=...
→ localStorage 저장 후 메인 페이지 이동
```

## 결제 흐름

```
사용자 → 6번째 섹션 클릭
→ 백엔드 402 응답
→ 페이월 팝업 표시
→ "프리미엄 시작하기" 클릭
→ 백엔드 /payment/checkout (Polar.sh 체크아웃 URL 생성)
→ Polar.sh 결제 페이지
→ 결제 완료
→ Polar.sh Webhook → 백엔드 /payment/webhook
→ 사용자 is_premium = True 업데이트
→ 모든 섹션 무제한 열람 가능
```

---

## 배포 과정 요약

### 프론트엔드 (Vercel)

1. Vercel 대시보드 → GitHub 저장소 연결
2. Root Directory: `frontend`
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. 환경변수 `VITE_API_URL` 추가
6. `vercel.json`에 SPA 라우팅 rewrites 설정

### 백엔드 (Railway)

1. Railway 대시보드 → GitHub 저장소 연결
2. Root Directory: `backend`
3. Dockerfile 자동 감지 및 빌드
4. 환경변수 설정 (위 목록 참고)
5. Networking → Port: `8080`
6. `run.py`에서 `PORT` 환경변수 읽어 uvicorn 실행

---

## 트러블슈팅 기록

| 문제 | 원인 | 해결 방법 |
|------|------|----------|
| Railway pip not found | nixpacks 빌드 오류 | Dockerfile로 전환 |
| $PORT not valid integer | railway.json startCommand에서 env var 미확장 | run.py에서 Python으로 PORT 읽기 |
| Railway port mismatch | 서버 8080 / Railway 네트워킹 8000 불일치 | Railway Networking 포트를 8080으로 변경 |
| Google OAuth invalid_request | GOOGLE_REDIRECT_URI에 개행문자 포함 | Railway Variables 값 재입력 |
| Vercel 404 on page refresh | SPA 라우팅 미설정 | vercel.json rewrites 추가 |
| 프론트에서 Google 리디렉션 안 됨 | 백엔드 URL 직접 호출 대신 API로 URL 받아야 함 | AuthContext.login()에서 /auth/google/login API 호출 후 리디렉션 |
| Polar.sh insufficient_scope | API 토큰 권한 부족 | 전체 권한으로 토큰 재발급 |
| 사용량 카운터 실시간 미반영 | 섹션 열람 후 refreshUsage 미호출 | ContentPage에서 섹션 로드 후 refreshUsage() 호출 |

---

## 문서

- [PRD](docs/PRD.md) - 제품 요구사항
- [TRD](docs/TRD.md) - 기술 요구사항
- [설정 가이드](docs/SETUP_GUIDE.md) - OAuth, Polar.sh, 환경변수 설정
- [배포 가이드](docs/DEPLOY_GUIDE.md) - GitHub → Vercel + Railway 배포
