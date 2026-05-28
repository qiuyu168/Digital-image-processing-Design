# 本文件用于实现 Canny 边缘检测算法
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import int_slider_value, odd_int_slider_value, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "canny_edge_detection",
    "display_name": "Canny边缘检测",
    "description": "使用 Canny 算子提取图像中的主要轮廓和结构边界。",
    "params": {
        "threshold1": {"type": "int", "default": 80, "min": 0, "max": 255, "step": 1, "label": "低阈值", "component": "slider"},
        "threshold2": {"type": "int", "default": 160, "min": 0, "max": 255, "step": 1, "label": "高阈值", "component": "slider"},
        "blur_size": {"type": "int", "default": 5, "min": 1, "max": 31, "step": 2, "label": "平滑核大小", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    threshold1 = int_slider_value(params, "threshold1", ALGORITHM_META)
    threshold2 = int_slider_value(params, "threshold2", ALGORITHM_META)
    if threshold1 > threshold2:
        threshold1, threshold2 = threshold2, threshold1
    blur_size = odd_int_slider_value(params, "blur_size", ALGORITHM_META)
    gray = to_gray(image)
    blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0) if blur_size > 1 else gray
    result = cv2.Canny(blurred, threshold1, threshold2).astype(np.uint8)
    edge_pixels = int(np.count_nonzero(result))
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "平滑图像", "image": blurred}, {"name": "处理结果", "image": result}],
        "metrics": {"threshold1": threshold1, "threshold2": threshold2, "blur_size": blur_size, "edge_pixels": edge_pixels, "edge_ratio": round(edge_pixels / result.size, 4)},
        "analysis": "Canny 边缘检测结合平滑、梯度、非极大值抑制和双阈值连接，能获得较连续的细线边缘。",
    }

