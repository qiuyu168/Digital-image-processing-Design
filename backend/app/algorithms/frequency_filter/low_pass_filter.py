# 本文件用于实现频域低通滤波的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "low_pass_filter",
    "display_name": "低通滤波",
    "description": "保留低频信息，抑制高频信息，实现图像平滑和降噪。",
    "params": {
        "radius": {
            "type": "int",
            "default": 30,
            "min": 1,
            "max": 300,
            "step": 1,
            "label": "频域滤波半径",
            "component": "slider",
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


def _normalize_uint8(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float32)
    if float(np.max(values)) == float(np.min(values)):
        return np.zeros(values.shape, dtype=np.uint8)
    return cv2.normalize(values, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def _radius(params: dict, image_shape: tuple[int, int]) -> int:
    limit = max(1, min(image_shape) // 2)
    value = int(params.get("radius", 30))
    return max(1, min(300, limit, value))


def _distance_grid(shape: tuple[int, int]) -> np.ndarray:
    rows, cols = shape
    y, x = np.ogrid[:rows, :cols]
    return np.sqrt((y - rows // 2) ** 2 + (x - cols // 2) ** 2)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    gray = _to_gray(image)
    radius = _radius(params, gray.shape)
    shifted = np.fft.fftshift(np.fft.fft2(gray.astype(np.float32)))
    distance = _distance_grid(gray.shape)
    mask = np.exp(-(distance ** 2) / (2 * float(radius ** 2)))
    filtered = shifted * mask
    result_float = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered)))
    result = _normalize_uint8(result_float)
    spectrum = _normalize_uint8(np.log1p(np.abs(shifted)))
    mask_display = _normalize_uint8(mask)

    return {
        "result": result,
        "steps": [
            {"name": "灰度图像", "image": gray},
            {"name": "中心化频谱", "image": spectrum},
            {"name": "低通掩膜", "image": mask_display},
            {"name": "低通滤波结果", "image": result},
        ],
        "metrics": {
            "radius": radius,
            "mask_mean": float(np.mean(mask)),
            "std_before": float(np.std(gray)),
            "std_after": float(np.std(result)),
        },
        "analysis": "低通滤波保留靠近频谱中心的低频成分，能够削弱噪声和细碎纹理，使图像整体更平滑。",
    }
