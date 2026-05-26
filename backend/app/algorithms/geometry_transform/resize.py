# 本文件用于实现图像缩放功能

import cv2
import numpy as np

ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "resize",
    "display_name": "缩放",
    "description": "改变图像尺寸，支持按比例缩放和指定宽高缩放",
    "params": {
        "width": {"type": "int", "default": 512, "min": 1, "max": 4096},
        "height": {"type": "int", "default": 512, "min": 1, "max": 4096}
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    # 参数处理
    if params is None:
        params = {}
    width = params.get("width", 512)
    height = params.get("height", 512)
    
    # 参数校验
    width = max(1, min(4096, width))
    height = max(1, min(4096, height))
    
    # 输入校验
    if image is None:
        raise ValueError("输入图像为空")
    
    # 缩放
    result = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    
    return {
        "result": result,
        "steps": [
            {"name": "缩放", "image": result}
        ],
        "metrics": {
            "original_size": f"{image.shape[1]}x{image.shape[0]}",
            "new_size": f"{width}x{height}"
        },
        "analysis": f"将图像从{image.shape[1]}x{image.shape[0]}缩放到{width}x{height}"
    }