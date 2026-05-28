# 本文件用于实现角点检测算法
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import int_slider_value, slider_value, to_bgr, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "corner_detection",
    "display_name": "角点检测",
    "description": "使用 Shi-Tomasi 方法检测局部结构变化明显的角点。",
    "params": {
        "max_corners": {"type": "int", "default": 80, "min": 1, "max": 500, "step": 1, "label": "最大角点数", "component": "slider"},
        "quality_level": {"type": "float", "default": 0.01, "min": 0.001, "max": 0.2, "step": 0.001, "label": "质量阈值", "component": "slider"},
        "min_distance": {"type": "float", "default": 8.0, "min": 1.0, "max": 50.0, "step": 1.0, "label": "最小距离", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    gray = to_gray(source)
    max_corners = int_slider_value(params, "max_corners", ALGORITHM_META)
    quality_level = slider_value(params, "quality_level", ALGORITHM_META)
    min_distance = slider_value(params, "min_distance", ALGORITHM_META)
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=max_corners, qualityLevel=quality_level, minDistance=min_distance)
    result = source.copy()
    count = 0
    if corners is not None:
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(result, (int(round(x)), int(round(y))), 4, (0, 0, 255), -1)
            count += 1
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"max_corners": max_corners, "quality_level": quality_level, "min_distance": min_distance, "corner_count": count},
        "analysis": "角点检测寻找两个方向灰度变化都明显的位置，这些点常用于形状描述、匹配和跟踪。",
    }
