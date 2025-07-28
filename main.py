from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio
import websockets
import json
import datetime

app = FastAPI()

# Async function to fetch V75 live price
async def fetch_v75_price():
    uri = "wss://ws.deriv.com/websockets/v3"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"ticks": "R_75"}))
        response = await websocket.recv()
        data = json.loads(response)
        return round(float(data["tick"]["quote"]), 2)

# Build signal using fetched price
async def generate_signal():
    price = await fetch_v75_price()
    direction = "BUY"  # Optional: logic can be added
    tp = round(price + 100, 2)
    sl = round(price - 50, 2)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return direction, price, tp, sl, timestamp

@app.get("/", response_class=HTMLResponse)
async def home():
    try:
        direction, entry, tp, sl, timestamp = await generate_signal()
    except Exception as e:
        return f"<h1>❌ Failed to fetch signal: {e}</h1>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live V75 Signal</title>
        <meta http-equiv='refresh' content='60'>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f9f9f9;
                padding: 30px;
            }}
            .signal-box {{
                background: #ffffff;
                border: 1px solid #ddd;
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
                margin-top: 20px;
                box-shadow: 0 0 10px rgba(0,0,0,0.05);
            }}
        </style>
    </head>
    <body>
        <h1>📈 <b>V75 Live Signal</b></h1>

        <div class="signal-box">
            <h2>📡 Signal Details</h2>
            <p><b>Direction:</b> {direction}</p>
            <p><b>Entry (Live Price):</b> {entry}</p>
            <p><b>Take Profit:</b> {tp}</p>
            <p><b>Stop Loss:</b> {sl}</p>
            <p><b>Time:</b> {timestamp}</p>
        </div>
    </body>
    </html>
    """
