# 本文件用于实现拉普拉斯锐化增强边缘的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "laplacian_sharpen",
    "display_name": "拉普拉斯锐化",
    "description": "增强图像边缘和细节，使轮廓更清晰。",
    "params": {
        "amount": {"type": "float", "default": 0.5, "min": 0.0, "max": 3.0, "label": "锐化强度"},
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
