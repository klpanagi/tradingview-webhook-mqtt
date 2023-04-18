.ONESHELL:
.PHONY: run
.PHONY: docker

run:
	docker compose build && docker compose up

docker:
	docker build -t klpanagi/tradingview-mqtt-bridge${TAG} -f Dockerfile .

