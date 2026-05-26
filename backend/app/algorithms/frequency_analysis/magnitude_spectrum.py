# 本文件用于实现图像幅度谱的计算与可视化显示。

import numpy as np
import cv2

ALGORITHM_META = {
    "module": "frequency_analysis",
    "name": "magnitude_spectrum",
    "display_name": "幅度谱显示",
    "description": "计算图像傅里叶变换的幅度谱，支持线性与对数两种刻度显示，并统计高低频能量分布，用于分析图像纹理复杂度与频率特征。",
    "params": {
        "scale_mode": {
            "type": "str",
            "default": "log",
            "options": ["log", "linear"],
            "label": "幅度刻度模式"
        },
        "colormap": {
            "type": "bool",
            "default": True,
            "label": "使用伪彩色映射"
        }
    }
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数。"""
    if params is None:
        params = {}

    scale_mode = params.get("scale_mode", "log")
    use_colormap = params.get("colormap", True)

    # 转为灰度图
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 执行 DFT 并中心化
    dft = np.fft.fft2(gray.astype(np.float64))
    dft_shift = np.fft.fftshift(dft)
    magnitude = np.abs(dft_shift)

    # 按刻度模式计算显示用幅度谱
    if scale_mode == "log":
        display_mag = np.log1p(magnitude)
        scale_label = "对数幅度谱"
    else:
        display_mag = magnitude.copy()
        scale_label = "线性幅度谱"

    # 归一化
    mag_norm = cv2.normalize(display_mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 伪彩色映射增强可视化
    if use_colormap:
        result = cv2.applyColorMap(mag_norm, cv2.COLORMAP_JET)
    else:
        result = cv2.cvtColor(mag_norm, cv2.COLOR_GRAY2BGR)

    # 线性幅度谱（对比步骤用）
    linear_norm = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    log_norm = cv2.normalize(np.log1p(magnitude), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    steps = [
        {"name": "原始灰度图", "image": cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)},
        {"name": "线性幅度谱", "image": cv2.cvtColor(linear_norm, cv2.COLOR_GRAY2BGR)},
        {"name": scale_label, "image": result}
    ]

    # 统计频率能量分布
    h, w = magnitude.shape
    cx, cy = h // 2, w // 2
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - cy) ** 2 + (Y - cx) ** 2)
    max_dist = np.sqrt(cx ** 2 + cy ** 2)

    total_energy = float(np.sum(magnitude ** 2))
    low_energy = float(np.sum((magnitude[dist <= max_dist * 0.1]) ** 2))
    mid_energy = float(np.sum((magnitude[(dist > max_dist * 0.1) & (dist <= max_dist * 0.4)]) ** 2))
    high_energy = float(np.sum((magnitude[dist > max_dist * 0.4]) ** 2))

    metrics = {
        "低频能量占比(%)": round(low_energy / (total_energy + 1e-10) * 100, 2),
        "中频能量占比(%)": round(mid_energy / (total_energy + 1e-10) * 100, 2),
        "高频能量占比(%)": round(high_energy / (total_energy + 1e-10) * 100, 2),
        "峰值幅度": round(float(np.max(magnitude)), 2)
    }

    analysis = (
        f"幅度谱以{scale_label}展示了图像各频率成分的强度分布。"
        "低频能量集中于中心，对应图像的平滑背景和整体亮度变化；"
        "高频能量分布于外围，对应图像的边缘、细节和噪声成分。"
        "图像纹理越复杂，高频能量占比越高；图像越平滑，低频能量越集中。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
