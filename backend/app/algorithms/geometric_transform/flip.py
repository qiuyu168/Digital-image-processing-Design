# 本文件用于实现图像翻转功能
from __future__ import annotations

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "geometric_transform",
    "name": "flip",
    "display_name": "图像翻转",
    "description": "实现水平、垂直或中心翻转，常用于图像增强和构图方向调整。",
    "params": {
        "flip_code": {
            "type": "select",
            "default": 1,
            "label": "翻转方向",
            "component": "select",
            "options": [
                {"label": "水平翻转", "value": 1},
                {"label": "垂直翻转", "value": 0},
                {"label": "中心翻转", "value": -1},
            ],
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    params = params or {}
    original = _ensure_uint8(image)
    flip_code = _get_flip_code(params)
    result = cv2.flip(original, flip_code)
    direction = {1: "水平翻转", 0: "垂直翻转", -1: "中心翻转"}[flip_code]
    return {
        "result": result,
        "steps": [{"name": "原始图像", "image": original}, {"name": direction, "image": result}],
        "metrics": {"flip_code": flip_code, "direction": direction},
        "analysis": f"已执行{direction}，图像尺寸和像素数据类型保持不变。",
    }


def _get_flip_code(params: dict) -> int:
    try:
        value = int(params.get("flip_code", ALGORITHM_META["params"]["flip_code"]["default"]))
    except (TypeError, ValueError):
        value = int(ALGORITHM_META["params"]["flip_code"]["default"])
    return value if value in {-1, 0, 1} else 1


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
