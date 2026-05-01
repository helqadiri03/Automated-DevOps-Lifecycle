# DevOps Tooling Makefile

.PHONY: up down restart logs ps clean help

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up        Start all services in detached mode"
	@echo "  down      Stop and remove all containers"
	@echo "  restart   Restart all services"
	@echo "  logs      Follow logs from all containers"
	@echo "  ps        List running containers"
	@echo "  clean     Remove all containers, networks, and volumes"

up:
	docker-compose up -d --build

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

ps:
	docker-compose ps

clean:
	docker-compose down -v --rmi all --remove-orphans
