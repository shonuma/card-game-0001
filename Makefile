.PHONY: build up down shell-redis

build:
	docker build -t card-game-server .
	docker-compose build

up:
	docker-compose up

shell-redis:
	docker-compose exec redis /bin/bash
