# 实现图像指数灰度变换
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, slider_value, to_gray


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "exponential_transform",
    "display_name": "指数变换",
    "description": "使用指数函数增强高灰度区域并压缩低灰度区域。",
    "params": {
        "gain": {"type": "float", "default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1, "label": "增益系数", "component": "slider"},
        "base": {"type": "float", "default": 2.0, "min": 1.01, "max": 10.0, "step": 0.01, "label": "指数底数", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    gain = slider_value(params, "gain", ALGORITHM_META)
    base = slider_value(params, "base", ALGORITHM_META)
    normalized = gray.astype(np.float32) / 255.0
    transformed = (np.power(base, normalized) - 1.0) / (base - 1.0)
    result = clip_uint8(transformed * 255.0 * gain)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"gain": gain, "base": base, **gray_metrics(gray, result)},
        "analysis": "指数变换会更强调较亮区域的变化，同时压缩暗部，适合观察高灰度层次的增强效果。",
    }
