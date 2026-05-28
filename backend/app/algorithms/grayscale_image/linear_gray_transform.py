# 实现图像线性灰度变换
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, slider_value, to_gray


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "linear_gray_transform",
    "display_name": "线性灰度变换",
    "description": "对灰度图执行 g = alpha * f + beta 的线性亮度和对比度调整。",
    "params": {
        "alpha": {"type": "float", "default": 1.0, "min": 0.0, "max": 3.0, "step": 0.1, "label": "对比度系数", "component": "slider"},
        "beta": {"type": "float", "default": 0.0, "min": -255.0, "max": 255.0, "step": 1.0, "label": "亮度偏移", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    alpha = slider_value(params, "alpha", ALGORITHM_META)
    beta = slider_value(params, "beta", ALGORITHM_META)
    result = clip_uint8(gray.astype(np.float32) * alpha + beta)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"alpha": alpha, "beta": beta, **gray_metrics(gray, result)},
        "analysis": "线性灰度变换通过 alpha 改变对比度、通过 beta 改变整体亮度，适合做基础灰度范围调整。",
    }
