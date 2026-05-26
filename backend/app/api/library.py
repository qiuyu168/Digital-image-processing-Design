# 本文件用于定义内置图片库相关 API 路由

from fastapi import APIRouter, HTTPException, Query


router = APIRouter(prefix="/api/library", tags=["library"])

UNIMPLEMENTED_SERVICE_DETAIL = "该接口框架已创建，具体业务逻辑待 service 层实现"

LIBRARY_CATEGORIES = [
    {
        "name": "anime_character",
        "display_name": "动漫人物图像",
        "count": 0,
    },
    {
        "name": "anime_scene",
        "display_name": "动漫场景图像",
        "count": 0,
    },
    {
        "name": "anime_avatar",
        "display_name": "动漫头像图像",
        "count": 0,
    },
    {
        "name": "course_samples",
        "display_name": "课程示例图像",
        "count": 0,
    },
    {
        "name": "other",
        "display_name": "其他图像",
        "count": 0,
    },
]


@router.get("/categories")
async def get_library_categories() -> dict[str, bool | list[dict[str, int | str]]]:
    """返回内置图片库分类。"""
    # TODO: 后续从 app.services.library_service 读取真实分类数量。
    return {
        "success": True,
        "categories": LIBRARY_CATEGORIES,
    }


@router.get("/images")
async def get_library_images(
    category: str = Query(default="anime_character", description="内置图片分类名称"),
) -> dict[str, bool | str | list[dict[str, str]]]:
    """返回指定内置分类下的图片列表。"""
    # TODO: 后续调用 app.services.library_service.list_library_images(category)。
    return {
        "success": True,
        "category": category,
        "images": [],
    }


@router.get("/image/{image_path:path}")
async def get_library_image(image_path: str) -> None:
    """返回内置图片库中的图片文件。"""
    # TODO: 后续调用 app.services.library_service.get_library_image_response(image_path) 安全返回文件。
    _ = image_path
    raise HTTPException(
        status_code=501,
        detail=UNIMPLEMENTED_SERVICE_DETAIL,
    )
