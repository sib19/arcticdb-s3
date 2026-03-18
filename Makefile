.PHONY: help setup build start stop logs clean test lint format

help:
	@echo "Arctic DB Project - Available Commands"
	@echo "======================================"
	@echo "Setup and Installation:"
	@echo "  make setup          - Initialize project and git repository"
	@echo "  make install        - Install Python dependencies"
	@echo "  make build          - Build Docker image"
	@echo ""
	@echo "Running:"
	@echo "  make start          - Start Docker containers"
	@echo "  make stop           - Stop Docker containers"
	@echo "  make logs           - View container logs"
	@echo "  make shell          - Open shell in running container"
	@echo ""
	@echo "Development:"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run linting checks"
	@echo "  make format         - Format code"
	@echo "  make examples       - Run example scripts"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Remove containers and volumes"
	@echo "  make reset          - Full reset (removes everything)"
	@echo ""

setup:
	@bash setup.sh
	@cp .env.example .env
	@echo "✅ Setup complete. Edit .env with your AWS credentials."

install:
	pip install -r requirements.txt

build:
	docker-compose build

start:
	docker-compose up -d
	@echo "✅ Started. API available at http://localhost:8080"

stop:
	docker-compose down

logs:
	docker-compose logs -f arctic-db

shell:
	docker-compose exec arctic-db /bin/bash

test:
	python -m pytest tests/ -v

lint:
	python -m flake8 app.py arctic_client.py examples.py

format:
	python -m black app.py arctic_client.py examples.py

examples:
	python examples.py

health:
	curl http://localhost:8080/health
	@echo ""

info:
	curl http://localhost:8080/api/v1/info
	@echo ""

clean:
	docker-compose down
	rm -rf __pycache__ .pytest_cache .coverage

reset: clean
	docker-compose down -v
	rm -rf data logs *.pyc
	@echo "✅ Project reset."

version:
	@echo "Arctic DB Project v1.0.0"

status:
	@docker-compose ps
