# 本文件用于实现图像缩放功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "resize",
    "display_name": "图像缩放",
    "description": "按比例改变图像宽高，适合观察不同尺寸下的图像处理效果。",
    "params": {
        "scale": {"type": "float", "default": 0.75, "min": 0.1, "max": 3.0, "step": 0.05, "label": "缩放比例", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}
    original = _ensure_uint8(image)
    scale = _get_float_param(params, "scale")
    height, width = original.shape[:2]
    new_width = max(1, int(round(width * scale)))
    new_height = max(1, int(round(height * scale)))
    interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
    result = cv2.resize(original, (new_width, new_height), interpolation=interpolation)
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": original}, {"name": "缩放结果", "image": result}],
        "metrics": {"scale": scale, "original_width": width, "original_height": height, "new_width": new_width, "new_height": new_height},
        "analysis": f"已按 {scale:.2f} 倍比例缩放图像，输出尺寸为 {new_width} x {new_height}。",
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
