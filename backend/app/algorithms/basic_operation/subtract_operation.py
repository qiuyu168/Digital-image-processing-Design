# 实现两张图像的减法差异运算
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, require_second_image, resize_like, slider_value, to_bgr


ALGORITHM_META = {
    "module": "basic_operation",
    "name": "subtract_operation",
    "display_name": "减法运算",
    "description": "计算第一张图像减去第二张图像后的像素差异。",
    "params": {
        "scale": {"type": "float", "default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1, "label": "差异放大系数", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    first = to_bgr(image)
    second = resize_like(to_bgr(require_second_image(params)), first)
    scale = slider_value(params, "scale", ALGORITHM_META)
    result = clip_uint8((first.astype(np.float32) - second.astype(np.float32)) * scale)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": first}, {"name": "处理结果", "image": result}],
        "metrics": {"scale": scale, **gray_metrics(first, result)},
        "analysis": "减法运算突出两张图像之间的像素差异，常用于变化检测；负值已按显示范围裁剪。",
    }

