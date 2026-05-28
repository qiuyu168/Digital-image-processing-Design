# 实现图像负片灰度变换
from __future__ import annotations

import numpy as np

from app.algorithms.common import bool_select_value, gray_metrics, to_bgr, to_gray


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "negative_transform",
    "display_name": "负片变换",
    "description": "将图像亮暗关系反转，可选择保留彩色通道或输出灰度负片。",
    "params": {
        "keep_color": {
            "type": "str",
            "default": "false",
            "label": "保留彩色",
            "component": "select",
            "options": [
                {"label": "输出灰度负片", "value": "false"},
                {"label": "保留彩色负片", "value": "true"},
            ],
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    keep_color = bool_select_value(params, "keep_color", ALGORITHM_META)
    source = to_bgr(image) if keep_color else to_gray(image)
    result = (255 - source).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"keep_color": keep_color, **gray_metrics(source, result)},
        "analysis": "负片变换把每个像素计算为 255 减原值，使亮暗关系完全反转，便于观察隐藏在亮区或暗区的结构。",
    }
