# 本文件用于校验上传图像的格式、大小、解码结果和分辨率
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.core.upload_config import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_IMAGE_MIME_TYPES,
    MAX_IMAGE_HEIGHT,
    MAX_IMAGE_WIDTH,
    MAX_UPLOAD_SIZE_BYTES,
    MIN_IMAGE_HEIGHT,
    MIN_IMAGE_WIDTH,
    MIN_UPLOAD_SIZE_BYTES,
)


def validate_upload_extension(filename: str) -> None:
    """校验上传文件扩展名是否属于允许的静态图像格式。"""
    suffix = Path(filename or "").suffix.lower().lstrip(".")
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = "、".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise ValueError(f"不支持的图像格式，仅支持：{allowed}")


def validate_upload_content_type(content_type: str | None) -> None:
    """校验上传文件 MIME 类型是否属于允许的静态图像类型。"""
    if not content_type:
        return
    normalized = content_type.lower().split(";", 1)[0].strip()
    if normalized not in ALLOWED_IMAGE_MIME_TYPES:
        allowed = "、".join(sorted(ALLOWED_IMAGE_MIME_TYPES))
        raise ValueError(f"不支持的图片 MIME 类型，仅支持：{allowed}")


def validate_upload_file_size(file_size: int) -> None:
    """校验上传文件大小是否在允许范围内。"""
    if file_size < MIN_UPLOAD_SIZE_BYTES:
        raise ValueError("图片文件过小，最小文件大小为 10KB")
    if file_size > MAX_UPLOAD_SIZE_BYTES:
        raise ValueError("图片文件过大，最大文件大小为 5MB")


def decode_image_from_bytes(file_bytes: bytes) -> np.ndarray:
    """将上传文件字节解码为 OpenCV BGR uint8 图像。"""
    if not file_bytes:
        raise ValueError("上传文件不能为空")

    buffer = np.frombuffer(file_bytes, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("图片解码失败，请上传有效的图像文件")

    image = _normalize_decoded_image(image)
    return np.ascontiguousarray(image)


def validate_image_resolution(image: np.ndarray) -> None:
    """校验图像分辨率是否在允许范围内。"""
    if image is None or not isinstance(image, np.ndarray) or image.ndim < 2:
        raise ValueError("图片内容无效")

    height, width = image.shape[:2]
    if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
        raise ValueError("图片分辨率过小，最小分辨率为 128 x 128")
    if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
        raise ValueError("图片分辨率过大，最大分辨率为 4096 x 4096")


def validate_uploaded_image(filename: str, file_bytes: bytes) -> np.ndarray:
    """完整校验上传图像并返回 BGR uint8 图像。"""
    validate_upload_extension(filename)
    validate_upload_file_size(len(file_bytes))
    image = decode_image_from_bytes(file_bytes)
    validate_image_resolution(image)
    return image


def _normalize_decoded_image(image: np.ndarray) -> np.ndarray:
    if image.dtype != np.uint8:
        image_float = image.astype(np.float32)
        max_value = float(np.max(image_float)) if image_float.size else 0.0
        if max_value > 255.0:
            image_float = image_float / max_value * 255.0
        image = np.clip(image_float, 0, 255).astype(np.uint8)

    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if image.ndim == 3 and image.shape[2] == 1:
        return cv2.cvtColor(image[:, :, 0], cv2.COLOR_GRAY2BGR)
    if image.ndim == 3 and image.shape[2] == 3:
        return image
    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    raise ValueError("图片通道数无效")
