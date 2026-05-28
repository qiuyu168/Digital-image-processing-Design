# 本文件用于实现将灰度图转换为黑白二值图像的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "binary_threshold",
    "display_name": "二值化",
    "description": "按照固定阈值将图像转换为黑白二值图，便于目标区域分割和形态学处理。",
    "params": {
        "threshold": {
            "type": "int",
            "default": 127,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "二值阈值",
            "component": "slider",
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    threshold = _get_int_param(params, "threshold")
    gray = _to_gray(_ensure_uint8(image))
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    foreground_pixels = int(np.count_nonzero(binary))
    total_pixels = int(binary.size)

    return {
        "result": binary,
        "steps": [
            {"name": "灰度图像", "image": gray},
            {"name": "二值化结果", "image": binary},
        ],
        "metrics": {
            "threshold": threshold,
            "foreground_pixels": foreground_pixels,
            "foreground_ratio": round(foreground_pixels / total_pixels, 4) if total_pixels else 0.0,
        },
        "analysis": f"已使用阈值 {threshold} 进行二值化，高于阈值的区域被设为白色，低于阈值的区域被设为黑色。",
    }


def _get_int_param(params: dict, name: str) -> int:
    meta = ALGORITHM_META["params"][name]
    try:
        value = int(round(float(params.get(name, meta["default"]))))
    except (TypeError, ValueError):
        value = int(meta["default"])
    return int(np.clip(value, meta["min"], meta["max"]))


def _to_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return np.ascontiguousarray(image)
    if image.ndim != 3:
        raise ValueError("输入图像必须是二维灰度图或三维彩色图")
    if image.shape[2] == 1:
        return np.ascontiguousarray(image[:, :, 0])
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2GRAY)


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.asarray(image)
    if array.size == 0:
        raise ValueError("输入图像不能为空数组")
    if array.dtype == np.uint8:
        return np.ascontiguousarray(array)
    array = np.nan_to_num(array.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    if 0.0 <= float(np.min(array)) and float(np.max(array)) <= 1.0:
        array = array * 255.0
    return np.ascontiguousarray(np.clip(array, 0, 255).astype(np.uint8))
