# 本文件用于实现图像翻转功能

import cv2
import numpy as np

ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "flip",
    "display_name": "翻转",
    "description": "实现水平翻转、垂直翻转",
    "params": {
        "direction": {"type": "string", "default": "horizontal", "enum": ["horizontal", "vertical"]}
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    # 参数处理
    if params is None:
        params = {}
    direction = params.get("direction", "horizontal")
    
    # 参数校验
    if direction not in ["horizontal", "vertical"]:
        direction = "horizontal"
    
    # 输入校验
    if image is None:
        raise ValueError("输入图像为空")
    
    # 翻转
    if direction == "horizontal":
        result = cv2.flip(image, 1)  # 水平翻转
        direction_name = "水平"
    else:
        result = cv2.flip(image, 0)  # 垂直翻转
        direction_name = "垂直"
    
    return {
        "result": result,
        "steps": [
            {"name": "翻转", "image": result}
        ],
        "metrics": {
            "direction": direction
        },
        "analysis": f"对图像进行{direction_name}翻转处理"
    }