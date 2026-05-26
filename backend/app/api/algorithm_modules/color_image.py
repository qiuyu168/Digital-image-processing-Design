# 本文件用于定义彩色图像类算法相关 API 路由

from typing import Any

from fastapi import APIRouter

from app.api.algorithm_modules.common import (
    CategoryRunRequest,
    build_module_algorithm_response,
    run_category_algorithm,
)


MODULE_NAME = "color_image"
router = APIRouter(prefix="/api/algorithms/color-image", tags=[MODULE_NAME])


@router.get("")
async def get_color_image_algorithms() -> dict[str, Any]:
    """返回彩色图像类算法列表。"""
    return build_module_algorithm_response(MODULE_NAME)


@router.post("/run")
async def run_color_image_algorithm(request: CategoryRunRequest) -> dict[str, Any]:
    """运行彩色图像类下的指定算法。"""
    return await run_category_algorithm(MODULE_NAME, request)
