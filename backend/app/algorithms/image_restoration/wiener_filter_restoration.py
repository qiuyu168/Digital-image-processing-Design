# 实现维纳滤波图像复原
from __future__ import annotations

import numpy as np

from app.algorithms.common import gray_metrics, normalize_uint8, slider_value, to_gray, turbulence_transfer


ALGORITHM_META = {
    "module": "image_restoration",
    "name": "wiener_filter_restoration",
    "display_name": "维纳滤波复原",
    "description": "使用维纳滤波在复原高频和抑制噪声之间取得平衡。",
    "params": {
        "k": {"type": "float", "default": 0.002, "min": 0.0001, "max": 0.02, "step": 0.0001, "label": "退化强度", "component": "slider"},
        "noise_power": {"type": "float", "default": 0.01, "min": 0.0001, "max": 1.0, "step": 0.0001, "label": "噪声功率", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    k = slider_value(params, "k", ALGORITHM_META)
    noise_power = slider_value(params, "noise_power", ALGORITHM_META)
    transfer = turbulence_transfer(gray.shape, k)
    spectrum = np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
    restored_spectrum = spectrum * np.conj(transfer) / (np.abs(transfer) ** 2 + noise_power)
    restored = np.real(np.fft.ifft2(np.fft.ifftshift(restored_spectrum)))
    result = normalize_uint8(restored)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"k": k, "noise_power": noise_power, **gray_metrics(gray, result)},
        "analysis": "维纳滤波在退化模型和噪声功率之间折中，比单纯逆滤波更稳定，适合含噪模糊图像的教学复原。",
    }

