# 实现两张图像的乘法增强运算
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, require_second_image, resize_like, slider_value, to_bgr


ALGORITHM_META = {
    "module": "basic_operation",
    "name": "multiply_operation",
    "display_name": "乘法运算",
    "description": "将两张图像归一化相乘，用第二张图像调制第一张图像亮度。",
    "params": {
        "scale": {"type": "float", "default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1, "label": "乘法缩放系数", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    first = to_bgr(image)
    second = resize_like(to_bgr(require_second_image(params)), first)
    scale = slider_value(params, "scale", ALGORITHM_META)
    result = clip_uint8((first.astype(np.float32) * second.astype(np.float32) / 255.0) * scale)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": first}, {"name": "处理结果", "image": result}],
        "metrics": {"scale": scale, **gray_metrics(first, result)},
        "analysis": "乘法运算会按照第二张图像的亮度分布调制第一张图像，暗区域被压低，亮区域保留更多细节。",
    }

