# 本文件用于实现图像膨胀操作的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "dilate",
    "display_name": "膨胀",
    "description": "扩大白色前景区域，连接断裂结构并增强目标边界。",
    "params": {
        "kernel_size": {"type": "odd_int", "default": 5, "min": 1, "max": 31, "step": 2, "label": "结构元素大小", "component": "slider"},
        "threshold": {"type": "int", "default": 127, "min": 0, "max": 255, "step": 1, "label": "二值阈值", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}
    kernel_size = _get_odd_param(params, "kernel_size")
    threshold = _get_int_param(params, "threshold")
    gray = _to_gray(_ensure_uint8(image))
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    result = cv2.dilate(binary, kernel)
    before = int(np.count_nonzero(binary))
    after = int(np.count_nonzero(result))
    return {
        "result": result,
        "steps": [
            {"name": "灰度图像", "image": gray},
            {"name": "二值化图像", "image": binary},
            {"name": "膨胀结果", "image": result},
        ],
        "metrics": {"kernel_size": kernel_size, "threshold": threshold, "foreground_before": before, "foreground_after": after},
        "analysis": "膨胀会扩大白色前景区域，可连接断裂笔画、线条或动漫图像中的细小目标结构。",
    }


def _get_int_param(params: dict, name: str) -> int:
    meta = ALGORITHM_META["params"][name]
    try:
        value = int(round(float(params.get(name, meta["default"]))))
    except (TypeError, ValueError):
        value = int(meta["default"])
    return int(np.clip(value, meta["min"], meta["max"]))


def _get_odd_param(params: dict, name: str) -> int:
    value = _get_int_param(params, name)
    if value % 2 == 0:
        value += 1
    return min(value, ALGORITHM_META["params"][name]["max"])


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
