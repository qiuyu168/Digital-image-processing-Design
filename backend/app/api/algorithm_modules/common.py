# 本文件用于定义算法分类 API 的共享常量和通用运行逻辑
from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from app.schemas.process_schema import CategoryProcessRequest
from app.services.algorithm_registry import ALGORITHM_MODULES, MODULE_DISPLAY_NAMES


CategoryRunRequest = CategoryProcessRequest


def build_module_algorithm_response(module_name: str) -> dict[str, Any]:
    """返回单个算法分类的元数据响应。"""
    service_result = get_algorithms_by_module(module_name)
    return {
        "success": True,
        "module": module_name,
        "module_display_name": MODULE_DISPLAY_NAMES[module_name],
        "algorithms": service_result["algorithms"],
    }


def get_algorithms_by_module(module_name: str) -> dict[str, Any]:
    """从服务层读取指定算法分类的元数据。"""
    from app.services.algorithm_registry import (
        get_algorithms_by_module as service_get_algorithms_by_module,
    )

    try:
        return service_get_algorithms_by_module(module_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


async def run_category_algorithm(
    module_name: str,
    request: CategoryRunRequest,
) -> dict[str, Any]:
    """运行当前分类下的指定算法。"""
    validate_algorithm_belongs_to_module(module_name, request.algorithm)
    from app.services.process_service import run_process

    payload = _request_to_dict(request)
    payload["module"] = module_name
    try:
        return run_process(payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"算法执行失败：{exc}") from exc


def validate_algorithm_belongs_to_module(module_name: str, algorithm_name: str) -> None:
    """校验算法是否属于当前算法大类。"""
    if algorithm_name not in ALGORITHM_MODULES[module_name]:
        raise HTTPException(
            status_code=400,
            detail="该算法不属于当前算法大类",
        )


def _request_to_dict(request: CategoryRunRequest) -> dict[str, Any]:
    if hasattr(request, "model_dump"):
        return request.model_dump()
    return request.dict()
