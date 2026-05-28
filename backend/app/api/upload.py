# 本文件用于定义图片上传和上传图片预览相关 API 路由
from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse


router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("/image")
async def upload_image(file: UploadFile = File(...)) -> dict:
    """接收上传图片，校验后保存到 data/uploads。"""
    from app.services.image_store import save_upload_image

    try:
        return await save_upload_image(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/preview/{image_path:path}")
async def preview_uploaded_image(image_path: str) -> FileResponse:
    """返回已上传图片预览文件。"""
    from app.services.image_store import get_upload_image_path

    try:
        resolved_path = get_upload_image_path(image_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return FileResponse(resolved_path, media_type="image/png")
