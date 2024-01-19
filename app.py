import os
from fastapi import FastAPI, Request
from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters
from commlib.msg import MessageHeader, PubSubMessage
from typing import Dict, Any
from dotenv import load_dotenv
from rich import print, pretty

pretty.install()

MQTT_HOST=os.getenv("MQTT_HOST", 'localhost')
MQTT_PORT=os.getenv("MQTT_PORT", 1883)
MQTT_USERNAME=os.getenv("MQTT_USERNAME", '')
MQTT_PASSWORD=os.getenv("MQTT_PASSWORD", '')
MQTT_TOPIC=os.getenv("MQTT_TOPIC", 'tv_alerts')
SEC_KEY=os.getenv("SEC_KEY", 'DEFAULT_KEY')
DEBUG=os.getenv("DEBUG", 0)


def print_config():
    print('Starting TradingView MQTT Bridge')
    print()
    print('Configuration:')
    print()
    print(f'- MQTT Broker: {MQTT_HOST}:{MQTT_PORT}')
    print(f'- Default MQTT Topic: {MQTT_TOPIC}')
    print(f'- Security Key: {SEC_KEY}')


class TradingViewAlert(PubSubMessage):
    header: MessageHeader = MessageHeader()
    data: Dict[str, Any]


app = FastAPI()

node = Node(node_name='tradingview.mqtt_bridge',
            connection_params=ConnectionParameters(
                host=MQTT_HOST,
                port=MQTT_PORT,
                username=MQTT_USERNAME,
                password=MQTT_PASSWORD
            ),
            debug=DEBUG)

mqtt_pub = node.create_mpublisher()

node.run()


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
        print(f'Received TV Event: {data}')
        if 'key' not in data:
            raise ValueError('Missing key!')
        key = data['key']
        if key == SEC_KEY:
            if 'data' not in data:
                raise ValueError(
                    'Wring Alert message format, "data" field not found!')
                return 400
            msg = TradingViewAlert(data=data['data'])
            if 'topic' in data:
                topic = data['topic']
                if topic == '':
                    topic = MQTT_TOPIC
            else:
                topic = MQTT_TOPIC
            print(f'Publishing TradingView Alert @ {topic}')
            mqtt_pub.publish(msg, topic)
            return 200
        else:
            return 400
