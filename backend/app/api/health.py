# 本文件用于定义后端健康检查相关 API 路由

from fastapi import APIRouter


router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, bool | str]:
    """返回后端服务健康状态。"""
    return {
        "success": True,
        "message": "后端服务运行正常",
    }
