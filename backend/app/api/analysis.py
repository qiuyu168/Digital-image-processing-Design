# 本文件用于定义图片指标分析相关 API 路由

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/api/analysis", tags=["analysis"])

UNIMPLEMENTED_SERVICE_DETAIL = "该接口框架已创建，具体业务逻辑待 service 层实现"


class MetricsRequest(BaseModel):
    """前端提交的图片指标分析请求。"""

    source_type: str = "upload"
    image_id: str | None = None
    image_path: str | None = None
    include_histogram: bool = False


@router.post("/metrics")
async def calculate_metrics(request: MetricsRequest) -> dict[str, Any]:
    """计算图片基础指标和可选分析结果。"""
    # TODO: 后续调用 app.services.analysis_service.calculate_image_metrics(request)。
    _ = request
    raise HTTPException(
        status_code=501,
        detail=UNIMPLEMENTED_SERVICE_DETAIL,
    )
