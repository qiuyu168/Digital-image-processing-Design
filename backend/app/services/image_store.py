# 本文件用于管理上传图像、内置图库图像和图像来源读取
from __future__ import annotations

import re
import uuid
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import UploadFile

from app.core.config import LIBRARY_DIR, UPLOAD_DIR, ensure_data_directories
from app.core.image_io import read_image_unicode, save_image_unicode
from app.core.upload_config import ALLOWED_IMAGE_EXTENSIONS
from app.core.upload_validator import validate_upload_content_type, validate_uploaded_image


LIBRARY_CATEGORIES = [
    ("anime_character", "动漫人物图像"),
    ("anime_scene", "动漫场景图像"),
    ("anime_avatar", "动漫头像图像"),
    ("course_samples", "课程示例图像"),
    ("other", "其他图像"),
]


async def save_upload_image(file: UploadFile) -> dict[str, Any]:
    """校验并保存上传图像，返回前端需要的图像信息。"""
    ensure_data_directories()
    validate_upload_content_type(file.content_type)
    file_bytes = await file.read()
    image = validate_uploaded_image(file.filename or "", file_bytes)

    image_path = f"upload_{uuid.uuid4().hex}.png"
    output_path = UPLOAD_DIR / image_path
    save_image_unicode(output_path, image)

    height, width = image.shape[:2]
    return {
        "success": True,
        "image_path": image_path,
        "filename": image_path,
        "width": int(width),
        "height": int(height),
        "preview_url": f"/api/upload/preview/{image_path}",
        "message": "图片上传成功",
    }


def get_upload_image_path(image_path: str) -> Path:
    """根据上传图像路径返回安全的本地文件路径。"""
    safe_name = _safe_filename_only(image_path, "上传图像路径")
    image_path = _resolve_under_base(UPLOAD_DIR, safe_name)
    if not image_path.exists() or not image_path.is_file():
        raise FileNotFoundError(f"上传图片不存在：{safe_name}")
    return image_path


def get_library_image_path(image_path: str) -> Path:
    """根据内置图库相对路径返回安全的本地文件路径。"""
    relative_path = _normalize_relative_path(image_path, "图库图像路径")
    resolved_path = _resolve_under_base(LIBRARY_DIR, relative_path)
    if not resolved_path.exists() or not resolved_path.is_file():
        raise FileNotFoundError(f"图库图片不存在：{relative_path}")
    return resolved_path


def list_library_categories() -> list[dict[str, Any]]:
    """列出内置图库分类和每个分类下的图片数量（排除 other 分类）。"""
    ensure_data_directories()
    categories: list[dict[str, Any]] = []
    for name, display_name in LIBRARY_CATEGORIES:
        if name == "other":
            continue
        category_dir = LIBRARY_DIR / name
        count = len([path for path in category_dir.iterdir() if _is_supported_image(path)])
        categories.append({"name": name, "display_name": display_name, "count": count})
    return categories


def list_library_images(category: str, page: int = 1, page_size: int = 6) -> dict[str, Any]:
    """列出指定内置图库分类下的图片（支持分页）。"""
    ensure_data_directories()
    category_names = {name for name, _ in LIBRARY_CATEGORIES}
    if category not in category_names:
        raise FileNotFoundError(f"图库分类不存在：{category}")

    category_dir = LIBRARY_DIR / category
    all_images: list[dict[str, str]] = []
    for image_path in sorted(category_dir.iterdir()):
        if not _is_supported_image(image_path):
            continue
        relative_path = image_path.relative_to(LIBRARY_DIR).as_posix()
        all_images.append(
            {
                "name": image_path.stem,
                "filename": image_path.name,
                "category": category,
                "image_path": relative_path,
                "preview_url": f"/api/library/image/{relative_path}",
            }
        )

    total = len(all_images)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "success": True,
        "category": category,
        "images": all_images[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def load_image_by_source(source_type: str, image_path: str) -> np.ndarray:
    """根据 upload 或 library 来源读取 BGR uint8 图像。"""
    source = (source_type or "").lower().strip()
    if source == "upload":
        resolved_path = get_upload_image_path(image_path)
    elif source == "library":
        resolved_path = get_library_image_path(image_path)
    else:
        raise ValueError("source_type 仅支持 upload 或 library")
    return read_image_unicode(resolved_path)


def _safe_filename_only(value: str, label: str) -> str:
    if not value:
        raise ValueError(f"{label}不能为空")
    normalized = value.replace("\\", "/")
    if "/" in normalized or normalized in {".", ".."}:
        raise ValueError(f"{label}不能包含路径分隔符")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", normalized):
        raise ValueError(f"{label}包含非法字符")
    return normalized


def _normalize_relative_path(value: str, label: str) -> str:
    if not value:
        raise ValueError(f"{label}不能为空")
    normalized = value.replace("\\", "/").removeprefix("/api/library/image/")
    path = Path(normalized)
    if path.is_absolute() or any(part in {"..", ""} for part in path.parts):
        raise ValueError(f"{label}不能包含绝对路径或上级目录")
    return path.as_posix()


def _resolve_under_base(base_dir: Path, relative_path: str) -> Path:
    base = base_dir.resolve()
    resolved = (base / relative_path).resolve()
    try:
        resolved.relative_to(base)
    except ValueError as exc:
        raise ValueError("图像路径超出允许范围") from exc
    return resolved


def _is_supported_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower().lstrip(".") in ALLOWED_IMAGE_EXTENSIONS
