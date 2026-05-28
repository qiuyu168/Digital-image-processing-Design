# 本文件用于实现高斯拉普拉斯 LoG 边缘检测
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import normalize_uint8, odd_int_slider_value, slider_value, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "log_edge_detection",
    "display_name": "LoG边缘检测",
    "description": "先高斯平滑再拉普拉斯二阶检测，突出零交叉附近边缘。",
    "params": {
        "kernel_size": {"type": "int", "default": 5, "min": 1, "max": 31, "step": 2, "label": "高斯核大小", "component": "slider"},
        "sigma": {"type": "float", "default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1, "label": "高斯标准差", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    kernel_size = odd_int_slider_value(params, "kernel_size", ALGORITHM_META)
    sigma = slider_value(params, "sigma", ALGORITHM_META)
    blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), sigma)
    result = normalize_uint8(np.abs(cv2.Laplacian(blurred, cv2.CV_32F, ksize=3)))
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "平滑图像", "image": blurred}, {"name": "处理结果", "image": result}],
        "metrics": {"kernel_size": kernel_size, "sigma": sigma, "edge_pixels": int(np.count_nonzero(result))},
        "analysis": "LoG 边缘检测先抑制噪声再计算二阶变化，对斑点、轮廓和灰度突变区域较敏感。",
    }

