import os, uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import stripe

from app.db.session import SessionLocal
from app.models.payment_request import PaymentRequest

router = APIRouter(prefix="/api", tags=["payments"])

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5173")
CURRENCY = os.getenv("CURRENCY", "GBP")
PHANTOMPAY_FEE_BPS = int(os.getenv("PHANTOMPAY_FEE_BPS", "100"))

stripe.api_key = STRIPE_SECRET_KEY

class CreateReqIn(BaseModel):
    amount: float = Field(..., gt=0, description="Amount in major units (e.g., 10.50)")
    description: str | None = None

@router.post("/create-request")
def create_request(body: CreateReqIn):
    h = uuid.uuid4().hex[:12]
    amount_minor = int(round(body.amount * 100))
    with SessionLocal() as db:
        pr = PaymentRequest(hash=h, amount_minor=amount_minor, description=body.description or "")
        db.add(pr)
        db.commit()
    return {"hash": h, "status": "created"}

@router.post("/checkout/{hash}")
def create_checkout(hash: str):
    with SessionLocal() as db:
        pr = db.query(PaymentRequest).filter_by(hash=hash).first()
        if not pr:
            raise HTTPException(status_code=404, detail="Not found")

        app_fee_minor = pr.amount_minor * PHANTOMPAY_FEE_BPS // 10_000
        try:
            session = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{
                    "price_data": {
                        "currency": CURRENCY.lower(),
                        "product_data": {"name": pr.description or "Payment"},
                        "unit_amount": pr.amount_minor,
                    },
                    "quantity": 1,
                }],
                success_url=f"{APP_BASE_URL}/success?hash={hash}",
                cancel_url=f"{APP_BASE_URL}/cancel?hash={hash}",
                automatic_tax={"enabled": False},
                payment_intent_data={
                    "application_fee_amount": app_fee_minor,
                }
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        pr.stripe_session_id = session.id
        pr.status = "pending"
        db.commit()

        return {"checkout_url": session.url}
