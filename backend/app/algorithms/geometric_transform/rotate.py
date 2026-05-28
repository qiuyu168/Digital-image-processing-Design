# 本文件用于实现支持任意中心的图像旋转功能
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import ensure_uint8, slider_value


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "rotate",
    "display_name": "图像旋转",
    "description": "围绕指定旋转中心按给定角度旋转图像，保持原始画布大小。",
    "params": {
        "angle": {"type": "float", "default": 45.0, "min": -360.0, "max": 360.0, "step": 1.0, "label": "旋转角度", "component": "slider"},
        "scale": {"type": "float", "default": 1.0, "min": 0.1, "max": 3.0, "step": 0.1, "label": "缩放比例", "component": "slider"},
        "center_x_ratio": {"type": "float", "default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "label": "旋转中心X比例", "component": "slider"},
        "center_y_ratio": {"type": "float", "default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01, "label": "旋转中心Y比例", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = ensure_uint8(image)
    angle = slider_value(params, "angle", ALGORITHM_META)
    scale = slider_value(params, "scale", ALGORITHM_META)
    center_x_ratio = slider_value(params, "center_x_ratio", ALGORITHM_META)
    center_y_ratio = slider_value(params, "center_y_ratio", ALGORITHM_META)
    height, width = source.shape[:2]
    center = (center_x_ratio * (width - 1), center_y_ratio * (height - 1))
    matrix = cv2.getRotationMatrix2D(center, angle, scale)
    result = cv2.warpAffine(
        source,
        matrix,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101,
    ).astype(np.uint8)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {
            "angle": angle,
            "scale": scale,
            "center_x_ratio": center_x_ratio,
            "center_y_ratio": center_y_ratio,
            "width": width,
            "height": height,
        },
        "analysis": f"已围绕指定中心旋转 {angle:.1f} 度，缩放比例为 {scale:.2f}，画布尺寸保持不变。",
    }

