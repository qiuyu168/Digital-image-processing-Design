# 本文件用于实现图像饱和度调整功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "color_image",
    "name": "saturation_adjust",
    "display_name": "饱和度调整",
    "description": "基于 HSV 色彩空间调整动漫图像的色相、饱和度和明度，使人物和场景颜色更突出。",
    "params": {
        "hue_shift": {
            "type": "int",
            "default": 0,
            "min": -180,
            "max": 180,
            "step": 1,
            "label": "色相偏移",
            "component": "slider",
        },
        "saturation_factor": {
            "type": "float",
            "default": 1.5,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "饱和度系数",
            "component": "slider",
        },
        "value_factor": {
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "明度系数",
            "component": "slider",
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    if params is None or not isinstance(params, dict):
        params = {}

    bgr_image = _prepare_bgr_image(image)
    hue_shift = _get_int_param(params, "hue_shift")
    saturation_factor = _get_float_param(params, "saturation_factor")
    value_factor = _get_float_param(params, "value_factor")

    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV).astype(np.float32)
    original_saturation = hsv_image[:, :, 1].copy()
    original_value = hsv_image[:, :, 2].copy()

    hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_shift) % 180
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 255)
    hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * value_factor, 0, 255)

    adjusted_hsv = hsv_image.astype(np.uint8)
    result = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)
    result = _ensure_uint8(result)

    saturation_step = cv2.cvtColor(
        cv2.merge([
            adjusted_hsv[:, :, 0],
            adjusted_hsv[:, :, 1],
            np.full_like(adjusted_hsv[:, :, 2], 255),
        ]),
        cv2.COLOR_HSV2BGR,
    )

    metrics = {
        "hue_shift": hue_shift,
        "saturation_factor": saturation_factor,
        "value_factor": value_factor,
        "mean_saturation_before": round(float(np.mean(original_saturation)), 2),
        "mean_saturation_after": round(float(np.mean(adjusted_hsv[:, :, 1])), 2),
        "mean_value_before": round(float(np.mean(original_value)), 2),
        "mean_value_after": round(float(np.mean(adjusted_hsv[:, :, 2])), 2),
    }

    return {
        "result": result,
        "steps": [
            {"name": "原始图像", "image": bgr_image},
            {"name": "饱和度色相预览", "image": saturation_step},
            {"name": "调整结果", "image": result},
        ],
        "metrics": metrics,
        "analysis": (
            f"已在 HSV 空间将色相偏移 {hue_shift}，饱和度放大为 {saturation_factor:.2f} 倍，"
            f"明度放大为 {value_factor:.2f} 倍。该处理适合增强动漫图像色彩表现，"
            "输出已限制在 0 到 255 的 uint8 范围内。"
        ),
    }


def _get_float_param(params: dict, name: str) -> float:
    meta = ALGORITHM_META["params"][name]
    try:
        value = float(params.get(name, meta["default"]))
    except (TypeError, ValueError):
        value = float(meta["default"])
    return float(np.clip(value, meta["min"], meta["max"]))


def _get_int_param(params: dict, name: str) -> int:
    meta = ALGORITHM_META["params"][name]
    try:
        value = int(round(float(params.get(name, meta["default"]))))
    except (TypeError, ValueError):
        value = int(meta["default"])
    return int(np.clip(value, meta["min"], meta["max"]))


def _prepare_bgr_image(image: np.ndarray) -> np.ndarray:
    array = _ensure_uint8(image)
    if array.ndim == 2:
        return cv2.cvtColor(array, cv2.COLOR_GRAY2BGR)
    if array.ndim != 3:
        raise ValueError("输入图像必须是二维灰度图或三维彩色图")
    if array.shape[2] == 1:
        return cv2.cvtColor(array[:, :, 0], cv2.COLOR_GRAY2BGR)
    if array.shape[2] == 4:
        return cv2.cvtColor(array, cv2.COLOR_BGRA2BGR)
    if array.shape[2] >= 3:
        return np.ascontiguousarray(array[:, :, :3])
    raise ValueError("输入图像通道数不正确")


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.asarray(image)
    if array.size == 0:
        raise ValueError("输入图像不能为空数组")
    if array.dtype == np.uint8:
        return np.ascontiguousarray(array)

    array = np.nan_to_num(array.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    if float(np.max(array)) <= 1.0 and float(np.min(array)) >= 0.0:
        array = array * 255.0
    return np.ascontiguousarray(np.clip(array, 0, 255).astype(np.uint8))
