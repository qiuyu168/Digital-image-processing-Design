# 实现约束最小二乘滤波图像复原
from __future__ import annotations

import numpy as np

from app.algorithms.common import (
    gray_metrics,
    laplacian_transfer,
    normalize_uint8,
    slider_value,
    to_gray,
    turbulence_transfer,
)


ALGORITHM_META = {
    "module": "image_restoration",
    "name": "constrained_least_squares_restoration",
    "display_name": "约束最小二乘滤波图像复原",
    "description": "使用拉普拉斯平滑约束的频域复原，降低逆滤波噪声放大。",
    "params": {
        "k": {"type": "float", "default": 0.002, "min": 0.0001, "max": 0.02, "step": 0.0001, "label": "退化强度", "component": "slider"},
        "gamma": {"type": "float", "default": 0.01, "min": 0.0001, "max": 1.0, "step": 0.0001, "label": "约束系数", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    k = slider_value(params, "k", ALGORITHM_META)
    gamma = slider_value(params, "gamma", ALGORITHM_META)
    transfer = turbulence_transfer(gray.shape, k)
    laplacian = laplacian_transfer(gray.shape)
    spectrum = np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
    denominator = np.abs(transfer) ** 2 + gamma * (np.abs(laplacian) ** 2) + 1e-6
    restored_spectrum = spectrum * np.conj(transfer) / denominator
    restored = np.real(np.fft.ifft2(np.fft.ifftshift(restored_spectrum)))
    result = normalize_uint8(restored)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"k": k, "gamma": gamma, **gray_metrics(gray, result)},
        "analysis": "约束最小二乘复原在反退化同时加入拉普拉斯平滑约束，可抑制噪声放大并保持较稳定的边缘复原效果。",
    }
