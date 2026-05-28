# 本文件用于实现彩色图像综合处理入口
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, slider_value, to_bgr


ALGORITHM_META = {
    "module": "color_image",
    "name": "color_comprehensive_processing",
    "display_name": "彩色图像综合处理",
    "description": "在 HSV 和 BGR 空间综合调整亮度、对比度、饱和度和锐化强度。",
    "params": {
        "brightness": {"type": "float", "default": 0.0, "min": -100.0, "max": 100.0, "step": 1.0, "label": "亮度偏移", "component": "slider"},
        "contrast": {"type": "float", "default": 1.0, "min": 0.2, "max": 3.0, "step": 0.1, "label": "对比度系数", "component": "slider"},
        "saturation": {"type": "float", "default": 1.2, "min": 0.0, "max": 3.0, "step": 0.1, "label": "饱和度系数", "component": "slider"},
        "sharpness": {"type": "float", "default": 0.5, "min": 0.0, "max": 3.0, "step": 0.1, "label": "锐化强度", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    brightness = slider_value(params, "brightness", ALGORITHM_META)
    contrast = slider_value(params, "contrast", ALGORITHM_META)
    saturation = slider_value(params, "saturation", ALGORITHM_META)
    sharpness = slider_value(params, "sharpness", ALGORITHM_META)
    adjusted = clip_uint8(source.astype(np.float32) * contrast + brightness)
    hsv = cv2.cvtColor(adjusted, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255)
    color_adjusted = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    blurred = cv2.GaussianBlur(color_adjusted, (0, 0), 1.2)
    result = clip_uint8(cv2.addWeighted(color_adjusted, 1.0 + sharpness, blurred, -sharpness, 0))
    return {
        "result": result,
        "steps": [
            {"name": "原始图像", "image": source},
            {"name": "颜色调整", "image": color_adjusted},
            {"name": "处理结果", "image": result},
        ],
        "metrics": {
            "brightness": brightness,
            "contrast": contrast,
            "saturation": saturation,
            "sharpness": sharpness,
            **gray_metrics(source, result),
        },
        "analysis": "彩色图像综合处理同时调整亮度、对比度、饱和度和锐化，适合快速改善动漫图像整体观感。",
    }
