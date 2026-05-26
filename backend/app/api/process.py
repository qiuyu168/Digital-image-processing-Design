# 本文件用于定义图片算法处理相关 API 路由

import base64
from importlib import import_module
from inspect import isawaitable
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import cv2
import numpy as np


router = APIRouter(prefix="/api/process", tags=["process"])

UNIMPLEMENTED_SERVICE_DETAIL = "该接口框架已创建，具体业务逻辑待 service 层实现"
BACKEND_ROOT = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BACKEND_ROOT / "data" / "uploads"
LIBRARY_DIR = BACKEND_ROOT / "data" / "library"

MODULE_DISPLAY_NAMES = {
    "color_image": "彩色图像类",
}

COLOR_IMAGE_ALGORITHM_MODULES = {
    "anime_color_enhance": "app.algorithms.color_image.anime_color_enhance",
    "color_space_convert": "app.algorithms.color_image.color_space_convert",
    "dominant_color_extract": "app.algorithms.color_image.dominant_color_extract",
    "saturation_adjust": "app.algorithms.color_image.saturation_adjust",
}


class ProcessRequest(BaseModel):
    """前端提交的算法处理请求。"""

    source_type: str = "upload"
    image_id: str | None = None
    image_path: str | None = None
    module: str
    module_display_name: str | None = None
    algorithm: str
    algorithm_display_name: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    return_steps: bool = True


def _request_to_dict(request: ProcessRequest) -> dict[str, Any]:
    if hasattr(request, "model_dump"):
        return request.model_dump()
    return request.dict()


@router.post("/run")
async def run_process(request: ProcessRequest) -> dict[str, Any]:
    """根据模块名和算法名运行图像处理流程。"""
    if request.module == "color_image":
        return _run_color_image_process(request)

    # TODO: 后续调用 app.services.process_service.run_process(payload)，不要在 API 层实现其他类别的图像处理逻辑。
    try:
        from app.services.process_service import run_process as service_run_process
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail=UNIMPLEMENTED_SERVICE_DETAIL,
        ) from None

    payload = _request_to_dict(request)
    result = service_run_process(payload)
    if isawaitable(result):
        result = await result
    return result


def _run_color_image_process(request: ProcessRequest) -> dict[str, Any]:
    algorithm_module = _load_color_image_algorithm(request.algorithm)
    algorithm_meta = getattr(algorithm_module, "ALGORITHM_META", {})
    run_algorithm = getattr(algorithm_module, "run", None)
    if not callable(run_algorithm):
        raise HTTPException(
            status_code=500,
            detail="彩色图像算法缺少 run(image, params) 接口",
        )

    image = _load_source_image(request)
    result = run_algorithm(image, request.params)
    _validate_algorithm_result(result)

    encoded_steps = []
    if request.return_steps:
        encoded_steps = [
            {
                "name": str(step["name"]),
                "image": _encode_image_to_data_url(step["image"]),
            }
            for step in result["steps"]
        ]

    return {
        "success": True,
        "module": request.module,
        "module_display_name": request.module_display_name
        or MODULE_DISPLAY_NAMES["color_image"],
        "algorithm": request.algorithm,
        "algorithm_display_name": request.algorithm_display_name
        or algorithm_meta.get("display_name", request.algorithm),
        "result_image": _encode_image_to_data_url(result["result"]),
        "steps": encoded_steps,
        "metrics": result["metrics"],
        "analysis": result["analysis"],
    }


def _load_color_image_algorithm(algorithm_name: str) -> Any:
    module_path = COLOR_IMAGE_ALGORITHM_MODULES.get(algorithm_name)
    if module_path is None:
        raise HTTPException(
            status_code=404,
            detail=f"未找到彩色图像算法：{algorithm_name}",
        )

    try:
        return import_module(module_path)
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"彩色图像算法模块导入失败：{algorithm_name}",
        ) from exc


def _load_source_image(request: ProcessRequest) -> np.ndarray:
    source_type = request.source_type.lower().strip()
    if source_type == "upload":
        image_path = _resolve_safe_image_path(
            UPLOAD_DIR,
            _normalize_upload_identifier(request.image_id),
        )
    elif source_type == "library":
        image_path = _resolve_safe_image_path(
            LIBRARY_DIR,
            _normalize_library_identifier(request.image_path or request.image_id),
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="source_type 目前支持 upload 或 library",
        )

    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"待处理图片不存在：{image_path.name}",
        )

    data = np.fromfile(str(image_path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(
            status_code=400,
            detail="图片读取失败，请确认图片格式正确",
        )
    return image


def _normalize_upload_identifier(image_id: str | None) -> str:
    if not image_id:
        raise HTTPException(status_code=400, detail="upload 来源必须提供 image_id")
    return image_id.replace("\\", "/").removeprefix("/api/upload/preview/")


def _normalize_library_identifier(image_path: str | None) -> str:
    if not image_path:
        raise HTTPException(
            status_code=400,
            detail="library 来源必须提供 image_path 或 image_id",
        )
    return image_path.replace("\\", "/").removeprefix("/api/library/image/")


def _resolve_safe_image_path(base_dir: Path, relative_path: str) -> Path:
    requested_path = Path(relative_path)
    if requested_path.is_absolute():
        raise HTTPException(status_code=400, detail="图片路径不能是绝对路径")
    if any(part == ".." for part in requested_path.parts):
        raise HTTPException(status_code=400, detail="图片路径不能包含上级目录")

    resolved_base = base_dir.resolve()
    resolved_path = (resolved_base / requested_path).resolve()
    try:
        resolved_path.relative_to(resolved_base)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="图片路径超出允许范围") from exc
    return resolved_path


def _validate_algorithm_result(result: Any) -> None:
    if not isinstance(result, dict):
        raise HTTPException(status_code=500, detail="算法返回值必须是 dict")

    required_keys = ["result", "steps", "metrics", "analysis"]
    missing_keys = [key for key in required_keys if key not in result]
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"算法返回值缺少字段：{', '.join(missing_keys)}",
        )

    if not isinstance(result["result"], np.ndarray):
        raise HTTPException(status_code=500, detail="算法 result 必须是 numpy.ndarray")
    if not isinstance(result["steps"], list):
        raise HTTPException(status_code=500, detail="算法 steps 必须是 list")
    if not isinstance(result["metrics"], dict):
        raise HTTPException(status_code=500, detail="算法 metrics 必须是 dict")
    if not isinstance(result["analysis"], str):
        raise HTTPException(status_code=500, detail="算法 analysis 必须是字符串")

    for index, step in enumerate(result["steps"], start=1):
        if not isinstance(step, dict):
            raise HTTPException(status_code=500, detail=f"第 {index} 个步骤必须是 dict")
        if "name" not in step or "image" not in step:
            raise HTTPException(
                status_code=500,
                detail=f"第 {index} 个步骤必须包含 name 和 image",
            )
        if not isinstance(step["image"], np.ndarray):
            raise HTTPException(
                status_code=500,
                detail=f"第 {index} 个步骤 image 必须是 numpy.ndarray",
            )


def _encode_image_to_data_url(image: np.ndarray) -> str:
    safe_image = _ensure_uint8_image(image)
    success, encoded = cv2.imencode(".png", safe_image)
    if not success:
        raise HTTPException(status_code=500, detail="处理结果图片编码失败")
    payload = base64.b64encode(encoded.tobytes()).decode("ascii")
    return f"data:image/png;base64,{payload}"


def _ensure_uint8_image(image: np.ndarray) -> np.ndarray:
    array = np.asarray(image)
    if array.size == 0:
        raise HTTPException(status_code=500, detail="算法返回了空图片")
    if array.dtype == np.uint8:
        return np.ascontiguousarray(array)

    array = np.nan_to_num(array.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    if float(np.max(array)) <= 1.0 and float(np.min(array)) >= 0.0:
        array = array * 255.0
    return np.ascontiguousarray(np.clip(array, 0, 255).astype(np.uint8))
