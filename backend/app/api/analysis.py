# 本文件用于定义图片指标分析相关 API 路由
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict


router = APIRouter(prefix="/api/analysis", tags=["analysis"])


class MetricsRequest(BaseModel):
    """前端提交的图片指标分析请求。"""

    model_config = ConfigDict(extra="forbid")

    source_type: str = "upload"
    image_path: str
    include_histogram: bool = False


@router.post("/metrics")
async def calculate_metrics(request: MetricsRequest) -> dict[str, Any]:
    """计算图片基础指标。"""
    from app.services.analysis_service import calculate_basic_metrics
    from app.services.image_store import load_image_by_source

    try:
        image = load_image_by_source(request.source_type, request.image_path)
        return {
            "success": True,
            "metrics": calculate_basic_metrics(
                image,
                include_histogram=request.include_histogram,
            ),
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
