# 本文件用于实现图像形态学膨胀操作
# 本文件用于实现图像膨胀操作的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "dilate",
    "display_name": "膨胀",
    "description": "扩大前景区域，连接断裂区域并增强目标。",
    "params": {
        "kernel_size": {
            "type": "odd_int",
            "default": 3,
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
        }
    }
    "description": "扩大前景区域，连接断裂区域或增强目标区域。",
    "params": {
        "kernel_size": {"type": "odd_int", "default": 5, "min": 1, "max": 31, "label": "结构元素大小"},
        "threshold": {"type": "int", "default": 127, "min": 0, "max": 255, "label": "二值阈值"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:

    if params is None:
        params = {}

    kernel_size = int(params.get("kernel_size", 3))
    iterations = int(params.get("iterations", 1))

    if kernel_size < 1:
        kernel_size = 1

    if kernel_size % 2 == 0:
        kernel_size += 1

    iterations = max(1, min(10, iterations))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.ones(
        (kernel_size, kernel_size),
        np.uint8
    )

    dilated = cv2.dilate(
        gray,
        kernel,
        iterations=iterations
    )

    result = dilated

    steps = [
        {
            "name": "灰度化",
            "image": gray
        },
        {
            "name": "膨胀结果",
            "image": dilated
        }
    ]

    metrics = {
        "kernel_size": kernel_size,
        "iterations": iterations
    }

    analysis = (
        "膨胀操作能够扩大目标区域，"
        "适合连接动漫线稿中的断裂边缘。"
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
