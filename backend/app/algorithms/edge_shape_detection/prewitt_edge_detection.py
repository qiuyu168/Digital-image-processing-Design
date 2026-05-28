# 本文件用于实现 Prewitt 边缘检测算法
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import normalize_uint8, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "prewitt_edge_detection",
    "display_name": "Prewitt边缘检测",
    "description": "使用 Prewitt 一阶梯度模板检测水平和垂直边缘。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    _ = params or {}
    gray = to_gray(image)
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
    gx = cv2.filter2D(gray.astype(np.float32), -1, kernel_x)
    gy = cv2.filter2D(gray.astype(np.float32), -1, kernel_y)
    result = normalize_uint8(np.sqrt(gx * gx + gy * gy))
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"edge_pixels": int(np.count_nonzero(result)), "edge_ratio": round(float(np.count_nonzero(result)) / result.size, 4)},
        "analysis": "Prewitt 算子使用均匀权重的一阶差分模板，能提取主要方向边缘并具有一定平滑作用。",
    }

