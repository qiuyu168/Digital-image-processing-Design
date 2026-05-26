# 本文件用于实现图像旋转功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "rotate",
    "display_name": "图像旋转",
    "description": "围绕图像中心按指定角度旋转，保持原始画布大小并使用反射边界填充。",
    "params": {
        "angle": {"type": "float", "default": 45.0, "min": -360.0, "max": 360.0, "step": 1.0, "label": "旋转角度", "component": "slider"},
        "scale": {"type": "float", "default": 1.0, "min": 0.1, "max": 3.0, "step": 0.1, "label": "缩放比例", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}
    original = _ensure_uint8(image)
    angle = _get_float_param(params, "angle")
    scale = _get_float_param(params, "scale")
    height, width = original.shape[:2]
    center = (width / 2.0, height / 2.0)
    matrix = cv2.getRotationMatrix2D(center, angle, scale)
    result = cv2.warpAffine(original, matrix, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": original}, {"name": "旋转结果", "image": result}],
        "metrics": {"angle": angle, "scale": scale, "width": width, "height": height},
        "analysis": f"已围绕图像中心旋转 {angle:.1f} 度，缩放比例为 {scale:.2f}，画布尺寸保持不变。",
    }


def _get_float_param(params: dict, name: str) -> float:
    meta = ALGORITHM_META["params"][name]
    try:
        value = float(params.get(name, meta["default"]))
    except (TypeError, ValueError):
        value = float(meta["default"])
    return float(np.clip(value, meta["min"], meta["max"]))


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.asarray(image)
    if array.size == 0:
        raise ValueError("输入图像不能为空数组")
    if array.dtype == np.uint8:
        return np.ascontiguousarray(array)
    array = np.nan_to_num(array.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    if 0.0 <= float(np.min(array)) and float(np.max(array)) <= 1.0:
        array = array * 255.0
    return np.ascontiguousarray(np.clip(array, 0, 255).astype(np.uint8))
