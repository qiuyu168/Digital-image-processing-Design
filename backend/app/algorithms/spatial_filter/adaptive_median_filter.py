# 本文件用于实现自适应中值滤波
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, odd_int_slider_value, to_bgr


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "adaptive_median_filter",
    "display_name": "自适应中值滤波",
    "description": "根据最大窗口限制进行中值滤波，适合演示椒盐噪声抑制。",
    "params": {
        "max_kernel_size": {"type": "int", "default": 7, "min": 3, "max": 31, "step": 2, "label": "最大窗口大小", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    max_kernel_size = odd_int_slider_value(params, "max_kernel_size", ALGORITHM_META)
    small = cv2.medianBlur(source, 3)
    result = cv2.medianBlur(small, max_kernel_size).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"max_kernel_size": max_kernel_size, **gray_metrics(source, result)},
        "analysis": "自适应中值滤波通过较小和较大窗口组合抑制脉冲噪声，在保留边缘与平滑噪声之间取得折中。",
    }

