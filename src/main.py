#!/usr/bin/env python3
"""
Years of Lead - Main Application Entry Point
A complex turn-based insurgency simulator with SYLVA & WREN integration
"""

import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from loguru import logger

from api.routes import api_router
from core.config import settings
from core.database import init_db, shutdown_db, get_db, get_mongodb
from models.sql_models import Base, engine

# Initialize the FastAPI app
app = FastAPI(
    title="Years of Lead API",
    description="Backend API for Years of Lead insurgency simulator",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, limit this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting Years of Lead API on {settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Initialize database connections
    success = await init_db()
    if not success:
        logger.error("Failed to initialize database connections")
        # In a production environment, you might want to exit here
        # But for development, we'll continue running
    else:
        logger.info("Database connections initialized successfully")
        
    # For minimum viable prototype, create tables if they don't exist
    # In production, this would be handled by migrations
    if settings.ENVIRONMENT == "development":
        logger.info("Creating database tables if they don't exist")
        # Create tables
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Years of Lead API")
    # Close database connections
    await shutdown_db()
    logger.info("Database connections closed")

# Health check endpoint
@app.get("/health")
async def health_check():
    db_status = "connected"
    mongo_status = "connected"
    
    try:
        # Test PostgreSQL connection
        db = next(get_db())
        db.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"
        
    try:
        # Test MongoDB connection
        mongodb = get_mongodb()
        await mongodb.command("ping")
    except Exception as e:
        mongo_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "connected" and mongo_status == "connected" else "degraded",
        "version": app.version,
        "databases": {
            "postgresql": db_status,
            "mongodb": mongo_status
        },
        "environment": settings.ENVIRONMENT
    }

# Simple root endpoint to redirect to API docs
@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/docs")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
