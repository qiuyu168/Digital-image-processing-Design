# 本文件用于定义图片算法处理相关 API 路由
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.schemas.process_schema import ProcessRequest


router = APIRouter(prefix="/api/process", tags=["process"])


def _request_to_dict(request: ProcessRequest) -> dict[str, Any]:
    if hasattr(request, "model_dump"):
        return request.model_dump()
    return request.dict()


@router.post("/run")
async def run_process(request: ProcessRequest) -> dict[str, Any]:
    """根据模块名和算法名运行图像处理流程。"""
    from app.services.process_service import run_process as service_run_process

    try:
        return service_run_process(_request_to_dict(request))
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"算法执行失败：{exc}") from exc
