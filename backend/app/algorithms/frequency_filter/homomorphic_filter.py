# 本文件用于实现同态滤波器
from __future__ import annotations

import numpy as np

from app.algorithms.common import distance_grid, gray_metrics, normalize_uint8, slider_value, to_gray


ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "homomorphic_filter",
    "display_name": "同态滤波",
    "description": "在对数域抑制低频照明并增强高频反射细节。",
    "params": {
        "gamma_low": {"type": "float", "default": 0.5, "min": 0.1, "max": 2.0, "step": 0.1, "label": "低频增益", "component": "slider"},
        "gamma_high": {"type": "float", "default": 1.8, "min": 0.5, "max": 5.0, "step": 0.1, "label": "高频增益", "component": "slider"},
        "cutoff": {"type": "float", "default": 30.0, "min": 1.0, "max": 300.0, "step": 1.0, "label": "截止频率", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    gamma_low = slider_value(params, "gamma_low", ALGORITHM_META)
    gamma_high = slider_value(params, "gamma_high", ALGORITHM_META)
    cutoff = slider_value(params, "cutoff", ALGORITHM_META)
    log_image = np.log1p(gray.astype(np.float32))
    spectrum = np.fft.fftshift(np.fft.fft2(log_image))
    distance = distance_grid(gray.shape)
    high_pass = 1.0 - np.exp(-(distance ** 2) / (2.0 * cutoff * cutoff))
    transfer = (gamma_high - gamma_low) * high_pass + gamma_low
    filtered = np.real(np.fft.ifft2(np.fft.ifftshift(spectrum * transfer)))
    result = normalize_uint8(np.expm1(filtered))
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"gamma_low": gamma_low, "gamma_high": gamma_high, "cutoff": cutoff, **gray_metrics(gray, result)},
        "analysis": "同态滤波把图像分解为照明和反射成分，在对数频域削弱缓慢变化照明并增强细节反射，可改善光照不均。",
    }
