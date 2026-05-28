# 本文件用于实现对比度受限自适应直方图均衡化算法
from __future__ import annotations

import cv2
import numpy as np

from app.algorithms.common import gray_metrics, int_slider_value, slider_value, to_gray


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "clahe_equalization",
    "display_name": "CLAHE直方图均衡化",
    "description": "使用对比度受限自适应直方图均衡化增强局部灰度层次。",
    "params": {
        "clip_limit": {
            "type": "float",
            "default": 2.0,
            "min": 0.1,
            "max": 10.0,
            "step": 0.1,
            "label": "对比度限制",
            "component": "slider",
        },
        "tile_grid_size": {
            "type": "int",
            "default": 8,
            "min": 2,
            "max": 32,
            "step": 1,
            "label": "分块网格大小",
            "component": "slider",
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    gray = to_gray(image)
    clip_limit = slider_value(params, "clip_limit", ALGORITHM_META)
    tile_grid_size = int_slider_value(params, "tile_grid_size", ALGORITHM_META)
    clahe = cv2.createCLAHE(
        clipLimit=clip_limit,
        tileGridSize=(tile_grid_size, tile_grid_size),
    )
    result = clahe.apply(gray).astype(np.uint8)
    return {
        "result": result,
        "steps": [
            {"name": "原始图像", "image": gray},
            {"name": "处理结果", "image": result},
        ],
        "metrics": {
            "clip_limit": clip_limit,
            "tile_grid_size": tile_grid_size,
            **gray_metrics(gray, result),
        },
        "analysis": "CLAHE 在局部小块内均衡灰度并限制对比度放大，能提升暗部层次，同时减少普通均衡化造成的噪声过增强。",
    }

