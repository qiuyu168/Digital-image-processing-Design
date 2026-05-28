# 本文件用于定义灰度图像类算法相关 API 路由

from typing import Any

from fastapi import APIRouter

from app.api.algorithm_modules.common import (
    CategoryRunRequest,
    build_module_algorithm_response,
    run_category_algorithm,
)


MODULE_NAME = "grayscale_image"
router = APIRouter(prefix="/api/algorithms/grayscale-image", tags=[MODULE_NAME])


@router.get("")
async def get_grayscale_image_algorithms() -> dict[str, Any]:
    """返回灰度图像类算法列表。"""
    return build_module_algorithm_response(MODULE_NAME)


@router.post("/run")
async def run_grayscale_image_algorithm(request: CategoryRunRequest) -> dict[str, Any]:
    """运行灰度图像类下的指定算法。"""
    return await run_category_algorithm(MODULE_NAME, request)
