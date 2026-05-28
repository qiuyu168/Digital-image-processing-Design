# 本文件用于实现中值滤波去除噪声的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "median_filter",
    "display_name": "中值滤波",
    "description": "使用邻域中值替代中心像素，对椒盐噪声有较好的抑制效果。",
    "params": {
        "kernel_size": {
            "type": "odd_int",
            "default": 5,
            "min": 3,
            "max": 31,
            "step": 2,
            "label": "滤波核大小",
            "component": "slider",
        },
    },
}


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.ascontiguousarray(image)
    if array.dtype == np.uint8:
        return array.copy()
    return cv2.normalize(array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def _odd_param(params: dict, name: str, default: int, minimum: int, maximum: int) -> int:
    value = int(params.get(name, default))
    value = max(minimum, min(maximum, value))
    if value % 2 == 0:
        value += 1 if value < maximum else -1
    return max(minimum, value)


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
    kernel_size = _odd_param(params, "kernel_size", 5, 3, 31)
    result = cv2.medianBlur(source, kernel_size)
    gray_source = _gray_for_metrics(source)
    gray_result = _gray_for_metrics(result)

    return {
        "result": result.astype(np.uint8),
        "steps": [
            {"name": "原始图像", "image": source},
            {"name": f"{kernel_size}x{kernel_size} 中值滤波", "image": result},
        ],
        "metrics": {
            "kernel_size": kernel_size,
            "std_before": float(np.std(gray_source)),
            "std_after": float(np.std(gray_result)),
            "changed_pixel_ratio": float(np.mean(gray_source != gray_result)),
        },
        "analysis": "中值滤波依据邻域排序后的中间值生成输出像素，能有效剔除孤立亮点或暗点，同时比线性平滑更容易保留明显边缘。",
    }
