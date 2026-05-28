# 实现图像伽马校正灰度变换
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, slider_value, to_gray


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "gamma_correction",
    "display_name": "伽马校正",
    "description": "对归一化灰度执行幂律变换，调整暗部或亮部细节。",
    "params": {
        "gamma": {"type": "float", "default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1, "label": "伽马值", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    gamma = slider_value(params, "gamma", ALGORITHM_META)
    normalized = gray.astype(np.float32) / 255.0
    result = clip_uint8(np.power(normalized, gamma) * 255.0)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"gamma": gamma, **gray_metrics(gray, result)},
        "analysis": "伽马校正是非线性灰度变换，gamma 小于 1 时提升暗部，gamma 大于 1 时压暗亮度并增强高亮层次。",
    }
