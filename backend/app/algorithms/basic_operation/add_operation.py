# 实现两张图像的加法融合运算
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import (
    clip_uint8,
    gray_metrics,
    require_second_image,
    resize_like,
    slider_value,
    to_bgr,
)


ALGORITHM_META = {
    "module": "basic_operation",
    "name": "add_operation",
    "display_name": "加法运算",
    "description": "按 alpha、beta 和 gamma 对两张图像进行加权加法融合。",
    "params": {
        "alpha": {"type": "float", "default": 1.0, "min": 0.0, "max": 3.0, "step": 0.1, "label": "第一图像权重", "component": "slider"},
        "beta": {"type": "float", "default": 1.0, "min": 0.0, "max": 3.0, "step": 0.1, "label": "第二图像权重", "component": "slider"},
        "gamma": {"type": "float", "default": 0.0, "min": -255.0, "max": 255.0, "step": 1.0, "label": "亮度偏移", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    first = to_bgr(image)
    second = resize_like(to_bgr(require_second_image(params)), first)
    alpha = slider_value(params, "alpha", ALGORITHM_META)
    beta = slider_value(params, "beta", ALGORITHM_META)
    gamma = slider_value(params, "gamma", ALGORITHM_META)
    result = cv2.addWeighted(first, alpha, second, beta, gamma)
    result = clip_uint8(result)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": first}, {"name": "处理结果", "image": result}],
        "metrics": {"alpha": alpha, "beta": beta, "gamma": gamma, **gray_metrics(first, result)},
        "analysis": "加法运算把两张图像的像素亮度叠加，可用于图像融合和整体增亮；结果已裁剪到 0-255 的 uint8 显示范围。",
    }

