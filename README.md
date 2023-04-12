# tradingview-webhook-mqtt
A Webhook server implementation for TradingView that forwards alerts to an MQTT broker

Set the following env variables in the `.env` file accordingly

```yaml
MQTT_HOST=emqx.local
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_TOPIC=tv_alerts
```

Build and run using docker compose

```bash
docker compose build && docker compose up
```
