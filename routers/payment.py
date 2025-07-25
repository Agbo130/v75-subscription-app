import os
from fastapi import APIRouter
import stripe
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/pay/stripe")
def create_stripe_session():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "V75 Subscription"},
                "unit_amount": 1000 * 100
            },
            "quantity": 1
        }],
        mode="payment",
        success_url="https://yourdomain.com/success",
        cancel_url="https://yourdomain.com/cancel"
    )
    return {"checkout_url": session.url}

