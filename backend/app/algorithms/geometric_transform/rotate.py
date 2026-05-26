# 本文件用于实现图像旋转功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "rotate",
    "display_name": "图像旋转",
    "description": "按指定角度旋转图像，支持边界填充和中心旋转。",
    "params": {
        "angle": {"type": "float", "default": 45.0, "min": -360.0, "max": 360.0, "label": "旋转角度"},
        "scale": {"type": "float", "default": 1.0, "min": 0.1, "max": 3.0, "label": "缩放比例"},
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
