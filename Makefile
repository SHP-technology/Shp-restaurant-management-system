# ==============================================================================
# SHP Restaurant Management System — Unified Makefile
# ==============================================================================
# Usage:
#   make help          Show all available commands
#   make setup         Complete setup: installs dependencies, migrates & seeds DB
#   make dev           Runs both Frontend & Backend concurrently
#   make redis         Start Redis server (Docker or native)
# ==============================================================================

SHELL := /bin/bash
PYTHON := backend/venv/bin/python
PIP := backend/venv/bin/pip
DAPHNE := backend/venv/bin/daphne
MANAGE := $(PYTHON) backend/manage.py
NPM := npm
REDIS_CONTAINER := restro-redis

.PHONY: help setup install install-frontend install-backend dev dev-frontend dev-backend dev-asgi redis redis-stop redis-status redis-cli build build-frontend collectstatic preview makemigrations migrate seed superuser shell reset-db test test-frontend test-backend lint clean

# Default target
.DEFAULT_GOAL := help

# Colors
COLOR_RESET   := \033[0m
COLOR_CYAN    := \033[36m
COLOR_GREEN   := \033[32m
COLOR_YELLOW  := \033[33m
COLOR_MAGENTA := \033[35m

## ----------------------------------------------------------------------
## ℹ️  HELP
## ----------------------------------------------------------------------
help:
	@echo -e "$(COLOR_MAGENTA)==================================================================$(COLOR_RESET)"
	@echo -e "$(COLOR_CYAN)    SHP Restaurant Management System — Command Center$(COLOR_RESET)"
	@echo -e "$(COLOR_MAGENTA)==================================================================$(COLOR_RESET)"
	@echo -e "$(COLOR_YELLOW)Usage:$(COLOR_RESET) make $(COLOR_GREEN)<target>$(COLOR_RESET)\n"
	@echo -e "$(COLOR_YELLOW)🚀 Quick Start & Setup:$(COLOR_RESET)"
	@echo -e "  $(COLOR_GREEN)make setup$(COLOR_RESET)             Full setup (install dependencies, migrate & seed database)"
	@echo -e "  $(COLOR_GREEN)make install$(COLOR_RESET)           Install both frontend (npm) and backend (pip) packages"
	@echo -e "  $(COLOR_GREEN)make dev$(COLOR_RESET)               Start both Frontend and Backend dev servers concurrently\n"
	@echo -e "$(COLOR_YELLOW)💻 Development Servers:$(COLOR_RESET)"
	@echo -e "  $(COLOR_GREEN)make dev-frontend$(COLOR_RESET)      Start Vite dev server (http://localhost:5173)"
	@echo -e "  $(COLOR_GREEN)make dev-backend$(COLOR_RESET)       Start Django HTTP dev server (http://localhost:8000)"
	@echo -e "  $(COLOR_GREEN)make dev-asgi$(COLOR_RESET)          Start Daphne ASGI server (WebSockets enabled on :8000)\n"
	@echo -e "$(COLOR_YELLOW)⚡ Redis & WebSockets Layer:$(COLOR_RESET)"
	@echo -e "  $(COLOR_GREEN)make redis$(COLOR_RESET)             Start Redis service (via Docker or local daemon)"
	@echo -e "  $(COLOR_GREEN)make redis-stop$(COLOR_RESET)        Stop Redis service"
	@echo -e "  $(COLOR_GREEN)make redis-status$(COLOR_RESET)      Check Redis connection status"
	@echo -e "  $(COLOR_GREEN)make redis-cli$(COLOR_RESET)         Open Redis CLI interactive console\n"
	@echo -e "$(COLOR_YELLOW)📦 Build & Production:$(COLOR_RESET)"
	@echo -e "  $(COLOR_GREEN)make build$(COLOR_RESET)             Build frontend production bundle"
	@echo -e "  $(COLOR_GREEN)make preview$(COLOR_RESET)           Preview production frontend build"
	@echo -e "  $(COLOR_GREEN)make collectstatic$(COLOR_RESET)     Collect Django backend static files\n"
	@echo -e "$(COLOR_YELLOW)🗄️ Database & Migrations:$(COLOR_RESET)"
	@echo -e "  $(COLOR_GREEN)make migrate$(COLOR_RESET)           Apply all pending database migrations"
	@echo -e "  $(COLOR_GREEN)make makemigrations$(COLOR_RESET)    Generate new database migrations"
	@echo -e "  $(COLOR_GREEN)make seed$(COLOR_RESET)              Seed demo restaurant, menu items, tables & admin user"
	@echo -e "  $(COLOR_GREEN)make reset-db$(COLOR_RESET)          Wipe database, re-run migrations and re-seed"
	@echo -e "  $(COLOR_GREEN)make superuser$(COLOR_RESET)         Create a new Django superuser interactively"
	@echo -e "  $(COLOR_GREEN)make shell$(COLOR_RESET)             Open Django Python interactive shell\n"
	@echo -e "$(COLOR_YELLOW)🧪 Testing & Code Quality:$(COLOR_RESET)"
	@echo -e "  $(COLOR_GREEN)make test$(COLOR_RESET)              Run all tests (frontend + backend)"
	@echo -e "  $(COLOR_GREEN)make test-frontend$(COLOR_RESET)     Run Vitest frontend unit tests"
	@echo -e "  $(COLOR_GREEN)make test-backend$(COLOR_RESET)      Run Django backend automated tests"
	@echo -e "  $(COLOR_GREEN)make lint$(COLOR_RESET)              Run Oxlint on frontend code"
	@echo -e "  $(COLOR_GREEN)make clean$(COLOR_RESET)             Remove build artifacts, cache, and temp files"
	@echo -e "$(COLOR_MAGENTA)==================================================================$(COLOR_RESET)"

## ----------------------------------------------------------------------
## 🚀 SETUP & INSTALLATION
## ----------------------------------------------------------------------
setup: install migrate seed
	@echo -e "\n$(COLOR_GREEN)✓ Setup complete! Run 'make dev' to start development servers.$(COLOR_RESET)"

install: install-frontend install-backend

install-frontend:
	@echo -e "$(COLOR_CYAN)Installing frontend dependencies...$(COLOR_RESET)"
	$(NPM) install

install-backend:
	@echo -e "$(COLOR_CYAN)Setting up backend virtual environment & dependencies...$(COLOR_RESET)"
	@if [ ! -d "backend/venv" ]; then python3 -m venv backend/venv; fi
	$(PIP) install --upgrade pip
	$(PIP) install -r backend/requirements.txt

## ----------------------------------------------------------------------
## 💻 DEVELOPMENT
## ----------------------------------------------------------------------
dev:
	@echo -e "$(COLOR_GREEN)Starting both Django Backend (:8000) and Vite Frontend (:5173)...$(COLOR_RESET)"
	@trap 'kill 0' EXIT; \
	$(MANAGE) runserver 8000 & \
	$(NPM) run dev

dev-frontend:
	$(NPM) run dev

dev-backend:
	$(MANAGE) runserver 8000

dev-asgi:
	PYTHONPATH=backend $(DAPHNE) -b 0.0.0.0 -p 8000 config.asgi:application

## ----------------------------------------------------------------------
## ⚡ REDIS MANAGEMENT
## ----------------------------------------------------------------------
redis:
	@echo -e "$(COLOR_CYAN)Starting Redis server...$(COLOR_RESET)"
	@if command -v redis-server >/dev/null 2>&1; then \
		echo -e "$(COLOR_GREEN)Starting local redis-server...$(COLOR_RESET)"; \
		redis-server --daemonize yes; \
	elif command -v docker >/dev/null 2>&1; then \
		if docker ps -a --format '{{.Names}}' | grep -q "^$(REDIS_CONTAINER)$$"; then \
			echo -e "$(COLOR_GREEN)Starting existing Docker Redis container ($(REDIS_CONTAINER))...$(COLOR_RESET)"; \
			docker start $(REDIS_CONTAINER); \
		else \
			echo -e "$(COLOR_GREEN)Creating & launching Docker Redis container on port 6379...$(COLOR_RESET)"; \
			docker run -d --name $(REDIS_CONTAINER) -p 6379:6379 redis:alpine; \
		fi; \
	else \
		echo -e "$(COLOR_YELLOW)Neither redis-server nor Docker is available. Please install Redis or Docker.$(COLOR_RESET)"; \
		exit 1; \
	fi
	@echo -e "$(COLOR_GREEN)✓ Redis is ready on localhost:6379$(COLOR_RESET)"

redis-stop:
	@echo -e "$(COLOR_YELLOW)Stopping Redis server...$(COLOR_RESET)"
	@if command -v docker >/dev/null 2>&1 && docker ps --format '{{.Names}}' | grep -q "^$(REDIS_CONTAINER)$$"; then \
		docker stop $(REDIS_CONTAINER); \
		echo -e "$(COLOR_GREEN)✓ Docker Redis container stopped.$(COLOR_RESET)"; \
	elif command -v redis-cli >/dev/null 2>&1; then \
		redis-cli shutdown 2>/dev/null || true; \
		echo -e "$(COLOR_GREEN)✓ Local redis-server stopped.$(COLOR_RESET)"; \
	else \
		echo -e "$(COLOR_YELLOW)No active Redis instance found to stop.$(COLOR_RESET)"; \
	fi

redis-status:
	@echo -e "$(COLOR_CYAN)Checking Redis connectivity...$(COLOR_RESET)"
	@if command -v redis-cli >/dev/null 2>&1; then \
		redis-cli ping || echo -e "$(COLOR_YELLOW)Redis is not responding on 6379.$(COLOR_RESET)"; \
	elif command -v docker >/dev/null 2>&1 && docker ps --format '{{.Names}}' | grep -q "^$(REDIS_CONTAINER)$$"; then \
		docker exec $(REDIS_CONTAINER) redis-cli ping; \
	else \
		echo -e "$(COLOR_YELLOW)Redis is not running.$(COLOR_RESET)"; \
	fi

redis-cli:
	@if command -v redis-cli >/dev/null 2>&1; then \
		redis-cli; \
	elif command -v docker >/dev/null 2>&1 && docker ps --format '{{.Names}}' | grep -q "^$(REDIS_CONTAINER)$$"; then \
		docker exec -it $(REDIS_CONTAINER) redis-cli; \
	else \
		echo -e "$(COLOR_YELLOW)Redis CLI not found. Start Redis with 'make redis' first.$(COLOR_RESET)"; \
	fi

## ----------------------------------------------------------------------
## 📦 BUILD
## ----------------------------------------------------------------------
build: build-frontend

build-frontend:
	@echo -e "$(COLOR_CYAN)Building frontend production bundle with code-splitting...$(COLOR_RESET)"
	$(NPM) run build

preview:
	$(NPM) run preview

collectstatic:
	$(MANAGE) collectstatic --noinput

## ----------------------------------------------------------------------
## 🗄️ DATABASE
## ----------------------------------------------------------------------
makemigrations:
	$(MANAGE) makemigrations

migrate:
	@echo -e "$(COLOR_CYAN)Applying database migrations...$(COLOR_RESET)"
	$(MANAGE) migrate

seed:
	@echo -e "$(COLOR_CYAN)Seeding initial restaurant data...$(COLOR_RESET)"
	$(MANAGE) seed_restaurant_data

reset-db:
	@echo -e "$(COLOR_YELLOW)Resetting SQLite database...$(COLOR_RESET)"
	rm -f backend/db.sqlite3
	$(MANAGE) migrate
	$(MANAGE) seed_restaurant_data
	@echo -e "$(COLOR_GREEN)✓ Database reset and seeded successfully!$(COLOR_RESET)"

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

## ----------------------------------------------------------------------
## 🧪 TESTING & LINTING
## ----------------------------------------------------------------------
test: test-frontend test-backend
	@echo -e "\n$(COLOR_GREEN)✓ All frontend and backend tests passed!$(COLOR_RESET)"

test-frontend:
	@echo -e "$(COLOR_CYAN)Running Vitest frontend tests...$(COLOR_RESET)"
	$(NPM) test

test-backend:
	@echo -e "$(COLOR_CYAN)Running Django backend tests...$(COLOR_RESET)"
	$(MANAGE) test apps.restaurants

lint:
	$(NPM) run lint

## ----------------------------------------------------------------------
## 🧹 CLEAN
## ----------------------------------------------------------------------
clean:
	@echo -e "$(COLOR_YELLOW)Cleaning build artifacts and cache...$(COLOR_RESET)"
	rm -rf dist dist-ssr .pytest_cache .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo -e "$(COLOR_GREEN)✓ Clean complete!$(COLOR_RESET)"
