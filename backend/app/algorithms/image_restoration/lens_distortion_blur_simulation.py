# 实现镜头畸变叠加模糊退化模拟
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, odd_int_slider_value, slider_value, to_bgr


ALGORITHM_META = {
    "module": "image_restoration",
    "name": "lens_distortion_blur_simulation",
    "display_name": "镜头畸变失真模糊",
    "description": "使用径向重映射和高斯模糊模拟镜头畸变退化。",
    "params": {
        "distortion_strength": {"type": "float", "default": 0.25, "min": -0.8, "max": 0.8, "step": 0.01, "label": "畸变强度", "component": "slider"},
        "blur_kernel_size": {"type": "int", "default": 5, "min": 1, "max": 31, "step": 2, "label": "模糊核大小", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    strength = slider_value(params, "distortion_strength", ALGORITHM_META)
    kernel_size = odd_int_slider_value(params, "blur_kernel_size", ALGORITHM_META)
    height, width = source.shape[:2]
    x = np.linspace(-1.0, 1.0, width, dtype=np.float32)
    y = np.linspace(-1.0, 1.0, height, dtype=np.float32)
    grid_x, grid_y = np.meshgrid(x, y)
    radius2 = grid_x * grid_x + grid_y * grid_y
    factor = 1.0 + strength * radius2
    map_x = ((grid_x * factor + 1.0) * 0.5 * (width - 1)).astype(np.float32)
    map_y = ((grid_y * factor + 1.0) * 0.5 * (height - 1)).astype(np.float32)
    distorted = cv2.remap(source, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    result = cv2.GaussianBlur(distorted, (kernel_size, kernel_size), 0).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"distortion_strength": strength, "blur_kernel_size": kernel_size, **gray_metrics(source, result)},
        "analysis": "镜头畸变会使图像边缘产生径向拉伸或压缩，再叠加平滑模糊后能模拟低质量镜头带来的失真退化。",
    }

