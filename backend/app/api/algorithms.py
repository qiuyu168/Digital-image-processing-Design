# 本文件用于定义算法元数据相关 API 路由

from importlib import import_module
from typing import Any

from fastapi import APIRouter


router = APIRouter(prefix="/api", tags=["algorithms"])

# TODO: 后续迁移到 services/algorithm_registry.py 或 core/config.py 中统一管理。
MODULE_DISPLAY_NAMES = {
    "grayscale_image": "灰度图像类",
    "color_image": "彩色图像类",
    "geometric_transform": "几何变换类",
    "spatial_filter": "空域滤波类",
    "frequency_analysis": "频域分析类",
    "frequency_filter": "频域滤波类",
}

MODULE_ORDER = [
    "grayscale_image",
    "color_image",
    "geometric_transform",
    "spatial_filter",
    "frequency_analysis",
    "frequency_filter",
]

COLOR_IMAGE_ALGORITHM_MODULES = [
    "anime_color_enhance",
    "color_space_convert",
    "dominant_color_extract",
    "saturation_adjust",
]


def _empty_module_response() -> list[dict[str, Any]]:
    return [
        {
            "module": module_name,
            "display_name": MODULE_DISPLAY_NAMES[module_name],
            "algorithms": [],
        }
        for module_name in MODULE_ORDER
    ]


def _normalize_algorithm(module_name: str, algorithm: dict[str, Any]) -> dict[str, Any]:
    module_display_name = MODULE_DISPLAY_NAMES[module_name]
    return {
        "module": module_name,
        "module_display_name": algorithm.get("module_display_name", module_display_name),
        "name": algorithm.get("name", ""),
        "display_name": algorithm.get("display_name", ""),
        "description": algorithm.get("description", ""),
        "params": algorithm.get("params", {}),
    }


def _normalize_registry_response(registry_data: Any) -> dict[str, Any]:
    modules = _empty_module_response()
    algorithms_by_module: dict[str, list[dict[str, Any]]] = {
        module_name: [] for module_name in MODULE_ORDER
    }

    if isinstance(registry_data, dict):
        raw_modules = registry_data.get("modules", [])
        raw_algorithms = registry_data.get("algorithms", [])
    elif isinstance(registry_data, list):
        raw_modules = []
        raw_algorithms = registry_data
    else:
        raw_modules = []
        raw_algorithms = []

    if isinstance(raw_modules, list):
        for module_info in raw_modules:
            if not isinstance(module_info, dict):
                continue
            module_name = module_info.get("module")
            if module_name not in algorithms_by_module:
                continue
            raw_module_algorithms = module_info.get("algorithms", [])
            if isinstance(raw_module_algorithms, list):
                algorithms_by_module[module_name].extend(
                    algorithm
                    for algorithm in raw_module_algorithms
                    if isinstance(algorithm, dict)
                )

    if isinstance(raw_algorithms, list):
        for algorithm in raw_algorithms:
            if not isinstance(algorithm, dict):
                continue
            module_name = algorithm.get("module")
            if module_name in algorithms_by_module:
                algorithms_by_module[module_name].append(algorithm)

    normalized_flat_algorithms: list[dict[str, Any]] = []
    for module_info in modules:
        module_name = module_info["module"]
        normalized_algorithms = [
            _normalize_algorithm(module_name, algorithm)
            for algorithm in algorithms_by_module[module_name]
        ]
        module_info["algorithms"] = normalized_algorithms
        normalized_flat_algorithms.extend(normalized_algorithms)

    return {
        "success": True,
        "modules": modules,
        "algorithms": normalized_flat_algorithms,
    }


def _load_registry_data() -> Any:
    # TODO: 后续实现 app.services.algorithm_registry.get_all_algorithms 后优先使用真实注册表。
    try:
        from app.services.algorithm_registry import get_all_algorithms
    except ImportError:
        return None

    try:
        return get_all_algorithms()
    except Exception:
        return None


def _load_color_image_algorithms() -> list[dict[str, Any]]:
    algorithms: list[dict[str, Any]] = []
    for module_name in COLOR_IMAGE_ALGORITHM_MODULES:
        try:
            module = import_module(f"app.algorithms.color_image.{module_name}")
        except ImportError:
            continue

        algorithm_meta = getattr(module, "ALGORITHM_META", None)
        if not isinstance(algorithm_meta, dict):
            continue

        normalized_meta = dict(algorithm_meta)
        normalized_meta["module"] = "color_image"
        normalized_meta.setdefault(
            "module_display_name",
            MODULE_DISPLAY_NAMES["color_image"],
        )
        normalized_meta.setdefault("params", {})
        algorithms.append(normalized_meta)
    return algorithms


def _merge_color_image_fallback(registry_data: Any) -> Any:
    color_image_algorithms = _load_color_image_algorithms()
    if not color_image_algorithms:
        return registry_data

    if registry_data is None:
        return {"algorithms": color_image_algorithms}

    if isinstance(registry_data, dict):
        merged_data = dict(registry_data)
        existing_algorithms = merged_data.get("algorithms", [])
        if not isinstance(existing_algorithms, list):
            existing_algorithms = []

        existing_color_names = {
            algorithm.get("name")
            for algorithm in existing_algorithms
            if isinstance(algorithm, dict) and algorithm.get("module") == "color_image"
        }
        raw_modules = merged_data.get("modules", [])
        if isinstance(raw_modules, list):
            for module_info in raw_modules:
                if not isinstance(module_info, dict):
                    continue
                if module_info.get("module") != "color_image":
                    continue
                raw_module_algorithms = module_info.get("algorithms", [])
                if not isinstance(raw_module_algorithms, list):
                    continue
                existing_color_names.update(
                    algorithm.get("name")
                    for algorithm in raw_module_algorithms
                    if isinstance(algorithm, dict)
                )
        merged_data["algorithms"] = [
            *existing_algorithms,
            *[
                algorithm
                for algorithm in color_image_algorithms
                if algorithm.get("name") not in existing_color_names
            ],
        ]
        return merged_data

    if isinstance(registry_data, list):
        existing_color_names = {
            algorithm.get("name")
            for algorithm in registry_data
            if isinstance(algorithm, dict) and algorithm.get("module") == "color_image"
        }
        return [
            *registry_data,
            *[
                algorithm
                for algorithm in color_image_algorithms
                if algorithm.get("name") not in existing_color_names
            ],
        ]

    return {"algorithms": color_image_algorithms}


@router.get("/algorithms")
async def get_algorithms() -> dict[str, Any]:
    """返回前端工作页所需的算法分类和参数元数据。"""
    registry_data = _load_registry_data()
    registry_data = _merge_color_image_fallback(registry_data)
    return _normalize_registry_response(registry_data)
