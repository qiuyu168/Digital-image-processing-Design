# 本文件用于实现频谱中心化显示算法。
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "frequency_analysis",
    "name": "spectrum_shift",
    "display_name": "频谱中心化",
    "description": "对傅里叶频谱进行中心化，将低频成分移动到频谱中心。",
    "params": {},
}


def _to_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image.astype(np.float32)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)


def _normalize_spectrum(values: np.ndarray) -> np.ndarray:
    spectrum = np.log1p(np.abs(values))
    return cv2.normalize(spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口。"""
    if image is None:
        raise ValueError("输入图像不能为空")
    if params is None:
        params = {}

    gray = _to_gray(image)
    dft = np.fft.fft2(gray)
    unshifted = _normalize_spectrum(dft)
    shifted = np.fft.fftshift(dft)
    shifted_spectrum = _normalize_spectrum(shifted)

    center_y, center_x = shifted_spectrum.shape[0] // 2, shifted_spectrum.shape[1] // 2

    return {
        "result": shifted_spectrum,
        "steps": [
            {"name": "灰度化", "image": gray.astype(np.uint8)},
            {"name": "原始频谱", "image": unshifted},
            {"name": "中心化频谱", "image": shifted_spectrum},
        ],
        "metrics": {
            "center_magnitude": int(shifted_spectrum[center_y, center_x]),
            "max_magnitude": int(shifted_spectrum.max()),
            "min_magnitude": int(shifted_spectrum.min()),
        },
        "analysis": "频谱中心化将低频信息移动到图像中心，便于观察图像频域能量分布。",
    }
