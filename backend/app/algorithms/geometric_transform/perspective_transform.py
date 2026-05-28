# 本文件用于实现图像投影变换
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import ensure_uint8, slider_value


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "perspective_transform",
    "display_name": "投影变换",
    "description": "通过四点映射模拟透视校正或透视扭曲。",
    "params": {
        "top_shrink": {"type": "float", "default": 0.12, "min": -0.4, "max": 0.4, "step": 0.01, "label": "上边收缩比例", "component": "slider"},
        "bottom_shrink": {"type": "float", "default": -0.05, "min": -0.4, "max": 0.4, "step": 0.01, "label": "下边收缩比例", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = ensure_uint8(image)
    top_shrink = slider_value(params, "top_shrink", ALGORITHM_META)
    bottom_shrink = slider_value(params, "bottom_shrink", ALGORITHM_META)
    height, width = source.shape[:2]
    src = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
    top_offset = top_shrink * width
    bottom_offset = bottom_shrink * width
    dst = np.float32([
        [top_offset, 0],
        [width - 1 - top_offset, 0],
        [width - 1 - bottom_offset, height - 1],
        [bottom_offset, height - 1],
    ])
    matrix = cv2.getPerspectiveTransform(src, dst)
    result = cv2.warpPerspective(source, matrix, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"top_shrink": top_shrink, "bottom_shrink": bottom_shrink, "width": width, "height": height},
        "analysis": "投影变换使用四点透视映射改变图像平面，可模拟拍摄视角变化或进行透视校正。",
    }
