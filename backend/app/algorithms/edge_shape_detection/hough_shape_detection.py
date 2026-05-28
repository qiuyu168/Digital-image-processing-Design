# 本文件用于实现 Hough 变换边缘与形状检测
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import int_slider_value, to_bgr, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "hough_shape_detection",
    "display_name": "Hough形状检测",
    "description": "基于 Canny 边缘和概率 Hough 变换检测直线形状。",
    "params": {
        "threshold": {"type": "int", "default": 60, "min": 1, "max": 200, "step": 1, "label": "投票阈值", "component": "slider"},
        "min_line_length": {"type": "int", "default": 30, "min": 1, "max": 300, "step": 1, "label": "最小线段长度", "component": "slider"},
        "max_line_gap": {"type": "int", "default": 10, "min": 0, "max": 100, "step": 1, "label": "最大线段间隙", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    gray = to_gray(source)
    threshold = int_slider_value(params, "threshold", ALGORITHM_META)
    min_line_length = int_slider_value(params, "min_line_length", ALGORITHM_META)
    max_line_gap = int_slider_value(params, "max_line_gap", ALGORITHM_META)
    edges = cv2.Canny(gray, 80, 160)
    result = source.copy()
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)
    line_count = 0
    if lines is not None:
        for line in lines[:200]:
            x1, y1, x2, y2 = line[0]
            cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 2)
            line_count += 1
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": source}, {"name": "边缘图像", "image": edges}, {"name": "处理结果", "image": result}],
        "metrics": {"threshold": threshold, "min_line_length": min_line_length, "max_line_gap": max_line_gap, "line_count": line_count},
        "analysis": "Hough 变换把边缘点映射到参数空间进行投票，能够从边缘图中提取直线等几何形状。",
    }

