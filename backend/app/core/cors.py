# 本文件用于配置后端允许访问的前端跨域来源
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def setup_cors(app: FastAPI) -> None:
    """为 FastAPI 应用添加 CORS 中间件。"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
