# 本文件用于实现傅里叶幅度谱显示算法。
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "frequency_analysis",
    "name": "magnitude_spectrum",
    "display_name": "幅度谱显示",
    "description": "计算并显示图像傅里叶变换后的幅度谱。",
    "params": {
        "shift_center": {"type": "bool", "default": True, "label": "频谱中心化"},
    },
}


def _to_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image.astype(np.float32)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口。"""
    if image is None:
        raise ValueError("输入图像不能为空")
    if params is None:
        params = {}

    shift_center = bool(params.get("shift_center", True))
    gray = _to_gray(image)
    dft = np.fft.fft2(gray)
    spectrum_source = np.fft.fftshift(dft) if shift_center else dft
    magnitude = 20 * np.log1p(np.abs(spectrum_source))
    magnitude_spectrum = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    return {
        "result": magnitude_spectrum,
        "steps": [
            {"name": "灰度化", "image": gray.astype(np.uint8)},
            {"name": "傅里叶变换", "image": magnitude_spectrum},
        ],
        "metrics": {
            "shift_center": shift_center,
            "max_magnitude": float(np.max(magnitude)),
            "mean_magnitude": float(np.mean(magnitude)),
        },
        "analysis": "幅度谱用于观察图像在不同频率上的能量强弱，亮区域代表频域能量更集中。",
    }
