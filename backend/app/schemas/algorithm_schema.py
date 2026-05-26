# 本文件用于定义算法模块、算法元数据和参数元数据结构
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AlgorithmParam(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str | None = None
    default: Any = None
    min: int | float | None = None
    max: int | float | None = None
    step: int | float | None = None
    label: str | None = None
    component: str | None = None
    options: list[Any] | None = None


class AlgorithmMeta(BaseModel):
    model_config = ConfigDict(extra="allow")

    module: str
    module_display_name: str
    name: str
    display_name: str
    description: str = ""
    params: dict[str, dict[str, Any] | AlgorithmParam] = Field(default_factory=dict)


class AlgorithmModule(BaseModel):
    module: str
    display_name: str
    algorithms: list[AlgorithmMeta] = Field(default_factory=list)


class AlgorithmListResponse(BaseModel):
    success: bool = True
    modules: list[AlgorithmModule] = Field(default_factory=list)
    algorithms: list[AlgorithmMeta] = Field(default_factory=list)
