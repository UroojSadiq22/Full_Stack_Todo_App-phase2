"""Main entry point for the Todo application API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth_router import router as auth_router
from .api.todo_router import router as todo_router
from .config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Todo API",
        description="A secure, multi-user todo application API",
        version="1.0.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(todo_router, prefix="/api/todos", tags=["todos"])

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Todo API"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)