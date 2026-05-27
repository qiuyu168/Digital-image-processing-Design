# 本文件用于读写兼容 Windows 中文路径的本地图像文件
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


SUPPORTED_SAVE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def read_image_unicode(path: str | Path) -> np.ndarray:
    """使用 OpenCV 解码方式读取可能包含中文路径的图像。"""
    image_path = Path(path)
    if not image_path.exists() or not image_path.is_file():
        raise FileNotFoundError(f"图像文件不存在：{image_path}")

    data = np.fromfile(str(image_path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"图像读取失败，请检查文件格式：{image_path}")
    return np.ascontiguousarray(image)


def save_image_unicode(path: str | Path, image: np.ndarray) -> Path:
    """使用 OpenCV 编码方式保存可能包含中文路径的图像。"""
    image_path = Path(path)
    image_path.parent.mkdir(parents=True, exist_ok=True)

    suffix = image_path.suffix.lower()
    if suffix not in SUPPORTED_SAVE_EXTENSIONS:
        image_path = image_path.with_suffix(".png")
        suffix = ".png"

    success, encoded = cv2.imencode(suffix, np.ascontiguousarray(image))
    if not success:
        raise ValueError(f"图像编码失败，无法保存：{image_path}")

    encoded.tofile(str(image_path))
    return image_path
