# 本文件用于实现动漫图像色彩增强功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "color_image",
    "name": "anime_color_enhance",
    "display_name": "动漫色彩增强",
    "description": "综合调整饱和度、对比度、亮度和轻微锐化，突出动漫图像的明快色彩与线条层次。",
    "params": {
        "saturation_factor": {
            "type": "float",
            "default": 1.25,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "饱和度系数",
            "component": "slider",
        },
        "contrast": {
            "type": "float",
            "default": 1.15,
            "min": 0.5,
            "max": 3.0,
            "step": 0.05,
            "label": "对比度系数",
            "component": "slider",
        },
        "brightness": {
            "type": "int",
            "default": 0,
            "min": -50,
            "max": 50,
            "step": 1,
            "label": "亮度偏移",
            "component": "slider",
        },
        "sharpen_strength": {
            "type": "float",
            "default": 0.25,
            "min": 0.0,
            "max": 1.0,
            "step": 0.05,
            "label": "线条锐化强度",
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
    saturation_factor = _get_float_param(params, "saturation_factor")
    contrast = _get_float_param(params, "contrast")
    brightness = _get_int_param(params, "brightness")
    sharpen_strength = _get_float_param(params, "sharpen_strength")

    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV).astype(np.float32)
    original_saturation = hsv_image[:, :, 1].copy()
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 255)
    saturation_enhanced = cv2.cvtColor(hsv_image.astype(np.uint8), cv2.COLOR_HSV2BGR)

    contrast_enhanced = cv2.convertScaleAbs(
        saturation_enhanced,
        alpha=contrast,
        beta=brightness,
    )

    if sharpen_strength > 0:
        blurred = cv2.GaussianBlur(contrast_enhanced, (0, 0), sigmaX=1.2)
        result = cv2.addWeighted(
            contrast_enhanced,
            1.0 + sharpen_strength,
            blurred,
            -sharpen_strength,
            0,
        )
    else:
        result = contrast_enhanced.copy()
    result = _ensure_uint8(result)

    metrics = {
        "saturation_factor": saturation_factor,
        "contrast": contrast,
        "brightness": brightness,
        "sharpen_strength": sharpen_strength,
        "mean_saturation_before": round(float(np.mean(original_saturation)), 2),
        "mean_saturation_after": round(float(np.mean(hsv_image[:, :, 1])), 2),
        "mean_intensity_before": round(float(np.mean(bgr_image)), 2),
        "mean_intensity_after": round(float(np.mean(result)), 2),
        "std_intensity_before": round(float(np.std(bgr_image)), 2),
        "std_intensity_after": round(float(np.std(result)), 2),
    }

    return {
        "result": result,
        "steps": [
            {"name": "原始图像", "image": bgr_image},
            {"name": "饱和度增强", "image": saturation_enhanced},
            {"name": "对比度亮度调整", "image": contrast_enhanced},
            {"name": "动漫色彩增强结果", "image": result},
        ],
        "metrics": metrics,
        "analysis": (
            f"已将饱和度调整为 {saturation_factor:.2f} 倍，对比度调整为 {contrast:.2f} 倍，"
            f"亮度偏移 {brightness}，锐化强度 {sharpen_strength:.2f}。该组合适合让动漫图像颜色更鲜明、"
            "线条更清晰，同时所有像素值都已裁剪为可保存的 uint8 图像。"
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
