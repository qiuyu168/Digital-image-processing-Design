# 实现图像对数灰度变换
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, slider_value, to_gray


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "log_transform",
    "display_name": "对数变换",
    "description": "使用对数函数扩展暗部灰度并压缩高亮区域。",
    "params": {
        "gain": {"type": "float", "default": 1.0, "min": 0.1, "max": 5.0, "step": 0.1, "label": "增益系数", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    gain = slider_value(params, "gain", ALGORITHM_META)
    result = clip_uint8(gain * np.log1p(gray.astype(np.float32)) / np.log(256.0) * 255.0)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"gain": gain, **gray_metrics(gray, result)},
        "analysis": "对数变换会放大低灰度区域的差别并压缩高灰度区域，常用于显示暗部细节较多的图像。",
    }
