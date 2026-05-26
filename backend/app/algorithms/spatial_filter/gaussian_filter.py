# 本文件用于实现高斯滤波平滑图像的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "gaussian_filter",
    "display_name": "高斯滤波",
    "description": "使用高斯核进行平滑处理，适合去除一般噪声并保留较自然的过渡。",
    "params": {
        "kernel_size": {"type": "odd_int", "default": 5, "min": 1, "max": 31, "label": "滤波核大小"},
        "sigma": {"type": "float", "default": 1.0, "min": 0.0, "max": 10.0, "label": "高斯标准差"},
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
