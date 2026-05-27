# 本文件用于实现将彩色图像转换为灰度图像的功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "grayscale",
    "display_name": "灰度化",
    "description": "将 BGR 彩色图像转换为单通道灰度图，作为二值化、边缘检测和频域分析的基础输入。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    _ = params or {}

    original = _ensure_uint8(image)
    gray = _to_gray(original)

    return {
        "result": gray,
        "steps": [
            {"name": "原始图像", "image": original},
            {"name": "灰度图像", "image": gray},
        ],
        "metrics": {
            "width": int(gray.shape[1]),
            "height": int(gray.shape[0]),
            "mean_gray": round(float(np.mean(gray)), 2),
            "std_gray": round(float(np.std(gray)), 2),
        },
        "analysis": "已将输入图像转换为灰度图，保留亮度结构并去除颜色信息，适合继续进行阈值分割和边缘分析。",
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
