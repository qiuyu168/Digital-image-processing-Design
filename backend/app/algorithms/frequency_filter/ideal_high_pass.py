# 本文件用于实现理想高通频域滤波算法。
from __future__ import annotations

import cv2
import numpy as np

from app.core.algorithm_framework import build_algorithm_meta, run_standard_algorithm


ALGORITHM_META = build_algorithm_meta("frequency_filter", "ideal_high_pass")


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口。"""
    if image is None:
        raise ValueError("输入图像不能为空")
    if params is None:
        params = {}

    return run_standard_algorithm(image, params, ALGORITHM_META)
