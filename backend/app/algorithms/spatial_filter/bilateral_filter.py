# 本文件用于实现双边滤波平滑并保留边缘的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "bilateral_filter",
    "display_name": "双边滤波",
    "description": "在平滑图像的同时尽量保留边缘，适合线稿、动漫风格图像和人像图像降噪。",
    "params": {
        "diameter": {
            "type": "int",
            "default": 9,
            "min": 1,
            "max": 31,
            "step": 2,
            "label": "邻域直径",
            "component": "slider",
        },
        "sigma_color": {
            "type": "float",
            "default": 75.0,
            "min": 1.0,
            "max": 200.0,
            "step": 1.0,
            "label": "颜色标准差",
            "component": "slider",
        },
        "sigma_space": {
            "type": "float",
            "default": 75.0,
            "min": 1.0,
            "max": 200.0,
            "step": 1.0,
            "label": "空间标准差",
            "component": "slider",
        },
    },
}


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.ascontiguousarray(image)
    if array.dtype == np.uint8:
        return array.copy()
    return cv2.normalize(array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def _int_param(params: dict, name: str, default: int, minimum: int, maximum: int) -> int:
    value = int(params.get(name, default))
    return max(minimum, min(maximum, value))


def _float_param(params: dict, name: str, default: float, minimum: float, maximum: float) -> float:
    value = float(params.get(name, default))
    return max(minimum, min(maximum, value))


def _gray_for_metrics(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    source = _ensure_uint8(image)
    diameter = _int_param(params, "diameter", 9, 1, 31)
    sigma_color = _float_param(params, "sigma_color", 75.0, 1.0, 200.0)
    sigma_space = _float_param(params, "sigma_space", 75.0, 1.0, 200.0)
    result = cv2.bilateralFilter(source, diameter, sigma_color, sigma_space)
    gray_source = _gray_for_metrics(source)
    gray_result = _gray_for_metrics(result)

    return {
        "result": result.astype(np.uint8),
        "steps": [
            {"name": "原始图像", "image": source},
            {"name": "双边滤波结果", "image": result},
        ],
        "metrics": {
            "diameter": diameter,
            "sigma_color": sigma_color,
            "sigma_space": sigma_space,
            "std_before": float(np.std(gray_source)),
            "std_after": float(np.std(gray_result)),
            "mean_abs_change": float(np.mean(np.abs(gray_source.astype(np.float32) - gray_result.astype(np.float32)))),
        },
        "analysis": "双边滤波同时考虑空间距离和颜色相似度，能平滑同一区域内的细碎噪声，并减少跨越明显边缘的混合。",
    }
