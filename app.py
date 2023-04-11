import os
from fastapi import FastAPI
from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters
from commlib.msg import MessageHeader, PubSubMessage
from typing import Dict, Any


MQTT_HOST=os.getenv("MQTT_HOST", 'localhost')
MQTT_PORT=os.getenv("MQTT_PORT", 1883)
MQTT_USERNAME=os.getenv("MQTT_USERNAME", '')
MQTT_PASSWORD=os.getenv("MQTT_PASSWORD", '')
MQTT_TOPIC=os.getenv("MQTT_TOPIC", 'tv_alerts')


class TradingViewSignal(PubSubMessage):
    header: MessageHeader = MessageHeader()
    data: Dict[str, Any]


app = FastAPI()

print(MQTT_HOST, MQTT_PORT)

node = Node(node_name='sensors.sonar.front',
            connection_params=ConnectionParameters(
                host=MQTT_HOST,
                port=MQTT_PORT,
                username=MQTT_USERNAME,
                password=MQTT_PASSWORD
            ),
            debug=False)

mqtt_pub = node.create_publisher(msg_type=TradingViewSignal,
                                 topic=MQTT_TOPIC)


@app.get("/")
async def root():
    return {"message": "TradingView-Webhook-MQTT-Bridge"}


@app.post("/webhook")
async def webhook(alert: Dict[Any, Any]):
    print(alert)
    msg = TradingViewSignal(data=alert)
    mqtt_pub.publish(msg)
