# 本文件用于实现直方图均衡化增强图像对比度的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "histogram_equalization",
    "display_name": "直方图均衡化",
    "description": "重新分配灰度级分布，提高低对比图像的整体明暗层次。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    _ = params or {}

    gray = _to_gray(_ensure_uint8(image))
    result = cv2.equalizeHist(gray)

    return {
        "result": result,
        "steps": [
            {"name": "灰度图像", "image": gray},
            {"name": "均衡化结果", "image": result},
        ],
        "metrics": {
            "std_before": round(float(np.std(gray)), 2),
            "std_after": round(float(np.std(result)), 2),
            "mean_before": round(float(np.mean(gray)), 2),
            "mean_after": round(float(np.mean(result)), 2),
        },
        "analysis": "已对灰度直方图进行均衡化处理，使灰度分布更分散，从而增强图像整体对比度和细节可见性。",
    }


def _to_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return np.ascontiguousarray(image)
    if image.ndim != 3:
        raise ValueError("输入图像必须是二维灰度图或三维彩色图")
    if image.shape[2] == 1:
        return np.ascontiguousarray(image[:, :, 0])
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2GRAY)


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.asarray(image)
    if array.size == 0:
        raise ValueError("输入图像不能为空数组")
    if array.dtype == np.uint8:
        return np.ascontiguousarray(array)
    array = np.nan_to_num(array.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    if 0.0 <= float(np.min(array)) and float(np.max(array)) <= 1.0:
        array = array * 255.0
    return np.ascontiguousarray(np.clip(array, 0, 255).astype(np.uint8))
