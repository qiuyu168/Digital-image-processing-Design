# 本文件用于实现图像基础边缘检测算法
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "edge_detection_basic",
    "display_name": "基础边缘检测",
    "description": "使用 Canny 算子提取图像中的主要轮廓、线条和结构边界。",
    "params": {
        "threshold1": {
            "type": "int",
            "default": 80,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "低阈值",
            "component": "slider",
        },
        "threshold2": {
            "type": "int",
            "default": 160,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "高阈值",
            "component": "slider",
        },
        "blur_size": {
            "type": "odd_int",
            "default": 5,
            "min": 1,
            "max": 31,
            "step": 2,
            "label": "平滑核大小",
            "component": "slider",
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}

    threshold1 = _get_int_param(params, "threshold1")
    threshold2 = _get_int_param(params, "threshold2")
    if threshold1 > threshold2:
        threshold1, threshold2 = threshold2, threshold1
    blur_size = _get_odd_param(params, "blur_size")

    gray = _to_gray(_ensure_uint8(image))
    blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0) if blur_size > 1 else gray
    edges = cv2.Canny(blurred, threshold1, threshold2)

    edge_pixels = int(np.count_nonzero(edges))
    total_pixels = int(edges.size)

    return {
        "result": edges,
        "steps": [
            {"name": "灰度图像", "image": gray},
            {"name": "高斯平滑", "image": blurred},
            {"name": "边缘检测结果", "image": edges},
        ],
        "metrics": {
            "threshold1": threshold1,
            "threshold2": threshold2,
            "blur_size": blur_size,
            "edge_pixels": edge_pixels,
            "edge_ratio": round(edge_pixels / total_pixels, 4) if total_pixels else 0.0,
        },
        "analysis": "已使用 Canny 算子提取图像边缘，平滑步骤可减少噪声干扰，边缘白色区域表示主要轮廓和结构变化位置。",
    }


def _get_int_param(params: dict, name: str) -> int:
    meta = ALGORITHM_META["params"][name]
    try:
        value = int(round(float(params.get(name, meta["default"]))))
    except (TypeError, ValueError):
        value = int(meta["default"])
    return int(np.clip(value, meta["min"], meta["max"]))


def _get_odd_param(params: dict, name: str) -> int:
    value = _get_int_param(params, name)
    if value % 2 == 0:
        value += 1
    return min(value, ALGORITHM_META["params"][name]["max"])


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
