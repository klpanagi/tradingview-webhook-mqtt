# tradingview-webhook-mqtt
A Webhook server implementation for TradingView that forwards alerts to an MQTT broker

Implemented using [FastAPI](https://github.com/tiangolo/fastapi) and [commlib-py](https://github.com/robotics-4-all/commlib-py).

## Usage

Set the following env variables in the `.env` file accordingly.

```yaml
MQTT_HOST=emqx.local
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_TOPIC=tradingview/alerts
SEC_KEY=123123
```

- MQTT_HOST: The hostname of a running message broker that supports the MQTT protocol (EMQX, Mosquitto, RabbitMQ etc)
- MQTT_PORT: The listening port of a running message broker that supports the MQTT protocol (EMQX, Mosquitto, RabbitMQ etc)
- MQTT_USERNAME: Username for connecting to the MQTT Broker
- MQTT_PASSWORD: Password for connecting to the MQTT Broker
- MQTT_TOPIC: The MQTT topic to forward inbound TradingView Alerts
- SEC_KEY: The security key to use for authorization. This key must be contained
in the alert messages (Explained below).


Build and run using docker compose

```bash
docker compose build && docker compose up
```

The example `docker-compose.yml` file includes an EMQX broker for testing.

The current implementation requires TV Alert messages to be defined in `application/json` and must follow the following model.

```json
{
    'key': '<SECURITY_KEY>',
    'data': {},
    'type': '<OPTIONAL_ALERT_TYPE>'
}
```

The `key` property of alert messages is mandatory in order to allow access to
the webhook server, as it implements a lightweight authorization layer. The
value of the `key` is defined on the server side via the `SEC_KEY` environmental
variable as earlier mentioned.


## Use in other deployments

Build the image using the following command:

```
docker build -t <MY_IMAGE_NAME> .
```
