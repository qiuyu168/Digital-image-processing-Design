# 本文件用于实现图像缩放功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "resize",
    "display_name": "图像缩放",
    "description": "改变图像尺寸，支持按比例缩放和指定宽高缩放。",
    "params": {
        "scale": {"type": "float", "default": 0.75, "min": 0.1, "max": 3.0, "label": "缩放比例"},
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
