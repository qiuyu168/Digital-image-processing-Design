# 本文件用于定义图像基本运算类算法相关 API 路由
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.api.algorithm_modules.common import (
    CategoryRunRequest,
    build_module_algorithm_response,
    run_category_algorithm,
)


MODULE_NAME = "basic_operation"
router = APIRouter(prefix="/api/algorithms/basic-operation", tags=[MODULE_NAME])


@router.get("")
async def get_basic_operation_algorithms() -> dict[str, Any]:
    """返回图像基本运算类算法列表。"""
    return build_module_algorithm_response(MODULE_NAME)


@router.post("/run")
async def run_basic_operation_algorithm(request: CategoryRunRequest) -> dict[str, Any]:
    """运行图像基本运算类下的指定算法。"""
    return await run_category_algorithm(MODULE_NAME, request)

