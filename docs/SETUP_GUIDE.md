# 설정 가이드

---

## 질문 1: Google Gmail OAuth 설정 방법

### 📌 어디서, 무엇을 해야 하는가?

#### Step 1: Google Cloud Console 접속
1. [https://console.cloud.google.com/](https://console.cloud.google.com/) 접속
2. Google 계정으로 로그인
3. 상단의 **프로젝트 선택** → **새 프로젝트** 클릭
4. 프로젝트 이름 입력 (예: `week5-webapp`) → **만들기**

#### Step 2: OAuth 동의 화면 설정
1. 좌측 메뉴 → **API 및 서비스** → **OAuth 동의 화면**
2. User Type: **외부** 선택 → **만들기**
3. 앱 정보 입력:
   - 앱 이름: `Week5 딥러닝 플랫폼`
   - 사용자 지원 이메일: 본인 Gmail 입력
   - 개발자 연락처 이메일: 본인 Gmail 입력
4. **저장 후 계속** 클릭 (나머지는 기본값)

#### Step 3: OAuth 2.0 클라이언트 ID 만들기
1. 좌측 메뉴 → **API 및 서비스** → **사용자 인증 정보**
2. **+ 사용자 인증 정보 만들기** → **OAuth 클라이언트 ID**
3. 애플리케이션 유형: **웹 애플리케이션**
4. 이름: `week5-webapp`
5. **승인된 리디렉션 URI** 에 추가:
   - `http://localhost:8000/auth/google/callback` (개발용)
   - `https://your-backend.railway.app/auth/google/callback` (배포용)
6. **만들기** 클릭

#### Step 4: 키 복사
- **클라이언트 ID** → `.env`의 `GOOGLE_CLIENT_ID`에 붙여넣기
- **클라이언트 보안 비밀번호** → `.env`의 `GOOGLE_CLIENT_SECRET`에 붙여넣기

#### ⚠️ 주의사항
- 배포 후에는 리디렉션 URI에 실제 도메인도 추가해야 합니다
- 앱이 "테스트" 상태일 때는 등록된 테스트 사용자만 로그인 가능
- 실제 서비스 시 **앱 게시** (프로덕션으로 전환) 필요

---

## 질문 2: Polar.sh 결제 설정 방법

### 📌 순서대로 따라하기

#### Step 1: Polar.sh 가입
1. [https://polar.sh](https://polar.sh) 접속
2. **Sign Up** → GitHub 계정으로 가입 (권장)

#### Step 2: Organization 만들기
1. 가입 후 **Create Organization** 클릭
2. 이름 입력 (예: `week5-learning`)
3. 슬러그(URL)는 자동 생성

#### Step 3: Product (상품) 만들기
1. 대시보드 → **Products** 탭 → **New Product** 클릭
2. 상품 정보 입력:
   - **Name**: `Week5 프리미엄 멤버십`
   - **Description**: 모든 딥러닝 섹션 무제한 접근
   - **Type**: One-time (일회성) 또는 Subscription (구독)
   - **Price**: 원하는 가격 설정 (예: $9.99)
3. **Create Product** 클릭
4. 생성된 Product의 **ID**를 복사 → `.env`의 `POLAR_PRODUCT_ID`

#### Step 4: API 토큰 발급
1. 우측 상단 프로필 → **Settings**
2. **API Keys** 탭 → **New API Key**
3. 이름 입력, 권한: `checkouts:write`, `orders:read` 선택
4. 생성된 토큰 복사 → `.env`의 `POLAR_ACCESS_TOKEN`

#### Step 5: Webhook 설정
1. Organization 설정 → **Webhooks** 탭
2. **Add Webhook**:
   - **URL**: `https://your-backend.railway.app/payment/webhook`
   - **Events**: `order.created` 체크
3. **Secret** 생성 → 복사 → `.env`의 `POLAR_WEBHOOK_SECRET`

#### ⚠️ 개발 환경에서 Webhook 테스트
로컬에서 Webhook을 받으려면 ngrok 사용:
```bash
# ngrok 설치 후
ngrok http 8000
# 출력된 https://xxxx.ngrok.io/payment/webhook 을 Polar Webhook URL로 설정
```

---

## 질문 3: Vercel에 GitHub 연동하여 배포하는 방법

### 📌 Frontend (React) → Vercel 배포

#### Step 1: GitHub에 코드 올리기 (다음 섹션 참조)
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/yourusername/week5-webapp.git
git push -u origin main
```

#### Step 2: Vercel 가입 및 연동
1. [https://vercel.com](https://vercel.com) → **Sign Up** → **Continue with GitHub**
2. GitHub 계정 연동

#### Step 3: 프로젝트 Import
1. Vercel 대시보드 → **Add New Project**
2. GitHub repository 목록에서 `week5-webapp` 선택 → **Import**

#### Step 4: 빌드 설정
```
Framework Preset: Vite
Root Directory: frontend          ← 반드시 설정!
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

#### Step 5: 환경 변수 설정
**Environment Variables** 섹션에 추가:
```
VITE_API_URL = https://your-backend.railway.app
```

#### Step 6: 배포
- **Deploy** 클릭 → 약 1-2분 후 배포 완료
- `https://week5-webapp.vercel.app` 형태의 URL 발급

#### Step 7: 자동 배포 (CI/CD)
- 이후 GitHub `main` 브랜치에 push 하면 **자동으로 재배포**됩니다!

### 📌 Backend (FastAPI) → Railway 배포

Vercel은 서버리스 환경이라 SQLite(파일 DB)와 맞지 않아 Backend는 Railway를 권장합니다.

#### Step 1: Railway 가입
1. [https://railway.app](https://railway.app) → **Login** → **GitHub 연동**

#### Step 2: 새 프로젝트
1. **New Project** → **Deploy from GitHub repo**
2. `week5-webapp` 선택

#### Step 3: 빌드 설정
- **Root Directory**: `backend`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Step 4: 환경 변수 설정
Railway 대시보드 → **Variables**에서 `.env` 내용 모두 입력

#### Step 5: 도메인 확인
- **Settings** → **Public Networking** → **Generate Domain**
- 발급된 URL을 Vercel의 `VITE_API_URL`과 Google OAuth 리디렉션 URI에 업데이트

---

## 질문 4: .env 파일 예시

`.env.example` 파일을 참조하세요. 아래는 실제 설정 순서입니다:

```env
# 1. Google Cloud Console에서 발급
GOOGLE_CLIENT_ID=123456789-abc.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxx

# 2. 콜백 URL (개발: localhost, 배포: 실제 도메인)
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# 3. JWT 시크릿 (임의의 긴 문자열 - 아래 명령으로 생성 가능)
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=a1b2c3d4e5f6...  # 64자리 hex 문자열
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7

# 4. Polar.sh 대시보드에서 발급
POLAR_ACCESS_TOKEN=polar_pat_xxxxxxxxxxxxxxxx
POLAR_PRODUCT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
POLAR_WEBHOOK_SECRET=your_webhook_secret

# 5. URL 설정 (개발 환경)
FRONTEND_URL=http://localhost:5173
DATABASE_URL=sqlite:///./app.db
FREE_USAGE_LIMIT=5
```

### SECRET_KEY 빠르게 생성하기
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
