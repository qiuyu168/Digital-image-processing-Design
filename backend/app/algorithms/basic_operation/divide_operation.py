# 实现两张图像的除法归一化运算
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, require_second_image, resize_like, slider_value, to_bgr


ALGORITHM_META = {
    "module": "basic_operation",
    "name": "divide_operation",
    "display_name": "除法运算",
    "description": "用第一张图像除以第二张图像，带 epsilon 防止除零。",
    "params": {
        "scale": {"type": "float", "default": 128.0, "min": 1.0, "max": 255.0, "step": 1.0, "label": "结果缩放系数", "component": "slider"},
        "epsilon": {"type": "float", "default": 1.0, "min": 0.001, "max": 20.0, "step": 0.001, "label": "除零保护值", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    first = to_bgr(image)
    second = resize_like(to_bgr(require_second_image(params)), first)
    scale = slider_value(params, "scale", ALGORITHM_META)
    epsilon = slider_value(params, "epsilon", ALGORITHM_META)
    result = clip_uint8(first.astype(np.float32) / (second.astype(np.float32) + epsilon) * scale)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": first}, {"name": "处理结果", "image": result}],
        "metrics": {"scale": scale, "epsilon": epsilon, **gray_metrics(first, result)},
        "analysis": "除法运算可用于照度归一化和比例差异观察，epsilon 避免第二张图像出现零值时产生数值异常。",
    }

