from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
import os
from urllib.parse import urlencode
from dotenv import load_dotenv

from database import get_db
import models
import schemas
from auth import create_access_token, get_current_user

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


@router.get("/google/login")
def google_login():
    """Google OAuth 로그인 URL 반환"""
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return {"url": url}


@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    """Google OAuth 콜백 처리 - 토큰 교환 및 JWT 발급"""
    # 1. Authorization code를 access token으로 교환
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )

    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Google 토큰 교환 실패")

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    # 2. Google Userinfo API로 사용자 정보 조회
    async with httpx.AsyncClient() as client:
        userinfo_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )

    if userinfo_response.status_code != 200:
        raise HTTPException(status_code=400, detail="사용자 정보 조회 실패")

    userinfo = userinfo_response.json()

    # 3. DB에 사용자 저장 또는 조회
    google_id = userinfo.get("sub")
    email = userinfo.get("email")
    name = userinfo.get("name", email)
    picture = userinfo.get("picture")

    user = db.query(models.User).filter(models.User.google_id == google_id).first()
    if not user:
        user = models.User(
            email=email,
            name=name,
            google_id=google_id,
            picture=picture,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # 프로필 정보 업데이트
        user.name = name
        user.picture = picture
        db.commit()

    # 4. JWT 발급
    jwt_token = create_access_token({"sub": str(user.id)})

    # 5. 프론트엔드로 리다이렉트 (토큰 전달)
    return RedirectResponse(
        url=f"{FRONTEND_URL}/auth/callback?token={jwt_token}"
    )


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    """현재 로그인한 사용자 정보 반환"""
    return current_user


@router.post("/logout")
def logout(current_user: models.User = Depends(get_current_user)):
    """로그아웃 (클라이언트에서 토큰 삭제)"""
    return {"message": "로그아웃 되었습니다."}
