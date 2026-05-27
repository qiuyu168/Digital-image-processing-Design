# 本文件用于计算图像的基础尺寸、像素统计指标和可选直方图
from __future__ import annotations

from typing import Any

import numpy as np

from app.core.image_codec import normalize_image_for_display


def calculate_basic_metrics(
    image: np.ndarray,
    include_histogram: bool = False,
) -> dict[str, Any]:
    """计算图像宽高、通道数、数据类型和基础像素统计信息。"""
    if image is None or not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("图像不能为空")

    height, width = image.shape[:2]
    channels = 1 if image.ndim == 2 else int(image.shape[2])
    metrics: dict[str, Any] = {
        "width": int(width),
        "height": int(height),
        "channels": channels,
        "dtype": str(image.dtype),
        "mean": round(float(np.mean(image)), 4),
        "std": round(float(np.std(image)), 4),
        "min": float(np.min(image)),
        "max": float(np.max(image)),
    }

    if include_histogram:
        metrics["histogram"] = calculate_histogram(image)

    return metrics


def calculate_histogram(image: np.ndarray) -> dict[str, Any]:
    """按图像通道统计 0-255 灰度直方图，返回 JSON 友好的列表数据。"""
    display_image = normalize_image_for_display(image)
    channel_items = _split_channels(display_image)

    channels: list[dict[str, Any]] = []
    for channel_name, channel_data in channel_items:
        values = np.bincount(channel_data.reshape(-1), minlength=256)[:256].astype(int)
        channels.append(
            {
                "name": channel_name,
                "values": values.tolist(),
                "pixel_count": int(channel_data.size),
                "peak_value": int(np.argmax(values)),
                "peak_count": int(np.max(values)),
            }
        )

    return {"bins": 256, "channels": channels}


def _split_channels(image: np.ndarray) -> list[tuple[str, np.ndarray]]:
    if image.ndim == 2:
        return [("gray", image)]
    if image.ndim == 3 and image.shape[2] == 3:
        return [
            ("blue", image[:, :, 0]),
            ("green", image[:, :, 1]),
            ("red", image[:, :, 2]),
        ]
    if image.ndim == 3 and image.shape[2] == 4:
        return [
            ("blue", image[:, :, 0]),
            ("green", image[:, :, 1]),
            ("red", image[:, :, 2]),
            ("alpha", image[:, :, 3]),
        ]
    raise ValueError("图像通道格式不支持直方图统计")
