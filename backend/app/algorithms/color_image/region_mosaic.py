# 本文件用于实现指定区域图像马赛克处理
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, int_slider_value, slider_value, to_bgr


ALGORITHM_META = {
    "module": "color_image",
    "name": "region_mosaic",
    "display_name": "指定区域马赛克",
    "description": "对指定相对区域进行像素块化马赛克处理。",
    "params": {
        "x_ratio": {"type": "float", "default": 0.25, "min": 0.0, "max": 1.0, "step": 0.01, "label": "区域左上角X比例", "component": "slider"},
        "y_ratio": {"type": "float", "default": 0.25, "min": 0.0, "max": 1.0, "step": 0.01, "label": "区域左上角Y比例", "component": "slider"},
        "width_ratio": {"type": "float", "default": 0.5, "min": 0.05, "max": 1.0, "step": 0.01, "label": "区域宽度比例", "component": "slider"},
        "height_ratio": {"type": "float", "default": 0.5, "min": 0.05, "max": 1.0, "step": 0.01, "label": "区域高度比例", "component": "slider"},
        "block_size": {"type": "int", "default": 12, "min": 2, "max": 80, "step": 1, "label": "马赛克块大小", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    height, width = source.shape[:2]
    x_ratio = slider_value(params, "x_ratio", ALGORITHM_META)
    y_ratio = slider_value(params, "y_ratio", ALGORITHM_META)
    width_ratio = slider_value(params, "width_ratio", ALGORITHM_META)
    height_ratio = slider_value(params, "height_ratio", ALGORITHM_META)
    block_size = int_slider_value(params, "block_size", ALGORITHM_META)
    x1 = min(width - 1, int(round(x_ratio * width)))
    y1 = min(height - 1, int(round(y_ratio * height)))
    x2 = max(x1 + 1, min(width, x1 + int(round(width_ratio * width))))
    y2 = max(y1 + 1, min(height, y1 + int(round(height_ratio * height))))
    result = source.copy()
    region = result[y1:y2, x1:x2]
    small_w = max(1, region.shape[1] // block_size)
    small_h = max(1, region.shape[0] // block_size)
    small = cv2.resize(region, (small_w, small_h), interpolation=cv2.INTER_LINEAR)
    result[y1:y2, x1:x2] = cv2.resize(small, (region.shape[1], region.shape[0]), interpolation=cv2.INTER_NEAREST)
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "block_size": block_size, **gray_metrics(source, result)},
        "analysis": "区域马赛克通过降低局部区域采样分辨率并最近邻放大，能够遮挡敏感区域或演示空间采样退化效果。",
    }

