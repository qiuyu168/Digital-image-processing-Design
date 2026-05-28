# 本文件用于定义内置图片库相关 API 路由
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse


router = APIRouter(prefix="/api/library", tags=["library"])


@router.get("/categories")
async def get_library_categories() -> dict:
    """返回内置图片库分类。"""
    from app.services.image_store import list_library_categories

    return {"success": True, "categories": list_library_categories()}


@router.get("/images")
async def get_library_images(
    category: str = Query(default="anime_character", description="内置图片分类名称"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=6, ge=1, le=100, description="每页数量"),
) -> dict:
    """返回指定内置分类下的图片列表（分页）。"""
    from app.services.image_store import list_library_images

    try:
        return list_library_images(category, page=page, page_size=page_size)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/image/{image_path:path}")
async def get_library_image(image_path: str) -> FileResponse:
    """返回内置图片库中的图片文件。"""
    from app.services.image_store import get_library_image_path

    try:
        file_path = get_library_image_path(image_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return FileResponse(file_path)
