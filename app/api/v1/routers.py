from fastapi import APIRouter

from app.api.v1.routes import scrapy

api_router = APIRouter()

api_router.include_router(router=scrapy.router, prefix="/scrapy", tags=["scrapy"])
