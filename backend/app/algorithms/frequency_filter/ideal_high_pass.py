# 本文件用于实现理想高通滤波器对图像进行频域边缘提取。

import numpy as np
import cv2

ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "ideal_high_pass",
    "display_name": "理想高通滤波",
    "description": "使用理想高通滤波器在频域对图像进行边缘增强，完全阻断截止频率以内的低频成分，仅保留圆形截止区域以外的高频成分（边缘、细节）。结果会出现振铃效应。",
    "params": {
        "cutoff_ratio": {"type": "float", "default": 0.10, "min": 0.01, "max": 0.99, "label": "截止频率比例"}
    }
}


def _ideal_high_pass(shape: tuple, cutoff_ratio: float) -> np.ndarray:
    """构建理想高通滤波器掩模（= 1 - 理想低通掩模）。"""
    h, w = shape
    cx, cy = h // 2, w // 2
    D0 = cutoff_ratio * min(h, w) / 2.0
    Y, X = np.ogrid[:h, :w]
    D = np.sqrt((X - cy) ** 2 + (Y - cx) ** 2)
    H = (D > D0).astype(np.float64)
    return H


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数。"""
    if params is None:
        params = {}

    cutoff_ratio = float(params.get("cutoff_ratio", 0.10))

    # 转为灰度图处理
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 构建理想高通滤波器
    H = _ideal_high_pass(gray.shape, cutoff_ratio)

    # 频域滤波
    dft = np.fft.fft2(gray.astype(np.float64))
    dft_shift = np.fft.fftshift(dft)
    filtered_shift = dft_shift * H

    # 逆变换
    filtered = np.fft.ifft2(np.fft.ifftshift(filtered_shift))
    filtered_img = np.clip(np.abs(filtered), 0, 255).astype(np.uint8)

    # 彩色输出
    result = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR)

    # 频谱可视化
    spectrum_orig = np.log1p(np.abs(dft_shift))
    spectrum_orig = cv2.normalize(spectrum_orig, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    spectrum_filtered = np.log1p(np.abs(filtered_shift))
    spectrum_filtered = cv2.normalize(spectrum_filtered, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 滤波器掩模可视化（中心圆孔）
    H_vis = (H * 255).astype(np.uint8)

    steps = [
        {"name": "原始灰度图", "image": cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)},
        {"name": "理想高通掩模（圆孔）", "image": cv2.cvtColor(H_vis, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波前频谱", "image": cv2.cvtColor(spectrum_orig, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波后频谱", "image": cv2.cvtColor(spectrum_filtered, cv2.COLOR_GRAY2BGR)},
        {"name": "理想高通滤波结果", "image": result}
    ]

    # 计算边缘增强效果
    pass_ratio = float(np.sum(H)) / H.size
    edges = cv2.Canny(filtered_img, 50, 150)
    edge_density = float(np.sum(edges > 0)) / edges.size
    mean_intensity = float(np.mean(filtered_img))

    metrics = {
        "截止频率比例": cutoff_ratio,
        "通过频率点占比(%)": round(pass_ratio * 100, 2),
        "结果边缘密度(%)": round(edge_density * 100, 2),
        "结果平均灰度": round(mean_intensity, 2)
    }

    analysis = (
        f"理想高通滤波器（截止频率比例={cutoff_ratio}）在频域中心挖去圆形低频区域，"
        "完全阻断截止频率内的低频成分，仅保留高频成分。"
        "结果图像主要呈现图像边缘和细节，背景区域趋于黑色（低频被完全去除）。"
        "由于频域的硬截断，结果同样存在振铃效应；相比巴特沃斯高通，边缘细节更锐利但伴随更多伪影。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
