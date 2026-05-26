# 本文件用于实现将彩色图像转换为灰度图像的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "grayscale",
    "display_name": "灰度化",
    "description": "将彩色图像转换为灰度图像，作为二值化、边缘检测、频域分析等算法的基础输入。",
    "params": {},
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
