# 本文件用于实现巴特沃斯低通滤波
from __future__ import annotations

import numpy as np

from app.algorithms.common import distance_grid, gray_metrics, int_slider_value, normalize_uint8, to_gray


ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "butterworth_low_pass",
    "display_name": "巴特沃斯低通滤波",
    "description": "使用巴特沃斯低通传递函数保留低频并平滑高频细节。",
    "params": {
        "cutoff": {"type": "int", "default": 30, "min": 1, "max": 300, "step": 1, "label": "截止频率", "component": "slider"},
        "order": {"type": "int", "default": 2, "min": 1, "max": 10, "step": 1, "label": "滤波阶数", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    cutoff = int_slider_value(params, "cutoff", ALGORITHM_META)
    order = int_slider_value(params, "order", ALGORITHM_META)
    distance = distance_grid(gray.shape)
    transfer = 1.0 / (1.0 + (distance / max(cutoff, 1)) ** (2 * order))
    spectrum = np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
    result = normalize_uint8(np.real(np.fft.ifft2(np.fft.ifftshift(spectrum * transfer))))
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"cutoff": cutoff, "order": order, "transfer_mean": round(float(np.mean(transfer)), 6), **gray_metrics(gray, result)},
        "analysis": "巴特沃斯低通滤波相较理想低通过渡更平滑，可减少振铃并实现频域平滑。",
    }

