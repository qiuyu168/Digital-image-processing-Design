# 本文件用于实现将灰度图转换为黑白二值图像的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "binary_threshold",
    "display_name": "二值化",
    "description": "将灰度图转换为黑白二值图，支持固定阈值和自适应阈值。",
    "params": {
        "threshold": {"type": "int", "default": 127, "min": 0, "max": 255, "label": "阈值"},
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
