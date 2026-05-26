# 本文件用于实现动漫图像的主色调提取功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "color_processing",
    "name": "dominant_color_extract",
    "display_name": "主色调提取",
    "description": "通过 K-Means 聚类提取动漫人物的头发、服装、背景等区域的主要颜色，生成色板与色彩占比分析。",
    "params": {
        "n_colors": {
            "type": "int",
            "default": 5,
            "min": 2,
            "max": 10,
            "label": "提取颜色数量"
        }
    }
}


def _bgr_to_hex(bgr: np.ndarray) -> str:
    """BGR 颜色值转为十六进制字符串（RGB 序）。"""
    r, g, b = int(bgr[2]), int(bgr[1]), int(bgr[0])
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def _create_palette_image(colors_bgr: list, percentages: list,
                          bar_height: int = 60, bar_width: int = 400) -> np.ndarray:
    """生成主色调色板可视化图像。

    Args:
        colors_bgr: BGR 颜色列表，每个颜色为 (3,) 的 uint8 ndarray。
        percentages: 对应的占比列表（0~100）。
        bar_height: 色板高度。
        bar_width: 色板宽度。

    Returns:
        色板 BGR 图像，shape (bar_height, bar_width, 3)。
    """
    palette = np.zeros((bar_height, bar_width, 3), dtype=np.uint8)
    x_start = 0
    for color, pct in zip(colors_bgr, percentages):
        width = max(1, int(bar_width * pct / 100.0))
        x_end = min(x_start + width, bar_width)
        palette[:, x_start:x_end] = color
        x_start = x_end
    return palette


def run(image: np.ndarray, params: dict) -> dict:
    """统一算法入口函数。"""
    if image is None:
        raise ValueError("输入图像不能为空")

    # 1. 读取并校验参数
    n_colors = int(params.get("n_colors", 5))
    if n_colors < 2:
        n_colors = 2
    if n_colors > 10:
        n_colors = 10

    # 2. 确保为三通道彩色图像
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    h, w = image.shape[:2]

    # 3. 降采样以加速 K-Means（最多处理约 20000 像素）
    max_pixels = 20000
    total_pixels = h * w
    if total_pixels > max_pixels:
        scale = (max_pixels / total_pixels) ** 0.5
        small_h, small_w = int(h * scale), int(w * scale)
        small_img = cv2.resize(image, (small_w, small_h), interpolation=cv2.INTER_AREA)
        n_colors = min(n_colors, small_h * small_w)
    else:
        small_img = image

    # 4. 重塑为二维像素数组并做 K-Means 聚类
    pixels = small_img.reshape(-1, 3).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(
        pixels, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    centers = centers.astype(np.uint8)

    # 5. 统计各聚类的像素数量与占比
    unique, counts = np.unique(labels, return_counts=True)
    total = counts.sum()
    color_data = []
    for idx, count in zip(unique, counts):
        pct = round(count / total * 100, 2)
        hex_color = _bgr_to_hex(centers[idx])
        color_data.append({
            "color_bgr": centers[idx].tolist(),
            "color_hex": hex_color,
            "percentage": pct,
            "pixel_count": int(count)
        })

    # 按占比降序排列
    color_data.sort(key=lambda x: x["percentage"], reverse=True)

    # 6. 生成量化图像（每个像素替换为所属聚类中心颜色）
    quantized_small = centers[labels.flatten()].reshape(small_img.shape).astype(np.uint8)
    if total_pixels > max_pixels:
        quantized = cv2.resize(quantized_small, (w, h), interpolation=cv2.INTER_NEAREST)
    else:
        quantized = quantized_small

    # 7. 生成色板图像
    palette_colors = [
        np.array(c["color_bgr"], dtype=np.uint8) for c in color_data
    ]
    palette_pcts = [c["percentage"] for c in color_data]
    palette_img = _create_palette_image(palette_colors, palette_pcts)

    # 8. 组织色彩描述文本
    color_info_lines = []
    for i, c in enumerate(color_data):
        color_info_lines.append(
            f"第{i + 1}主色 {c['color_hex']} 占比 {c['percentage']:.1f}%"
        )

    # 9. 组织分步结果
    steps = [
        {"name": "原始图像", "image": image},
        {"name": "色彩量化结果", "image": quantized},
        {"name": "主色调色板", "image": palette_img}
    ]

    analysis = (
        f"提取了 {len(color_data)} 种主色调。" + "；".join(color_info_lines) + "。"
        f"动漫图像的色调分布可以反映角色发色、服装颜色和背景氛围色，"
        f"色彩量化图将原图简化为有限的几种主色，直观展示图像的整体色彩构成。"
    )

    return {
        "result": quantized,
        "steps": steps,
        "metrics": {},
        "analysis": analysis,
        "extra": {
            "dominant_colors": [
                {"hex": c["color_hex"], "percentage": c["percentage"]}
                for c in color_data
            ]
        }
    }
