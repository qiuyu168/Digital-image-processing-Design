# 本文件用于将算法步骤图像转换为前端可显示的 Base64 数据
from __future__ import annotations

from typing import Any

import numpy as np

from app.core.image_codec import image_to_base64


def encode_steps(steps: list) -> list[dict[str, Any]]:
    """将算法步骤列表中的图像转为 PNG Base64。"""
    encoded_steps: list[dict[str, Any]] = []
    for index, step in enumerate(steps or [], start=1):
        if not isinstance(step, dict):
            encoded_steps.append({"name": f"步骤 {index}", "error": "步骤格式不是 dict"})
            continue

        name = str(step.get("name") or f"步骤 {index}")
        image = step.get("image")
        if not isinstance(image, np.ndarray):
            encoded_steps.append({"name": name, "error": "步骤图像不是 numpy.ndarray"})
            continue

        encoded_steps.append({"name": name, "image": image_to_base64(image)})
    return encoded_steps
