# 本文件用于定义六大算法分类 API 的共享常量和通用脚手架逻辑

from inspect import isawaitable
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, Field


UNIMPLEMENTED_SERVICE_DETAIL = "该接口框架已创建，具体业务逻辑待 service 层实现"

MODULE_DISPLAY_NAMES = {
    "grayscale_image": "灰度图像类",
    "color_image": "彩色图像类",
    "geometric_transform": "几何变换类",
    "spatial_filter": "空域滤波类",
    "frequency_analysis": "频域分析类",
    "frequency_filter": "频域滤波类",
}

CATEGORY_API_PATHS = {
    "grayscale_image": "grayscale-image",
    "color_image": "color-image",
    "geometric_transform": "geometric-transform",
    "spatial_filter": "spatial-filter",
    "frequency_analysis": "frequency-analysis",
    "frequency_filter": "frequency-filter",
}

ALGORITHM_MODULES = {
    "grayscale_image": [
        "grayscale",
        "binary_threshold",
        "histogram_equalization",
        "edge_detection_basic",
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

MODULE_ORDER = [
    "grayscale_image",
    "color_image",
    "geometric_transform",
    "spatial_filter",
    "frequency_analysis",
    "frequency_filter",
]


class CategoryRunRequest(BaseModel):
    """分类算法运行请求体。"""

    source_type: str = "upload"
    image_id: str | None = None
    image_path: str | None = None
    algorithm: str
    params: dict[str, Any] = Field(default_factory=dict)
    return_steps: bool = True


def build_module_algorithm_response(module_name: str) -> dict[str, Any]:
    return {
        "success": True,
        "module": module_name,
        "module_display_name": MODULE_DISPLAY_NAMES[module_name],
        "algorithms": get_algorithms_by_module(module_name),
    }


def get_algorithms_by_module(module_name: str) -> list[dict[str, Any]]:
    # TODO: 后续迁移到 app.services.algorithm_registry.get_algorithms_by_module(module_name)。
    try:
        from app.services.algorithm_registry import (
            get_algorithms_by_module as service_get_algorithms_by_module,
        )
    except ImportError:
        return []

    try:
        service_result = service_get_algorithms_by_module(module_name)
    except Exception:
        return []

    raw_algorithms = _extract_algorithm_list(service_result)
    return [
        _normalize_algorithm_meta(module_name, algorithm)
        for algorithm in raw_algorithms
        if isinstance(algorithm, dict)
    ]


async def run_category_algorithm(
    module_name: str,
    request: CategoryRunRequest,
) -> dict[str, Any]:
    validate_algorithm_belongs_to_module(module_name, request.algorithm)

    # TODO: 后续接入 app.services.process_service.run_algorithm 负责加载图片并调用算法。
    try:
        from app.services.process_service import run_algorithm as service_run_algorithm
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail=UNIMPLEMENTED_SERVICE_DETAIL,
        ) from None

    payload = _request_to_dict(request)
    result = service_run_algorithm(
        source_type=payload["source_type"],
        image_id=payload.get("image_id"),
        image_path=payload.get("image_path"),
        module_name=module_name,
        algorithm_name=payload["algorithm"],
        params=payload["params"],
        return_steps=payload["return_steps"],
    )
    if isawaitable(result):
        result = await result
    return result


def validate_algorithm_belongs_to_module(module_name: str, algorithm_name: str) -> None:
    if algorithm_name not in ALGORITHM_MODULES[module_name]:
        raise HTTPException(
            status_code=400,
            detail="该算法不属于当前算法大类",
        )


def _extract_algorithm_list(service_result: Any) -> list[Any]:
    if isinstance(service_result, list):
        return service_result
    if isinstance(service_result, dict):
        algorithms = service_result.get("algorithms", [])
        if isinstance(algorithms, list):
            return algorithms
    return []


def _normalize_algorithm_meta(
    module_name: str,
    algorithm: dict[str, Any],
) -> dict[str, Any]:
    module_display_name = MODULE_DISPLAY_NAMES[module_name]
    return {
        "module": module_name,
        "module_display_name": algorithm.get("module_display_name", module_display_name),
        "name": algorithm.get("name", ""),
        "display_name": algorithm.get("display_name", ""),
        "description": algorithm.get("description", ""),
        "params": algorithm.get("params", {}),
    }


def _request_to_dict(request: CategoryRunRequest) -> dict[str, Any]:
    if hasattr(request, "model_dump"):
        return request.model_dump()
    return request.dict()
