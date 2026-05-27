# 本文件用于定义六大算法分类 API 的共享常量和通用逻辑
from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from app.schemas.process_schema import CategoryProcessRequest


MODULE_DISPLAY_NAMES = {
    "grayscale_image": "灰度图像类",
    "color_image": "彩色图像类",
    "geometric_transform": "几何变换类",
    "spatial_filter": "空域滤波类",
    "frequency_analysis": "频域分析类",
    "frequency_filter": "频域滤波类",
}

ALGORITHM_MODULES = {
    "grayscale_image": [
        "grayscale",
        "binary_threshold",
        "histogram_equalization",
        "edge_detection_basic",
        "sobel_edge_detection",
        "erode",
        "dilate",
        "open_operation",
        "close_operation",
    ],
    "color_image": [
        "color_space_convert",
        "saturation_adjust",
        "anime_color_enhance",
        "dominant_color_extract",
    ],
    "geometric_transform": [
        "resize",
        "rotate",
        "flip",
    ],
    "spatial_filter": [
        "mean_filter",
        "gaussian_filter",
        "median_filter",
        "bilateral_filter",
        "laplacian_sharpen",
    ],
    "frequency_analysis": [
        "dft_spectrum",
        "spectrum_shift",
        "magnitude_spectrum",
    ],
    "frequency_filter": [
        "low_pass_filter",
        "high_pass_filter",
        "ideal_low_pass",
        "ideal_high_pass",
        "gaussian_low_pass",
        "gaussian_high_pass",
    ],
}

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
    """校验算法是否属于当前分类。"""
    if algorithm_name not in ALGORITHM_MODULES[module_name]:
        raise HTTPException(
            status_code=400,
            detail="该算法不属于当前算法大类",
        )


def _request_to_dict(request: CategoryRunRequest) -> dict[str, Any]:
    if hasattr(request, "model_dump"):
        return request.model_dump()
    return request.dict()
