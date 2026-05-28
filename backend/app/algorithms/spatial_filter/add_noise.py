# 本文件用于实现图像噪声添加功能
from __future__ import annotations

import numpy as np

from app.algorithms.common import clip_uint8, gray_metrics, int_slider_value, slider_value, to_bgr


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "add_noise",
    "display_name": "添加噪声",
    "description": "向图像添加高斯噪声或椒盐噪声，便于滤波实验对比。",
    "params": {
        "noise_type": {
            "type": "str",
            "default": "gaussian",
            "label": "噪声类型",
            "component": "select",
            "options": [
                {"label": "高斯噪声", "value": "gaussian"},
                {"label": "椒盐噪声", "value": "salt_pepper"},
            ],
        },
        "amount": {"type": "float", "default": 0.03, "min": 0.0, "max": 0.3, "step": 0.01, "label": "噪声比例", "component": "slider"},
        "sigma": {"type": "float", "default": 20.0, "min": 1.0, "max": 100.0, "step": 1.0, "label": "高斯标准差", "component": "slider"},
        "seed": {"type": "int", "default": 2026, "min": 0, "max": 9999, "step": 1, "label": "随机种子", "component": "slider"},
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    params = params or {}
    source = to_bgr(image)
    noise_type = str(params.get("noise_type", "gaussian"))
    amount = slider_value(params, "amount", ALGORITHM_META)
    sigma = slider_value(params, "sigma", ALGORITHM_META)
    seed = int_slider_value(params, "seed", ALGORITHM_META)
    rng = np.random.default_rng(seed)
    if noise_type == "salt_pepper":
        result = source.copy()
        mask = rng.random(source.shape[:2])
        result[mask < amount / 2] = 0
        result[(mask >= amount / 2) & (mask < amount)] = 255
    else:
        noise = rng.normal(0.0, sigma, source.shape).astype(np.float32)
        result = clip_uint8(source.astype(np.float32) + noise)
        noise_type = "gaussian"
    return {
        "result": result.astype(np.uint8),
        "steps": [{"name": "原始图像", "image": source}, {"name": "处理结果", "image": result}],
        "metrics": {"noise_type": noise_type, "amount": amount, "sigma": sigma, "seed": seed, **gray_metrics(source, result)},
        "analysis": "添加噪声用于构造滤波实验输入，高斯噪声模拟传感器随机扰动，椒盐噪声模拟脉冲型黑白点干扰。",
    }
