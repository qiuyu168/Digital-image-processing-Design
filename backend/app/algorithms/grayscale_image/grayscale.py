# 本文件用于实现图像灰度化处理功能

import cv2
import numpy as np

ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "grayscale",
    "display_name": "灰度化",
    "description": "将彩色图像转换为灰度图像",
    "params": {}
}

def run(image: np.ndarray, params: dict = None) -> dict:
    # 输入校验
    if image is None:
        raise ValueError("输入图像为空")
    
    # 如果已经是灰度图，直接返回
    if len(image.shape) == 2:
        result = image.copy()
    else:
        # 加权灰度化
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return {
        "result": result,
        "steps": [
            {"name": "灰度化", "image": result}
        ],
        "metrics": {},
        "analysis": "已将彩色图像转换为灰度图像"
    }