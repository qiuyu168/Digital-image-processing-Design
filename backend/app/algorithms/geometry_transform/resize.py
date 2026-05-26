# 本文件用于实现图像缩放功能，支持按比例缩放和指定宽高缩放
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "geometry",
    "name": "resize",
    "display_name": "图像缩放",
    "description": "改变图像尺寸，支持按比例缩放和指定宽高缩放。可选择不同的插值方法平衡速度与质量。",
    "params": {
        "resize_type": {
            "type": "choice",
            "default": "by_ratio",
            "options": ["by_ratio", "by_size"],
            "label": "缩放方式",
            "description": "by_ratio: 按比例缩放; by_size: 指定目标尺寸"
        },
        "width_ratio": {
            "type": "float",
            "default": 0.5,
            "label": "宽度缩放比例",
            "description": "仅 by_ratio 模式有效"
        },
        "height_ratio": {
            "type": "float",
            "default": 0.5,
            "label": "高度缩放比例",
            "description": "仅 by_ratio 模式有效"
        },
        "target_width": {
            "type": "int",
            "default": 512,
            "label": "目标宽度",
            "description": "仅 by_size 模式有效，单位：像素"
        },
        "target_height": {
            "type": "int",
            "default": 512,
            "label": "目标高度",
            "description": "仅 by_size 模式有效，单位：像素"
        },
        "interpolation": {
            "type": "choice",
            "default": "area",
            "options": ["nearest", "linear", "cubic", "area", "lanczos"],
            "label": "插值方法",
            "description": "nearest: 最近邻（快，锯齿）; linear: 双线性（平衡）; cubic: 双三次（平滑）; area: 像素区域（缩小推荐）; lanczos: Lanczos（高质量）"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行缩放
    :param image: 输入图像
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    resize_type = params.get("resize_type", "by_ratio")
    width_ratio = params.get("width_ratio", 0.5)
    height_ratio = params.get("height_ratio", 0.5)
    target_width = params.get("target_width", 512)
    target_height = params.get("target_height", 512)
    interpolation = params.get("interpolation", "area")
    
    # 参数校验
    if resize_type not in ["by_ratio", "by_size"]:
        resize_type = "by_ratio"
    
    # 只校验正数，不设上下限
    if width_ratio <= 0:
        width_ratio = 0.5
    if height_ratio <= 0:
        height_ratio = 0.5
    
    if target_width <= 0:
        target_width = 512
    if target_height <= 0:
        target_height = 512
    
    # 插值方法映射
    interpolation_map = {
        "nearest": cv2.INTER_NEAREST,
        "linear": cv2.INTER_LINEAR,
        "cubic": cv2.INTER_CUBIC,
        "area": cv2.INTER_AREA,
        "lanczos": cv2.INTER_LANCZOS4
    }
    interp = interpolation_map.get(interpolation, cv2.INTER_AREA)
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 获取原始尺寸
    h, w = image.shape[:2]
    
    steps.append({
        "name": f"原始尺寸: {w} x {h}",
        "image": _draw_size_info(image, f"原始尺寸: {w} x {h}")
    })
    
    # 计算目标尺寸
    if resize_type == "by_ratio":
        new_width = int(w * width_ratio)
        new_height = int(h * height_ratio)
        analysis = f"按比例缩放：宽度缩放 {width_ratio:.2f} 倍，高度缩放 {height_ratio:.2f} 倍。"
    else:
        new_width = target_width
        new_height = target_height
        analysis = f"指定尺寸缩放：目标宽度 {target_width}，目标高度 {target_height}。"
    
    # 确保尺寸至少为1
    if new_width < 1:
        new_width = 1
    if new_height < 1:
        new_height = 1
    
    # 执行缩放
    result = cv2.resize(image, (new_width, new_height), interpolation=interp)
    
    interpolation_names = {
        "nearest": "最近邻插值",
        "linear": "双线性插值",
        "cubic": "双三次插值",
        "area": "像素区域插值",
        "lanczos": "Lanczos插值"
    }
    interp_name = interpolation_names.get(interpolation, "像素区域插值")
    
    steps.append({
        "name": f"缩放后尺寸: {new_width} x {new_height} ({interp_name})",
        "image": _draw_size_info(result, f"缩放后尺寸: {new_width} x {new_height}")
    })
    
    # 补充分析文本
    if new_width < w and new_height < h:
        analysis += f" 图像被缩小为原来的 {new_width/w:.1%} x {new_height/h:.1%}，使用{interp_name}。"
    elif new_width > w and new_height > h:
        analysis += f" 图像被放大为原来的 {new_width/w:.1%} x {new_height/h:.1%}，使用{interp_name}。放大时推荐使用双三次或Lanczos插值以获得更平滑效果。"
    else:
        analysis += f" 图像尺寸从 {w}x{h} 变为 {new_width}x{new_height}，使用{interp_name}。"
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }


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