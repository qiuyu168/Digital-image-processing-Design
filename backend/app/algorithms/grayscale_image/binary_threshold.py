# 本文件用于实现图像二值化处理功能

import cv2
import numpy as np

ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "binary_threshold",
    "display_name": "二值化",
    "description": "将灰度图像转换为黑白二值图像",
    "params": {
        "threshold": {"type": "int", "default": 127, "min": 0, "max": 255},
        "max_value": {"type": "int", "default": 255, "min": 0, "max": 255}
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    # 参数处理
    if params is None:
        params = {}
    threshold = params.get("threshold", 127)
    max_value = params.get("max_value", 255)
    
    # 参数校验
    threshold = max(0, min(255, threshold))
    max_value = max(0, min(255, max_value))
    
    # 输入校验
    if image is None:
        raise ValueError("输入图像为空")
    
    # 如果是彩色图，先转为灰度图
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # 二值化
    _, result = cv2.threshold(gray, threshold, max_value, cv2.THRESH_BINARY)
    
    return {
        "result": result,
        "steps": [
            {"name": "二值化", "image": result}
        ],
        "metrics": {
            "threshold": threshold,
            "max_value": max_value
        },
        "analysis": f"使用阈值{threshold}将灰度图像二值化，大于阈值的像素设为{max_value}，其余设为0"
    }