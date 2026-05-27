# 本文件用于在 OpenCV 图像数组和前端 PNG Base64 字符串之间转换
from __future__ import annotations

import base64
import re

import cv2
import numpy as np


DATA_URL_PATTERN = re.compile(r"^data:image/[^;]+;base64,", re.IGNORECASE)


def normalize_image_for_display(image: np.ndarray) -> np.ndarray:
    """将算法输出转换为可安全显示和编码的 uint8 图像。"""
    if image is None:
        raise ValueError("图像不能为空")

    array = np.asarray(image)
    if array.size == 0:
        raise ValueError("图像数组不能为空")

    if array.dtype == np.bool_:
        array = array.astype(np.uint8) * 255
    elif array.dtype != np.uint8:
        array = np.nan_to_num(array.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
        min_value = float(np.min(array))
        max_value = float(np.max(array))
        if 0.0 <= min_value and max_value <= 1.0:
            array = array * 255.0
        array = np.clip(array, 0, 255).astype(np.uint8)

    if array.ndim == 2:
        return np.ascontiguousarray(array)
    if array.ndim == 3 and array.shape[2] == 1:
        return np.ascontiguousarray(array[:, :, 0])
    if array.ndim == 3 and array.shape[2] in (3, 4):
        return np.ascontiguousarray(array)

    raise ValueError("图像必须是灰度图、BGR 图或 BGRA 图")


def image_to_base64(image: np.ndarray) -> str:
    """将图像编码为前端可直接展示的 PNG Base64 Data URL。"""
    display_image = normalize_image_for_display(image)
    success, encoded = cv2.imencode(".png", display_image)
    if not success:
        raise ValueError("图像 PNG 编码失败")
    payload = base64.b64encode(encoded.tobytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def base64_to_image(data: str) -> np.ndarray:
    """将 Base64 Data URL 或纯 Base64 字符串解码为 OpenCV BGR 图像。"""
    if not data:
        raise ValueError("Base64 图像数据不能为空")

    payload = DATA_URL_PATTERN.sub("", data.strip())
    try:
        raw = base64.b64decode(payload, validate=True)
    except Exception as exc:
        raise ValueError("Base64 图像数据解码失败") from exc

    buffer = np.frombuffer(raw, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Base64 图像内容不是有效图像")
    return np.ascontiguousarray(image)
