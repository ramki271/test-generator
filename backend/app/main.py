from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.config import get_settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Test Case Generator Service",
    description="Microservice for generating test cases from JIRA acceptance criteria using Claude Agent SDK",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["test-cases"])


@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    logger.info(f"Starting Test Case Generator Service on port {settings.service_port}")
    logger.info(f"Log level: {settings.log_level}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Test Case Generator Service")


@app.get("/")
async def root():
    return {
        "service": "Test Case Generator",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/v1/health",
            "generate_test_cases": "/api/v1/generate-test-cases",
            "get_jira_issue": "/api/v1/jira/issue/{issue_key}",
            "docs": "/docs",
        }
    }


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.service_port,
        reload=True,
        log_level=settings.log_level.lower()
    )
