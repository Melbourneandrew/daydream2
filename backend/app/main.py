from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.health_controller import router as health_router

# Create FastAPI instance
app = FastAPI(
    title="Daydream2 API",
    description="Backend API for Daydream2 application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
