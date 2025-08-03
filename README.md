# Daydream2

A full-stack application with a React frontend and FastAPI backend.

## Tech Stack

### Frontend (Client)

- **Vite** - Fast build tool and dev server
- **React 19** - UI library with TypeScript
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Modern component library

### Backend (API)

- **FastAPI** - Modern Python web framework
- **Poetry** - Python dependency management
- **PostgreSQL** - Database
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Alembic** - Database migration tool

## Project Structure

```
daydream2/
├── client/                 # Frontend React application
│   ├── src/
│   │   ├── components/     # React components
│   │   │   └── ui/         # shadcn/ui components
│   │   ├── lib/           # Utility functions
│   │   ├── App.tsx        # Main App component
│   │   ├── main.tsx       # App entry point
│   │   └── index.css      # Tailwind CSS imports
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── backend/               # Backend FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py        # FastAPI application
│   │   └── database.py    # Database configuration
│   ├── pyproject.toml     # Poetry configuration
│   ├── run.py            # Development server script
│   └── Dockerfile
├── docker-compose.yml     # Multi-service orchestration
└── README.md
```

## Getting Started

### Prerequisites

- **Docker & Docker Compose** (recommended for full setup)
- **Node.js 18+** (for local frontend development)
- **Python 3.11+** (for local backend development)
- **Poetry** (for Python dependency management)

### Option 1: Docker Compose (Recommended)

Start all services (database, backend, frontend):

```bash
docker-compose up --build
```

This will start:

- **PostgreSQL** on `localhost:5435`
- **Backend API** on `http://localhost:8000`
- **Frontend** on `http://localhost:3000`

### Option 2: Local Development

#### Backend Setup

1. Navigate to backend directory:

   ```bash
   cd backend
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Start PostgreSQL (using Docker):

   ```bash
   docker run -d -p 5435:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=daydream2_db postgres:15
   ```

4. Run the backend:
   ```bash
   poetry run python run.py
   ```

The API will be available at `http://localhost:8000`

#### Frontend Setup

1. Navigate to client directory:

   ```bash
   cd client
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Health Check

- `GET /` - Root endpoint
- `GET /health` - Health check

### Items CRUD

- `GET /items` - Get all items
- `POST /items` - Create new item
- `GET /items/{id}` - Get item by ID
- `DELETE /items/{id}` - Delete item by ID

### Interactive API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Development

### Frontend Development

The frontend uses:

- **Hot Module Replacement (HMR)** for instant updates
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **shadcn/ui** components for consistent UI

Key files:

- `src/App.tsx` - Main application component
- `src/components/ui/` - Reusable UI components
- `src/lib/utils.ts` - Utility functions
- `tailwind.config.js` - Tailwind configuration

### Backend Development

The backend uses:

- **FastAPI** for automatic API documentation
- **Poetry** for dependency management
- **SQLAlchemy** for database operations
- **Alembic** for database migrations

Key files:

- `app/main.py` - FastAPI application
- `app/database.py` - Database configuration
- `pyproject.toml` - Project dependencies

### Database

PostgreSQL database with:

- **User**: `postgres`
- **Password**: `postgres`
- **Database**: `daydream2_db`
- **Port**: `5435`

## Environment Variables

### Backend

- `DATABASE_URL` - PostgreSQL connection string
- `CORS_ORIGINS` - Allowed CORS origins

### Frontend

- `VITE_API_URL` - Backend API URL

## Available Scripts

### Makefile Commands

```bash
make help                         # Show all available commands
make install-all                  # Install all dependencies
make start-frontend               # Start frontend development server
make start-backend                # Start backend development server
make start-db                     # Start PostgreSQL database
make start-all                    # Start all services with Docker Compose
make build-frontend               # Build frontend for production
make test-backend                 # Run backend tests
make format-backend               # Format backend code
make lint-frontend                # Lint frontend code
make clean                        # Clean build artifacts
```

### VS Code Integration

This project includes VS Code configuration for enhanced development:

- **Tasks** (`Ctrl+Shift+P` → `Tasks: Run Task`):

  - Start Frontend / Backend / Database
  - Install Dependencies
  - Build and Test commands
  - Full Docker Compose setup

- **Debug Configuration**:

  - Debug Backend (FastAPI) with breakpoints
  - Attach to running backend process

- **Recommended Extensions**:
  - Python, ESLint, Prettier, Tailwind CSS
  - Docker, GitLens, REST Client
  - Auto-install prompt on first open

### Manual Commands

#### Backend

```bash
cd backend
poetry run python run.py          # Start development server
poetry run black .                # Format code
poetry run isort .                # Sort imports
poetry run flake8                 # Lint code
poetry run pytest                 # Run tests
```

#### Frontend

```bash
cd client
npm run dev                       # Start development server
npm run build                     # Build for production
npm run preview                   # Preview production build
npm run lint                      # Lint code
```

## Docker Services

### Full Stack

```bash
docker-compose up --build         # Start all services
docker-compose down               # Stop all services
docker-compose logs -f [service]  # View service logs
```

### Individual Services

```bash
docker-compose up db              # Database only
docker-compose up backend         # Backend only
docker-compose up client          # Frontend only
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).
