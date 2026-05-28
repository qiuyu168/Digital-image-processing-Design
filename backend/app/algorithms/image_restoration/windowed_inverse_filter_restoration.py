# 本文件用于实现加窗逆滤波图像复原
from __future__ import annotations

import numpy as np

from app.algorithms.common import distance_grid, gray_metrics, normalize_uint8, slider_value, to_gray, turbulence_transfer


ALGORITHM_META = {
    "module": "image_restoration",
    "name": "windowed_inverse_filter_restoration",
    "display_name": "加窗逆滤波复原",
    "description": "在逆滤波基础上加入频域窗口，限制高频噪声放大。",
    "params": {
        "k": {"type": "float", "default": 0.002, "min": 0.0001, "max": 0.02, "step": 0.0001, "label": "退化强度", "component": "slider"},
        "epsilon": {"type": "float", "default": 0.05, "min": 0.001, "max": 1.0, "step": 0.001, "label": "稳定阈值", "component": "slider"},
        "window_radius": {"type": "float", "default": 80.0, "min": 5.0, "max": 300.0, "step": 1.0, "label": "窗口半径", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    k = slider_value(params, "k", ALGORITHM_META)
    epsilon = slider_value(params, "epsilon", ALGORITHM_META)
    window_radius = slider_value(params, "window_radius", ALGORITHM_META)
    transfer = turbulence_transfer(gray.shape, k)
    safe_transfer = np.where(np.abs(transfer) < epsilon, epsilon, transfer)
    distance = distance_grid(gray.shape)
    window = np.exp(-(distance ** 2) / (2.0 * window_radius * window_radius))
    spectrum = np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
    restored = np.real(np.fft.ifft2(np.fft.ifftshift((spectrum / safe_transfer) * window)))
    result = normalize_uint8(restored)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"k": k, "epsilon": epsilon, "window_radius": window_radius, **gray_metrics(gray, result)},
        "analysis": "加窗逆滤波在反退化时用频域窗口限制高频增益，比直接逆滤波更能抑制噪声放大和振铃。",
    }
