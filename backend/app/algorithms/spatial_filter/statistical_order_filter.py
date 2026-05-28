# 本文件用于实现统计排序滤波统一入口
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, odd_int_slider_value, to_bgr


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "statistical_order_filter",
    "display_name": "统计排序滤波",
    "description": "统一演示中值、最大值和最小值等统计排序滤波。",
    "params": {
        "mode": {
            "type": "str",
            "default": "median",
            "label": "滤波模式",
            "component": "select",
            "options": [
                {"label": "中值滤波", "value": "median"},
                {"label": "最大值滤波", "value": "max"},
                {"label": "最小值滤波", "value": "min"},
            ],
        },
        "kernel_size": {"type": "int", "default": 5, "min": 1, "max": 31, "step": 2, "label": "滤波窗口大小", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    mode = str(params.get("mode", "median"))
    if mode not in {"median", "max", "min"}:
        mode = "median"
    kernel_size = odd_int_slider_value(params, "kernel_size", ALGORITHM_META)
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    if mode == "max":
        result = cv2.dilate(source, kernel)
    elif mode == "min":
        result = cv2.erode(source, kernel)
    else:
        result = cv2.medianBlur(source, kernel_size)
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"mode": mode, "kernel_size": kernel_size, **gray_metrics(source, result)},
        "analysis": "统计排序滤波根据邻域像素排序后的统计值生成输出，可抑制脉冲噪声或强调局部亮暗极值。",
    }
