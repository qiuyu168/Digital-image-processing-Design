# 本文件用于实现傅里叶变换并显示频谱图的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "frequency_analysis",
    "name": "dft_spectrum",
    "display_name": "傅里叶频谱",
    "description": "将图像转换到频域并显示频谱图，用于观察图像低频和高频信息分布。",
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
