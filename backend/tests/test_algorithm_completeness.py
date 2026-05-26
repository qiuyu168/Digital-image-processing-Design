# 本文件用于检查全部算法文件是否已实现并符合前端参数元数据规范
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

import numpy as np


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


ALGORITHM_MODULES = {
    "grayscale_image": [
        "grayscale",
        "binary_threshold",
        "histogram_equalization",
        "edge_detection_basic",
        "erode",
        "dilate",
        "open_operation",
        "close_operation",
    ],
    "color_image": [
        "color_space_convert",
        "saturation_adjust",
        "anime_color_enhance",
        "dominant_color_extract",
    ],
    "geometric_transform": ["resize", "rotate", "flip"],
    "spatial_filter": [
        "mean_filter",
        "gaussian_filter",
        "median_filter",
        "bilateral_filter",
        "laplacian_sharpen",
    ],
    "frequency_analysis": ["dft_spectrum", "spectrum_shift", "magnitude_spectrum"],
    "frequency_filter": [
        "low_pass_filter",
        "high_pass_filter",
        "ideal_low_pass",
        "ideal_high_pass",
        "gaussian_low_pass",
        "gaussian_high_pass",
    ],
}


def sample_image() -> np.ndarray:
    y = np.linspace(0, 255, 160, dtype=np.uint8)[:, None]
    x = np.linspace(0, 255, 160, dtype=np.uint8)[None, :]
    return np.dstack([
        np.broadcast_to(x, (160, 160)),
        np.broadcast_to(y, (160, 160)),
        ((x.astype(np.uint16) + y.astype(np.uint16)) // 2).astype(np.uint8),
    ])


def default_params(meta: dict[str, Any]) -> dict[str, Any]:
    return {
        name: info["default"]
        for name, info in meta.get("params", {}).items()
        if isinstance(info, dict) and "default" in info
    }


def test_all_algorithm_files_are_complete_and_runnable() -> None:
    failures: list[str] = []
    image = sample_image()

    for module_name, algorithm_names in ALGORITHM_MODULES.items():
        for algorithm_name in algorithm_names:
            import_path = f"app.algorithms.{module_name}.{algorithm_name}"
            module = importlib.import_module(import_path)
            file_path = BACKEND_ROOT / "app" / "algorithms" / module_name / f"{algorithm_name}.py"
            first_line = file_path.read_text(encoding="utf-8").splitlines()[0]

            if not first_line.startswith("# "):
                failures.append(f"{import_path}: first line is not a Chinese comment")
            if "cv2.imshow" in file_path.read_text(encoding="utf-8"):
                failures.append(f"{import_path}: uses cv2.imshow")

            meta = getattr(module, "ALGORITHM_META", None)
            if not isinstance(meta, dict):
                failures.append(f"{import_path}: missing ALGORITHM_META")
                continue
            if meta.get("module") != module_name:
                failures.append(f"{import_path}: ALGORITHM_META module mismatch")
            if meta.get("name") != algorithm_name:
                failures.append(f"{import_path}: ALGORITHM_META name mismatch")

            for param_name, param_info in meta.get("params", {}).items():
                if not isinstance(param_info, dict):
                    failures.append(f"{import_path}.{param_name}: metadata is not dict")
                    continue
                for key in ["type", "default", "label", "component"]:
                    if key not in param_info:
                        failures.append(f"{import_path}.{param_name}: missing {key}")
                if param_info.get("component") == "slider":
                    for key in ["min", "max", "step"]:
                        if key not in param_info:
                            failures.append(f"{import_path}.{param_name}: missing slider {key}")
                if param_info.get("component") == "select" and "options" not in param_info:
                    failures.append(f"{import_path}.{param_name}: missing select options")

            run = getattr(module, "run", None)
            if not callable(run):
                failures.append(f"{import_path}: missing run")
                continue

            try:
                result = run(image[:, ::-1], default_params(meta))
            except Exception as exc:
                failures.append(f"{import_path}: run failed: {exc}")
                continue

            if not isinstance(result, dict):
                failures.append(f"{import_path}: result is not dict")
                continue
            for key in ["result", "steps", "metrics", "analysis"]:
                if key not in result:
                    failures.append(f"{import_path}: missing return key {key}")
            if not isinstance(result.get("result"), np.ndarray):
                failures.append(f"{import_path}: result image is not ndarray")
            if not isinstance(result.get("steps"), list) or not result.get("steps"):
                failures.append(f"{import_path}: steps must be non-empty list")
            else:
                for index, step in enumerate(result["steps"], start=1):
                    if not isinstance(step, dict) or "name" not in step or "image" not in step:
                        failures.append(f"{import_path}: invalid step {index}")
                    elif not isinstance(step["image"], np.ndarray):
                        failures.append(f"{import_path}: step {index} image is not ndarray")
            if not isinstance(result.get("metrics"), dict):
                failures.append(f"{import_path}: metrics is not dict")
            analysis = result.get("analysis")
            if not isinstance(analysis, str) or not analysis.strip():
                failures.append(f"{import_path}: analysis is empty")
            elif any(word in analysis for word in ["占位", "框架", "替换", "未实现"]):
                failures.append(f"{import_path}: analysis still looks like placeholder")

    assert not failures, "\n".join(failures)
