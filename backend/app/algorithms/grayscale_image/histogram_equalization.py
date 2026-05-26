# 本文件用于实现直方图均衡化处理功能

import cv2
import numpy as np

ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "histogram_equalization",
    "display_name": "直方图均衡化",
    "description": "增强灰度图像整体对比度，使灰度分布更加均衡",
    "params": {}
}

def run(image: np.ndarray, params: dict = None) -> dict:
    # 输入校验
    if image is None:
        raise ValueError("输入图像为空")
    
    # 如果是彩色图，先转为灰度图
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # 直方图均衡化
    result = cv2.equalizeHist(gray)
    
    return {
        "result": result,
        "steps": [
            {"name": "直方图均衡化", "image": result}
        ],
        "metrics": {},
        "analysis": "通过直方图均衡化增强了图像对比度，使灰度分布更加均匀"
    }