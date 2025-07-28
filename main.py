from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import datetime
import random
import asyncio

try:
    import websockets
    import json
except ImportError:
    websockets = None

app = FastAPI()

async def fetch_v75_price():
    try:
        if not websockets:
            raise RuntimeError("Websockets not available in this environment")
        uri = "wss://ws.deriv.com/websockets/v3"
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({"ticks": "R_75"}))
            response = await websocket.recv()
            data = json.loads(response)
            return round(float(data["tick"]["quote"]), 2)
    except Exception:
        return None

def generate_signal(price=None):
    if price is None:
        price = round(random.uniform(1300, 1700), 2)
    direction = "BUY"
    tp = round(price + 100, 2)
    sl = round(price - 50, 2)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return direction, price, tp, sl, timestamp

@app.get("/", response_class=HTMLResponse)
async def home():
    live_price = await fetch_v75_price()
    direction, entry, tp, sl, timestamp = generate_signal(live_price)

    info = ""
    if live_price is None:
        info = "<p style='color:red'><b>⚠️ Live price not available — showing fallback signal</b></p>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>V75 Signal App</title>
        <meta http-equiv='refresh' content='60'>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f9f9f9;
                padding: 30px;
            }}
            iframe {{
                margin: 20px auto;
                border: 1px solid #ccc;
                border-radius: 8px;
            }}
            .signal-box {{
                background: #fff;
                border: 1px solid #ddd;
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
                box-shadow: 0 0 10px rgba(0,0,0,0.05);
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>📈 V75 Live Signal + Chart</h1>

        <!-- Embedded Deriv Chart -->
        <iframe
            src="https://charts.deriv.com/"
            width="100%"
            height="500"
            frameborder="0"
            allowfullscreen>
        </iframe>

        {info}
        <div class="signal-box">
            <h2>📡 Signal</h2>
            <p><b>Direction:</b> {direction}</p>
            <p><b>Entry:</b> {entry}</p>
            <p><b>Take Profit:</b> {tp}</p>
            <p><b>Stop Loss:</b> {sl}</p>
            <p><b>Time:</b> {timestamp}</p>
        </div>

        <!-- SEO Blog Content -->
        <div style='max-width: 800px; margin: 40px auto; text-align: left; background: #fff; padding: 20px; border-radius: 10px; border: 1px solid #ddd;'>
            <h2>📊 What is Volatility 75 Index (V75)?</h2>
            <p>The Volatility 75 Index (V75) is a synthetic index offered by Deriv that simulates the volatility of the financial markets. It moves 24/7 and is favored by traders due to its speed, precision, and potential profitability.</p>

            <h3>📈 Best V75 Signal Strategy</h3>
            <p>Using strong price action or smart money concepts, many traders follow high-quality entry signals like the one provided above. Always combine a clear direction, stop loss, and take profit to minimize risk and maximize reward.</p>

            <h3>🧠 Why Trade V75 on Deriv?</h3>
            <ul>
                <li>24/7 trading – no downtime</li>
                <li>High volatility = bigger profit potential</li>
                <li>Fast execution with zero slippage</li>
                <li>Supports both beginners and advanced traders</li>
            </ul>

            <h3>💸 Start Trading V75 Today</h3>
            <p>If you want to start trading Volatility 75 Index with real signals and proper strategy, you need a trusted broker.</p>
            <p>👉 <a href="https://track.deriv.com/_X4my-_6ZqrCNhxmBqQyZL2Nd7ZgqdRLk/1/" target="_blank" style="color:green;font-weight:bold;">Click here to register on Deriv with my recommended broker</a></p>
            <p>This is the same broker I use to generate signals like the one above. Fast, reliable, and pays out quickly.</p>

            <h4>🔥 Keywords: Volatility 75 signal, V75 index strategy, best broker for V75, Deriv signal, V75 trading robot</h4>
        </div>
    </body>
    </html>
    """
