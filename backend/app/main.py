# 本文件是 FastAPI 后端项目入口文件
# 启动命令：python -m uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.algorithms import router as algorithms_router
from app.api.upload import router as upload_router
from app.api.library import router as library_router
from app.api.process import router as process_router
from app.api.analysis import router as analysis_router

from app.api.algorithm_modules.grayscale_image import router as grayscale_image_router
from app.api.algorithm_modules.color_image import router as color_image_router
from app.api.algorithm_modules.geometric_transform import router as geometric_transform_router
from app.api.algorithm_modules.spatial_filter import router as spatial_filter_router
from app.api.algorithm_modules.frequency_analysis import router as frequency_analysis_router
from app.api.algorithm_modules.frequency_filter import router as frequency_filter_router


app = FastAPI(
    title="动漫图像识别项目后端",
    description="数字图像处理课程设计后端接口服务",
    version="1.0.0",
)

# 允许前端跨域访问后端
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 开发阶段直接放开
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基础接口
app.include_router(health_router)
app.include_router(algorithms_router)
app.include_router(upload_router)
app.include_router(library_router)
app.include_router(process_router)
app.include_router(analysis_router)

# 六大算法分类接口
app.include_router(grayscale_image_router)
app.include_router(color_image_router)
app.include_router(geometric_transform_router)
app.include_router(spatial_filter_router)
app.include_router(frequency_analysis_router)
app.include_router(frequency_filter_router)


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "后端服务已启动",
    }