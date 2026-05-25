# 本文件用于实现图像线性变换功能，调整图像的对比度和亮度
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "gray_transform",
    "name": "linear_transform",
    "display_name": "线性变换（对比度/亮度调整）",
    "description": "通过线性变换调整图像的对比度和亮度，公式为 g(x,y) = α * f(x,y) + β，其中α控制对比度，β控制亮度。",
    "params": {
        "alpha": {
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 3.0,
            "label": "对比度系数 α",
            "description": "控制图像对比度，>1 增强对比度，<1 降低对比度"
        },
        "beta": {
            "type": "int",
            "default": 0,
            "min": -100,
            "max": 100,
            "label": "亮度增量 β",
            "description": "控制图像亮度，正值变亮，负值变暗"
        },
        "clip": {
            "type": "boolean",
            "default": True,
            "label": "是否裁剪到0-255范围",
            "description": "确保输出像素值在有效范围内"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行线性变换，调整对比度和亮度
    :param image: 输入图像 (BGR或灰度图)
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    alpha = params.get("alpha", 1.0)
    beta = params.get("beta", 0)
    clip = params.get("clip", True)
    
    # 参数校验
    alpha = max(0.0, min(3.0, alpha))
    beta = max(-100, min(100, beta))
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 判断图像类型，决定处理方式
    is_color = len(image.shape) == 3
    
    if is_color:
        # 彩色图像：转换到HSV，只调整亮度通道V，保持色彩
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        steps.append({
            "name": "转换到HSV空间",
            "image": cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        })
        
        # 对V通道进行线性变换
        v_transformed = v.astype(np.float32) * alpha + beta
        if clip:
            v_transformed = np.clip(v_transformed, 0, 255)
        v_result = v_transformed.astype(np.uint8)
        
        # 合并通道并转回BGR
        hsv_result = cv2.merge([h, s, v_result])
        result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
        
        steps.append({
            "name": "亮度通道线性变换",
            "image": cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
        })
        
    else:
        # 灰度图像：直接对灰度值进行线性变换
        gray = image.copy()
        
        steps.append({
            "name": "灰度图像",
            "image": gray.copy()
        })
        
        # 线性变换
        result = gray.astype(np.float32) * alpha + beta
        if clip:
            result = np.clip(result, 0, 255)
        result = result.astype(np.uint8)
        
        steps.append({
            "name": f"线性变换 (α={alpha:.2f}, β={beta:+d})",
            "image": result.copy()
        })
    
    # 生成分析文本
    alpha_effect = "增强" if alpha > 1.0 else ("降低" if alpha < 1.0 else "保持")
    alpha_pct = abs(alpha - 1.0) * 100
    beta_effect = "提高" if beta > 0 else ("降低" if beta < 0 else "保持")
    
    if alpha != 1.0 and beta != 0:
        analysis = f"对图像进行了线性变换：对比度{alpha_effect}了{alpha_pct:.0f}%，亮度{beta_effect}了{abs(beta)}。"
    elif alpha != 1.0:
        analysis = f"对图像进行了线性变换：对比度{alpha_effect}了{alpha_pct:.0f}%。"
    elif beta != 0:
        analysis = f"对图像进行了线性变换：亮度{beta_effect}了{abs(beta)}。"
    else:
        analysis = "图像未发生变化。"
    
    analysis += " 线性变换公式为 g = α·f + β，其中α控制对比度，β控制亮度。"
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }