# 本文件用于实现图像仿射变换
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import ensure_uint8, slider_value


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "affine_transform",
    "display_name": "仿射变换",
    "description": "使用三点控制实现平移、缩放、旋转和剪切组合变换。",
    "params": {
        "skew_x": {"type": "float", "default": 0.15, "min": -0.8, "max": 0.8, "step": 0.01, "label": "水平剪切", "component": "slider"},
        "skew_y": {"type": "float", "default": 0.0, "min": -0.8, "max": 0.8, "step": 0.01, "label": "垂直剪切", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = ensure_uint8(image)
    skew_x = slider_value(params, "skew_x", ALGORITHM_META)
    skew_y = slider_value(params, "skew_y", ALGORITHM_META)
    height, width = source.shape[:2]
    src = np.float32([[0, 0], [width - 1, 0], [0, height - 1]])
    dst = np.float32([[0, 0], [width - 1, skew_y * height], [skew_x * width, height - 1]])
    matrix = cv2.getAffineTransform(src, dst)
    result = cv2.warpAffine(source, matrix, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"skew_x": skew_x, "skew_y": skew_y, "width": width, "height": height},
        "analysis": "仿射变换保持直线和平行关系，可同时表达平移、旋转、缩放和剪切等几何变化。",
    }

