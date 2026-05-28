# 本文件用于实现 Sobel 边缘检测算法
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import int_slider_value, normalize_uint8, odd_int_slider_value, slider_value, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "sobel_edge_detection",
    "display_name": "Sobel边缘检测",
    "description": "使用 Sobel 一阶梯度算子提取水平、垂直或综合边缘。",
    "params": {
        "direction": {
            "type": "str",
            "default": "both",
            "label": "检测方向",
            "component": "select",
            "options": [
                {"label": "综合边缘", "value": "both"},
                {"label": "X方向梯度", "value": "x"},
                {"label": "Y方向梯度", "value": "y"},
            ],
        },
        "kernel_size": {"type": "int", "default": 3, "min": 1, "max": 7, "step": 2, "label": "Sobel核大小", "component": "slider"},
        "scale": {"type": "float", "default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1, "label": "梯度缩放", "component": "slider"},
        "delta": {"type": "int", "default": 0, "min": 0, "max": 255, "step": 1, "label": "亮度偏移", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    direction = str(params.get("direction", "both"))
    if direction not in {"x", "y", "both"}:
        direction = "both"
    kernel_size = odd_int_slider_value(params, "kernel_size", ALGORITHM_META)
    scale = slider_value(params, "scale", ALGORITHM_META)
    delta = int_slider_value(params, "delta", ALGORITHM_META)
    sobel_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=kernel_size, scale=scale, delta=delta)
    sobel_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=kernel_size, scale=scale, delta=delta)
    abs_x = cv2.convertScaleAbs(sobel_x)
    abs_y = cv2.convertScaleAbs(sobel_y)
    if direction == "x":
        result = abs_x
    elif direction == "y":
        result = abs_y
    else:
        result = normalize_uint8(cv2.magnitude(sobel_x, sobel_y))
    edge_pixels = int(np.count_nonzero(result))
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": gray}, {"name": "Sobel X", "image": abs_x}, {"name": "Sobel Y", "image": abs_y}, {"name": "处理结果", "image": result}],
        "metrics": {"direction": direction, "kernel_size": kernel_size, "scale": scale, "delta": delta, "edge_pixels": edge_pixels, "edge_ratio": round(edge_pixels / result.size, 4)},
        "analysis": "Sobel 算子通过一阶梯度近似突出灰度变化强的位置，适合观察边缘方向和边缘强度。",
    }

