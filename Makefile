# Daydream2 Makefile
# Simple commands for frontend and backend development

.PHONY: help install-all install-frontend install-backend start-frontend start-backend kill-backend kill-frontend kill-all

# Default target
help:
	@echo "Available commands:"
	@echo "  install-all      - Install all dependencies (frontend + backend)"
	@echo "  install-frontend - Install frontend dependencies"
	@echo "  install-backend  - Install backend dependencies"
	@echo "  start-frontend   - Start frontend development server"
	@echo "  start-backend    - Start backend development server"
	@echo "  kill-backend     - Kill backend processes"
	@echo "  kill-frontend    - Kill frontend processes"
	@echo "  kill-all         - Kill all development processes"

# Installation commands
install-all: install-frontend install-backend

install-frontend:
	@echo "Installing frontend dependencies..."
	cd client && npm install

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && poetry install

# Development server commands
start-frontend:
	@echo "Starting frontend development server..."
	cd client && exec npm run dev

start-backend:
	@echo "Starting backend development server..."
	cd backend && exec poetry run python run.py

# Cleanup commands
kill-backend:
	@echo "Killing backend processes..."
	@pkill -f "python run.py" || true
	@pkill -f "uvicorn" || true

kill-frontend:
	@echo "Killing frontend processes..."
	@pkill -f "npm run dev" || true
	@pkill -f "vite" || true

kill-all: kill-backend kill-frontend