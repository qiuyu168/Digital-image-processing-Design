# 本文件用于实现图像形态学腐蚀操作
# 本文件用于实现图像腐蚀操作的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "erode",
    "display_name": "腐蚀",
    "description": "缩小前景区域，去除小白点和细小噪声。",
    "params": {
        "kernel_size": {
            "type": "odd_int",
            "default": 5,
            "min": 1,
            "max": 21,
            "label": "结构元素大小"
        },
        "iterations": {
            "type": "int",
            "default": 1,
            "min": 1,
            "max": 10,
            "label": "迭代次数"
        },
        "threshold": {
            "type": "int",
            "default": 127,
            "min": 0,
            "max": 255,
            "label": "二值化阈值"
        }
    }
    "description": "缩小前景区域，去除小白点或细小噪声。",
    "params": {
        "kernel_size": {"type": "odd_int", "default": 5, "min": 1, "max": 31, "label": "结构元素大小"},
        "threshold": {"type": "int", "default": 127, "min": 0, "max": 255, "label": "二值阈值"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:

    if params is None:
        params = {}

    kernel_size = int(params.get("kernel_size", 5))
    iterations = int(params.get("iterations", 1))
    threshold = int(params.get("threshold", 127))

    if kernel_size < 1:
        kernel_size = 1

    if kernel_size % 2 == 0:
        kernel_size += 1

    iterations = max(1, min(10, iterations))
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

    eroded = cv2.erode(
        binary,
        kernel,
        iterations=iterations
    )

    removed_pixels = int(np.sum(binary != eroded))

    result = eroded

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
            "name": "腐蚀结果",
            "image": eroded
        }
    ]

    metrics = {
        "kernel_size": kernel_size,
        "iterations": iterations,
        "threshold": threshold,
        "removed_pixels": removed_pixels
    }

    analysis = (
        "腐蚀操作会缩小白色前景区域，"
        "能够有效去除动漫图像中的小白点噪声和细小连接区域。"
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
