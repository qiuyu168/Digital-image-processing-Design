# 本文件用于实现基础边缘检测统一入口
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import normalize_uint8, to_gray


ALGORITHM_META = {
    "module": "edge_shape_detection",
    "name": "basic_edge_detection",
    "display_name": "基础边缘检测",
    "description": "统一演示 Canny、Sobel 和 Laplacian 基础边缘检测方法。",
    "params": {
        "method": {
            "type": "str",
            "default": "canny",
            "label": "检测方法",
            "component": "select",
            "options": [
                {"label": "Canny", "value": "canny"},
                {"label": "Sobel", "value": "sobel"},
                {"label": "Laplacian", "value": "laplacian"},
            ],
        }
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    method = str(params.get("method", "canny"))
    if method == "sobel":
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        result = normalize_uint8(cv2.magnitude(gx, gy))
    elif method == "laplacian":
        result = cv2.convertScaleAbs(cv2.Laplacian(gray, cv2.CV_32F, ksize=3))
    else:
        method = "canny"
        result = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 80, 160)
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": gray}, {"name": "处理结果", "image": result}],
        "metrics": {"method": method, "edge_pixels": int(np.count_nonzero(result)), "edge_ratio": round(float(np.count_nonzero(result)) / result.size, 4)},
        "analysis": "基础边缘检测统一入口用于比较不同基础算子的边缘响应，白色区域代表检测到的明显结构变化。",
    }

