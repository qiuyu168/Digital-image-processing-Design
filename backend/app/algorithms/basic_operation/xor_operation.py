# 实现两张图像的按位异或运算
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, require_second_image, resize_like, to_bgr


ALGORITHM_META = {
    "module": "basic_operation",
    "name": "xor_operation",
    "display_name": "异或运算",
    "description": "对两张 uint8 图像执行按位异或运算，突出不同的像素位。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    first = to_bgr(image)
    second = resize_like(to_bgr(require_second_image(params)), first)
    result = cv2.bitwise_xor(first, second).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": first}, {"name": "处理结果", "image": result}],
        "metrics": gray_metrics(first, result),
        "analysis": "异或运算在两张图像二进制位不同的位置输出亮值，因此适合突出差异区域。",
    }
