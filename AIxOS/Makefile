# AIxOS Makefile

# Default shell for make
SHELL := /bin/bash

# Docker-compose command
COMPOSE := docker-compose

# Default target
.DEFAULT_GOAL := help

# Project variables
PROJECT_NAME := aixos

.PHONY: help build up down logs shell test clean

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help         Show this help message"
	@echo "  build        Build the Docker images"
	@echo "  up           Start the services in detached mode"
	@echo "  down         Stop and remove the services"
	@echo "  logs         Follow the logs of the services"
	@echo "  shell        Get a shell into the running container"
	@echo "  test         Run the test suite"
	@echo "  clean        Remove all build artifacts and data"

build:
	@echo "Building Docker images..."
	@$(COMPOSE) build

up:
	@echo "Starting services..."
	@$(COMPOSE) up -d

down:
	@echo "Stopping services..."
	@$(COMPOSE) down

logs:
	@echo "Following logs..."
	@$(COMPOSE) logs -f

shell:
	@echo "Getting a shell into the container..."
	@$(COMPOSE) exec $(PROJECT_NAME) /bin/bash

test:
	@echo "Running tests..."
	@$(COMPOSE) run --rm $(PROJECT_NAME) pytest

clean:
	@echo "Cleaning up..."
	@$(COMPOSE) down -v --remove-orphans
	@sudo rm -rf data logs