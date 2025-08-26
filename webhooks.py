import os, json
from fastapi import APIRouter, Request, HTTPException
import stripe
from app.db.session import SessionLocal
from app.models.payment_request import PaymentRequest

router = APIRouter(prefix="/webhook", tags=["webhooks"])

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=sig, secret=STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    etype = event.get("type")
    data = event.get("data", {}).get("object", {})
    session_id = None
    if etype == "checkout.session.completed":
        session_id = data.get("id")
    elif etype == "payment_intent.succeeded":
        session_id = data.get("checkout_session_id")

    if session_id:
        with SessionLocal() as db:
            pr = db.query(PaymentRequest).filter_by(stripe_session_id=session_id).first()
            if pr:
                pr.status = "paid"
                db.commit()

    return {"received": True}
