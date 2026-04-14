# Week 5 딥러닝 학습 플랫폼

딥러닝 5주차 핵심 개념(Regularization, Overfitting, Data Augmentation, Transfer Learning, CNN)을
Google OAuth 로그인과 Freemium 모델(5회 무료 → 유료)로 제공하는 학습 플랫폼입니다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | React 18 + Tailwind CSS + Vite |
| Backend | FastAPI + SQLAlchemy |
| DB | SQLite |
| 인증 | Google OAuth 2.0 |
| 결제 | Polar.sh |
| 배포 | Vercel (Frontend) + Railway (Backend) |

## 빠른 시작

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

## 설정 파일
- `.env.example` → `backend/.env`로 복사 후 값 입력
- `frontend/.env.example` → `frontend/.env.local`로 복사

## 문서
- [PRD](docs/PRD.md) - 제품 요구사항
- [TRD](docs/TRD.md) - 기술 요구사항
- [설정 가이드](docs/SETUP_GUIDE.md) - OAuth, Polar.sh, 환경변수 설정
- [배포 가이드](docs/DEPLOY_GUIDE.md) - GitHub → Vercel + Railway 배포

## URL
- 프론트엔드: http://localhost:5173
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs
