# 배포 가이드: GitHub → Vercel + Railway

---

## 전체 배포 흐름

```
로컬 코드
  ↓ git push
GitHub 저장소
  ↓ 자동 감지
Vercel (Frontend)   +   Railway (Backend)
  ↓
서비스 운영 중
```

---

## Step 1: GitHub 저장소 만들기

### 1-1. GitHub에서 새 저장소 생성
1. [https://github.com](https://github.com) 로그인
2. 우측 상단 **+** → **New repository**
3. 설정:
   - **Repository name**: `week5-webapp`
   - **Visibility**: Public (Vercel 무료 플랜은 Public 권장)
   - **Initialize**: 체크 해제 (이미 로컬에 코드가 있으므로)
4. **Create repository** 클릭

### 1-2. 로컬에서 Git 초기화 및 Push

```bash
# week5-webapp 폴더에서 실행
cd C:\Users\my\week5-webapp

# Git 초기화
git init

# 모든 파일 스테이징 (.gitignore가 .env 제외)
git add .

# 첫 커밋
git commit -m "feat: Week5 딥러닝 학습 플랫폼 초기 구성"

# GitHub 원격 저장소 연결 (URL은 본인 저장소로 변경)
git remote add origin https://github.com/your-username/week5-webapp.git

# main 브랜치로 push
git branch -M main
git push -u origin main
```

> ⚠️ `.env` 파일이 push되지 않도록 `.gitignore`를 반드시 확인하세요!

---

## Step 2: Backend → Railway 배포

### 2-1. Railway 가입 및 프로젝트 생성
1. [https://railway.app](https://railway.app) → **Login** → **GitHub 연동**
2. **New Project** → **Deploy from GitHub repo**
3. `week5-webapp` 저장소 선택

### 2-2. Service 설정
Railway가 자동으로 코드를 감지하지만, 루트가 `backend/`이므로:
1. 서비스 선택 → **Settings**
2. **Root Directory**: `backend`
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2-3. 환경 변수 설정
서비스 → **Variables** 탭:
```
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=https://your-railway-app.railway.app/auth/google/callback
SECRET_KEY=...
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7
POLAR_ACCESS_TOKEN=...
POLAR_PRODUCT_ID=...
POLAR_WEBHOOK_SECRET=...
FRONTEND_URL=https://week5-webapp.vercel.app  ← Vercel 배포 후 업데이트
DATABASE_URL=sqlite:///./app.db
FREE_USAGE_LIMIT=5
```

### 2-4. 도메인 확인
- **Settings** → **Networking** → **Generate Domain**
- 예: `https://week5-webapp-production.up.railway.app`
- 이 URL을 기억해두세요!

### 2-5. Google OAuth 리디렉션 URI 업데이트
[Google Cloud Console](https://console.cloud.google.com) → OAuth 클라이언트 설정에서:
- 기존: `http://localhost:8000/auth/google/callback`
- 추가: `https://your-railway-app.railway.app/auth/google/callback`

---

## Step 3: Frontend → Vercel 배포

### 3-1. Vercel 가입
1. [https://vercel.com](https://vercel.com) → **Sign Up** → **Continue with GitHub**

### 3-2. 프로젝트 Import
1. Vercel 대시보드 → **Add New...** → **Project**
2. GitHub 저장소 목록에서 `week5-webapp` → **Import**

### 3-3. 빌드 설정 (매우 중요!)
```
Framework Preset:   Vite
Root Directory:     frontend          ← 클릭하여 frontend 선택
Build Command:      npm run build
Output Directory:   dist
Install Command:    npm install
```

### 3-4. 환경 변수 추가
**Environment Variables** 섹션:
```
Name:  VITE_API_URL
Value: https://your-railway-app.railway.app   ← Railway URL
```

### 3-5. Deploy!
- **Deploy** 클릭
- 약 1-2분 후 완료
- 발급된 URL: `https://week5-webapp.vercel.app`

---

## Step 4: 최종 URL 업데이트

배포 완료 후 각 서비스에 실제 URL 반영:

### Railway 환경 변수 업데이트
```
FRONTEND_URL = https://week5-webapp.vercel.app
```

### Polar.sh Webhook URL 업데이트
Polar.sh → Webhooks → URL 변경:
```
https://your-railway-app.railway.app/payment/webhook
```

### Google OAuth 리디렉션 URI 확인
Google Cloud Console에서 추가된 URI 확인:
```
https://your-railway-app.railway.app/auth/google/callback
```

---

## Step 5: 배포 확인

1. `https://week5-webapp.vercel.app` 접속
2. "Google로 로그인" 클릭 → 정상 로그인 확인
3. 섹션 5개 클릭해서 사용량 카운트 확인
4. 6번째 클릭 시 결제 모달 표시 확인

---

## 자동 재배포 (CI/CD)

이후 코드 수정 시:
```bash
git add .
git commit -m "fix: 버그 수정"
git push origin main
```
→ GitHub push 감지 → **Vercel/Railway 자동 재배포** 🚀

---

## 트러블슈팅

### CORS 오류 발생 시
`backend/main.py`의 `allow_origins`에 Vercel URL 추가:
```python
allow_origins=["https://week5-webapp.vercel.app", ...]
```

### SQLite 데이터 초기화 문제
Railway 재배포 시 SQLite 파일이 리셋될 수 있습니다.
- 개발/테스트 용도로는 OK
- 프로덕션에서는 Railway의 PostgreSQL 플러그인 사용 권장

### Google 로그인 "redirect_uri_mismatch" 오류
Google Cloud Console에서 리디렉션 URI가 정확히 등록되었는지 확인:
- 끝에 슬래시(/) 없어야 함
- http/https 정확히 구분
