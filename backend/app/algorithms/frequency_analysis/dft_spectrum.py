# 本文件用于实现傅里叶变换并显示频谱图的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "frequency_analysis",
    "name": "dft_spectrum",
    "display_name": "傅里叶频谱",
    "description": "将图像转换到频域并显示频谱图，用于观察图像低频和高频信息分布。",
    "params": {},
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


def _spectrum_display(values: np.ndarray) -> np.ndarray:
    magnitude = np.log1p(np.abs(values))
    if float(np.max(magnitude)) == float(np.min(magnitude)):
        return np.zeros(magnitude.shape, dtype=np.uint8)
    return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    gray = _to_gray(image)
    dft = np.fft.fft2(gray.astype(np.float32))
    raw_spectrum = _spectrum_display(dft)
    shifted = np.fft.fftshift(dft)
    shifted_spectrum = _spectrum_display(shifted)
    center_y, center_x = shifted_spectrum.shape[0] // 2, shifted_spectrum.shape[1] // 2

    return {
        "result": shifted_spectrum,
        "steps": [
            {"name": "灰度图像", "image": gray},
            {"name": "原始频谱", "image": raw_spectrum},
            {"name": "中心化频谱", "image": shifted_spectrum},
        ],
        "metrics": {
            "height": int(gray.shape[0]),
            "width": int(gray.shape[1]),
            "center_magnitude": int(shifted_spectrum[center_y, center_x]),
            "max_magnitude": int(shifted_spectrum.max()),
        },
        "analysis": "傅里叶频谱把图像分解为不同频率成分，中心化后低频能量位于图像中心，高频细节分布在远离中心的位置。",
    }
