# 本文件用于定义后端通用响应数据结构
from __future__ import annotations

from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool
    message: str | None = None
