# 本文件用于手动测试单个后端图像处理算法是否能够读取本地图片并生成处理结果。
from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import cv2
import numpy as np


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


# 小组成员常用配置区

ALGORITHM_IMPORT_PATH = "app.algorithms.grayscale_image.erode"
INPUT_IMAGE_PATH = "data/test_images/yc_test.jpg"
OUTPUT_IMAGE_PATH = "data/test_outputs/result.png"
PARAMS = {
    "saturation_factor": 0.1
}


def read_image_unicode(path: str | Path) -> np.ndarray:
    """读取本地图片，兼容 Windows 中文路径。"""
    image_path = _resolve_backend_path(path)
    if not image_path.exists():
        raise FileNotFoundError(f"输入图片不存在：{image_path}")

    data = np.fromfile(str(image_path), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"图片读取失败，请检查格式是否正确：{image_path}")
    return image


def save_image_unicode(path: str | Path, image: np.ndarray) -> Path:
    """保存本地图片，兼容 Windows 中文路径。"""
    image_path = _resolve_backend_path(path)
    image_path.parent.mkdir(parents=True, exist_ok=True)

    if image is None:
        raise ValueError("要保存的图片不能为空")
    if not isinstance(image, np.ndarray):
        raise TypeError("要保存的图片必须是 numpy.ndarray")

    suffix = image_path.suffix.lower()
    if suffix not in [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"]:
        image_path = image_path.with_suffix(".png")
        suffix = ".png"

    success, encoded = cv2.imencode(suffix, image)
    if not success:
        raise ValueError(f"图片编码失败，无法保存：{image_path}")
    encoded.tofile(str(image_path))
    return image_path


def load_algorithm(import_path: str):
    """根据导入路径动态加载算法模块。"""
    module = importlib.import_module(import_path)
    if not hasattr(module, "ALGORITHM_META"):
        raise AttributeError(f"算法模块缺少 ALGORITHM_META：{import_path}")
    if not hasattr(module, "run"):
        raise AttributeError(f"算法模块缺少 run(image, params)：{import_path}")
    return module.run, module.ALGORITHM_META


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


def save_steps(output_image_path: str | Path, steps: list[dict[str, Any]]) -> Path:
    """保存算法返回的步骤图。"""
    output_path = _resolve_backend_path(output_image_path)
    step_dir = output_path.parent / f"{output_path.stem}_steps"
    step_dir.mkdir(parents=True, exist_ok=True)

    for index, step in enumerate(steps, start=1):
        step_name = _safe_filename(str(step.get("name", f"step_{index}")))
        step_path = step_dir / f"{index:02d}_{step_name}.png"
        save_image_unicode(step_path, step["image"])
    return step_dir


def main() -> None:
    """执行一次本地算法测试。"""
    args = _parse_args()
    config = _load_config(args)

    algorithm_import_path = config["algorithm_import_path"]
    input_image_path = config["input_image_path"]
    output_image_path = config["output_image_path"]
    params = config["params"]

    print("=" * 68)
    print("开始进行图像处理算法本地测试")
    print("=" * 68)
    print(f"算法导入路径：{algorithm_import_path}")
    print(f"输入图片路径：{input_image_path}")
    print(f"输出图片路径：{output_image_path}")
    print(f"算法参数：{json.dumps(params, ensure_ascii=False)}")

    run_algorithm, algorithm_meta = load_algorithm(algorithm_import_path)
    image = read_image_unicode(input_image_path)
    result = run_algorithm(image, params)
    check_result_format(result)

    saved_output = save_image_unicode(output_image_path, result["result"])
    saved_steps = save_steps(output_image_path, result["steps"])

    print("-" * 68)
    print(f"算法名称：{algorithm_meta.get('display_name', algorithm_meta.get('name', '未知算法'))}")
    print(f"原图尺寸：{image.shape}")
    print(f"结果图片已保存：{saved_output}")
    print(f"步骤图片已保存：{saved_steps}")

    if result["metrics"]:
        print("指标信息：")
        for key, value in result["metrics"].items():
            print(f"  {key}: {value}")
    else:
        print("指标信息：无")

    print(f"分析说明：{result['analysis']}")
    print("=" * 68)
    print("测试完成")
    print("=" * 68)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="手动测试单个后端图像处理算法")
    parser.add_argument("--config", help="JSON 配置文件路径，例如 tests/sample_test_configs/canny_example.json")
    parser.add_argument("--algorithm", help="算法导入路径，例如 app.algorithms.edge_detection.canny")
    parser.add_argument("--input", help="输入图片路径，例如 data/test_images/anime_test.png")
    parser.add_argument("--output", help="输出图片路径，例如 data/test_outputs/canny_result.png")
    parser.add_argument("--params", help="JSON 字符串参数，例如 {\"threshold1\": 80, \"threshold2\": 160}")
    return parser.parse_args()


def _load_config(args: argparse.Namespace) -> dict[str, Any]:
    config = {
        "algorithm_import_path": ALGORITHM_IMPORT_PATH,
        "input_image_path": INPUT_IMAGE_PATH,
        "output_image_path": OUTPUT_IMAGE_PATH,
        "params": PARAMS.copy(),
    }

    if args.config:
        config_path = _resolve_backend_path(args.config)
        with config_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
        config.update({
            "algorithm_import_path": loaded.get("algorithm_import_path", config["algorithm_import_path"]),
            "input_image_path": loaded.get("input_image_path", config["input_image_path"]),
            "output_image_path": loaded.get("output_image_path", config["output_image_path"]),
            "params": loaded.get("params", config["params"]),
        })

    if args.algorithm:
        config["algorithm_import_path"] = args.algorithm
    if args.input:
        config["input_image_path"] = args.input
    if args.output:
        config["output_image_path"] = args.output
    if args.params:
        config["params"] = json.loads(args.params)

    return config


def _resolve_backend_path(path: str | Path) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return BACKEND_ROOT / path


def _safe_filename(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|\\s]+", "_", name.strip())
    return name[:40] or "step"


if __name__ == "__main__":
    main()
