from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random, datetime

app = FastAPI()

def generate_signal():
    direction = random.choice(["BUY", "SELL"])
    entry = round(random.uniform(1000, 2000), 2)
    tp = entry + random.uniform(50, 100) if direction == "BUY" else entry - random.uniform(50, 100)
    sl = entry - random.uniform(30, 50) if direction == "BUY" else entry + random.uniform(30, 50)
    return {
        "pair": "V75",
        "signal": direction,
        "entry": entry,
        "tp": round(tp, 2),
        "sl": round(sl, 2),
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>V75 App</title></head>
        <body style='font-family:sans-serif;text-align:center;padding:50px'>
            <h1>📈 V75 Signal & Chart Viewer</h1>
            <p><a href='/chart' target='_blank'>View Chart</a></p>
            <p><a href='/signal' target='_blank'>Get Signal</a></p>
        </body>
    </html>
    """

@app.get("/chart", response_class=HTMLResponse)
def chart():
    return """
    <iframe src='https://s.tradingview.com/widgetembed/?frameElementId=tradingview_0d7f4&symbol=DERIV:V75USD&interval=1&theme=dark' 
            width='100%' height='500' frameborder='0' allowtransparency='true' scrolling='no'>
    </iframe>
    """

@app.get("/signal")
def signal():
    return generate_signal()
