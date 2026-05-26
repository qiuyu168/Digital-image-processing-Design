# 本文件用于实现图像旋转功能

import cv2
import numpy as np

ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "rotate",
    "display_name": "旋转",
    "description": "按指定角度旋转图像",
    "params": {
        "angle": {"type": "int", "default": 90, "min": -360, "max": 360}
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    # 参数处理
    if params is None:
        params = {}
    angle = params.get("angle", 90)
    
    # 参数校验
    angle = max(-360, min(360, angle))
    
    # 输入校验
    if image is None:
        raise ValueError("输入图像为空")
    
    # 获取图像尺寸
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    # 旋转矩阵
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # 计算新边界
    cos = abs(M[0, 0])
    sin = abs(M[0, 1])
    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)
    
    # 调整平移矩阵
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
    # 旋转
    result = cv2.warpAffine(image, M, (new_w, new_h))
    
    return {
        "result": result,
        "steps": [
            {"name": "旋转", "image": result}
        ],
        "metrics": {
            "angle": angle,
            "original_size": f"{w}x{h}",
            "new_size": f"{new_w}x{new_h}"
        },
        "analysis": f"将图像旋转{angle}度，图像尺寸已自动调整以适应旋转后的内容"
    }