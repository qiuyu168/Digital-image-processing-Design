# 本文件用于实现最大值滤波
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, odd_int_slider_value, to_bgr


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "max_filter",
    "display_name": "最大值滤波",
    "description": "用邻域最大值替代中心像素，增强亮区域并扩展高亮结构。",
    "params": {
        "kernel_size": {"type": "int", "default": 5, "min": 1, "max": 31, "step": 2, "label": "滤波窗口大小", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    kernel_size = odd_int_slider_value(params, "kernel_size", ALGORITHM_META)
    result = cv2.dilate(source, np.ones((kernel_size, kernel_size), dtype=np.uint8)).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"kernel_size": kernel_size, **gray_metrics(source, result)},
        "analysis": "最大值滤波输出邻域内最大灰度，能扩张亮细节，对暗噪声有一定抑制作用。",
    }

