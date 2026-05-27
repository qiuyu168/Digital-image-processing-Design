# 本文件用于调度算法运行并组装图像处理流程响应
from __future__ import annotations

from typing import Any

import numpy as np

from app.core.image_codec import image_to_base64
from app.services.algorithm_registry import get_algorithm, get_module_display_name
from app.services.image_store import load_image_by_source
from app.services.step_service import encode_steps


def run_algorithm(
    image: np.ndarray,
    module_name: str,
    algorithm_name: str,
    params: dict | None,
) -> dict[str, Any]:
    """运行指定算法模块的 run(image, params) 并校验返回格式。"""
    module = get_algorithm(module_name, algorithm_name)
    run_function = getattr(module, "run")
    result = run_function(image, params or {})
    validate_algorithm_result(result)
    return result


def validate_algorithm_result(result: dict) -> None:
    """校验算法统一返回格式。"""
    if not isinstance(result, dict):
        raise ValueError("算法返回值必须是 dict")

    required_keys = ["result", "steps", "metrics", "analysis"]
    missing = [key for key in required_keys if key not in result]
    if missing:
        raise ValueError(f"算法返回值缺少字段：{', '.join(missing)}")

    if not isinstance(result["result"], np.ndarray):
        raise ValueError("算法 result 必须是 numpy.ndarray")
    if not isinstance(result["steps"], list):
        raise ValueError("算法 steps 必须是 list")
    if not isinstance(result["metrics"], dict):
        raise ValueError("算法 metrics 必须是 dict")
    if not isinstance(result["analysis"], str):
        raise ValueError("算法 analysis 必须是字符串")

    for index, step in enumerate(result["steps"], start=1):
        if not isinstance(step, dict):
            raise ValueError(f"第 {index} 个步骤必须是 dict")
        if "name" not in step or "image" not in step:
            raise ValueError(f"第 {index} 个步骤必须包含 name 和 image")
        if not isinstance(step["image"], np.ndarray):
            raise ValueError(f"第 {index} 个步骤 image 必须是 numpy.ndarray")


def run_process(payload: dict[str, Any]) -> dict[str, Any]:
    """从请求数据加载图像、运行算法并返回前端响应。"""
    source_type = str(payload.get("source_type") or "upload")
    image_path = str(payload.get("image_path") or "")
    module_name = str(payload.get("module") or "")
    algorithm_name = str(payload.get("algorithm") or "")
    params = payload.get("params") if isinstance(payload.get("params"), dict) else {}
    return_steps = bool(payload.get("return_steps", True))

    image = load_image_by_source(source_type, image_path)
    result = run_algorithm(image, module_name, algorithm_name, params)
    algorithm_meta = getattr(get_algorithm(module_name, algorithm_name), "ALGORITHM_META", {})

    return {
        "success": True,
        "module": module_name,
        "module_display_name": get_module_display_name(module_name),
        "algorithm": algorithm_name,
        "algorithm_display_name": algorithm_meta.get("display_name", algorithm_name),
        "result_image": image_to_base64(result["result"]),
        "steps": encode_steps(result["steps"]) if return_steps else [],
        "metrics": result["metrics"],
        "analysis": result["analysis"],
    }
