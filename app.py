import os
from fastapi import FastAPI, Request
from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters
from commlib.msg import MessageHeader, PubSubMessage
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST=os.getenv("MQTT_HOST", 'localhost')
MQTT_PORT=os.getenv("MQTT_PORT", 1883)
MQTT_USERNAME=os.getenv("MQTT_USERNAME", '')
MQTT_PASSWORD=os.getenv("MQTT_PASSWORD", '')
MQTT_TOPIC=os.getenv("MQTT_TOPIC", 'tv_alerts')
SEC_KEY=os.getenv("SEC_KEY", 'DEFAULT_KEY')


class TradingViewAlert(PubSubMessage):
    header: MessageHeader = MessageHeader()
    data: Any


app = FastAPI()

node = Node(node_name='sensors.sonar.front',
            connection_params=ConnectionParameters(
                host=MQTT_HOST,
                port=MQTT_PORT,
                username=MQTT_USERNAME,
                password=MQTT_PASSWORD
            ),
            debug=False)

mqtt_pub = node.create_publisher(msg_type=TradingViewAlert,
                                 topic=MQTT_TOPIC)


@app.get("/")
async def root():
    return {"message": "TradingView-Webhook-MQTT-Bridge"}


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    headers = request.headers
    qparams = request.query_params
    pparams = request.path_params

    if 'text/plain' in headers['content-type']:
        raise ValueError('Alert Message must be of type application/json')
    elif 'application/json' in headers['content-type']:
        data = await request.json()
        if 'key' not in data:
            raise ValueError('Missing key!')
        key = data['key']
        if key == SEC_KEY:
            msg = TradingViewAlert(data=data.pop('key'))
            mqtt_pub.publish(msg)
            return 200
        else:
            return 400
