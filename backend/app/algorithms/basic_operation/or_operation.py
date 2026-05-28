# 实现两张图像的按位或运算
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, require_second_image, resize_like, to_bgr


ALGORITHM_META = {
    "module": "basic_operation",
    "name": "or_operation",
    "display_name": "或运算",
    "description": "对两张 uint8 图像执行按位或运算，合并两张图像的亮像素位。",
    "params": {},
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    first = to_bgr(image)
    second = resize_like(to_bgr(require_second_image(params)), first)
    result = cv2.bitwise_or(first, second).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": first}, {"name": "处理结果", "image": result}],
        "metrics": gray_metrics(first, result),
        "analysis": "或运算会合并两张图像中任一图像为亮的二进制位，结果通常比单张输入更亮。",
    }

