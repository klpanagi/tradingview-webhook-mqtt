# tradingview-webhook-mqtt
A lightweight webhook server implementation that forwards TradingView Alerts to an MQTT broker.

This was initially developed as an integration module for hummingbot and enables implementing a trading logic/strategy based on input TradingView Alerts.

All incoming Alerts are forwarded to a single MQTT topic, from where hummingbot bots can subscribe (using the MQTT module) and implement custom strategies and perform trades using the internal DSL of hummingbot.

Furthermore, a lightweight API-key based authorization scheme is adopted. Alerts
must include the API key (see Usage section) in the body of the message in order
to pass the authorization layer.

Implemented using [FastAPI](https://github.com/tiangolo/fastapi) and [commlib-py](https://github.com/robotics-4-all/commlib-py).

## Usage

Set the following environment variables in the `docker-compose.yml` file accordingly.

```bash
environment:
  - MQTT_HOST=emqx.local
  - MQTT_PORT=1883
  - MQTT_USERNAME=
  - MQTT_PASSWORD=
  - MQTT_TOPIC=tradingview/alerts
  - SEC_KEY=123123
```

- `MQTT_HOST`: The hostname of a running message broker that supports the MQTT protocol (EMQX, Mosquitto, RabbitMQ etc)
- `MQTT_PORT`: The listening port of a running message broker that supports the MQTT protocol (EMQX, Mosquitto, RabbitMQ etc)
- `MQTT_USERNAME`: Username for connecting to the MQTT Broker
- `MQTT_PASSWORD`: Password for connecting to the MQTT Broker
- `MQTT_TOPIC`: The MQTT topic to forward inbound TradingView Alerts
- `SEC_KEY`: The security key to use for authorization. This key must be contained
in the alert messages (Explained below).


Build and run using docker compose

```bash
docker compose build && docker compose up
```

The example `docker-compose.yml` file includes an EMQX broker for testing.

The current implementation requires TV Alert messages to be defined in `application/json` and must conform to the following model.

```json
{
    "key": "SECURITY_KEY",
    "data": {},
    "topic": "OPTIONAL_MQTT_TOPIC"
}
```

The `key` property of alert messages is mandatory in order to allow access to
the webhook server, as it implements a lightweight authorization layer. The
value of the `key` is defined on the server side via the `SEC_KEY` environmental
variable as earlier mentioned.

The `data` property can include custom schemes/models, though it must be of type
dictionary.

Finally, the `topic` property is **optional** and can be used to force
publishing to a specific topic, instead of the default one defined by the
`MQTT_TOPIC` variable on the server-side.

## Use in other deployments

Build the image using the following command:

```
docker build -t <MY_IMAGE_NAME> .
```
