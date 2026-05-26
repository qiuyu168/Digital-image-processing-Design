# 本文件用于定义图片上传和上传图片预览相关 API 路由

from fastapi import APIRouter, File, HTTPException, UploadFile


router = APIRouter(prefix="/api/upload", tags=["upload"])

UNIMPLEMENTED_SERVICE_DETAIL = "该接口框架已创建，具体业务逻辑待 service 层实现"


@router.post("/image")
async def upload_image(file: UploadFile = File(...)) -> dict[str, bool | int | str]:
    """接收上传图片，并返回前端可直接使用的占位响应。"""
    # TODO: 后续调用 app.services.upload_service.save_upload_image(file) 完成校验、保存和尺寸读取。
    _ = file
    image_id = "placeholder.png"
    return {
        "success": True,
        "image_id": image_id,
        "filename": image_id,
        "width": 0,
        "height": 0,
        "preview_url": f"/api/upload/preview/{image_id}",
        "message": "图片上传成功",
    }


@router.get("/preview/{image_id}")
async def preview_uploaded_image(image_id: str) -> None:
    """返回已上传图片预览文件。"""
    # TODO: 后续调用 app.services.upload_service.get_upload_preview_response(image_id) 安全返回文件。
    _ = image_id
    raise HTTPException(
        status_code=501,
        detail=UNIMPLEMENTED_SERVICE_DETAIL,
    )
