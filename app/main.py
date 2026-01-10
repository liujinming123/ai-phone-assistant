from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import routes as api_router
from app.api import websocket as ws_router
from app.services.logger_service import logger_service
from loguru import logger

app = FastAPI(
    title="AI Phone Assistant",
    version="1.0.0",
    description="AI电话助理服务"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router.router, prefix="/api")
app.include_router(ws_router.router, prefix="/ws")

@app.on_event("startup")
async def startup():
    logger.info("AI电话助理服务启动")
    logger.info(f"服务地址: http://{settings.host}:{settings.port}")

@app.on_event("shutdown")
async def shutdown():
    logger.info("AI电话助理服务关闭")

@app.get("/")
async def root():
    return {
        "message": "AI Phone Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "ai-phone-assistant"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )
