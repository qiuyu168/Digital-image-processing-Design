# 本文件用于实现 Scharr 边缘检测算法
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import normalize_uint8, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "scharr_edge_detection",
    "display_name": "Scharr边缘检测",
    "description": "使用 Scharr 算子获得比 3x3 Sobel 更精细的梯度响应。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    _ = params or {}
    gray = to_gray(image)
    gx = cv2.Scharr(gray, cv2.CV_32F, 1, 0)
    gy = cv2.Scharr(gray, cv2.CV_32F, 0, 1)
    result = normalize_uint8(np.sqrt(gx * gx + gy * gy))
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"edge_pixels": int(np.count_nonzero(result)), "edge_ratio": round(float(np.count_nonzero(result)) / result.size, 4)},
        "analysis": "Scharr 算子改进了 3x3 梯度核的旋转对称性，适合提取较精细的边缘方向变化。",
    }

