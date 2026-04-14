from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from database import engine, Base
from routers import auth, content, payment

load_dotenv()

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Week 5 딥러닝 학습 플랫폼 API",
    description="Regularization, Overfitting, Data Augmentation, Transfer Learning, CNN 학습 플랫폼",
    version="1.0.0"
)

# CORS 설정
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(content.router)
app.include_router(payment.router)


@app.get("/")
def root():
    return {
        "message": "Week 5 딥러닝 학습 플랫폼 API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}
