# 本文件用于定义后端项目目录和数据存储目录配置
from __future__ import annotations

from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
APP_ROOT = BACKEND_ROOT / "app"
DATA_DIR = BACKEND_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
LIBRARY_DIR = DATA_DIR / "library"
OUTPUT_DIR = DATA_DIR / "outputs"
TEST_IMAGE_DIR = DATA_DIR / "test_images"
TEST_OUTPUT_DIR = DATA_DIR / "test_outputs"


REQUIRED_DATA_DIRS = [
    UPLOAD_DIR,
    LIBRARY_DIR / "anime_character",
    LIBRARY_DIR / "anime_scene",
    LIBRARY_DIR / "anime_avatar",
    LIBRARY_DIR / "course_samples",
    LIBRARY_DIR / "other",
    OUTPUT_DIR,
    TEST_IMAGE_DIR,
    TEST_OUTPUT_DIR,
]


def ensure_data_directories() -> None:
    """创建后端运行所需的数据目录。"""
    for directory in REQUIRED_DATA_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
