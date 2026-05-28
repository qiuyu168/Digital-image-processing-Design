# 实现大气湍流频域模糊模拟
from __future__ import annotations

import numpy as np

from app.algorithms.common import gray_metrics, normalize_uint8, slider_value, to_bgr, turbulence_transfer


ALGORITHM_META = {
    "module": "image_restoration",
    "name": "atmospheric_turbulence_blur_simulation",
    "display_name": "大气湍流模糊模拟",
    "description": "在频域使用大气湍流传递函数衰减高频信息。",
    "params": {
        "k": {"type": "float", "default": 0.002, "min": 0.0001, "max": 0.02, "step": 0.0001, "label": "湍流强度", "component": "slider"},
    },
}


def _filter_channel(channel: np.ndarray, transfer: np.ndarray) -> np.ndarray:
    """Apply the turbulence transfer function to one 2D channel.

    np.fft.fft2 uses the last two axes by default.  The old code passed
    H x W x 1 arrays produced by np.dsplit(), so fft2 was accidentally
    applied on the W x 1 axes instead of the H x W image plane.  For
    non-square images this caused shape-broadcast errors and returned
    400 Bad Request; for square images it could even expand to a huge
    intermediate array.  Keeping every channel strictly 2D avoids both
    problems.
    """
    if channel.ndim != 2:
        channel = np.squeeze(channel)
    if channel.ndim != 2:
        raise ValueError("大气湍流模糊模拟仅支持二维单通道滤波")

    spectrum = np.fft.fftshift(np.fft.fft2(channel.astype(np.float32)))
    restored = np.fft.ifft2(np.fft.ifftshift(spectrum * transfer))
    return normalize_uint8(np.real(restored))


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    k = slider_value(params, "k", ALGORITHM_META)
    transfer = turbulence_transfer(source.shape[:2], k)
    channels = [_filter_channel(channel, transfer) for channel in np.rollaxis(source, 2)]
    result = np.dstack(channels).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"k": k, "transfer_mean": round(float(np.mean(transfer)), 6), **gray_metrics(source, result)},
        "analysis": "大气湍流模型在频域按距离衰减高频成分，k 越大细节越模糊，适合教学演示远距离成像退化。",
    }

