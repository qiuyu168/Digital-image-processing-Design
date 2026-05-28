# 本文件用于定义图像处理流程请求和响应数据结构
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProcessRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_type: str
    image_path: str
    second_image_path: str | None = None
    module: str
    module_display_name: str | None = None
    algorithm: str
    algorithm_display_name: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    return_steps: bool = True


class CategoryProcessRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_type: str
    image_path: str
    second_image_path: str | None = None
    algorithm: str
    algorithm_display_name: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    return_steps: bool = True


class StepImage(BaseModel):
    name: str
    image: str | None = None
    error: str | None = None


class ProcessResponse(BaseModel):
    success: bool
    module: str
    module_display_name: str
    algorithm: str
    algorithm_display_name: str
    result_image: str
    steps: list[StepImage] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    analysis: str
