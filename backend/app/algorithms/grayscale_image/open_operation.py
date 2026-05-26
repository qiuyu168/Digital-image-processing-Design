# 本文件用于实现图像形态学开运算
# 本文件用于实现图像开运算操作的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "open_operation",
    "display_name": "开运算",
    "description": "先腐蚀后膨胀，用于去除小噪声。",
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
    "description": "先腐蚀后膨胀，适合去除小噪声。",
    "params": {
        "kernel_size": {"type": "odd_int", "default": 5, "min": 1, "max": 31, "label": "结构元素大小"},
        "threshold": {"type": "int", "default": 127, "min": 0, "max": 255, "label": "二值阈值"},
    },
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

    opened = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        kernel
    )

    noise_removed = int(np.sum(binary != opened))

    result = opened

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
            "name": "开运算结果",
            "image": opened
        }
    ]

    metrics = {
        "kernel_size": kernel_size,
        "threshold": threshold,
        "changed_pixels": noise_removed
    }

    analysis = (
        "开运算先进行腐蚀再进行膨胀，"
        "能够有效去除动漫图像中的小白点和离散噪声。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
    if image is None:
        raise ValueError("输入图像不能为空")
    if params is None:
        params = {}

    result = image.copy()
    return {
        "result": result,
        "steps": [
            {"name": "原始图像", "image": result},
        ],
        "metrics": {},
        "analysis": "当前为框架占位实现，小组成员可直接替换 run(image, params) 内部逻辑。",
    }
