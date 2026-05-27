# 本文件用于手动测试单个后端图像处理算法，初学者只需要修改三个路径变量
from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path
from typing import Any

import cv2
import numpy as np


INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/result.png"
ALGORITHM_IMPORT_PATH = "app.algorithms.color_image.saturation_adjust"


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def main() -> None:
    """执行一次本地算法测试。"""
    print("=" * 68)
    print("开始进行图像处理算法本地测试")
    print("=" * 68)
    print(f"输入图片路径：{INPUT_IMAGE_PATH}")
    print(f"输出图片路径：{OUTPUT_IMAGE_PATH}")
    print(f"算法导入路径：{ALGORITHM_IMPORT_PATH}")

    module = load_algorithm(ALGORITHM_IMPORT_PATH)
    params = build_default_params(module.ALGORITHM_META)
    print(f"自动使用默认参数：{params}")

    image = read_image_unicode(INPUT_IMAGE_PATH)
    result = module.run(image, params)
    check_result_format(result)

    saved_output = save_image_unicode(OUTPUT_IMAGE_PATH, result["result"])
    saved_steps = save_steps(OUTPUT_IMAGE_PATH, result.get("steps", []))

    print("-" * 68)
    print(f"算法名称：{module.ALGORITHM_META.get('display_name', module.ALGORITHM_META.get('name', '未知算法'))}")
    print(f"原图尺寸：{image.shape}")
    print(f"结果图片已保存：{saved_output}")
    if saved_steps is not None:
        print(f"步骤图片已保存：{saved_steps}")

    metrics = result.get("metrics", {})
    if metrics:
        print("指标信息：")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
    else:
        print("指标信息：无")

    print(f"分析说明：{result.get('analysis', '无')}")
    print("=" * 68)
    print("测试完成")
    print("=" * 68)


def load_algorithm(import_path: str):
    """根据导入路径加载算法模块。"""
    try:
        module = importlib.import_module(import_path)
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            f"算法模块导入失败：{import_path}\n"
            "请确认 ALGORITHM_IMPORT_PATH 是否正确，并在 backend 目录下运行脚本。"
        ) from exc

    if not hasattr(module, "ALGORITHM_META"):
        raise AttributeError(f"算法模块缺少 ALGORITHM_META：{import_path}")
    if not hasattr(module, "run"):
        raise AttributeError(f"算法模块缺少 run(image, params)：{import_path}")
    return module


def build_default_params(algorithm_meta: dict[str, Any]) -> dict[str, Any]:
    """根据 ALGORITHM_META 自动生成默认参数。"""
    params_schema = algorithm_meta.get("params", {})
    if not isinstance(params_schema, dict):
        return {}

    params: dict[str, Any] = {}
    for param_name, param_info in params_schema.items():
        if isinstance(param_info, dict) and "default" in param_info:
            params[param_name] = param_info["default"]
    return params


def read_image_unicode(path: str | Path) -> np.ndarray:
    """读取本地图片，兼容 Windows 中文路径。"""
    image_path = resolve_backend_path(path)
    if not image_path.exists() or not image_path.is_file():
        raise FileNotFoundError(f"输入图片不存在：{image_path}")

    data = np.fromfile(str(image_path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"图片读取失败，请检查文件格式：{image_path}")
    return np.ascontiguousarray(image)


def save_image_unicode(path: str | Path, image: np.ndarray) -> Path:
    """保存本地图片，兼容 Windows 中文路径。"""
    if image is None or not isinstance(image, np.ndarray):
        raise TypeError("要保存的图片必须是 numpy.ndarray")

    image_path = resolve_backend_path(path)
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_to_save = normalize_image_for_save(image)

    suffix = image_path.suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}:
        image_path = image_path.with_suffix(".png")
        suffix = ".png"

    success, encoded = cv2.imencode(suffix, image_to_save)
    if not success:
        raise ValueError(f"图片编码失败，无法保存：{image_path}")
    encoded.tofile(str(image_path))
    return image_path


def normalize_image_for_save(image: np.ndarray) -> np.ndarray:
    """将算法输出转换为可保存的 uint8 图片。"""
    if image.dtype == np.uint8:
        return np.ascontiguousarray(image)
    if image.dtype == np.bool_:
        return np.ascontiguousarray(image.astype(np.uint8) * 255)

    image_float = np.nan_to_num(image.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    min_value = float(np.min(image_float))
    max_value = float(np.max(image_float))
    if 0.0 <= min_value and max_value <= 1.0:
        image_float = image_float * 255.0
    return np.ascontiguousarray(np.clip(image_float, 0, 255).astype(np.uint8))


def check_result_format(result: dict[str, Any]) -> None:
    """检查算法返回值是否符合统一格式。"""
    if not isinstance(result, dict):
        raise TypeError("算法返回值必须是 dict")

    required_keys = ["result", "steps", "metrics", "analysis"]
    missing = [key for key in required_keys if key not in result]
    if missing:
        raise KeyError(f"算法返回值缺少字段：{', '.join(missing)}")

    if not isinstance(result["result"], np.ndarray):
        raise TypeError("result 字段必须是 numpy.ndarray")
    if not isinstance(result["steps"], list):
        raise TypeError("steps 字段必须是 list")
    if not isinstance(result["metrics"], dict):
        raise TypeError("metrics 字段必须是 dict")
    if not isinstance(result["analysis"], str):
        raise TypeError("analysis 字段必须是 str")

    for index, step in enumerate(result["steps"], start=1):
        if not isinstance(step, dict):
            raise TypeError(f"第 {index} 个 step 必须是 dict")
        if "name" not in step or "image" not in step:
            raise KeyError(f"第 {index} 个 step 必须包含 name 和 image")
        if not isinstance(step["image"], np.ndarray):
            raise TypeError(f"第 {index} 个 step 的 image 必须是 numpy.ndarray")


def save_steps(output_image_path: str | Path, steps: list[dict[str, Any]]) -> Path | None:
    """保存算法返回的步骤图。"""
    if not steps:
        return None

    output_path = resolve_backend_path(output_image_path)
    step_dir = output_path.parent / f"{output_path.stem}_steps"
    step_dir.mkdir(parents=True, exist_ok=True)

    for index, step in enumerate(steps, start=1):
        step_name = safe_filename(str(step.get("name", f"step_{index}")))
        step_path = step_dir / f"{index:02d}_{step_name}.png"
        save_image_unicode(step_path, step["image"])
    return step_dir


def resolve_backend_path(path: str | Path) -> Path:
    """将相对路径解析为 backend 目录下的路径。"""
    target_path = Path(path)
    if target_path.is_absolute():
        return target_path
    return BACKEND_ROOT / target_path


def safe_filename(name: str) -> str:
    """把步骤名转换为安全文件名。"""
    normalized = re.sub(r"[\\/:*?\"<>|\s]+", "_", name.strip())
    return normalized[:40] or "step"


if __name__ == "__main__":
    main()
