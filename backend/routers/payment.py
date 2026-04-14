from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
import os
import hmac
import hashlib
import httpx
import json
from dotenv import load_dotenv

from database import get_db
import models
import schemas
from auth import get_current_user

load_dotenv()

router = APIRouter(prefix="/payment", tags=["payment"])

POLAR_ACCESS_TOKEN = os.getenv("POLAR_ACCESS_TOKEN")
POLAR_PRODUCT_ID = os.getenv("POLAR_PRODUCT_ID")
POLAR_WEBHOOK_SECRET = os.getenv("POLAR_WEBHOOK_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


@router.get("/checkout", response_model=schemas.CheckoutResponse)
async def get_checkout_url(current_user: models.User = Depends(get_current_user)):
    """Polar.sh 결제 URL 생성"""
    if current_user.is_premium:
        raise HTTPException(status_code=400, detail="이미 프리미엄 사용자입니다.")

    # Polar.sh Checkout 세션 생성
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.polar.sh/v1/checkouts/",
            headers={
                "Authorization": f"Bearer {POLAR_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "product_id": POLAR_PRODUCT_ID,
                "success_url": f"{FRONTEND_URL}/payment/success",
                "customer_email": current_user.email,
                "metadata": {
                    "user_id": str(current_user.id),
                    "user_email": current_user.email
                }
            }
        )

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=500,
            detail=f"결제 링크 생성 실패: {response.text}"
        )

    data = response.json()
    checkout_url = data.get("url") or data.get("checkout_url")

    if not checkout_url:
        raise HTTPException(status_code=500, detail="결제 URL을 받지 못했습니다.")

    return {"checkout_url": checkout_url}


@router.post("/webhook")
async def polar_webhook(
    request: Request,
    webhook_id: str = Header(None, alias="webhook-id"),
    webhook_timestamp: str = Header(None, alias="webhook-timestamp"),
    webhook_signature: str = Header(None, alias="webhook-signature"),
    db: Session = Depends(get_db)
):
    """Polar.sh Webhook 처리 - 결제 완료 시 프리미엄 활성화"""
    body = await request.body()

    # Webhook 서명 검증 (보안)
    if POLAR_WEBHOOK_SECRET:
        expected_signature = hmac.new(
            POLAR_WEBHOOK_SECRET.encode(),
            msg=f"{webhook_id}.{webhook_timestamp}.{body.decode()}".encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        received_sig = webhook_signature.split(",")[-1] if webhook_signature else ""
        if not hmac.compare_digest(f"v1={expected_signature}", received_sig):
            raise HTTPException(status_code=401, detail="Webhook 서명 검증 실패")

    payload = json.loads(body)
    event_type = payload.get("type")

    # 주문 완료 이벤트 처리
    if event_type in ("order.created", "subscription.created", "subscription.active"):
        data = payload.get("data", {})

        # 고객 이메일 추출 (이벤트 구조에 따라 경로 다를 수 있음)
        customer_email = (
            data.get("customer", {}).get("email") or
            data.get("customer_email") or
            payload.get("data", {}).get("metadata", {}).get("user_email")
        )

        if customer_email:
            user = db.query(models.User).filter(
                models.User.email == customer_email
            ).first()

            if user:
                user.is_premium = True
                db.commit()
                return {"status": "success", "message": f"{customer_email} 프리미엄 활성화"}

    return {"status": "received", "type": event_type}
