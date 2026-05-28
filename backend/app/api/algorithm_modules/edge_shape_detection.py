# 本文件用于定义边缘与形状检测类算法相关 API 路由
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.api.algorithm_modules.common import (
    CategoryRunRequest,
    build_module_algorithm_response,
    run_category_algorithm,
)


MODULE_NAME = "edge_shape_detection"
router = APIRouter(prefix="/api/algorithms/edge-shape-detection", tags=[MODULE_NAME])


@router.get("")
async def get_edge_shape_detection_algorithms() -> dict[str, Any]:
    """返回边缘与形状检测类算法列表。"""
    return build_module_algorithm_response(MODULE_NAME)


@router.post("/run")
async def run_edge_shape_detection_algorithm(request: CategoryRunRequest) -> dict[str, Any]:
    """运行边缘与形状检测类下的指定算法。"""
    return await run_category_algorithm(MODULE_NAME, request)

