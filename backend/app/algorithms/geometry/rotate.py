# 本文件用于实现图像旋转功能，支持任意角度旋转和边界填充
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "geometry",
    "name": "rotate",
    "display_name": "图像旋转",
    "description": "按指定角度旋转图像，支持边界填充和中心旋转。可自定义旋转后图像尺寸是否自适应。",
    "params": {
        "angle": {
            "type": "float",
            "default": 45.0,
            "min": -360.0,
            "max": 360.0,
            "label": "旋转角度（度）",
            "description": "正值表示逆时针旋转，负值表示顺时针旋转"
        },
        "scale": {
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "label": "缩放比例",
            "description": "旋转同时进行缩放，1.0 表示不缩放"
        },
        "auto_crop": {
            "type": "boolean",
            "default": False,
            "label": "自适应裁剪",
            "description": "True: 自动调整输出尺寸包含整个旋转图像; False: 保持原图尺寸，超出部分裁剪"
        },
        "border_mode": {
            "type": "choice",
            "default": "constant",
            "options": ["constant", "replicate", "reflect", "wrap"],
            "label": "边界填充模式",
            "description": "constant: 常数填充（黑边）; replicate: 边缘复制; reflect: 镜像反射; wrap: 环绕重复"
        },
        "border_value": {
            "type": "int",
            "default": 0,
            "min": 0,
            "max": 255,
            "label": "边界填充颜色",
            "description": "仅 constant 模式有效，0=黑色，255=白色"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行旋转
    :param image: 输入图像
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    angle = params.get("angle", 45.0)
    scale = params.get("scale", 1.0)
    auto_crop = params.get("auto_crop", False)
    border_mode = params.get("border_mode", "constant")
    border_value = params.get("border_value", 0)
    
    # 参数校验
    angle = max(-360.0, min(360.0, angle))
    scale = max(0.1, min(3.0, scale))
    border_value = max(0, min(255, border_value))
    
    valid_border_modes = ["constant", "replicate", "reflect", "wrap"]
    if border_mode not in valid_border_modes:
        border_mode = "constant"
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 获取图像尺寸
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    steps.append({
        "name": f"原始尺寸: {w} x {h}, 旋转中心: {center}",
        "image": _draw_center_info(image, center, f"原始尺寸: {w} x {h}")
    })
    
    # 获取旋转矩阵
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    
    # 计算旋转后的边界
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    
    if auto_crop:
        # 自动计算新尺寸，确保整个旋转图像都在画面内
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        
        # 调整旋转矩阵的平移部分
        rotation_matrix[0, 2] += (new_w / 2) - center[0]
        rotation_matrix[1, 2] += (new_h / 2) - center[1]
        
        dst_size = (new_w, new_h)
    else:
        # 保持原尺寸，超出部分裁剪
        dst_size = (w, h)
    
    # 边界填充模式映射
    border_mode_map = {
        "constant": cv2.BORDER_CONSTANT,
        "replicate": cv2.BORDER_REPLICATE,
        "reflect": cv2.BORDER_REFLECT,
        "wrap": cv2.BORDER_WRAP
    }
    border = border_mode_map.get(border_mode, cv2.BORDER_CONSTANT)
    
    # 执行旋转
    if border_mode == "constant":
        result = cv2.warpAffine(image, rotation_matrix, dst_size, 
                                flags=cv2.INTER_LINEAR, 
                                borderMode=border, 
                                borderValue=(border_value, border_value, border_value))
    else:
        result = cv2.warpAffine(image, rotation_matrix, dst_size, 
                                flags=cv2.INTER_LINEAR, 
                                borderMode=border)
    
    border_names = {
        "constant": "常数填充",
        "replicate": "边缘复制",
        "reflect": "镜像反射",
        "wrap": "环绕重复"
    }
    border_name = border_names.get(border_mode, "常数填充")
    
    # 生成分析文本
    rotation_direction = "逆时针" if angle > 0 else ("顺时针" if angle < 0 else "不")
    abs_angle = abs(angle)
    
    if auto_crop:
        analysis = f"图像{rotation_direction}旋转 {abs_angle:.1f}°，缩放比例 {scale:.2f}，自适应裁剪模式（输出尺寸 {dst_size[0]} x {dst_size[1]}）。边界填充模式：{border_name}。"
    else:
        analysis = f"图像{rotation_direction}旋转 {abs_angle:.1f}°，缩放比例 {scale:.2f}，保持原尺寸模式（输出尺寸 {w} x {h}，超出部分裁剪）。边界填充模式：{border_name}。"
    
    if border_mode == "constant" and border_value == 0:
        analysis += " 超出区域填充为黑色。"
    elif border_mode == "constant" and border_value == 255:
        analysis += " 超出区域填充为白色。"
    
    # 显示旋转结果
    info_text = f"旋转角度: {angle:.1f}° | 输出尺寸: {result.shape[1]} x {result.shape[0]}"
    result_with_info = _draw_size_info(result, info_text)
    
    steps.append({
        "name": f"旋转 {angle:.1f}° 完成",
        "image": result_with_info
    })
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }


def _draw_center_info(image: np.ndarray, center: tuple, text: str) -> np.ndarray:
    """
    在图像上绘制中心点信息（用于步骤展示）
    :param image: 输入图像
    :param center: 中心点坐标 (x, y)
    :param text: 要显示的文本
    :return: 添加了标记的图像
    """
    img_copy = image.copy()
    h, w = img_copy.shape[:2]
    
    # 绘制中心点标记
    cv2.circle(img_copy, center, 8, (0, 0, 255), -1)
    cv2.circle(img_copy, center, 15, (0, 0, 255), 2)
    
    # 绘制十字线
    cv2.line(img_copy, (center[0] - 25, center[1]), (center[0] + 25, center[1]), (0, 0, 255), 2)
    cv2.line(img_copy, (center[0], center[1] - 25), (center[0], center[1] + 25), (0, 0, 255), 2)
    
    # 添加半透明背景和文字
    overlay = img_copy.copy()
    cv2.rectangle(overlay, (10, 10), (w - 10, 60), (0, 0, 0), -1)
    img_copy = cv2.addWeighted(img_copy, 0.7, overlay, 0.3, 0)
    cv2.putText(img_copy, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return img_copy


def _draw_size_info(image: np.ndarray, text: str) -> np.ndarray:
    """
    在图像上绘制尺寸信息（用于步骤展示）
    :param image: 输入图像
    :param text: 要显示的文本
    :return: 添加了文本的图像
    """
    img_copy = image.copy()
    h, w = img_copy.shape[:2]
    
    # 添加半透明背景
    overlay = img_copy.copy()
    cv2.rectangle(overlay, (10, 10), (w - 10, 60), (0, 0, 0), -1)
    img_copy = cv2.addWeighted(img_copy, 0.7, overlay, 0.3, 0)
    
    # 添加文字
    cv2.putText(img_copy, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return img_copy