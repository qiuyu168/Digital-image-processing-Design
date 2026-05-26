# 本文件用于实现图像形态学闭运算

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "close_operation",
    "display_name": "闭运算",
    "description": "先膨胀后腐蚀，用于填补孔洞和连接断裂区域。",
    "params": {
        "kernel_size": {
            "type": "odd_int",
            "default": 5,
            "min": 1,
            "max": 21,
            "label": "结构元素大小"
        },
        "threshold": {
            "type": "int",
            "default": 127,
            "min": 0,
            "max": 255,
            "label": "二值化阈值"
        }
    }
}


def run(image: np.ndarray, params: dict | None = None) -> dict:

    if params is None:
        params = {}

    kernel_size = int(params.get("kernel_size", 5))
    threshold = int(params.get("threshold", 127))

    if kernel_size < 1:
        kernel_size = 1

    if kernel_size % 2 == 0:
        kernel_size += 1

    threshold = max(0, min(255, threshold))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(
        gray,
        threshold,
        255,
        cv2.THRESH_BINARY
    )

    kernel = np.ones(
        (kernel_size, kernel_size),
        np.uint8
    )

    closed = cv2.morphologyEx(
        binary,
        cv2.MORPH_CLOSE,
        kernel
    )

    filled_pixels = int(np.sum(binary != closed))

    result = closed

    steps = [
        {
            "name": "灰度化",
            "image": gray
        },
        {
            "name": "二值化",
            "image": binary
        },
        {
            "name": "闭运算结果",
            "image": closed
        }
    ]

    metrics = {
        "kernel_size": kernel_size,
        "threshold": threshold,
        "changed_pixels": filled_pixels
    }

    analysis = (
        "闭运算先进行膨胀再进行腐蚀，"
        "适合填补动漫图像中的小孔洞并连接断裂边缘。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }