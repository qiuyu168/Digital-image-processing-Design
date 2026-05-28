# 实现运动模糊退化模拟
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, int_slider_value, slider_value, to_bgr


ALGORITHM_META = {
    "module": "image_restoration",
    "name": "motion_blur_simulation",
    "display_name": "运动模糊模拟",
    "description": "使用指定长度和角度的线性点扩散函数模拟相机或目标运动。",
    "params": {
        "length": {"type": "int", "default": 15, "min": 1, "max": 80, "step": 1, "label": "运动长度", "component": "slider"},
        "angle": {"type": "float", "default": 0.0, "min": -180.0, "max": 180.0, "step": 1.0, "label": "运动角度", "component": "slider"},
    },
}


def _motion_kernel(length: int, angle: float) -> np.ndarray:
    length = max(1, int(length))
    kernel = np.zeros((length, length), dtype=np.float32)
    kernel[length // 2, :] = 1.0
    matrix = cv2.getRotationMatrix2D((length / 2 - 0.5, length / 2 - 0.5), angle, 1.0)
    kernel = cv2.warpAffine(kernel, matrix, (length, length), flags=cv2.INTER_LINEAR)
    kernel /= max(float(np.sum(kernel)), 1.0)
    return kernel


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    length = int_slider_value(params, "length", ALGORITHM_META)
    angle = slider_value(params, "angle", ALGORITHM_META)
    kernel = _motion_kernel(length, angle)
    result = cv2.filter2D(source, -1, kernel, borderType=cv2.BORDER_REFLECT).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"length": length, "angle": angle, **gray_metrics(source, result)},
        "analysis": "运动模糊沿指定角度扩散像素能量，长度越大拖影越明显，用于模拟拍摄抖动或目标快速移动。",
    }

