# 本文件用于实现图像翻转功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "flip",
    "display_name": "图像翻转",
    "description": "实现水平翻转、垂直翻转和中心翻转。",
    "params": {
        "flip_code": {"type": "int", "default": 1, "min": -1, "max": 1, "label": "翻转方向"},
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
