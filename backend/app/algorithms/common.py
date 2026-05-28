# 本文件提供新增数字图像处理算法共用的图像准备和数值工具
from __future__ import annotations

from typing import Any

import cv2
import numpy as np


def ensure_uint8(image: np.ndarray) -> np.ndarray:
    """Return a contiguous uint8 copy that is safe for OpenCV operations."""
    if image is None:
        raise ValueError("输入图像不能为空")
    array = np.asarray(image)
    if array.size == 0:
        raise ValueError("输入图像不能为空数组")
    array = np.ascontiguousarray(array)
    if array.dtype == np.uint8:
        return array.copy()

    values = np.nan_to_num(array.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    if 0.0 <= float(np.min(values)) and float(np.max(values)) <= 1.0:
        values = values * 255.0
    return np.clip(values, 0, 255).astype(np.uint8)


def to_bgr(image: np.ndarray) -> np.ndarray:
    """Normalize grayscale, BGR, and BGRA images to BGR uint8."""
    source = ensure_uint8(image)
    if source.ndim == 2:
        return cv2.cvtColor(source, cv2.COLOR_GRAY2BGR)
    if source.ndim != 3:
        raise ValueError("输入图像必须是二维灰度图或三维彩色图")
    if source.shape[2] == 1:
        return cv2.cvtColor(source[:, :, 0], cv2.COLOR_GRAY2BGR)
    if source.shape[2] == 4:
        return cv2.cvtColor(source, cv2.COLOR_BGRA2BGR)
    if source.shape[2] >= 3:
        return np.ascontiguousarray(source[:, :, :3])
    raise ValueError("输入图像通道数不正确")


def to_gray(image: np.ndarray) -> np.ndarray:
    """Normalize grayscale, BGR, and BGRA images to a single uint8 gray channel."""
    source = ensure_uint8(image)
    if source.ndim == 2:
        return np.ascontiguousarray(source)
    if source.ndim != 3:
        raise ValueError("输入图像必须是二维灰度图或三维彩色图")
    if source.shape[2] == 1:
        return np.ascontiguousarray(source[:, :, 0])
    if source.shape[2] == 4:
        return cv2.cvtColor(source, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(source[:, :, :3], cv2.COLOR_BGR2GRAY)


def resize_like(second_image: np.ndarray, first_image: np.ndarray) -> np.ndarray:
    """Resize the second image to match the first image height and width."""
    if second_image.shape[:2] == first_image.shape[:2]:
        return second_image.copy()
    height, width = first_image.shape[:2]
    return cv2.resize(second_image, (width, height), interpolation=cv2.INTER_LINEAR)


def require_second_image(params: dict | None) -> np.ndarray:
    """Extract the injected second image or raise a clear request error."""
    if not isinstance(params, dict) or params.get("_second_image") is None:
        raise ValueError("This algorithm requires second_image_path / _second_image")
    second_image = params["_second_image"]
    if not isinstance(second_image, np.ndarray):
        raise ValueError("第二张图像必须是 numpy.ndarray")
    return second_image


def slider_value(params: dict[str, Any], name: str, meta: dict[str, Any]) -> float:
    param_meta = meta["params"][name]
    try:
        value = float(params.get(name, param_meta["default"]))
    except (TypeError, ValueError):
        value = float(param_meta["default"])
    return float(np.clip(value, param_meta["min"], param_meta["max"]))


def int_slider_value(params: dict[str, Any], name: str, meta: dict[str, Any]) -> int:
    param_meta = meta["params"][name]
    try:
        value = int(round(float(params.get(name, param_meta["default"]))))
    except (TypeError, ValueError):
        value = int(param_meta["default"])
    return int(np.clip(value, param_meta["min"], param_meta["max"]))


def odd_int_slider_value(params: dict[str, Any], name: str, meta: dict[str, Any]) -> int:
    value = int_slider_value(params, name, meta)
    param_meta = meta["params"][name]
    if value % 2 == 0:
        value += 1 if value < int(param_meta["max"]) else -1
    return max(int(param_meta["min"]), value)


def bool_select_value(params: dict[str, Any], name: str, meta: dict[str, Any]) -> bool:
    param_meta = meta["params"][name]
    value = params.get(name, param_meta["default"])
    if isinstance(value, bool):
        return value
    return str(value).lower().strip() in {"true", "1", "yes", "color"}


def normalize_uint8(values: np.ndarray) -> np.ndarray:
    values = np.nan_to_num(np.asarray(values, dtype=np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    minimum = float(np.min(values))
    maximum = float(np.max(values))
    if maximum <= minimum:
        return np.zeros(values.shape, dtype=np.uint8)
    return cv2.normalize(values, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def clip_uint8(values: np.ndarray) -> np.ndarray:
    return np.clip(np.nan_to_num(values, nan=0.0, posinf=255.0, neginf=0.0), 0, 255).astype(np.uint8)


def gray_metrics(before: np.ndarray, after: np.ndarray) -> dict[str, float]:
    before_gray = to_gray(before).astype(np.float32)
    after_gray = to_gray(after).astype(np.float32)
    return {
        "mean_before": round(float(np.mean(before_gray)), 3),
        "mean_after": round(float(np.mean(after_gray)), 3),
        "std_before": round(float(np.std(before_gray)), 3),
        "std_after": round(float(np.std(after_gray)), 3),
        "mean_abs_change": round(float(np.mean(np.abs(before_gray - after_gray))), 3),
    }


def distance_grid(shape: tuple[int, int]) -> np.ndarray:
    rows, cols = shape
    y, x = np.ogrid[:rows, :cols]
    return np.sqrt((y - rows // 2) ** 2 + (x - cols // 2) ** 2)


def turbulence_transfer(shape: tuple[int, int], k: float) -> np.ndarray:
    distance = distance_grid(shape)
    return np.exp(-max(k, 0.0) * np.power(distance, 5.0 / 3.0)).astype(np.float32)


def laplacian_transfer(shape: tuple[int, int]) -> np.ndarray:
    rows, cols = shape
    y, x = np.ogrid[:rows, :cols]
    fy = (y - rows // 2) / max(rows, 1)
    fx = (x - cols // 2) / max(cols, 1)
    return -4.0 * np.pi * np.pi * (fx * fx + fy * fy)
