# 本文件用于实现图像颜色空间转换功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "color_image",
    "name": "color_space_convert",
    "display_name": "颜色空间转换",
    "description": "将 BGR 图像转换为灰度、HSV 或 Lab 表示，并生成便于保存和展示的可视化结果。",
    "params": {
        "target_space": {
            "type": "select",
            "default": "gray",
            "options": [
                {"label": "灰度图", "value": "gray"},
                {"label": "HSV 可视化", "value": "hsv"},
                {"label": "Lab 可视化", "value": "lab"},
            ],
            "label": "目标颜色空间",
            "component": "select",
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    if params is None or not isinstance(params, dict):
        params = {}

    bgr_image = _prepare_bgr_image(image)
    target_space = _get_select_param(params, "target_space")

    if target_space == "gray":
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        result = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        steps = [
            {"name": "原始图像", "image": bgr_image},
            {"name": "灰度转换结果", "image": result},
        ]
        metrics = {
            "target_space": target_space,
            "gray_mean": round(float(np.mean(gray_image)), 2),
            "gray_std": round(float(np.std(gray_image)), 2),
            "gray_min": int(np.min(gray_image)),
            "gray_max": int(np.max(gray_image)),
        }
        analysis = "已将图像转换为灰度表示，结果使用三通道灰度图保存，便于前端和本地测试统一显示。"
    elif target_space == "hsv":
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hue_visual = cv2.cvtColor(
            cv2.merge([
                hsv_image[:, :, 0],
                np.full_like(hsv_image[:, :, 1], 255),
                np.full_like(hsv_image[:, :, 2], 255),
            ]),
            cv2.COLOR_HSV2BGR,
        )
        hsv_visual = cv2.merge([
            np.uint8(np.round(hsv_image[:, :, 0].astype(np.float32) * 255.0 / 179.0)),
            hsv_image[:, :, 1],
            hsv_image[:, :, 2],
        ])
        result = _ensure_uint8(hsv_visual)
        steps = [
            {"name": "原始图像", "image": bgr_image},
            {"name": "色相预览", "image": hue_visual},
            {"name": "HSV 通道可视化", "image": result},
        ]
        metrics = {
            "target_space": target_space,
            "hue_mean": round(float(np.mean(hsv_image[:, :, 0])), 2),
            "saturation_mean": round(float(np.mean(hsv_image[:, :, 1])), 2),
            "value_mean": round(float(np.mean(hsv_image[:, :, 2])), 2),
        }
        analysis = "已转换到 HSV 空间，并将 H/S/V 三个通道归一化为可保存的伪彩色可视化图。"
    else:
        lab_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2LAB)
        result = _ensure_uint8(lab_image)
        steps = [
            {"name": "原始图像", "image": bgr_image},
            {"name": "Lab 通道可视化", "image": result},
        ]
        metrics = {
            "target_space": target_space,
            "l_mean": round(float(np.mean(lab_image[:, :, 0])), 2),
            "a_mean": round(float(np.mean(lab_image[:, :, 1])), 2),
            "b_mean": round(float(np.mean(lab_image[:, :, 2])), 2),
        }
        analysis = "已转换到 Lab 空间，结果图用于观察亮度通道与颜色对立通道的分布，不代表自然 BGR 颜色。"

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis,
    }


def _get_select_param(params: dict, name: str) -> str:
    meta = ALGORITHM_META["params"][name]
    allowed_values = {option["value"] for option in meta["options"]}
    value = params.get(name, meta["default"])
    if value not in allowed_values:
        return str(meta["default"])
    return str(value)


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
