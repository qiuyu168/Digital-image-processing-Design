# 本文件用于定义算法元数据相关 API 路由
from __future__ import annotations

from typing import Any

from fastapi import APIRouter


router = APIRouter(prefix="/api", tags=["algorithms"])


@router.get("/algorithms")
async def get_algorithms() -> dict[str, Any]:
    """返回前端需要的算法分类和参数元数据。"""
    from app.services.algorithm_registry import get_all_algorithms

    return get_all_algorithms()
