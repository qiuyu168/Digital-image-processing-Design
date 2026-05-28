# 本文件用于实现两张图像的直方图匹配算法
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, require_second_image, resize_like, to_gray


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "histogram_matching",
    "display_name": "直方图匹配",
    "description": "将输入图像的灰度分布匹配到第二张参考图像的灰度分布。",
    "params": {},
}


def _match_histogram(source: np.ndarray, reference: np.ndarray) -> np.ndarray:
    source_values, source_indices, source_counts = np.unique(
        source.ravel(),
        return_inverse=True,
        return_counts=True,
    )
    reference_values, reference_counts = np.unique(reference.ravel(), return_counts=True)
    source_quantiles = np.cumsum(source_counts).astype(np.float64)
    source_quantiles /= source_quantiles[-1]
    reference_quantiles = np.cumsum(reference_counts).astype(np.float64)
    reference_quantiles /= reference_quantiles[-1]
    matched = np.interp(source_quantiles, reference_quantiles, reference_values)
    return matched[source_indices].reshape(source.shape).astype(np.uint8)


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    reference = resize_like(to_gray(require_second_image(params)), gray)
    result = _match_histogram(gray, reference)
    before_hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()
    after_hist = cv2.calcHist([result], [0], None, [256], [0, 256]).ravel()
    reference_hist = cv2.calcHist([reference], [0], None, [256], [0, 256]).ravel()
    return {
        "result": result,
        "steps": [
            {"name": "原始图像", "image": gray},
            {"name": "参考图像", "image": reference},
            {"name": "处理结果", "image": result},
        ],
        "metrics": {
            "source_mean": round(float(np.mean(gray)), 3),
            "reference_mean": round(float(np.mean(reference)), 3),
            "result_mean": round(float(np.mean(result)), 3),
            "histogram_distance_before": round(float(np.linalg.norm(before_hist - reference_hist)), 3),
            "histogram_distance_after": round(float(np.linalg.norm(after_hist - reference_hist)), 3),
            **gray_metrics(gray, result),
        },
        "analysis": "直方图匹配把原图灰度累计分布映射到参考图像分布，适合统一两张图像的亮度风格和对比度层次。",
    }
