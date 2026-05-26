# 本文件用于实现高斯低通频域滤波的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "gaussian_low_pass",
    "display_name": "高斯低通滤波",
    "description": "使用高斯频域掩膜进行平滑，过渡更自然。",
    "params": {
        "radius": {"type": "int", "default": 30, "min": 1, "max": 300, "label": "频域滤波半径"},
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
