.ONESHELL:
.PHONY: run
.PHONY: docker

run:
	docker compose build && docker compose up

docker:
	docker build -t klpanagi/tv-wh-mqtt-bridge${TAG} -f Dockerfile .

