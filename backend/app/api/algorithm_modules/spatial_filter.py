# 本文件用于定义空域滤波类算法相关 API 路由

from typing import Any

from fastapi import APIRouter

from app.api.algorithm_modules.common import (
    CategoryRunRequest,
    build_module_algorithm_response,
    run_category_algorithm,
)


MODULE_NAME = "spatial_filter"
router = APIRouter(prefix="/api/algorithms/spatial-filter", tags=[MODULE_NAME])


@router.get("")
async def get_spatial_filter_algorithms() -> dict[str, Any]:
    """返回空域滤波类算法列表。"""
    return build_module_algorithm_response(MODULE_NAME)


@router.post("/run")
async def run_spatial_filter_algorithm(request: CategoryRunRequest) -> dict[str, Any]:
    """运行空域滤波类下的指定算法。"""
    return await run_category_algorithm(MODULE_NAME, request)
