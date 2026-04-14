@echo off
chcp 65001 > nul
title Week5 딥러닝 학습 플랫폼 - 설치 및 실행

echo.
echo ====================================================
echo   Week 5 딥러닝 학습 플랫폼 - 자동 설치 스크립트
echo ====================================================
echo.

:: ─────────────────────────────────────────
:: 1. Python 버전 확인
:: ─────────────────────────────────────────
echo [1/6] Python 버전 확인 중...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python 3.10+ 를 설치해 주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

:: ─────────────────────────────────────────
:: 2. Node.js 버전 확인
:: ─────────────────────────────────────────
echo [2/6] Node.js 버전 확인 중...
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Node.js가 설치되어 있지 않습니다.
    echo Node.js 18+ 를 설치해 주세요: https://nodejs.org/
    pause
    exit /b 1
)
node --version
npm --version
echo.

:: ─────────────────────────────────────────
:: 3. 백엔드 .env 파일 설정
:: ─────────────────────────────────────────
echo [3/6] 환경 변수 파일 설정 중...

if not exist "backend\.env" (
    if exist ".env.example" (
        copy .env.example backend\.env > nul
        echo [생성] backend\.env 파일이 생성되었습니다.
        echo.
        echo ============================================================
        echo  ⚠️  중요: backend\.env 파일을 열어 다음 값을 입력하세요:
        echo ============================================================
        echo   GOOGLE_CLIENT_ID    = Google Cloud Console에서 발급
        echo   GOOGLE_CLIENT_SECRET= Google Cloud Console에서 발급
        echo   SECRET_KEY          = 랜덤 문자열 (아래 명령으로 생성)
        echo   POLAR_ACCESS_TOKEN  = Polar.sh 대시보드에서 발급
        echo   POLAR_PRODUCT_ID    = Polar.sh 상품 ID
        echo   POLAR_WEBHOOK_SECRET= Polar.sh Webhook 시크릿
        echo ============================================================
        echo.
        echo  SECRET_KEY 생성 방법:
        echo  python -c "import secrets; print(secrets.token_hex(32))"
        echo.
        echo  설정 가이드: docs\SETUP_GUIDE.md 파일 참조
        echo.
        set /p CONTINUE="backend\.env 파일 수정 후 Enter를 누르세요..."
    ) else (
        echo [경고] .env.example 파일을 찾을 수 없습니다.
    )
) else (
    echo [확인] backend\.env 파일이 이미 존재합니다.
)

:: Frontend .env
if not exist "frontend\.env.local" (
    if exist "frontend\.env.example" (
        copy frontend\.env.example frontend\.env.local > nul
        echo [생성] frontend\.env.local 파일이 생성되었습니다.
    )
)
echo.

:: ─────────────────────────────────────────
:: 4. 백엔드 패키지 설치
:: ─────────────────────────────────────────
echo [4/6] 백엔드 패키지 설치 중...
cd backend

python -m venv venv > nul 2>&1
if %errorlevel% neq 0 (
    echo [경고] 가상환경 생성 실패. 전역 pip로 설치합니다.
    pip install -r requirements.txt
) else (
    echo [완료] 가상환경 생성 완료
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

if %errorlevel% neq 0 (
    echo [오류] 백엔드 패키지 설치 실패
    cd ..
    pause
    exit /b 1
)
echo [완료] 백엔드 패키지 설치 완료
cd ..
echo.

:: ─────────────────────────────────────────
:: 5. 프론트엔드 패키지 설치
:: ─────────────────────────────────────────
echo [5/6] 프론트엔드 패키지 설치 중...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo [오류] 프론트엔드 패키지 설치 실패
    cd ..
    pause
    exit /b 1
)
echo [완료] 프론트엔드 패키지 설치 완료
cd ..
echo.

:: ─────────────────────────────────────────
:: 6. 서버 실행
:: ─────────────────────────────────────────
echo [6/6] 서버 시작 중...
echo.
echo ====================================================
echo   서버 시작 완료!
echo ====================================================
echo.
echo   🔵 백엔드 API:  http://localhost:8000
echo   🟢 프론트엔드:  http://localhost:5173
echo   📖 API 문서:    http://localhost:8000/docs
echo.
echo   종료: Ctrl+C (각 창에서)
echo ====================================================
echo.

:: 백엔드 서버 (새 창에서 실행)
start "백엔드 서버 (FastAPI)" cmd /k "cd /d %~dp0backend && (if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) else (echo 가상환경 없음)) && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: 3초 대기 후 프론트엔드 실행
timeout /t 3 /nobreak > nul

:: 프론트엔드 서버 (새 창에서 실행)
start "프론트엔드 서버 (React)" cmd /k "cd /d %~dp0frontend && npm run dev"

:: 5초 후 브라우저 열기
timeout /t 5 /nobreak > nul
start http://localhost:5173

echo.
echo 두 개의 서버 창이 열렸습니다.
echo 브라우저에서 http://localhost:5173 을 확인하세요.
echo.
pause
