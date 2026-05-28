# 本文件用于实现频域拉普拉斯图像锐化
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, laplacian_transfer, slider_value, to_gray


ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "frequency_laplacian_sharpen",
    "display_name": "频域拉普拉斯锐化",
    "description": "在频域使用拉普拉斯算子增强高频边缘。",
    "params": {
        "amount": {"type": "float", "default": 0.8, "min": 0.0, "max": 5.0, "step": 0.1, "label": "锐化强度", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    amount = slider_value(params, "amount", ALGORITHM_META)
    spectrum = np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
    laplacian = laplacian_transfer(gray.shape)
    detail = np.real(np.fft.ifft2(np.fft.ifftshift(spectrum * laplacian)))
    result = clip_uint8(gray.astype(np.float32) - amount * detail)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"amount": amount, **gray_metrics(gray, result)},
        "analysis": "频域拉普拉斯锐化通过增强二阶导数对应的高频成分突出边缘，与空间域拉普拉斯锐化等价但便于观察频域机制。",
    }

