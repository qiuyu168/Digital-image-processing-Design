# 本文件用于创建 FastAPI 后端应用并注册全部 API 路由
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.algorithm_modules.basic_operation import router as basic_operation_router
from app.api.algorithm_modules.color_image import router as color_image_router
from app.api.algorithm_modules.edge_shape_detection import router as edge_shape_detection_router
from app.api.algorithm_modules.frequency_analysis import router as frequency_analysis_router
from app.api.algorithm_modules.frequency_filter import router as frequency_filter_router
from app.api.algorithm_modules.geometric_transform import router as geometric_transform_router
from app.api.algorithm_modules.grayscale_image import router as grayscale_image_router
from app.api.algorithm_modules.image_restoration import router as image_restoration_router
from app.api.algorithm_modules.spatial_filter import router as spatial_filter_router
from app.api.algorithms import router as algorithms_router
from app.api.analysis import router as analysis_router
from app.api.health import router as health_router
from app.api.library import router as library_router
from app.api.process import router as process_router
from app.api.upload import router as upload_router
from app.core.config import ensure_data_directories
from app.core.cors import setup_cors


app = FastAPI(
    title="Interactive Digital Image Processing Backend",
    description="基于动漫图像识别的交互式数字图像处理系统后端",
    version="1.0.0",
)

setup_cors(app)
ensure_data_directories()

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(library_router)
app.include_router(algorithms_router)
app.include_router(process_router)
app.include_router(analysis_router)

app.include_router(basic_operation_router)
app.include_router(grayscale_image_router)
app.include_router(color_image_router)
app.include_router(geometric_transform_router)
app.include_router(spatial_filter_router)
app.include_router(frequency_analysis_router)
app.include_router(frequency_filter_router)
app.include_router(image_restoration_router)
app.include_router(edge_shape_detection_router)


@app.get("/")
async def root() -> dict[str, str | bool]:
    """返回后端根路径说明。"""
    return {
        "success": True,
        "message": "Interactive Digital Image Processing Backend",
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """将 HTTPException 转换为统一 JSON 响应。"""
    _ = request
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """将请求体验证错误转换为统一 JSON 响应。"""
    _ = request
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "请求参数校验失败", "errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """将未捕获异常转换为统一 JSON 响应。"""
    _ = request
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": f"服务器内部错误：{exc}"},
    )
