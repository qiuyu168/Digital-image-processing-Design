# 本文件用于实现图像主色调提取功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "color_image",
    "name": "dominant_color_extract",
    "display_name": "主色调提取",
    "description": "使用 K-Means 聚类提取动漫图像中的主要颜色，并生成主色调量化可视化结果。",
    "params": {
        "color_count": {
            "type": "int",
            "default": 5,
            "min": 2,
            "max": 10,
            "step": 1,
            "label": "主色数量",
            "component": "slider",
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    if image is None:
        raise ValueError("输入图像不能为空")
    if params is None or not isinstance(params, dict):
        params = {}

    bgr_image = _prepare_bgr_image(image)
    color_count = _get_int_param(params, "color_count")

    centers, percentages = _extract_dominant_colors(bgr_image, color_count)
    result = _quantize_image(bgr_image, centers)
    palette_image = _build_palette_image(bgr_image.shape[1], centers, percentages)

    dominant_colors = []
    for center, percentage in zip(centers, percentages, strict=False):
        b, g, r = [int(value) for value in center]
        dominant_colors.append({
            "bgr": [b, g, r],
            "rgb": [r, g, b],
            "hex": f"#{r:02X}{g:02X}{b:02X}",
            "percentage": round(float(percentage), 4),
        })

    metrics = {
        "requested_color_count": color_count,
        "actual_color_count": len(dominant_colors),
        "dominant_colors": dominant_colors,
    }

    return {
        "result": result,
        "steps": [
            {"name": "原始图像", "image": bgr_image},
            {"name": "主色调色板", "image": palette_image},
            {"name": "主色调量化结果", "image": result},
        ],
        "metrics": metrics,
        "analysis": (
            f"已提取 {len(dominant_colors)} 个主色调，并将原图量化为主色调可视化结果。"
            "色板宽度按采样像素占比显示，可用于分析动漫人物、服装和背景的主要配色。"
        ),
    }


def _get_int_param(params: dict, name: str) -> int:
    meta = ALGORITHM_META["params"][name]
    try:
        value = int(round(float(params.get(name, meta["default"]))))
    except (TypeError, ValueError):
        value = int(meta["default"])
    return int(np.clip(value, meta["min"], meta["max"]))


def _extract_dominant_colors(image: np.ndarray, color_count: int) -> tuple[np.ndarray, np.ndarray]:
    pixels = image.reshape(-1, 3)
    total_pixels = pixels.shape[0]
    max_sample_count = 20000
    if total_pixels > max_sample_count:
        sample_indices = np.linspace(0, total_pixels - 1, max_sample_count, dtype=np.int64)
        sample_pixels = pixels[sample_indices]
    else:
        sample_pixels = pixels

    unique_sample = np.unique(sample_pixels, axis=0)
    cluster_count = int(min(color_count, max(1, unique_sample.shape[0])))
    if cluster_count == 1:
        center = unique_sample[0].reshape(1, 3).astype(np.uint8)
        return center, np.array([1.0], dtype=np.float32)

    samples = sample_pixels.astype(np.float32)
    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        30,
        0.5,
    )
    cv2.setRNGSeed(12345)
    _, labels, centers = cv2.kmeans(
        samples,
        cluster_count,
        None,
        criteria,
        3,
        cv2.KMEANS_PP_CENTERS,
    )

    counts = np.bincount(labels.reshape(-1), minlength=cluster_count).astype(np.float32)
    order = np.argsort(-counts)
    sorted_centers = np.clip(centers[order], 0, 255).astype(np.uint8)
    sorted_percentages = counts[order] / max(float(np.sum(counts)), 1.0)
    return sorted_centers, sorted_percentages.astype(np.float32)


def _quantize_image(image: np.ndarray, centers: np.ndarray) -> np.ndarray:
    flat_pixels = image.reshape(-1, 3).astype(np.float32)
    centers_float = centers.astype(np.float32)
    output = np.empty((flat_pixels.shape[0], 3), dtype=np.uint8)
    chunk_size = 200000

    for start in range(0, flat_pixels.shape[0], chunk_size):
        end = min(start + chunk_size, flat_pixels.shape[0])
        chunk = flat_pixels[start:end]
        distances = np.sum((chunk[:, None, :] - centers_float[None, :, :]) ** 2, axis=2)
        labels = np.argmin(distances, axis=1)
        output[start:end] = centers[labels]

    return output.reshape(image.shape)


def _build_palette_image(width: int, centers: np.ndarray, percentages: np.ndarray) -> np.ndarray:
    palette_height = 80
    palette_width = max(int(width), 128)
    palette = np.zeros((palette_height, palette_width, 3), dtype=np.uint8)
    start_x = 0

    for index, (center, percentage) in enumerate(zip(centers, percentages, strict=False)):
        if index == len(centers) - 1:
            end_x = palette_width
        else:
            end_x = min(palette_width, start_x + int(round(float(percentage) * palette_width)))
        palette[:, start_x:end_x] = center
        start_x = end_x

    if start_x < palette_width:
        palette[:, start_x:] = centers[-1]
    return palette


def _prepare_bgr_image(image: np.ndarray) -> np.ndarray:
    array = _ensure_uint8(image)
    if array.ndim == 2:
        return cv2.cvtColor(array, cv2.COLOR_GRAY2BGR)
    if array.ndim != 3:
        raise ValueError("输入图像必须是二维灰度图或三维彩色图")
    if array.shape[2] == 1:
        return cv2.cvtColor(array[:, :, 0], cv2.COLOR_GRAY2BGR)
    if array.shape[2] == 4:
        return cv2.cvtColor(array, cv2.COLOR_BGRA2BGR)
    if array.shape[2] >= 3:
        return np.ascontiguousarray(array[:, :, :3])
    raise ValueError("输入图像通道数不正确")


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    array = np.asarray(image)
    if array.size == 0:
        raise ValueError("输入图像不能为空数组")
    if array.dtype == np.uint8:
        return np.ascontiguousarray(array)

    array = np.nan_to_num(array.astype(np.float32), nan=0.0, posinf=255.0, neginf=0.0)
    if float(np.max(array)) <= 1.0 and float(np.min(array)) >= 0.0:
        array = array * 255.0
    return np.ascontiguousarray(np.clip(array, 0, 255).astype(np.uint8))
