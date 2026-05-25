# 本文件用于实现图像基础边缘检测算法。
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "edge_detection_basic",
    "display_name": "基础边缘检测",
    "description": "使用 Canny 算子提取图像中的主要轮廓和边界。",
    "params": {
        "threshold1": {"type": "int", "default": 80, "min": 0, "max": 255, "label": "低阈值"},
        "threshold2": {"type": "int", "default": 160, "min": 0, "max": 255, "label": "高阈值"},
        "blur_size": {"type": "int", "default": 5, "min": 1, "max": 31, "label": "平滑核大小"},
    },
}


def _to_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image.copy()
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口。"""
    if image is None:
        raise ValueError("输入图像不能为空")
    if params is None:
        params = {}

    threshold1 = int(params.get("threshold1", 80))
    threshold2 = int(params.get("threshold2", 160))
    blur_size = int(params.get("blur_size", 5))
    blur_size = max(1, min(31, blur_size))
    if blur_size % 2 == 0:
        blur_size += 1

    gray = _to_gray(image)
    blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0) if blur_size > 1 else gray
    edges = cv2.Canny(blurred, threshold1, threshold2)

    edge_pixels = int(np.count_nonzero(edges))
    total_pixels = int(edges.size)

    return {
        "result": edges,
        "steps": [
            {"name": "灰度化", "image": gray},
            {"name": "高斯平滑", "image": blurred},
            {"name": "基础边缘检测", "image": edges},
        ],
        "metrics": {
            "threshold1": threshold1,
            "threshold2": threshold2,
            "blur_size": blur_size,
            "edge_pixels": edge_pixels,
            "edge_ratio": edge_pixels / total_pixels if total_pixels else 0.0,
        },
        "analysis": "基础边缘检测用于突出图像中的主要轮廓、线条和结构边界。",
    }
