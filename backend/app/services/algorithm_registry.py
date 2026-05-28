# 本文件用于动态加载算法模块并生成前端可用的算法元数据注册表
from __future__ import annotations

import importlib
import logging
from types import ModuleType
from typing import Any


logger = logging.getLogger(__name__)

MODULE_ORDER = [
    "basic_operation",
    "grayscale_image",
    "color_image",
    "geometric_transform",
    "spatial_filter",
    "frequency_analysis",
    "frequency_filter",
    "image_restoration",
    "edge_shape_detection",
]

MODULE_DISPLAY_NAMES = {
    "basic_operation": "图像基本运算类",
    "grayscale_image": "灰度图像类",
    "color_image": "彩色图像类",
    "geometric_transform": "几何变换类",
    "spatial_filter": "空间滤波类",
    "frequency_analysis": "频域分析类",
    "frequency_filter": "频域滤波类",
    "image_restoration": "图像复原与图像修复类",
    "edge_shape_detection": "边缘与形状检测类",
}

ALGORITHM_MODULES = {
    "basic_operation": [
        "add_operation",
        "subtract_operation",
        "multiply_operation",
        "divide_operation",
        "and_operation",
        "or_operation",
        "not_operation",
        "xor_operation",
    ],
    "grayscale_image": [
        "linear_gray_transform",
        "gamma_correction",
        "log_transform",
        "exponential_transform",
        "negative_transform",
        "grayscale",
        "binary_threshold",
        "histogram_equalization",
        "clahe_equalization",
        "histogram_matching",
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
        "region_mosaic",
        "color_comprehensive_processing",
    ],
    "geometric_transform": [
        "resize",
        "rotate",
        "flip",
        "translate",
        "affine_transform",
        "perspective_transform",
    ],
    "spatial_filter": [
        "mean_filter",
        "gaussian_filter",
        "median_filter",
        "bilateral_filter",
        "laplacian_sharpen",
        "statistical_order_filter",
        "max_filter",
        "min_filter",
        "adaptive_median_filter",
        "unsharp_masking",
        "add_noise",
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
        "butterworth_low_pass",
        "butterworth_high_pass",
        "frequency_laplacian_sharpen",
        "homomorphic_filter",
    ],
    "image_restoration": [
        "defocus_blur_simulation",
        "lens_distortion_blur_simulation",
        "motion_blur_simulation",
        "atmospheric_turbulence_blur_simulation",
        "inverse_filter_restoration",
        "windowed_inverse_filter_restoration",
        "wiener_filter_restoration",
        "constrained_least_squares_restoration",
    ],
    "edge_shape_detection": [
        "basic_edge_detection",
        "canny_edge_detection",
        "sobel_edge_detection",
        "roberts_cross",
        "prewitt_edge_detection",
        "scharr_edge_detection",
        "log_edge_detection",
        "hough_shape_detection",
        "corner_detection",
    ],
}


def get_all_algorithms() -> dict[str, Any]:
    """返回九个算法模块及其所有可导入算法元数据。"""
    modules: list[dict[str, Any]] = []
    flat_algorithms: list[dict[str, Any]] = []

    for module_name in MODULE_ORDER:
        algorithms = _load_algorithms_for_module(module_name)
        modules.append(
            {
                "module": module_name,
                "display_name": get_module_display_name(module_name),
                "algorithms": algorithms,
            }
        )
        flat_algorithms.extend(algorithms)

    return {"success": True, "modules": modules, "algorithms": flat_algorithms}


def get_algorithms_by_module(module_name: str) -> dict[str, Any]:
    """返回指定算法大类下的算法元数据。"""
    _validate_module_name(module_name)
    algorithms = _load_algorithms_for_module(module_name)
    return {
        "success": True,
        "module": module_name,
        "module_display_name": get_module_display_name(module_name),
        "algorithms": algorithms,
    }


def get_algorithm(module_name: str, algorithm_name: str) -> ModuleType:
    """根据算法大类和算法名导入算法模块对象。"""
    _validate_module_name(module_name)
    if algorithm_name not in ALGORITHM_MODULES[module_name]:
        raise ValueError(f"算法不存在：{module_name}/{algorithm_name}")

    module = importlib.import_module(f"app.algorithms.{module_name}.{algorithm_name}")
    run_function = getattr(module, "run", None)
    if not callable(run_function):
        raise ValueError(f"算法缺少 run(image, params) 接口：{module_name}/{algorithm_name}")
    return module


def get_module_display_name(module_name: str) -> str:
    """返回算法大类中文显示名。"""
    _validate_module_name(module_name)
    return MODULE_DISPLAY_NAMES[module_name]


def _load_algorithms_for_module(module_name: str) -> list[dict[str, Any]]:
    algorithms: list[dict[str, Any]] = []
    for algorithm_name in ALGORITHM_MODULES[module_name]:
        try:
            module = importlib.import_module(f"app.algorithms.{module_name}.{algorithm_name}")
            meta = getattr(module, "ALGORITHM_META", {})
            if not isinstance(meta, dict):
                raise ValueError("ALGORITHM_META 必须是 dict")
            algorithms.append(_normalize_algorithm_meta(module_name, algorithm_name, meta))
        except Exception as exc:
            logger.exception("算法导入失败：%s/%s", module_name, algorithm_name)
            algorithms.append(
                {
                    "module": module_name,
                    "module_display_name": get_module_display_name(module_name),
                    "name": algorithm_name,
                    "display_name": algorithm_name,
                    "description": "",
                    "params": {},
                    "error": str(exc),
                }
            )
    return algorithms


def _normalize_algorithm_meta(
    module_name: str,
    algorithm_name: str,
    meta: dict[str, Any],
) -> dict[str, Any]:
    normalized = dict(meta)
    normalized["module"] = module_name
    normalized["module_display_name"] = meta.get("module_display_name", get_module_display_name(module_name))
    normalized["name"] = meta.get("name") or algorithm_name
    normalized["display_name"] = meta.get("display_name") or normalized["name"]
    normalized["description"] = meta.get("description") or ""
    normalized["params"] = meta.get("params") if isinstance(meta.get("params"), dict) else {}
    return normalized


def _validate_module_name(module_name: str) -> None:
    if module_name not in MODULE_ORDER:
        raise ValueError(f"算法模块不存在：{module_name}")

