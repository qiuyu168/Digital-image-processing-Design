# 本文件用于实现高斯滤波平滑图像的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "gaussian_filter",
    "display_name": "高斯滤波",
    "description": "使用高斯核进行加权平滑，适合去除一般噪声并保留较自然的过渡。",
    "params": {
        "kernel_size": {
            "type": "odd_int",
            "default": 5,
            "min": 1,
            "max": 31,
            "step": 2,
            "label": "滤波核大小",
            "component": "slider",
        },
        "sigma": {
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 10.0,
            "step": 0.1,
            "label": "高斯标准差",
            "component": "slider",
        },
    },
}


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.ascontiguousarray(image)
    if array.dtype == np.uint8:
        return array.copy()
    return cv2.normalize(array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def _odd_param(params: dict, name: str, default: int, minimum: int, maximum: int) -> int:
    value = int(params.get(name, default))
    value = max(minimum, min(maximum, value))
    if value % 2 == 0:
        value += 1 if value < maximum else -1
    return max(minimum, value)


def _float_param(params: dict, name: str, default: float, minimum: float, maximum: float) -> float:
    value = float(params.get(name, default))
    return max(minimum, min(maximum, value))


def _gray_for_metrics(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    source = _ensure_uint8(image)
    kernel_size = _odd_param(params, "kernel_size", 5, 1, 31)
    sigma = _float_param(params, "sigma", 1.0, 0.0, 10.0)
    result = cv2.GaussianBlur(source, (kernel_size, kernel_size), sigmaX=sigma, sigmaY=sigma)
    gray_source = _gray_for_metrics(source)
    gray_result = _gray_for_metrics(result)

    return {
        "result": result.astype(np.uint8),
        "steps": [
            {"name": "原始图像", "image": source},
            {"name": f"{kernel_size}x{kernel_size} 高斯滤波", "image": result},
        ],
        "metrics": {
            "kernel_size": kernel_size,
            "sigma": sigma,
            "std_before": float(np.std(gray_source)),
            "std_after": float(np.std(gray_result)),
            "mean_abs_change": float(np.mean(np.abs(gray_source.astype(np.float32) - gray_result.astype(np.float32)))),
        },
        "analysis": "高斯滤波对中心像素附近赋予更高权重，能以较自然的方式降低噪声和纹理抖动，边缘损失通常小于同尺寸均值滤波。",
    }
