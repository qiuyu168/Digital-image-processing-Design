# 本文件用于实现图像二值化处理功能，将灰度图转换为黑白二值图
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "gray_transform",
    "name": "binary_threshold",
    "display_name": "图像二值化",
    "description": "将灰度图转换为黑白二值图，可支持固定阈值和自适应阈值，用于图像分割、轮廓提取等预处理。",
    "params": {
        "threshold_type": {
            "type": "choice",
            "default": "fixed",
            "options": ["fixed", "adaptive"],
            "label": "阈值类型",
            "description": "fixed: 固定阈值; adaptive: 自适应阈值"
        },
        "thresh": {
            "type": "int",
            "default": 127,
            "min": 0,
            "max": 255,
            "label": "固定阈值",
            "description": "仅 fixed 模式有效，像素值大于等于该值设为白色，否则黑色"
        },
        "maxval": {
            "type": "int",
            "default": 255,
            "min": 0,
            "max": 255,
            "label": "最大值",
            "description": "二值化后的最大值（通常为255白色）"
        },
        "adaptive_method": {
            "type": "choice",
            "default": "mean",
            "options": ["mean", "gaussian"],
            "label": "自适应方法",
            "description": "mean: 邻域均值法; gaussian: 高斯加权法"
        },
        "block_size": {
            "type": "int",
            "default": 11,
            "min": 3,
            "max": 255,
            "label": "邻域大小",
            "description": "必须是正奇数，用于计算局部阈值的像素邻域大小"
        },
        "C": {
            "type": "int",
            "default": 2,
            "min": 0,
            "max": 50,
            "label": "常数C",
            "description": "从均值或加权和中减去的常数值"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    将灰度图转换为黑白二值图
    :param image: 输入图像 (BGR或灰度图)
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    threshold_type = params.get("threshold_type", "fixed")
    thresh = params.get("thresh", 127)
    maxval = params.get("maxval", 255)
    adaptive_method = params.get("adaptive_method", "mean")
    block_size = params.get("block_size", 11)
    c_value = params.get("C", 2)
    
    # 参数校验
    thresh = max(0, min(255, thresh))
    maxval = max(0, min(255, maxval))
    
    # block_size 必须是正奇数
    if block_size % 2 == 0:
        block_size += 1
    block_size = max(3, min(255, block_size))
    
    c_value = max(0, min(50, c_value))
    
    valid_threshold_types = ["fixed", "adaptive"]
    if threshold_type not in valid_threshold_types:
        threshold_type = "fixed"
    
    valid_adaptive_methods = ["mean", "gaussian"]
    if adaptive_method not in valid_adaptive_methods:
        adaptive_method = "mean"
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 转换为灰度图
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    steps.append({
        "name": "灰度图像",
        "image": gray.copy()
    })
    
    # 二值化处理
    if threshold_type == "fixed":
        # 固定阈值二值化
        _, result = cv2.threshold(gray, thresh, maxval, cv2.THRESH_BINARY)
        
        steps.append({
            "name": f"固定阈值二值化 (阈值={thresh})",
            "image": result.copy()
        })
        
        analysis = f"使用固定阈值 {thresh} 对灰度图进行二值化。像素值 ≥ {thresh} 变为 {maxval}（白色），< {thresh} 变为 0（黑色）。该方法简单高效，适用于光照均匀的图像。"
    
    else:
        # 自适应阈值二值化
        if adaptive_method == "mean":
            adaptive_mode = cv2.ADAPTIVE_THRESH_MEAN_C
            method_name = "均值法"
        else:
            adaptive_mode = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
            method_name = "高斯加权法"
        
        result = cv2.adaptiveThreshold(gray, maxval, adaptive_mode, cv2.THRESH_BINARY, block_size, c_value)
        
        steps.append({
            "name": f"自适应阈值二值化 ({method_name}, block_size={block_size}, C={c_value})",
            "image": result.copy()
        })
        
        analysis = f"使用自适应阈值二值化，方法为{method_name}，邻域大小为 {block_size}，常数 C={c_value}。该方法根据局部像素值动态计算阈值，能更好地处理光照不均匀的图像，适合动漫扫描线稿等场景。"
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }