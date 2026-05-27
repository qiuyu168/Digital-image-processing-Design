# 本文件用于实现 Sobel 边缘检测算法
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "sobel_edge_detection",
    "display_name": "Sobel边缘检测",
    "description": "使用 Sobel 一阶梯度算子提取图像水平、垂直或综合边缘，适合观察灰度变化方向和轮廓强度。",
    "params": {
        "direction": {
            "type": "select",
            "default": "both",
            "label": "检测方向",
            "component": "select",
            "options": [
                {"label": "综合边缘", "value": "both"},
                {"label": "X 方向梯度", "value": "x"},
                {"label": "Y 方向梯度", "value": "y"},
            ],
        },
        "kernel_size": {
            "type": "odd_int",
            "default": 3,
            "min": 1,
            "max": 7,
            "step": 2,
            "label": "Sobel核大小",
            "component": "slider",
        },
        "scale": {
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 5.0,
            "step": 0.1,
            "label": "梯度缩放",
            "component": "slider",
        },
        "delta": {
            "type": "int",
            "default": 0,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "亮度偏移",
            "component": "slider",
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    direction = _get_direction(params)
    kernel_size = _get_odd_param(params, "kernel_size")
    scale = _get_float_param(params, "scale")
    delta = _get_int_param(params, "delta")

    gray = _to_gray(_ensure_uint8(image))
    sobel_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=kernel_size, scale=scale, delta=delta)
    sobel_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=kernel_size, scale=scale, delta=delta)
    abs_x = cv2.convertScaleAbs(sobel_x)
    abs_y = cv2.convertScaleAbs(sobel_y)

    if direction == "x":
        result = abs_x
        direction_label = "X 方向梯度"
    elif direction == "y":
        result = abs_y
        direction_label = "Y 方向梯度"
    else:
        magnitude = cv2.magnitude(sobel_x, sobel_y)
        result = _normalize_gradient(magnitude)
        direction_label = "综合边缘"

    edge_pixels = int(np.count_nonzero(result))
    total_pixels = int(result.size)

    return {
        "result": result,
        "steps": [
            {"name": "灰度图像", "image": gray},
            {"name": "Sobel X 方向梯度", "image": abs_x},
            {"name": "Sobel Y 方向梯度", "image": abs_y},
            {"name": direction_label, "image": result},
        ],
        "metrics": {
            "direction": direction,
            "kernel_size": kernel_size,
            "scale": scale,
            "delta": delta,
            "edge_pixels": edge_pixels,
            "edge_ratio": round(edge_pixels / total_pixels, 4) if total_pixels else 0.0,
            "gradient_mean": round(float(np.mean(result)), 4),
            "gradient_max": int(np.max(result)) if result.size else 0,
        },
        "analysis": f"已使用 Sobel 算子计算{direction_label}，亮度越高表示该位置灰度变化越强，适合观察轮廓方向和边缘强度。",
    }


def _get_direction(params: dict) -> str:
    value = str(params.get("direction", ALGORITHM_META["params"]["direction"]["default"]))
    return value if value in {"x", "y", "both"} else "both"


def _get_int_param(params: dict, name: str) -> int:
    meta = ALGORITHM_META["params"][name]
    try:
        value = int(round(float(params.get(name, meta["default"]))))
    except (TypeError, ValueError):
        value = int(meta["default"])
    return int(np.clip(value, meta["min"], meta["max"]))


def _get_float_param(params: dict, name: str) -> float:
    meta = ALGORITHM_META["params"][name]
    try:
        value = float(params.get(name, meta["default"]))
    except (TypeError, ValueError):
        value = float(meta["default"])
    return float(np.clip(value, meta["min"], meta["max"]))


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


def _normalize_gradient(image: np.ndarray) -> np.ndarray:
    max_value = float(np.max(image)) if image.size else 0.0
    if max_value <= 0.0:
        return np.zeros(image.shape, dtype=np.uint8)
    normalized = image.astype(np.float32) * 255.0 / max_value
    return np.ascontiguousarray(np.clip(normalized, 0, 255).astype(np.uint8))
