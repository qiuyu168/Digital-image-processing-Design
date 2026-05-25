# 本文件用于提供后端算法文件的通用运行框架和示例实现。
from __future__ import annotations

import cv2
import numpy as np


MODULE_DESCRIPTIONS = {
    "basic_operations": "用于演示数字图像基础像素运算，便于动漫图像的亮度、差异和掩膜处理。",
    "geometry": "用于演示数字图像几何变换，便于调整动漫图像的位置、角度和视角。",
    "gray_transform": "用于演示灰度变换方法，便于观察动漫图像的亮度层次和明暗分布。",
    "spatial_filter": "用于演示空间域滤波方法，便于平滑噪声或增强动漫图像细节。",
    "frequency_filter": "用于演示频域滤波方法，便于观察和处理动漫图像的频谱信息。",
    "color_processing": "用于演示彩色图像处理方法，便于调整动漫图像的色彩表现。",
    "restoration": "用于演示图像复原和修复方法，便于处理模糊、噪声或局部缺损图像。",
    "morphology": "用于演示形态学处理方法，便于分析动漫图像中的区域、轮廓和结构。",
    "edge_detection": "用于演示边缘检测方法，便于提取动漫人物和场景线条。",
    "anime_recognition": "用于演示动漫图像识别相关的轻量特征分析流程。",
}


DISPLAY_NAMES = {
    "image_add": "图像加法",
    "image_subtract": "图像减法",
    "image_blend": "图像融合",
    "logic_and": "逻辑与",
    "logic_or": "逻辑或",
    "logic_not": "逻辑非",
    "mask_apply": "掩膜应用",
    "resize": "图像缩放",
    "rotate": "图像旋转",
    "translate": "图像平移",
    "affine": "仿射变换",
    "perspective": "透视变换",
    "grayscale": "灰度化",
    "binary_threshold": "二值阈值",
    "linear_transform": "线性灰度变换",
    "gamma_transform": "伽马变换",
    "log_transform": "对数变换",
    "histogram_equalization": "直方图均衡化",
    "clahe": "自适应直方图均衡化",
    "mean_filter": "均值滤波",
    "gaussian_filter": "高斯滤波",
    "median_filter": "中值滤波",
    "bilateral_filter": "双边滤波",
    "laplacian_sharpen": "拉普拉斯锐化",
    "unsharp_mask": "反锐化掩膜",
    "dft_spectrum": "傅里叶频谱",
    "ideal_low_pass": "理想低通滤波",
    "ideal_high_pass": "理想高通滤波",
    "gaussian_low_pass": "高斯低通滤波",
    "gaussian_high_pass": "高斯高通滤波",
    "homomorphic_filter": "同态滤波",
    "rgb_channel": "RGB 通道分离",
    "hsv_adjust": "HSV 调整",
    "color_balance": "色彩平衡",
    "pseudo_color": "伪彩色",
    "anime_color_enhance": "动漫色彩增强",
    "motion_blur": "运动模糊",
    "inverse_filter": "逆滤波复原",
    "wiener_filter": "维纳滤波复原",
    "denoise": "图像去噪",
    "inpaint": "图像修复",
    "erode": "腐蚀",
    "dilate": "膨胀",
    "open_operation": "开运算",
    "close_operation": "闭运算",
    "top_hat": "顶帽变换",
    "black_hat": "黑帽变换",
    "connected_components": "连通域分析",
    "sobel": "Sobel 边缘检测",
    "scharr": "Scharr 边缘检测",
    "laplace": "Laplace 边缘检测",
    "log_edge": "LoG 边缘检测",
    "canny": "Canny 边缘检测",
    "hough_line": "霍夫直线检测",
    "hough_circle": "霍夫圆检测",
    "anime_face_detect": "动漫人脸检测",
    "dominant_color_extract": "主色提取",
    "line_style_analyze": "线条风格分析",
    "feature_extract": "特征提取",
    "gallery_match": "图库匹配",
}


def _p_int(default: int, min_value: int, max_value: int, label: str) -> dict:
    return {"type": "int", "default": default, "min": min_value, "max": max_value, "label": label}


def _p_float(default: float, min_value: float, max_value: float, label: str) -> dict:
    return {"type": "float", "default": default, "min": min_value, "max": max_value, "label": label}


def _p_odd(default: int, min_value: int, max_value: int, label: str) -> dict:
    return {"type": "odd_int", "default": default, "min": min_value, "max": max_value, "label": label}


def _p_select(default: str, options: list[str], label: str) -> dict:
    return {"type": "select", "default": default, "options": options, "label": label}


PARAMS_BY_NAME = {
    "image_add": {"value": _p_int(40, 0, 255, "加法亮度值")},
    "image_subtract": {"value": _p_int(40, 0, 255, "减法亮度值")},
    "image_blend": {"alpha": _p_float(0.6, 0.0, 1.0, "原图权重"), "blur_size": _p_odd(9, 1, 31, "模糊核大小")},
    "logic_and": {"threshold": _p_int(127, 0, 255, "掩膜阈值")},
    "logic_or": {"value": _p_int(64, 0, 255, "或运算参考值")},
    "mask_apply": {"radius_percent": _p_int(35, 5, 50, "圆形掩膜半径百分比")},
    "resize": {"scale": _p_float(0.75, 0.1, 3.0, "缩放比例")},
    "rotate": {"angle": _p_float(45.0, -360.0, 360.0, "旋转角度"), "scale": _p_float(1.0, 0.1, 3.0, "缩放比例")},
    "translate": {"shift_x": _p_int(30, -500, 500, "水平平移像素"), "shift_y": _p_int(20, -500, 500, "垂直平移像素")},
    "affine": {"offset": _p_float(0.12, -0.4, 0.4, "仿射偏移比例")},
    "perspective": {"margin_percent": _p_int(8, 0, 30, "透视边距百分比")},
    "binary_threshold": {"threshold": _p_int(127, 0, 255, "阈值")},
    "linear_transform": {"alpha": _p_float(1.2, 0.1, 3.0, "对比度系数"), "beta": _p_int(10, -100, 100, "亮度偏移")},
    "gamma_transform": {"gamma": _p_float(0.8, 0.1, 5.0, "伽马系数")},
    "log_transform": {"gain": _p_float(1.0, 0.1, 5.0, "增强系数")},
    "clahe": {"clip_limit": _p_float(2.0, 0.1, 10.0, "对比度限制"), "tile_grid_size": _p_int(8, 2, 16, "网格大小")},
    "mean_filter": {"kernel_size": _p_odd(5, 1, 31, "滤波核大小")},
    "gaussian_filter": {"kernel_size": _p_odd(5, 1, 31, "滤波核大小"), "sigma": _p_float(1.0, 0.0, 10.0, "高斯标准差")},
    "median_filter": {"kernel_size": _p_odd(5, 1, 31, "滤波核大小")},
    "bilateral_filter": {"diameter": _p_int(9, 1, 31, "邻域直径"), "sigma_color": _p_float(75.0, 1.0, 200.0, "颜色标准差"), "sigma_space": _p_float(75.0, 1.0, 200.0, "空间标准差")},
    "laplacian_sharpen": {"amount": _p_float(0.5, 0.0, 3.0, "锐化强度")},
    "unsharp_mask": {"kernel_size": _p_odd(7, 1, 31, "模糊核大小"), "amount": _p_float(1.0, 0.0, 3.0, "锐化强度")},
    "ideal_low_pass": {"radius": _p_int(30, 1, 300, "频域滤波半径")},
    "ideal_high_pass": {"radius": _p_int(30, 1, 300, "频域滤波半径")},
    "gaussian_low_pass": {"radius": _p_int(30, 1, 300, "频域滤波半径")},
    "gaussian_high_pass": {"radius": _p_int(30, 1, 300, "频域滤波半径")},
    "homomorphic_filter": {"cutoff": _p_float(30.0, 1.0, 300.0, "截止频率"), "gamma_low": _p_float(0.5, 0.1, 2.0, "低频增益"), "gamma_high": _p_float(1.5, 0.1, 5.0, "高频增益")},
    "rgb_channel": {"channel": _p_select("red", ["red", "green", "blue"], "显示通道")},
    "hsv_adjust": {"hue_shift": _p_int(0, -180, 180, "色相偏移"), "saturation_factor": _p_float(1.5, 0.0, 3.0, "饱和度系数"), "value_factor": _p_float(1.0, 0.0, 3.0, "明度系数")},
    "color_balance": {"blue_gain": _p_float(1.0, 0.0, 3.0, "蓝色增益"), "green_gain": _p_float(1.0, 0.0, 3.0, "绿色增益"), "red_gain": _p_float(1.1, 0.0, 3.0, "红色增益")},
    "pseudo_color": {"color_map": _p_select("jet", ["jet", "hot", "cool", "rainbow"], "颜色映射")},
    "anime_color_enhance": {"saturation_factor": _p_float(1.25, 0.0, 3.0, "饱和度系数"), "contrast": _p_float(1.15, 0.5, 3.0, "对比度系数")},
    "motion_blur": {"kernel_size": _p_odd(15, 3, 51, "运动模糊核大小")},
    "inverse_filter": {"amount": _p_float(0.8, 0.0, 3.0, "复原增强强度")},
    "wiener_filter": {"strength": _p_float(0.4, 0.0, 1.0, "平滑强度")},
    "denoise": {"h": _p_float(7.0, 1.0, 30.0, "去噪强度")},
    "inpaint": {"radius_percent": _p_int(8, 1, 30, "中心修复区域百分比"), "inpaint_radius": _p_int(3, 1, 15, "修复半径")},
    "erode": {"kernel_size": _p_odd(5, 1, 31, "结构元素大小"), "threshold": _p_int(127, 0, 255, "二值阈值")},
    "dilate": {"kernel_size": _p_odd(5, 1, 31, "结构元素大小"), "threshold": _p_int(127, 0, 255, "二值阈值")},
    "open_operation": {"kernel_size": _p_odd(5, 1, 31, "结构元素大小"), "threshold": _p_int(127, 0, 255, "二值阈值")},
    "close_operation": {"kernel_size": _p_odd(5, 1, 31, "结构元素大小"), "threshold": _p_int(127, 0, 255, "二值阈值")},
    "top_hat": {"kernel_size": _p_odd(5, 1, 31, "结构元素大小"), "threshold": _p_int(127, 0, 255, "二值阈值")},
    "black_hat": {"kernel_size": _p_odd(5, 1, 31, "结构元素大小"), "threshold": _p_int(127, 0, 255, "二值阈值")},
    "connected_components": {"threshold": _p_int(127, 0, 255, "二值阈值"), "min_area": _p_int(20, 0, 10000, "最小区域面积")},
    "sobel": {"kernel_size": _p_odd(3, 1, 7, "Sobel 核大小")},
    "laplace": {"kernel_size": _p_odd(3, 1, 7, "Laplace 核大小")},
    "log_edge": {"kernel_size": _p_odd(5, 3, 31, "高斯核大小"), "sigma": _p_float(1.0, 0.0, 10.0, "高斯标准差")},
    "canny": {"threshold1": _p_int(80, 0, 255, "低阈值"), "threshold2": _p_int(160, 0, 255, "高阈值"), "blur_size": _p_odd(3, 1, 15, "平滑核大小")},
    "hough_line": {"threshold": _p_int(80, 1, 300, "累加器阈值"), "min_line_length": _p_int(40, 1, 500, "最短线段长度"), "max_line_gap": _p_int(10, 0, 100, "最大线段间隔")},
    "hough_circle": {"min_radius": _p_int(5, 1, 300, "最小半径"), "max_radius": _p_int(80, 1, 500, "最大半径")},
    "anime_face_detect": {"scale_percent": _p_int(50, 10, 100, "中心框尺寸百分比")},
    "dominant_color_extract": {"color_count": _p_int(5, 2, 10, "主色数量")},
    "line_style_analyze": {"threshold1": _p_int(60, 0, 255, "低阈值"), "threshold2": _p_int(150, 0, 255, "高阈值")},
    "feature_extract": {"max_features": _p_int(200, 10, 1000, "最大特征点数")},
    "gallery_match": {"resize_width": _p_int(320, 64, 1024, "归一化宽度")},
}


def build_algorithm_meta(module: str, name: str) -> dict:
    """生成算法文件使用的统一元信息。"""
    display_name = DISPLAY_NAMES.get(name, name)
    module_description = MODULE_DESCRIPTIONS.get(module, "用于演示数字图像处理算法。")
    return {
        "module": module,
        "name": name,
        "display_name": display_name,
        "description": f"{module_description}当前文件提供 {display_name} 的可运行框架。",
        "params": PARAMS_BY_NAME.get(name, {}),
    }


def run_standard_algorithm(image: np.ndarray, params: dict | None, meta: dict) -> dict:
    """按照算法名称运行对应的简单实现或安全占位实现。"""
    _validate_image(image)
    params = {} if params is None else dict(params)
    name = str(meta.get("name", ""))
    handler = HANDLERS.get(name, _run_placeholder)
    return handler(_ensure_color(image), params, meta)


def _validate_image(image: np.ndarray) -> None:
    if image is None:
        raise ValueError("输入图像不能为空")
    if not isinstance(image, np.ndarray):
        raise TypeError("输入图像必须是 numpy.ndarray")
    if image.size == 0:
        raise ValueError("输入图像内容不能为空")


def _clamp_int(value, default: int, min_value: int, max_value: int) -> int:
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = default
    return max(min_value, min(max_value, value))


def _clamp_float(value, default: float, min_value: float, max_value: float) -> float:
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = default
    return max(min_value, min(max_value, value))


def _ensure_odd_int(value, default: int = 3, min_value: int = 1, max_value: int = 31) -> int:
    value = _clamp_int(value, default, min_value, max_value)
    if value % 2 == 0:
        value += 1
    if value > max_value:
        value = max_value if max_value % 2 == 1 else max_value - 1
    return max(min_value, value)


def _ensure_color(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return image.copy()


def _as_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image.copy()
    return cv2.cvtColor(_ensure_color(image), cv2.COLOR_BGR2GRAY)


def _clip_uint8(image: np.ndarray) -> np.ndarray:
    return np.clip(image, 0, 255).astype(np.uint8)


def _normalize_uint8(image: np.ndarray) -> np.ndarray:
    return _clip_uint8(cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX))


def _step(name: str, image: np.ndarray) -> dict:
    return {"name": name, "image": _clip_uint8(image)}


def _response(result: np.ndarray, steps: list[dict], metrics: dict, analysis: str) -> dict:
    return {"result": _clip_uint8(result), "steps": steps, "metrics": metrics, "analysis": analysis}


def _run_placeholder(image: np.ndarray, params: dict, meta: dict) -> dict:
    result = image.copy()
    display_name = meta.get("display_name", "算法")
    return _response(
        result,
        [_step("原始图像", image), _step("占位处理结果", result)],
        {},
        f"{display_name} 当前提供可运行占位框架，小组成员可直接替换 run(image, params) 内部逻辑。",
    )


def _run_image_add(image: np.ndarray, params: dict, meta: dict) -> dict:
    value = _clamp_int(params.get("value"), 40, 0, 255)
    result = cv2.add(image, np.full_like(image, value))
    return _response(result, [_step("原始图像", image), _step("图像加法结果", result)], {"value": value}, f"图像加法把每个通道增加 {value}。")


def _run_image_subtract(image: np.ndarray, params: dict, meta: dict) -> dict:
    value = _clamp_int(params.get("value"), 40, 0, 255)
    result = cv2.subtract(image, np.full_like(image, value))
    return _response(result, [_step("原始图像", image), _step("图像减法结果", result)], {"value": value}, f"图像减法把每个通道减少 {value}。")


def _run_image_blend(image: np.ndarray, params: dict, meta: dict) -> dict:
    alpha = _clamp_float(params.get("alpha"), 0.6, 0.0, 1.0)
    blur_size = _ensure_odd_int(params.get("blur_size"), 9, 1, 31)
    blurred = cv2.GaussianBlur(image, (blur_size, blur_size), 0)
    result = cv2.addWeighted(image, alpha, blurred, 1.0 - alpha, 0)
    return _response(result, [_step("原始图像", image), _step("模糊参考图", blurred), _step("融合结果", result)], {"alpha": alpha, "blur_size": blur_size}, "图像融合将原图与模糊图按权重叠加。")


def _run_logic_and(image: np.ndarray, params: dict, meta: dict) -> dict:
    threshold = _clamp_int(params.get("threshold"), 127, 0, 255)
    gray = _as_gray(image)
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    result = cv2.bitwise_and(image, image, mask=mask)
    return _response(result, [_step("二值掩膜", mask), _step("逻辑与结果", result)], {"threshold": threshold}, "逻辑与保留掩膜中的亮区域。")


def _run_logic_or(image: np.ndarray, params: dict, meta: dict) -> dict:
    value = _clamp_int(params.get("value"), 64, 0, 255)
    reference = np.full_like(image, value)
    result = cv2.bitwise_or(image, reference)
    return _response(result, [_step("参考图像", reference), _step("逻辑或结果", result)], {"value": value}, "逻辑或会提高低位像素值。")


def _run_logic_not(image: np.ndarray, params: dict, meta: dict) -> dict:
    result = cv2.bitwise_not(image)
    return _response(result, [_step("原始图像", image), _step("逻辑非结果", result)], {}, "逻辑非会反转每个像素的颜色。")


def _run_mask_apply(image: np.ndarray, params: dict, meta: dict) -> dict:
    radius_percent = _clamp_int(params.get("radius_percent"), 35, 5, 50)
    h, w = image.shape[:2]
    radius = max(1, int(min(h, w) * radius_percent / 100))
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (w // 2, h // 2), radius, 255, -1)
    result = cv2.bitwise_and(image, image, mask=mask)
    return _response(result, [_step("圆形掩膜", mask), _step("掩膜应用结果", result)], {"radius_percent": radius_percent, "radius": radius}, "掩膜应用只保留中心区域。")


def _run_resize(image: np.ndarray, params: dict, meta: dict) -> dict:
    scale = _clamp_float(params.get("scale"), 0.75, 0.1, 3.0)
    result = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    return _response(result, [_step("原始图像", image), _step("缩放结果", result)], {"scale": scale, "output_size": [int(result.shape[1]), int(result.shape[0])]}, "图像缩放改变图像尺寸。")


def _run_rotate(image: np.ndarray, params: dict, meta: dict) -> dict:
    angle = _clamp_float(params.get("angle"), 45.0, -360.0, 360.0)
    scale = _clamp_float(params.get("scale"), 1.0, 0.1, 3.0)
    h, w = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
    result = cv2.warpAffine(image, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
    return _response(result, [_step("原始图像", image), _step("旋转结果", result)], {"angle": angle, "scale": scale}, "图像旋转用于改变动漫图像方向。")


def _run_translate(image: np.ndarray, params: dict, meta: dict) -> dict:
    shift_x = _clamp_int(params.get("shift_x"), 30, -500, 500)
    shift_y = _clamp_int(params.get("shift_y"), 20, -500, 500)
    h, w = image.shape[:2]
    matrix = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    result = cv2.warpAffine(image, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
    return _response(result, [_step("原始图像", image), _step("平移结果", result)], {"shift_x": shift_x, "shift_y": shift_y}, "图像平移改变画面主体位置。")


def _run_affine(image: np.ndarray, params: dict, meta: dict) -> dict:
    offset = _clamp_float(params.get("offset"), 0.12, -0.4, 0.4)
    h, w = image.shape[:2]
    src = np.float32([[0, 0], [w - 1, 0], [0, h - 1]])
    dst = np.float32([[w * abs(offset), 0], [w - 1, h * abs(offset)], [0, h - 1]])
    result = cv2.warpAffine(image, cv2.getAffineTransform(src, dst), (w, h), borderMode=cv2.BORDER_REFLECT)
    return _response(result, [_step("原始图像", image), _step("仿射变换结果", result)], {"offset": offset}, "仿射变换会产生轻微倾斜效果。")


def _run_perspective(image: np.ndarray, params: dict, meta: dict) -> dict:
    margin_percent = _clamp_int(params.get("margin_percent"), 8, 0, 30)
    h, w = image.shape[:2]
    m = int(min(h, w) * margin_percent / 100)
    src = np.float32([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]])
    dst = np.float32([[m, m], [w - 1 - m, 0], [0, h - 1 - m], [w - 1, h - 1]])
    result = cv2.warpPerspective(image, cv2.getPerspectiveTransform(src, dst), (w, h), borderMode=cv2.BORDER_REFLECT)
    return _response(result, [_step("原始图像", image), _step("透视变换结果", result)], {"margin_percent": margin_percent}, "透视变换模拟视角变化。")


def _run_grayscale(image: np.ndarray, params: dict, meta: dict) -> dict:
    gray = _as_gray(image)
    return _response(gray, [_step("原始图像", image), _step("灰度化结果", gray)], {"mean_gray": float(np.mean(gray))}, "灰度化去除颜色信息，保留亮度结构。")


def _run_binary_threshold(image: np.ndarray, params: dict, meta: dict) -> dict:
    threshold = _clamp_int(params.get("threshold"), 127, 0, 255)
    gray = _as_gray(image)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return _response(binary, [_step("灰度图像", gray), _step("二值化结果", binary)], {"threshold": threshold, "foreground_ratio": float(np.count_nonzero(binary) / binary.size)}, "二值阈值把图像分成前景和背景。")


def _run_linear_transform(image: np.ndarray, params: dict, meta: dict) -> dict:
    alpha = _clamp_float(params.get("alpha"), 1.2, 0.1, 3.0)
    beta = _clamp_int(params.get("beta"), 10, -100, 100)
    result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return _response(result, [_step("原始图像", image), _step("线性变换结果", result)], {"alpha": alpha, "beta": beta}, "线性灰度变换调整整体对比度和亮度。")


def _run_gamma_transform(image: np.ndarray, params: dict, meta: dict) -> dict:
    gamma = _clamp_float(params.get("gamma"), 0.8, 0.1, 5.0)
    table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in range(256)], dtype=np.uint8)
    result = cv2.LUT(image, table)
    return _response(result, [_step("原始图像", image), _step("伽马变换结果", result)], {"gamma": gamma}, "伽马变换用于非线性亮度调整。")


def _run_log_transform(image: np.ndarray, params: dict, meta: dict) -> dict:
    gain = _clamp_float(params.get("gain"), 1.0, 0.1, 5.0)
    result = _normalize_uint8(gain * np.log1p(image.astype(np.float32)))
    return _response(result, [_step("原始图像", image), _step("对数变换结果", result)], {"gain": gain}, "对数变换会压缩高亮并提升暗部细节。")


def _run_histogram_equalization(image: np.ndarray, params: dict, meta: dict) -> dict:
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    equalized_y = cv2.equalizeHist(y)
    result = cv2.cvtColor(cv2.merge([equalized_y, cr, cb]), cv2.COLOR_YCrCb2BGR)
    return _response(result, [_step("亮度通道", y), _step("均衡化亮度通道", equalized_y), _step("均衡化结果", result)], {"mean_before": float(np.mean(y)), "mean_after": float(np.mean(equalized_y))}, "直方图均衡化增强亮度层次。")


def _run_clahe(image: np.ndarray, params: dict, meta: dict) -> dict:
    clip_limit = _clamp_float(params.get("clip_limit"), 2.0, 0.1, 10.0)
    tile_grid_size = _clamp_int(params.get("tile_grid_size"), 8, 2, 16)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
    enhanced_l = clahe.apply(l_channel)
    result = cv2.cvtColor(cv2.merge([enhanced_l, a_channel, b_channel]), cv2.COLOR_LAB2BGR)
    return _response(result, [_step("亮度通道", l_channel), _step("CLAHE 亮度通道", enhanced_l), _step("CLAHE 结果", result)], {"clip_limit": clip_limit, "tile_grid_size": tile_grid_size}, "CLAHE 对局部区域做亮度均衡。")


def _run_mean_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 5, 1, 31)
    result = cv2.blur(image, (kernel_size, kernel_size))
    return _response(result, [_step("原始图像", image), _step("均值滤波结果", result)], {"kernel_size": kernel_size}, "均值滤波用邻域平均平滑图像。")


def _run_gaussian_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 5, 1, 31)
    sigma = _clamp_float(params.get("sigma"), 1.0, 0.0, 10.0)
    result = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return _response(result, [_step("原始图像", image), _step("高斯滤波结果", result)], {"kernel_size": kernel_size, "sigma": sigma}, "高斯滤波按距离加权平滑图像。")


def _run_median_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 5, 1, 31)
    result = cv2.medianBlur(image, kernel_size)
    return _response(result, [_step("原始图像", image), _step("中值滤波结果", result)], {"kernel_size": kernel_size}, "中值滤波对椒盐噪声较有效。")


def _run_bilateral_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    diameter = _clamp_int(params.get("diameter"), 9, 1, 31)
    sigma_color = _clamp_float(params.get("sigma_color"), 75.0, 1.0, 200.0)
    sigma_space = _clamp_float(params.get("sigma_space"), 75.0, 1.0, 200.0)
    result = cv2.bilateralFilter(image, diameter, sigma_color, sigma_space)
    return _response(result, [_step("原始图像", image), _step("双边滤波结果", result)], {"diameter": diameter, "sigma_color": sigma_color, "sigma_space": sigma_space}, "双边滤波在平滑色块的同时尽量保留边缘。")


def _run_laplacian_sharpen(image: np.ndarray, params: dict, meta: dict) -> dict:
    amount = _clamp_float(params.get("amount"), 0.5, 0.0, 3.0)
    laplacian = cv2.Laplacian(image, cv2.CV_32F)
    result = _clip_uint8(image.astype(np.float32) - amount * laplacian)
    return _response(result, [_step("拉普拉斯响应", _normalize_uint8(np.abs(laplacian))), _step("锐化结果", result)], {"amount": amount}, "拉普拉斯锐化增强高频细节。")


def _run_unsharp_mask(image: np.ndarray, params: dict, meta: dict) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 7, 1, 31)
    amount = _clamp_float(params.get("amount"), 1.0, 0.0, 3.0)
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    result = cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)
    return _response(result, [_step("模糊图像", blurred), _step("反锐化掩膜结果", result)], {"kernel_size": kernel_size, "amount": amount}, "反锐化掩膜通过原图减去模糊图增强细节。")


def _frequency_filter(image: np.ndarray, params: dict, display: str, mode: str, gaussian: bool) -> dict:
    radius = _clamp_int(params.get("radius"), 30, 1, 300)
    gray = _as_gray(image)
    fft = np.fft.fftshift(np.fft.fft2(gray))
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    distance = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
    if gaussian:
        low_mask = np.exp(-(distance**2) / (2 * (radius**2)))
    else:
        low_mask = (distance <= radius).astype(np.float32)
    mask = low_mask if mode == "low" else 1.0 - low_mask
    filtered = fft * mask
    result = _normalize_uint8(np.abs(np.fft.ifft2(np.fft.ifftshift(filtered))))
    analysis = f"{display}用于{'保留平滑亮度成分、抑制高频细节' if mode == 'low' else '保留边缘和纹理等高频成分、抑制低频背景'}。"
    return _response(result, [_step("灰度图像", gray), _step("频域掩膜", _normalize_uint8(mask)), _step("滤波结果", result)], {"radius": radius}, analysis)


def _run_dft_spectrum(image: np.ndarray, params: dict, meta: dict) -> dict:
    gray = _as_gray(image)
    magnitude = 20 * np.log(np.abs(np.fft.fftshift(np.fft.fft2(gray))) + 1)
    result = _normalize_uint8(magnitude)
    return _response(result, [_step("灰度图像", gray), _step("频谱幅值图", result)], {"spectrum_mean": float(np.mean(result))}, "傅里叶频谱展示图像频率分布。")


def _run_homomorphic_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    cutoff = _clamp_float(params.get("cutoff"), 30.0, 1.0, 300.0)
    gamma_low = _clamp_float(params.get("gamma_low"), 0.5, 0.1, 2.0)
    gamma_high = _clamp_float(params.get("gamma_high"), 1.5, 0.1, 5.0)
    gray = _as_gray(image).astype(np.float32)
    log_image = np.log1p(gray)
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    distance2 = (x - ccol) ** 2 + (y - crow) ** 2
    high_boost = (gamma_high - gamma_low) * (1 - np.exp(-distance2 / (2 * cutoff * cutoff))) + gamma_low
    filtered = np.fft.fftshift(np.fft.fft2(log_image)) * high_boost
    result = _normalize_uint8(np.expm1(np.real(np.fft.ifft2(np.fft.ifftshift(filtered)))))
    return _response(result, [_step("灰度图像", gray), _step("同态滤波增益", _normalize_uint8(high_boost)), _step("同态滤波结果", result)], {"cutoff": cutoff, "gamma_low": gamma_low, "gamma_high": gamma_high}, "同态滤波通过压制低频照明并增强高频细节。")


def _run_rgb_channel(image: np.ndarray, params: dict, meta: dict) -> dict:
    channel = str(params.get("channel", "red")).lower()
    if channel not in {"red", "green", "blue"}:
        channel = "red"
    result = np.zeros_like(image)
    result[:, :, {"blue": 0, "green": 1, "red": 2}[channel]] = image[:, :, {"blue": 0, "green": 1, "red": 2}[channel]]
    return _response(result, [_step("原始图像", image), _step(f"{channel} 通道结果", result)], {"channel": channel}, "RGB 通道分离用于观察不同颜色通道的贡献。")


def _run_hsv_adjust(image: np.ndarray, params: dict, meta: dict) -> dict:
    hue_shift = _clamp_int(params.get("hue_shift"), 0, -180, 180)
    saturation_factor = _clamp_float(params.get("saturation_factor"), 1.5, 0.0, 3.0)
    value_factor = _clamp_float(params.get("value_factor"), 1.0, 0.0, 3.0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_factor, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * value_factor, 0, 255)
    result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    return _response(result, [_step("原始图像", image), _step("HSV 调整结果", result)], {"hue_shift": hue_shift, "saturation_factor": saturation_factor, "value_factor": value_factor}, "HSV 调整可改变色相、饱和度和明度。")


def _run_color_balance(image: np.ndarray, params: dict, meta: dict) -> dict:
    gains = np.array([
        _clamp_float(params.get("blue_gain"), 1.0, 0.0, 3.0),
        _clamp_float(params.get("green_gain"), 1.0, 0.0, 3.0),
        _clamp_float(params.get("red_gain"), 1.1, 0.0, 3.0),
    ], dtype=np.float32)
    result = _clip_uint8(image.astype(np.float32) * gains)
    return _response(result, [_step("原始图像", image), _step("色彩平衡结果", result)], {"blue_gain": float(gains[0]), "green_gain": float(gains[1]), "red_gain": float(gains[2])}, "色彩平衡通过分别调整 BGR 通道增益改变整体色调。")


def _run_pseudo_color(image: np.ndarray, params: dict, meta: dict) -> dict:
    color_map = str(params.get("color_map", "jet")).lower()
    maps = {"jet": cv2.COLORMAP_JET, "hot": cv2.COLORMAP_HOT, "cool": cv2.COLORMAP_COOL, "rainbow": cv2.COLORMAP_RAINBOW}
    if color_map not in maps:
        color_map = "jet"
    gray = _as_gray(image)
    result = cv2.applyColorMap(gray, maps[color_map])
    return _response(result, [_step("灰度图像", gray), _step("伪彩色结果", result)], {"color_map": color_map}, "伪彩色把灰度强度映射为颜色。")


def _run_anime_color_enhance(image: np.ndarray, params: dict, meta: dict) -> dict:
    saturation_factor = _clamp_float(params.get("saturation_factor"), 1.25, 0.0, 3.0)
    contrast = _clamp_float(params.get("contrast"), 1.15, 0.5, 3.0)
    smooth = cv2.bilateralFilter(image, 7, 50, 50)
    hsv = cv2.cvtColor(smooth, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_factor, 0, 255)
    enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    result = cv2.convertScaleAbs(enhanced, alpha=contrast, beta=0)
    return _response(result, [_step("双边平滑", smooth), _step("动漫色彩增强结果", result)], {"saturation_factor": saturation_factor, "contrast": contrast}, "动漫色彩增强让色块更鲜明。")


def _run_motion_blur(image: np.ndarray, params: dict, meta: dict) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 15, 3, 51)
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    kernel[kernel_size // 2, :] = 1.0 / kernel_size
    result = cv2.filter2D(image, -1, kernel)
    return _response(result, [_step("原始图像", image), _step("运动模糊结果", result)], {"kernel_size": kernel_size}, "运动模糊模型用于模拟横向相机或物体运动造成的退化效果。")


def _run_inverse_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    amount = _clamp_float(params.get("amount"), 0.8, 0.0, 3.0)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    result = cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)
    return _response(result, [_step("估计模糊图", blurred), _step("简化逆滤波结果", result)], {"amount": amount}, "当前为简化可运行的逆滤波占位实现。")


def _run_wiener_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    strength = _clamp_float(params.get("strength"), 0.4, 0.0, 1.0)
    denoised = cv2.fastNlMeansDenoisingColored(image, None, 5, 5, 7, 21)
    result = cv2.addWeighted(image, 1.0 - strength, denoised, strength, 0)
    return _response(result, [_step("去噪估计图", denoised), _step("简化维纳滤波结果", result)], {"strength": strength}, "当前为简化可运行的维纳滤波占位实现。")


def _run_denoise(image: np.ndarray, params: dict, meta: dict) -> dict:
    h = _clamp_float(params.get("h"), 7.0, 1.0, 30.0)
    result = cv2.fastNlMeansDenoisingColored(image, None, h, h, 7, 21)
    return _response(result, [_step("原始图像", image), _step("去噪结果", result)], {"h": h}, "非局部均值去噪可减少颜色噪声。")


def _run_inpaint(image: np.ndarray, params: dict, meta: dict) -> dict:
    radius_percent = _clamp_int(params.get("radius_percent"), 8, 1, 30)
    inpaint_radius = _clamp_int(params.get("inpaint_radius"), 3, 1, 15)
    h, w = image.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (w // 2, h // 2), max(1, int(min(h, w) * radius_percent / 100)), 255, -1)
    result = cv2.inpaint(image, mask, inpaint_radius, cv2.INPAINT_TELEA)
    return _response(result, [_step("修复掩膜", mask), _step("修复结果", result)], {"radius_percent": radius_percent, "inpaint_radius": inpaint_radius}, "图像修复根据掩膜周围内容估计缺损区域。")


def _run_morphology(image: np.ndarray, params: dict, meta: dict, operation: int, label: str) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 5, 1, 31)
    threshold = _clamp_int(params.get("threshold"), 127, 0, 255)
    gray = _as_gray(image)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    result = cv2.morphologyEx(binary, operation, kernel)
    return _response(result, [_step("二值图像", binary), _step(f"{label}结果", result)], {"kernel_size": kernel_size, "threshold": threshold}, f"{label}用于分析二值区域的结构变化。")


def _run_connected_components(image: np.ndarray, params: dict, meta: dict) -> dict:
    threshold = _clamp_int(params.get("threshold"), 127, 0, 255)
    min_area = _clamp_int(params.get("min_area"), 20, 0, 10000)
    gray = _as_gray(image)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(binary)
    result = np.zeros((*gray.shape, 3), dtype=np.uint8)
    valid_count = 0
    for label in range(1, count):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if area < min_area:
            continue
        valid_count += 1
        result[labels == label] = np.array([(label * 37) % 255, (label * 79) % 255, (label * 113) % 255], dtype=np.uint8)
    return _response(result, [_step("二值图像", binary), _step("连通域着色结果", result)], {"threshold": threshold, "min_area": min_area, "component_count": valid_count}, "连通域分析统计二值图中的独立区域。")


def _run_sobel(image: np.ndarray, params: dict, meta: dict) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 3, 1, 7)
    gray = _as_gray(image)
    grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=kernel_size)
    grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=kernel_size)
    result = _normalize_uint8(cv2.magnitude(grad_x, grad_y))
    return _response(result, [_step("灰度图像", gray), _step("Sobel 边缘结果", result)], {"kernel_size": kernel_size}, "Sobel 边缘检测通过水平和垂直梯度突出轮廓。")


def _run_scharr(image: np.ndarray, params: dict, meta: dict) -> dict:
    gray = _as_gray(image)
    result = _normalize_uint8(cv2.magnitude(cv2.Scharr(gray, cv2.CV_32F, 1, 0), cv2.Scharr(gray, cv2.CV_32F, 0, 1)))
    return _response(result, [_step("灰度图像", gray), _step("Scharr 边缘结果", result)], {}, "Scharr 算子对小尺寸梯度更敏感。")


def _run_laplace(image: np.ndarray, params: dict, meta: dict) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 3, 1, 7)
    gray = _as_gray(image)
    result = _normalize_uint8(np.abs(cv2.Laplacian(gray, cv2.CV_32F, ksize=kernel_size)))
    return _response(result, [_step("灰度图像", gray), _step("Laplace 边缘结果", result)], {"kernel_size": kernel_size}, "Laplace 边缘检测对二阶灰度变化敏感。")


def _run_log_edge(image: np.ndarray, params: dict, meta: dict) -> dict:
    kernel_size = _ensure_odd_int(params.get("kernel_size"), 5, 3, 31)
    sigma = _clamp_float(params.get("sigma"), 1.0, 0.0, 10.0)
    gray = _as_gray(image)
    blurred = cv2.GaussianBlur(gray, (kernel_size, kernel_size), sigma)
    result = _normalize_uint8(np.abs(cv2.Laplacian(blurred, cv2.CV_32F)))
    return _response(result, [_step("高斯平滑", blurred), _step("LoG 边缘结果", result)], {"kernel_size": kernel_size, "sigma": sigma}, "LoG 先平滑再检测二阶边缘。")


def _run_canny(image: np.ndarray, params: dict, meta: dict) -> dict:
    threshold1 = _clamp_int(params.get("threshold1"), 80, 0, 255)
    threshold2 = _clamp_int(params.get("threshold2"), 160, 0, 255)
    blur_size = _ensure_odd_int(params.get("blur_size"), 3, 1, 15)
    gray = _as_gray(image)
    blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)
    result = cv2.Canny(blurred, threshold1, threshold2)
    return _response(result, [_step("高斯平滑", blurred), _step("Canny 边缘结果", result)], {"threshold1": threshold1, "threshold2": threshold2, "blur_size": blur_size}, "Canny 边缘检测可稳定提取动漫人物轮廓和场景线条。")


def _run_hough_line(image: np.ndarray, params: dict, meta: dict) -> dict:
    threshold = _clamp_int(params.get("threshold"), 80, 1, 300)
    min_line_length = _clamp_int(params.get("min_line_length"), 40, 1, 500)
    max_line_gap = _clamp_int(params.get("max_line_gap"), 10, 0, 100)
    edges = cv2.Canny(_as_gray(image), 80, 160)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)
    result = image.copy()
    line_count = 0
    if lines is not None:
        for line in lines[:200]:
            x1, y1, x2, y2 = line[0]
            cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 2)
            line_count += 1
    return _response(result, [_step("边缘图像", edges), _step("霍夫直线检测结果", result)], {"line_count": line_count}, "霍夫直线检测用于提取规则线条结构。")


def _run_hough_circle(image: np.ndarray, params: dict, meta: dict) -> dict:
    min_radius = _clamp_int(params.get("min_radius"), 5, 1, 300)
    max_radius = _clamp_int(params.get("max_radius"), 80, min_radius, 500)
    gray = cv2.medianBlur(_as_gray(image), 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30, param1=100, param2=30, minRadius=min_radius, maxRadius=max_radius)
    result = image.copy()
    circle_count = 0
    if circles is not None:
        for x, y, r in np.uint16(np.around(circles[0, :50])):
            cv2.circle(result, (int(x), int(y)), int(r), (0, 255, 0), 2)
            circle_count += 1
    return _response(result, [_step("平滑灰度图像", gray), _step("霍夫圆检测结果", result)], {"circle_count": circle_count}, "霍夫圆检测用于查找圆形或近圆形结构。")


def _run_anime_face_detect(image: np.ndarray, params: dict, meta: dict) -> dict:
    scale_percent = _clamp_int(params.get("scale_percent"), 50, 10, 100)
    result = image.copy()
    h, w = result.shape[:2]
    box_w = int(w * scale_percent / 100)
    box_h = int(h * scale_percent / 100)
    x1 = max(0, (w - box_w) // 2)
    y1 = max(0, (h - box_h) // 2)
    cv2.rectangle(result, (x1, y1), (min(w - 1, x1 + box_w), min(h - 1, y1 + box_h)), (0, 255, 255), 2)
    return _response(result, [_step("原始图像", image), _step("动漫人脸检测占位结果", result)], {"candidate_boxes": 1}, "当前为动漫人脸检测占位框架。")


def _run_dominant_color_extract(image: np.ndarray, params: dict, meta: dict) -> dict:
    color_count = _clamp_int(params.get("color_count"), 5, 2, 10)
    small = cv2.resize(image, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    samples = small.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(samples, color_count, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
    centers = _clip_uint8(centers)
    counts = np.bincount(labels.flatten(), minlength=color_count)
    order = np.argsort(-counts)
    palette = np.zeros((80, 80 * color_count, 3), dtype=np.uint8)
    for idx, center_index in enumerate(order):
        palette[:, idx * 80 : (idx + 1) * 80] = centers[center_index]
    return _response(palette, [_step("原始图像", image), _step("主色调色板", palette)], {"color_count": color_count, "dominant_colors_bgr": centers[order].tolist()}, "主色提取统计动漫图像中最主要的色彩。")


def _run_line_style_analyze(image: np.ndarray, params: dict, meta: dict) -> dict:
    threshold1 = _clamp_int(params.get("threshold1"), 60, 0, 255)
    threshold2 = _clamp_int(params.get("threshold2"), 150, 0, 255)
    edges = cv2.Canny(_as_gray(image), threshold1, threshold2)
    return _response(edges, [_step("线条提取结果", edges)], {"edge_density": float(np.count_nonzero(edges) / edges.size)}, "线条风格分析通过边缘密度粗略描述线稿复杂程度。")


def _run_feature_extract(image: np.ndarray, params: dict, meta: dict) -> dict:
    max_features = _clamp_int(params.get("max_features"), 200, 10, 1000)
    gray = _as_gray(image)
    keypoints, _ = cv2.ORB_create(nfeatures=max_features).detectAndCompute(gray, None)
    result = cv2.drawKeypoints(image, keypoints or [], None, color=(0, 255, 0), flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    return _response(result, [_step("灰度图像", gray), _step("ORB 特征点结果", result)], {"feature_count": len(keypoints or [])}, "特征提取使用 ORB 关键点作为轻量示例。")


def _run_gallery_match(image: np.ndarray, params: dict, meta: dict) -> dict:
    resize_width = _clamp_int(params.get("resize_width"), 320, 64, 1024)
    h, w = image.shape[:2]
    result = cv2.resize(image, (resize_width, max(1, int(h * resize_width / max(1, w)))), interpolation=cv2.INTER_AREA)
    return _response(result, [_step("原始图像", image), _step("图库匹配归一化图像", result)], {"resize_width": resize_width}, "当前为图库匹配占位框架，仅完成尺寸归一化。")


HANDLERS = {
    "image_add": _run_image_add,
    "image_subtract": _run_image_subtract,
    "image_blend": _run_image_blend,
    "logic_and": _run_logic_and,
    "logic_or": _run_logic_or,
    "logic_not": _run_logic_not,
    "mask_apply": _run_mask_apply,
    "resize": _run_resize,
    "rotate": _run_rotate,
    "translate": _run_translate,
    "affine": _run_affine,
    "perspective": _run_perspective,
    "grayscale": _run_grayscale,
    "binary_threshold": _run_binary_threshold,
    "linear_transform": _run_linear_transform,
    "gamma_transform": _run_gamma_transform,
    "log_transform": _run_log_transform,
    "histogram_equalization": _run_histogram_equalization,
    "clahe": _run_clahe,
    "mean_filter": _run_mean_filter,
    "gaussian_filter": _run_gaussian_filter,
    "median_filter": _run_median_filter,
    "bilateral_filter": _run_bilateral_filter,
    "laplacian_sharpen": _run_laplacian_sharpen,
    "unsharp_mask": _run_unsharp_mask,
    "dft_spectrum": _run_dft_spectrum,
    "ideal_low_pass": lambda image, params, meta: _frequency_filter(image, params, "理想低通滤波", "low", False),
    "ideal_high_pass": lambda image, params, meta: _frequency_filter(image, params, "理想高通滤波", "high", False),
    "gaussian_low_pass": lambda image, params, meta: _frequency_filter(image, params, "高斯低通滤波", "low", True),
    "gaussian_high_pass": lambda image, params, meta: _frequency_filter(image, params, "高斯高通滤波", "high", True),
    "homomorphic_filter": _run_homomorphic_filter,
    "rgb_channel": _run_rgb_channel,
    "hsv_adjust": _run_hsv_adjust,
    "color_balance": _run_color_balance,
    "pseudo_color": _run_pseudo_color,
    "anime_color_enhance": _run_anime_color_enhance,
    "motion_blur": _run_motion_blur,
    "inverse_filter": _run_inverse_filter,
    "wiener_filter": _run_wiener_filter,
    "denoise": _run_denoise,
    "inpaint": _run_inpaint,
    "erode": lambda image, params, meta: _run_morphology(image, params, meta, cv2.MORPH_ERODE, "腐蚀"),
    "dilate": lambda image, params, meta: _run_morphology(image, params, meta, cv2.MORPH_DILATE, "膨胀"),
    "open_operation": lambda image, params, meta: _run_morphology(image, params, meta, cv2.MORPH_OPEN, "开运算"),
    "close_operation": lambda image, params, meta: _run_morphology(image, params, meta, cv2.MORPH_CLOSE, "闭运算"),
    "top_hat": lambda image, params, meta: _run_morphology(image, params, meta, cv2.MORPH_TOPHAT, "顶帽变换"),
    "black_hat": lambda image, params, meta: _run_morphology(image, params, meta, cv2.MORPH_BLACKHAT, "黑帽变换"),
    "connected_components": _run_connected_components,
    "sobel": _run_sobel,
    "scharr": _run_scharr,
    "laplace": _run_laplace,
    "log_edge": _run_log_edge,
    "canny": _run_canny,
    "hough_line": _run_hough_line,
    "hough_circle": _run_hough_circle,
    "anime_face_detect": _run_anime_face_detect,
    "dominant_color_extract": _run_dominant_color_extract,
    "line_style_analyze": _run_line_style_analyze,
    "feature_extract": _run_feature_extract,
    "gallery_match": _run_gallery_match,
}


def _run_color_space_convert(image: np.ndarray, params: dict, meta: dict) -> dict:
    target_space = str(params.get("target_space", "gray")).lower()
    if target_space not in {"gray", "hsv", "lab"}:
        target_space = "gray"

    if target_space == "gray":
        gray = _as_gray(image)
        result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif target_space == "hsv":
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        result = cv2.cvtColor(converted, cv2.COLOR_HSV2BGR)
    else:
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        result = cv2.cvtColor(converted, cv2.COLOR_LAB2BGR)

    return _response(
        result,
        [_step("原始图像", image), _step("颜色空间转换结果", result)],
        {"target_space": target_space},
        "颜色空间转换用于演示 BGR 图像到灰度、HSV 或 LAB 空间的转换效果。",
    )


def _run_saturation_adjust(image: np.ndarray, params: dict, meta: dict) -> dict:
    return _run_hsv_adjust(image, params, meta)


def _run_flip(image: np.ndarray, params: dict, meta: dict) -> dict:
    flip_code = _clamp_int(params.get("flip_code"), 1, -1, 1)
    result = cv2.flip(image, flip_code)
    return _response(
        result,
        [_step("原始图像", image), _step("翻转结果", result)],
        {"flip_code": flip_code},
        "图像翻转用于演示水平、垂直或同时翻转的几何变换。",
    )


def _run_edge_detection(image: np.ndarray, params: dict, meta: dict) -> dict:
    return _run_canny(image, params, meta)


def _run_low_pass_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    return _frequency_filter(image, params, "低通滤波", "low", False)


def _run_high_pass_filter(image: np.ndarray, params: dict, meta: dict) -> dict:
    return _frequency_filter(image, params, "高通滤波", "high", False)


MODULE_DESCRIPTIONS.update({
    "grayscale_image": "用于演示灰度图像处理方法，便于完成灰度化、二值化、边缘和形态学处理。",
    "color_image": "用于演示彩色图像处理方法，便于完成颜色空间转换和饱和度调整。",
    "geometric_transform": "用于演示几何变换方法，便于完成缩放、旋转和翻转处理。",
    "frequency_analysis": "用于演示频域分析方法，便于观察动漫图像的频谱分布。",
})

DISPLAY_NAMES.update({
    "edge_detection": "边缘检测",
    "color_space_convert": "颜色空间转换",
    "saturation_adjust": "饱和度调整",
    "flip": "图像翻转",
    "low_pass_filter": "低通滤波",
    "high_pass_filter": "高通滤波",
})

PARAMS_BY_NAME.update({
    "edge_detection": {
        "threshold1": _p_int(80, 0, 255, "低阈值"),
        "threshold2": _p_int(160, 0, 255, "高阈值"),
        "blur_size": _p_odd(3, 1, 15, "平滑核大小"),
    },
    "color_space_convert": {
        "target_space": _p_select("gray", ["gray", "hsv", "lab"], "目标颜色空间"),
    },
    "saturation_adjust": {
        "hue_shift": _p_int(0, -180, 180, "色相偏移"),
        "saturation_factor": _p_float(1.5, 0.0, 3.0, "饱和度系数"),
        "value_factor": _p_float(1.0, 0.0, 3.0, "明度系数"),
    },
    "flip": {
        "flip_code": _p_int(1, -1, 1, "翻转方向"),
    },
    "low_pass_filter": {
        "radius": _p_int(30, 1, 300, "频域滤波半径"),
    },
    "high_pass_filter": {
        "radius": _p_int(30, 1, 300, "频域滤波半径"),
    },
})

HANDLERS.update({
    "edge_detection": _run_edge_detection,
    "color_space_convert": _run_color_space_convert,
    "saturation_adjust": _run_saturation_adjust,
    "flip": _run_flip,
    "low_pass_filter": _run_low_pass_filter,
    "high_pass_filter": _run_high_pass_filter,
})
