import os
import stripe
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, schemas, crud

APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5173")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_123")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_123")

stripe.api_key = STRIPE_SECRET_KEY

app = FastAPI(title="PhantomPay API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    database.init_db()

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/create-request")
def create_request(payload: schemas.RequestCreate, db: Session = database.get_db()):
    return crud.create_request(db, payload)

@app.post("/api/checkout/{hash_id}")
def create_checkout(hash_id: str, db: Session = database.get_db()):
    request_obj = crud.get_request_by_hash(db, hash_id)
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")

    amount_with_fee = int(request_obj.amount * 1.01)
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "PhantomPay Request"},
                "unit_amount": amount_with_fee,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{APP_BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{APP_BASE_URL}/cancel",
        metadata={"request_hash": hash_id},
    )
    return {"url": session.url}

@app.get("/api/status/{hash_id}")
def get_status(hash_id: str, db: Session = database.get_db()):
    request_obj = crud.get_request_by_hash(db, hash_id)
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"status": request_obj.status}

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request, db: Session = database.get_db()):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        hash_id = session["metadata"]["request_hash"]
        crud.mark_request_paid(db, hash_id)
    return {"status": "success"}

@app.post("/customer-portal")
async def customer_portal(request: Request):
    data = await request.json()
    customer_id = data.get("customer_id")
    if not customer_id:
        raise HTTPException(status_code=400, detail="customer_id is required")

    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=APP_BASE_URL,
        )
        return {"url": portal_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
