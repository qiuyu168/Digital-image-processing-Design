# 本文件用于实现图像平移功能，在水平和垂直方向上移动图像
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "geometry",
    "name": "translate",
    "display_name": "图像平移",
    "description": "在水平和垂直方向上移动图像，移动后空白区域用指定颜色填充。",
    "params": {
        "tx": {
            "type": "int",
            "default": 50,
            "label": "水平平移量（像素）",
            "description": "正值向右移动，负值向左移动"
        },
        "ty": {
            "type": "int",
            "default": 50,
            "label": "垂直平移量（像素）",
            "description": "正值向下移动，负值向上移动"
        },
        "border_mode": {
            "type": "choice",
            "default": "constant",
            "options": ["constant", "replicate", "reflect", "wrap"],
            "label": "边界填充模式",
            "description": "constant: 常数填充; replicate: 边缘复制; reflect: 镜像反射; wrap: 环绕重复"
        },
        "border_value": {
            "type": "int",
            "default": 0,
            "min": 0,
            "max": 255,
            "label": "边界填充颜色",
            "description": "仅 constant 模式有效，0=黑色，255=白色"
        },
        "keep_size": {
            "type": "boolean",
            "default": True,
            "label": "保持原始尺寸",
            "description": "True: 输出图像尺寸不变; False: 输出图像尺寸自动扩展以包含全部平移内容"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行平移
    :param image: 输入图像
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    tx = params.get("tx", 50)
    ty = params.get("ty", 50)
    border_mode = params.get("border_mode", "constant")
    border_value = params.get("border_value", 0)
    keep_size = params.get("keep_size", True)
    
    # 参数校验（只校验边界颜色范围，tx和ty不设上下限）
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
    
    steps.append({
        "name": f"原始尺寸: {w} x {h}",
        "image": _draw_text_on_image(image, f"原始尺寸: {w} x {h}")
    })
    
    # 边界填充模式映射
    border_mode_map = {
        "constant": cv2.BORDER_CONSTANT,
        "replicate": cv2.BORDER_REPLICATE,
        "reflect": cv2.BORDER_REFLECT,
        "wrap": cv2.BORDER_WRAP
    }
    border = border_mode_map.get(border_mode, cv2.BORDER_CONSTANT)
    
    border_names = {
        "constant": "常数填充",
        "replicate": "边缘复制",
        "reflect": "镜像反射",
        "wrap": "环绕重复"
    }
    border_name = border_names.get(border_mode, "常数填充")
    
    if keep_size:
        # 保持原尺寸：创建平移矩阵并执行仿射变换
        translation_matrix = np.float32([
            [1, 0, tx],
            [0, 1, ty]
        ])
        
        if border_mode == "constant":
            result = cv2.warpAffine(image, translation_matrix, (w, h),
                                    flags=cv2.INTER_LINEAR,
                                    borderMode=border,
                                    borderValue=(border_value, border_value, border_value))
        else:
            result = cv2.warpAffine(image, translation_matrix, (w, h),
                                    flags=cv2.INTER_LINEAR,
                                    borderMode=border)
        
        # 显示平移后图像上的偏移信息
        info_text = f"平移量: dx={tx:+d}, dy={ty:+d} | 输出尺寸: {w} x {h}"
        result_with_info = _draw_text_on_image(result, info_text)
        
        steps.append({
            "name": f"平移后 (dx={tx:+d}, dy={ty:+d})",
            "image": result_with_info
        })
        
        # 生成分析文本
        direction_x = "向右" if tx > 0 else ("向左" if tx < 0 else "不水平移动")
        direction_y = "向下" if ty > 0 else ("向上" if ty < 0 else "不垂直移动")
        
        if tx != 0 and ty != 0:
            analysis = f"图像{direction_x}平移 {abs(tx)} 像素，{direction_y}平移 {abs(ty)} 像素。输出图像保持原始尺寸 ({w} x {h})，平移后空白区域使用{border_name}填充。"
        elif tx != 0:
            analysis = f"图像{direction_x}平移 {abs(tx)} 像素。输出图像保持原始尺寸 ({w} x {h})，平移后空白区域使用{border_name}填充。"
        elif ty != 0:
            analysis = f"图像{direction_y}平移 {abs(ty)} 像素。输出图像保持原始尺寸 ({w} x {h})，平移后空白区域使用{border_name}填充。"
        else:
            analysis = f"图像未发生平移。"
        
        if border_mode == "constant" and border_value == 0:
            analysis += " 空白区域填充为黑色。"
        elif border_mode == "constant" and border_value == 255:
            analysis += " 空白区域填充为白色。"
    
    else:
        # 自动扩展尺寸：计算新尺寸
        new_w = w + abs(tx)
        new_h = h + abs(ty)
        
        # 调整平移量（如果为负，需要调整起始位置）
        adjusted_tx = tx
        adjusted_ty = ty
        
        if tx < 0:
            adjusted_tx = new_w - abs(tx)
        if ty < 0:
            adjusted_ty = new_h - abs(ty)
        
        translation_matrix = np.float32([
            [1, 0, adjusted_tx],
            [0, 1, adjusted_ty]
        ])
        
        if border_mode == "constant":
            result = cv2.warpAffine(image, translation_matrix, (new_w, new_h),
                                    flags=cv2.INTER_LINEAR,
                                    borderMode=border,
                                    borderValue=(border_value, border_value, border_value))
        else:
            result = cv2.warpAffine(image, translation_matrix, (new_w, new_h),
                                    flags=cv2.INTER_LINEAR,
                                    borderMode=border)
        
        # 显示平移后图像上的信息
        info_text = f"平移量: dx={tx:+d}, dy={ty:+d} | 输出尺寸: {new_w} x {new_h}"
        result_with_info = _draw_text_on_image(result, info_text)
        
        steps.append({
            "name": f"平移后 (dx={tx:+d}, dy={ty:+d})",
            "image": result_with_info
        })
        
        # 生成分析文本
        direction_x = "向右" if tx > 0 else ("向左" if tx < 0 else "不水平移动")
        direction_y = "向下" if ty > 0 else ("向上" if ty < 0 else "不垂直移动")
        
        analysis = f"图像{direction_x}平移 {abs(tx)} 像素，{direction_y}平移 {abs(ty)} 像素。输出图像自动扩展为 {new_w} x {new_h}，包含完整平移内容。"
        
        if border_mode == "constant":
            analysis += f" 扩展区域使用{border_name}，颜色值为 {border_value}。"
        else:
            analysis += f" 扩展区域使用{border_name}填充。"
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }


def _draw_text_on_image(image: np.ndarray, text: str) -> np.ndarray:
    """
    在图像上绘制文本信息（用于步骤展示）
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