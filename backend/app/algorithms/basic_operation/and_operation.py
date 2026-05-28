# 实现两张图像的按位与运算
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, require_second_image, resize_like, to_bgr


ALGORITHM_META = {
    "module": "basic_operation",
    "name": "and_operation",
    "display_name": "与运算",
    "description": "对两张 uint8 图像执行按位与运算，保留共同为亮的像素位。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    first = to_bgr(image)
    second = resize_like(to_bgr(require_second_image(params)), first)
    result = cv2.bitwise_and(first, second).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": first}, {"name": "处理结果", "image": result}],
        "metrics": gray_metrics(first, result),
        "analysis": "与运算只保留两张图像在二进制位上同时为 1 的部分，适合演示掩膜交集效果。",
    }

