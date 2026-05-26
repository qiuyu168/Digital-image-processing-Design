# 本文件用于实现图像闭运算操作的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "close_operation",
    "display_name": "闭运算",
    "description": "先膨胀后腐蚀，适合填补小孔洞、连接断裂区域。",
    "params": {
        "kernel_size": {"type": "odd_int", "default": 5, "min": 1, "max": 31, "label": "结构元素大小"},
        "threshold": {"type": "int", "default": 127, "min": 0, "max": 255, "label": "二值阈值"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
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
