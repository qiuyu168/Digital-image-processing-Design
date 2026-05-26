# 本文件用于实现动漫图像的色彩增强功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "color_image",
    "name": "anime_color_enhance",
    "display_name": "动漫色彩增强",
    "description": "综合亮度、饱和度和对比度调整，突出动漫图像的主题风格。通过 HSV 空间分别控制亮度与饱和度，并结合 CLAHE 局部对比度增强实现。",
    "params": {
        "brightness": {
            "type": "float",
            "default": 1.1,
            "min": 0.5,
            "max": 2.0,
            "step": 0.1,
            "label": "亮度系数",
            "component": "slider"
        },
        "saturation": {
            "type": "float",
            "default": 1.3,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "饱和度系数",
            "component": "slider"
        },
        "contrast": {
            "type": "float",
            "default": 1.2,
            "min": 0.5,
            "max": 2.0,
            "step": 0.1,
            "label": "对比度系数",
            "component": "slider"
        }
    }
}


def run(image: np.ndarray, params: dict = None) -> dict:
    """统一算法入口函数。"""
    if image is None:
        raise ValueError("输入图像不能为空")

    if params is None:
        params = {}

    # 1. 读取并校验参数，使用与 ALGORITHM_META 一致的默认值
    brightness = float(params.get("brightness", 1.1))
    saturation = float(params.get("saturation", 1.3))
    contrast = float(params.get("contrast", 1.2))

    brightness = max(0.5, min(2.0, brightness))
    saturation = max(0.0, min(3.0, saturation))
    contrast = max(0.5, min(2.0, contrast))

    # 2. 处理灰度 / Alpha 通道
    is_gray = (len(image.shape) == 2)
    has_alpha = (len(image.shape) == 3 and image.shape[2] == 4)

    if has_alpha:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]
    elif is_gray:
        bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        alpha = None
    else:
        bgr = image
        alpha = None

    steps = []
    metrics = {}
    analysis = ""

    # 3. 根据是否为灰度选择不同处理路径
    if is_gray:
        # 灰度图像仅做 CLAHE 对比度增强
        clahe = cv2.createCLAHE(clipLimit=contrast * 2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(image)
        result = cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2BGR)

        # 保留原图的 BGR 版本用于步骤展示
        original_display = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        steps = [
            {"name": "原始图像", "image": original_display},
            {"name": "CLAHE 对比度增强结果", "image": result}
        ]

        mean_before = float(np.mean(image))
        mean_after = float(np.mean(enhanced_gray))
        metrics = {
            "mean_pixel_before": round(mean_before, 2),
            "mean_pixel_after": round(mean_after, 2)
        }
        analysis = (
            f"对比度系数为 {contrast:.1f}（CLAHE）。"
            f"灰度图像仅应用了局部对比度增强，使明暗层次更加分明，"
            f"动漫线稿或灰度插画的细节更加清晰。"
        )

    else:
        # 4. 彩色图像处理
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
        h, s, v = cv2.split(hsv)

        # 5. 对 V 通道做 CLAHE 局部对比度增强
        v_u8 = np.clip(v, 0.0, 255.0).astype(np.uint8)
        clahe = cv2.createCLAHE(clipLimit=contrast * 2.0, tileGridSize=(8, 8))
        v_clahe = clahe.apply(v_u8).astype(np.float32)

        # 6. 生成中间结果（仅 CLAHE 增强）供分步展示
        hsv_mid = cv2.merge([h, s, v_clahe])
        hsv_mid = np.clip(hsv_mid, 0.0, 255.0).astype(np.uint8)
        mid_result = cv2.cvtColor(hsv_mid, cv2.COLOR_HSV2BGR)

        # 7. 调整亮度（V 通道缩放）
        v_enhanced = np.clip(v_clahe * brightness, 0.0, 255.0)

        # 8. 调整饱和度（S 通道缩放）
        s_enhanced = np.clip(s * saturation, 0.0, 255.0)

        # 9. 合并通道并转回 BGR
        hsv_final = cv2.merge([h, s_enhanced, v_enhanced])
        hsv_final = np.clip(hsv_final, 0.0, 255.0).astype(np.uint8)
        result_bgr = cv2.cvtColor(hsv_final, cv2.COLOR_HSV2BGR)

        # 10. 如果有 Alpha 通道，合并回去
        if has_alpha:
            result = np.dstack((result_bgr, alpha))
        else:
            result = result_bgr

        # 11. 统计指标
        gray_before = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        gray_after = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2GRAY)
        metrics = {
            "mean_brightness_before": round(float(np.mean(v_u8)), 2),
            "mean_brightness_after": round(float(np.mean(v_enhanced)), 2),
            "mean_saturation_before": round(float(np.mean(s)), 2),
            "mean_saturation_after": round(float(np.mean(s_enhanced)), 2),
            "std_contrast_before": round(float(np.std(gray_before)), 2),
            "std_contrast_after": round(float(np.std(gray_after)), 2)
        }

        # 12. 组织分步结果
        steps = [
            {"name": "原始图像", "image": bgr.copy()},
            {"name": "CLAHE 对比度增强（V 通道）", "image": mid_result},
            {"name": "动漫色彩增强结果", "image": result}
        ]

        analysis = (
            f"亮度系数 {brightness:.1f}，饱和度系数 {saturation:.1f}，对比度系数 {contrast:.1f}（CLAHE）。"
            f"平均亮度从 {metrics['mean_brightness_before']:.1f} 变为 {metrics['mean_brightness_after']:.1f}，"
            f"平均饱和度从 {metrics['mean_saturation_before']:.1f} 变为 {metrics['mean_saturation_after']:.1f}。"
            f"CLAHE 局部对比度增强让画面明暗层次更丰富，"
            f"适当提高饱和度和亮度使动漫角色的发色、服装和场景色彩更加鲜明突出。"
        )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }