# 实现镜头离焦模糊退化模拟
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, int_slider_value, to_bgr


ALGORITHM_META = {
    "module": "image_restoration",
    "name": "defocus_blur_simulation",
    "display_name": "镜头聚焦失真模糊",
    "description": "使用圆盘点扩散函数模拟镜头离焦造成的均匀模糊。",
    "params": {
        "radius": {"type": "int", "default": 8, "min": 1, "max": 40, "step": 1, "label": "离焦半径", "component": "slider"},
    },
}


def _disk_kernel(radius: int) -> np.ndarray:
    size = radius * 2 + 1
    y, x = np.ogrid[:size, :size]
    center = radius
    mask = (x - center) ** 2 + (y - center) ** 2 <= radius ** 2
    kernel = np.zeros((size, size), dtype=np.float32)
    kernel[mask] = 1.0
    kernel /= max(float(np.sum(kernel)), 1.0)
    return kernel


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    radius = int_slider_value(params, "radius", ALGORITHM_META)
    kernel = _disk_kernel(radius)
    result = cv2.filter2D(source, -1, kernel, borderType=cv2.BORDER_REFLECT).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"radius": radius, "kernel_size": int(kernel.shape[0]), **gray_metrics(source, result)},
        "analysis": "离焦模糊使用圆盘形点扩散函数平均邻域像素，半径越大，高频细节和边缘越明显被削弱。",
    }

