from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "TradingView-Webhook-MQTT-Bridge"}


@app.post("/webhook")
async def webhook(alert):
    print(alert)
