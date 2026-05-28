# 本文件用于实现锐化掩膜图像锐化
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, slider_value, to_bgr


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "unsharp_masking",
    "display_name": "锐化掩膜",
    "description": "通过原图减去模糊图获得高频掩膜并叠加回原图。",
    "params": {
        "amount": {"type": "float", "default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1, "label": "锐化强度", "component": "slider"},
        "sigma": {"type": "float", "default": 1.2, "min": 0.1, "max": 10.0, "step": 0.1, "label": "模糊标准差", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    amount = slider_value(params, "amount", ALGORITHM_META)
    sigma = slider_value(params, "sigma", ALGORITHM_META)
    blurred = cv2.GaussianBlur(source, (0, 0), sigma)
    result = clip_uint8(source.astype(np.float32) + amount * (source.astype(np.float32) - blurred.astype(np.float32)))
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "模糊掩膜", "image": blurred}, {"name": "处理结果", "image": result}],
        "metrics": {"amount": amount, "sigma": sigma, **gray_metrics(source, result)},
        "analysis": "锐化掩膜提取原图与模糊图之间的高频差异，再按强度叠加回原图，从而增强边缘和纹理细节。",
    }

