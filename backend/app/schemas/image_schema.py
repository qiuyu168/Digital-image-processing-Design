# 本文件用于定义上传图像和内置图库相关响应数据结构
from __future__ import annotations

from pydantic import BaseModel

from app.schemas.response_schema import BaseResponse


class UploadImageResponse(BaseResponse):
    image_path: str
    filename: str
    width: int
    height: int
    preview_url: str


class LibraryCategory(BaseModel):
    name: str
    display_name: str
    count: int


class LibraryImageInfo(BaseModel):
    name: str
    filename: str
    category: str
    image_path: str
    preview_url: str
