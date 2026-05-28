# 实现逆滤波图像复原
from __future__ import annotations

import numpy as np

from app.algorithms.common import gray_metrics, normalize_uint8, slider_value, to_gray, turbulence_transfer


ALGORITHM_META = {
    "module": "image_restoration",
    "name": "inverse_filter_restoration",
    "display_name": "逆滤波复原",
    "description": "基于退化函数的频域逆滤波复原，带 epsilon 防止除零。",
    "params": {
        "k": {"type": "float", "default": 0.002, "min": 0.0001, "max": 0.02, "step": 0.0001, "label": "退化强度", "component": "slider"},
        "epsilon": {"type": "float", "default": 0.05, "min": 0.001, "max": 1.0, "step": 0.001, "label": "稳定阈值", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    k = slider_value(params, "k", ALGORITHM_META)
    epsilon = slider_value(params, "epsilon", ALGORITHM_META)
    transfer = turbulence_transfer(gray.shape, k)
    safe_transfer = np.where(np.abs(transfer) < epsilon, epsilon, transfer)
    spectrum = np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
    restored = np.real(np.fft.ifft2(np.fft.ifftshift(spectrum / safe_transfer)))
    result = normalize_uint8(restored)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"k": k, "epsilon": epsilon, **gray_metrics(gray, result)},
        "analysis": "逆滤波尝试用退化函数的倒数恢复高频信息；epsilon 限制过小分母，避免噪声和数值误差被无限放大。",
    }

