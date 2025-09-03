from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from blog_app.api.endpoints.user import router as user_router
from blog_app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="A FastAPI backend application with modular architecture",
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router, prefix="/api/auth", tags=["Authentication"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Blog App Backend",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
