from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.routers import api_router
from app.core.settings import settings

app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.api_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_router, prefix=settings.app_v1_prefix)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="app.main:app", host="0.0.0.0", port=settings.port, log_level="info", reload=settings.debug, workers=3)
