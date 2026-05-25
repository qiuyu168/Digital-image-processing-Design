# 本文件用于实现图像灰度化处理功能
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "gray_transform",
    "name": "grayscale",
    "display_name": "图像灰度化",
    "description": "将彩色图像转换为灰度图像，作为二值化、边缘检测、频域分析等算法的基础输入。",
    "params": {
        "method": {
            "type": "choice",
            "default": "weighted",
            "options": ["standard", "weighted", "average"],
            "label": "灰度化方法",
            "description": "standard: OpenCV标准BGR转灰度; weighted: 加权平均法(0.299R+0.587G+0.114B); average: 简单平均法(R+G+B)/3"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    将彩色图像转换为灰度图像
    :param image: 输入图像 (BGR格式)，由后端预处理，可直接使用
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    method = params.get("method", "weighted")
    
    # 参数校验
    valid_methods = ["standard", "weighted", "average"]
    if method not in valid_methods:
        method = "weighted"
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 判断是否已是灰度图
    if len(image.shape) == 2:
        result = image.copy()
        analysis = "输入图像已经是灰度图像，无需转换。"
        
        steps.append({
            "name": "灰度化结果",
            "image": result.copy()
        })
        
        return {
            "result": result,
            "steps": steps,
            "analysis": analysis
        }
    
    # 灰度化处理
    if method == "standard":
        # OpenCV 标准灰度化
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        analysis = "使用OpenCV标准方法将彩色图像转换为灰度图像。"
    
    elif method == "weighted":
        # 加权平均法（人眼感知权重）
        b, g, r = cv2.split(image)
        result = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
        analysis = "使用加权平均法进行灰度化：Y = 0.299R + 0.587G + 0.114B。该方法符合人眼对绿色最敏感的视觉特性。"
    
    else:  # average
        # 简单平均法
        b, g, r = cv2.split(image)
        result = ((r.astype(np.float32) + g.astype(np.float32) + b.astype(np.float32)) / 3).astype(np.uint8)
        analysis = "使用简单平均法进行灰度化：Y = (R+G+B)/3。该方法计算简单，但不符合人眼视觉特性。"
    
    # 记录结果
    steps.append({
        "name": "灰度化结果",
        "image": result.copy()
    })
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }