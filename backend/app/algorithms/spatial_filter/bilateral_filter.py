# 本文件用于实现双边滤波平滑并保留边缘的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "bilateral_filter",
    "display_name": "双边滤波",
    "description": "在平滑图像的同时尽量保留边缘，适合动漫线条图像降噪。",
    "params": {
        "diameter": {"type": "int", "default": 9, "min": 1, "max": 31, "label": "邻域直径"},
        "sigma_color": {"type": "float", "default": 75.0, "min": 1.0, "max": 200.0, "label": "颜色标准差"},
        "sigma_space": {"type": "float", "default": 75.0, "min": 1.0, "max": 200.0, "label": "空间标准差"},
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
