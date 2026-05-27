# 本文件用于实现拉普拉斯锐化增强边缘的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "laplacian_sharpen",
    "display_name": "拉普拉斯锐化",
    "description": "通过二阶导数增强图像边缘和细节，使轮廓更加清晰。",
    "params": {
        "amount": {
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "锐化强度",
            "component": "slider",
        },
    },
}


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.ascontiguousarray(image)
    if array.dtype == np.uint8:
        return array.copy()
    return cv2.normalize(array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def _float_param(params: dict, name: str, default: float, minimum: float, maximum: float) -> float:
    value = float(params.get(name, default))
    return max(minimum, min(maximum, value))


def _gray_for_metrics(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def _normalize_uint8(values: np.ndarray) -> np.ndarray:
    if float(np.max(values)) == float(np.min(values)):
        return np.zeros(values.shape[:2], dtype=np.uint8)
    return cv2.normalize(values, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    source = _ensure_uint8(image)
    amount = _float_param(params, "amount", 0.5, 0.0, 3.0)
    laplacian = cv2.Laplacian(source.astype(np.float32), cv2.CV_32F, ksize=3)
    sharpened = np.clip(source.astype(np.float32) - amount * laplacian, 0, 255).astype(np.uint8)
    laplacian_display = _normalize_uint8(np.abs(_gray_for_metrics(laplacian)))
    gray_source = _gray_for_metrics(source)
    gray_result = _gray_for_metrics(sharpened)

    return {
        "result": sharpened,
        "steps": [
            {"name": "原始图像", "image": source},
            {"name": "拉普拉斯响应", "image": laplacian_display},
            {"name": "锐化结果", "image": sharpened},
        ],
        "metrics": {
            "amount": amount,
            "edge_response_mean": float(np.mean(laplacian_display)),
            "std_before": float(np.std(gray_source)),
            "std_after": float(np.std(gray_result)),
        },
        "analysis": "拉普拉斯算子突出灰度变化剧烈的位置，将响应按强度回加到原图后，边缘和纹理细节会更加清晰。",
    }
