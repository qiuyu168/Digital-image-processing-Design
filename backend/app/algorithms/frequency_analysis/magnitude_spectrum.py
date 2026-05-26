# 本文件用于实现傅里叶幅度谱显示算法
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "frequency_analysis",
    "name": "magnitude_spectrum",
    "display_name": "幅度谱显示",
    "description": "计算并显示图像傅里叶变换后的幅度谱。",
    "params": {
        "shift_center": {
            "type": "bool",
            "default": True,
            "label": "频谱中心化",
            "component": "switch",
        },
    },
}


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.ascontiguousarray(image)
    if array.dtype == np.uint8:
        return array.copy()
    return cv2.normalize(array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def _to_gray(image: np.ndarray) -> np.ndarray:
    source = _ensure_uint8(image)
    if source.ndim == 2:
        return source
    if source.shape[2] == 4:
        return cv2.cvtColor(source, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)


def _normalize_spectrum(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    magnitude = 20 * np.log1p(np.abs(values))
    if float(np.max(magnitude)) == float(np.min(magnitude)):
        return np.zeros(magnitude.shape, dtype=np.uint8), magnitude
    return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8), magnitude


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    shift_center = bool(params.get("shift_center", True))
    gray = _to_gray(image)
    dft = np.fft.fft2(gray.astype(np.float32))
    spectrum_source = np.fft.fftshift(dft) if shift_center else dft
    magnitude_spectrum, magnitude = _normalize_spectrum(spectrum_source)

    return {
        "result": magnitude_spectrum,
        "steps": [
            {"name": "灰度图像", "image": gray},
            {"name": "幅度谱", "image": magnitude_spectrum},
        ],
        "metrics": {
            "shift_center": shift_center,
            "max_magnitude": float(np.max(magnitude)),
            "mean_magnitude": float(np.mean(magnitude)),
        },
        "analysis": "幅度谱展示不同频率上的能量强弱，亮区域表示该频率成分更集中，中心化显示便于观察低频和高频的相对位置。",
    }
