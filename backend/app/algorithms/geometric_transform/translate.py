# 本文件用于实现图像平移变换
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import ensure_uint8, slider_value


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "translate",
    "display_name": "图像平移",
    "description": "按水平和垂直像素偏移移动图像。",
    "params": {
        "shift_x": {"type": "float", "default": 20.0, "min": -300.0, "max": 300.0, "step": 1.0, "label": "水平平移", "component": "slider"},
        "shift_y": {"type": "float", "default": 20.0, "min": -300.0, "max": 300.0, "step": 1.0, "label": "垂直平移", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = ensure_uint8(image)
    shift_x = slider_value(params, "shift_x", ALGORITHM_META)
    shift_y = slider_value(params, "shift_y", ALGORITHM_META)
    height, width = source.shape[:2]
    matrix = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    result = cv2.warpAffine(source, matrix, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"shift_x": shift_x, "shift_y": shift_y, "width": width, "height": height},
        "analysis": "图像平移通过仿射矩阵改变像素位置，可用于演示二维空间坐标变换和边界填充效果。",
    }

