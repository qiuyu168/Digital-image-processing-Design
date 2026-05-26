# 本文件用于定义几何变换类算法相关 API 路由

from typing import Any

from fastapi import APIRouter

from app.api.algorithm_modules.common import (
    CategoryRunRequest,
    build_module_algorithm_response,
    run_category_algorithm,
)


MODULE_NAME = "geometric_transform"
router = APIRouter(prefix="/api/algorithms/geometric-transform", tags=[MODULE_NAME])


@router.get("")
async def get_geometric_transform_algorithms() -> dict[str, Any]:
    """返回几何变换类算法列表。"""
    return build_module_algorithm_response(MODULE_NAME)


@router.post("/run")
async def run_geometric_transform_algorithm(request: CategoryRunRequest) -> dict[str, Any]:
    """运行几何变换类下的指定算法。"""
    return await run_category_algorithm(MODULE_NAME, request)
