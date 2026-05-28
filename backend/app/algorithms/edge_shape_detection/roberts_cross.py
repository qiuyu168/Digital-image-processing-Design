# 本文件用于实现 Roberts 交叉算子边缘检测
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import normalize_uint8, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "roberts_cross",
    "display_name": "Roberts交叉边缘检测",
    "description": "使用 2x2 Roberts 交叉梯度核检测细小边缘。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    _ = params or {}
    gray = to_gray(image)
    kernel_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    gx = cv2.filter2D(gray.astype(np.float32), -1, kernel_x)
    gy = cv2.filter2D(gray.astype(np.float32), -1, kernel_y)
    result = normalize_uint8(np.sqrt(gx * gx + gy * gy))
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"edge_pixels": int(np.count_nonzero(result)), "edge_ratio": round(float(np.count_nonzero(result)) / result.size, 4)},
        "analysis": "Roberts 算子用 2x2 交叉模板计算局部梯度，对细小边缘敏感，但抗噪能力相对较弱。",
    }

