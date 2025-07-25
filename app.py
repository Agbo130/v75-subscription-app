from fastapi import FastAPI
from routers import payment

app = FastAPI()

app.include_router(payment.router)

@app.get("/")
def root():
    return {"message": "Welcome to the V75 Subscription App"}

