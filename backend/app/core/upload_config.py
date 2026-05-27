# 本文件用于定义图像上传相关的后端校验配置
from __future__ import annotations


ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "webp", "tif", "tiff"}
ALLOWED_IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/bmp",
    "image/webp",
    "image/tiff",
}

MIN_UPLOAD_SIZE_BYTES = 10 * 1024
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024

MIN_IMAGE_WIDTH = 128
MIN_IMAGE_HEIGHT = 128

MAX_IMAGE_WIDTH = 4096
MAX_IMAGE_HEIGHT = 4096
