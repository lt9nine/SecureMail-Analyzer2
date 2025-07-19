from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "SecureMail Analyzer API",
        "version": settings.VERSION,
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import and include routers here
# from app.api import auth, users, mail_accounts, emails, analysis
# app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
# app.include_router(users.router, prefix="/api/users", tags=["users"])
# app.include_router(mail_accounts.router, prefix="/api/mail-accounts", tags=["mail-accounts"])
# app.include_router(emails.router, prefix="/api/emails", tags=["emails"])
# app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 