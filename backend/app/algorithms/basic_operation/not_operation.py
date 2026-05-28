# 实现单张图像的按位非运算
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, to_bgr


ALGORITHM_META = {
    "module": "basic_operation",
    "name": "not_operation",
    "display_name": "非运算",
    "description": "对单张 uint8 图像执行按位取反，得到类似负片的效果。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    _ = params or {}
    source = to_bgr(image)
    result = cv2.bitwise_not(source).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": gray_metrics(source, result),
        "analysis": "非运算把每个像素位取反，亮暗关系反转，常用于解释数字图像的补码和负片效果。",
    }

