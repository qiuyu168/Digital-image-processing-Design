# 本文件用于实现高斯高通滤波器对图像进行频域边缘增强处理。

import numpy as np
import cv2

ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "gaussian_high_pass",
    "display_name": "高斯高通滤波",
    "description": "使用高斯高通滤波器在频域对图像进行边缘增强，频率响应为1减去高斯低通，过渡平滑无振铃效应。可用于图像锐化、边缘提取和细节增强，效果优于理想高通滤波器。",
    "params": {
        "sigma_ratio": {"type": "float", "default": 0.10, "min": 0.01, "max": 0.99, "label": "高斯标准差比例（控制截止带宽）"}
    }
}


def _gaussian_high_pass(shape: tuple, sigma_ratio: float) -> np.ndarray:
    """构建高斯高通滤波器掩模（= 1 - 高斯低通）。"""
    h, w = shape
    cx, cy = h // 2, w // 2
    sigma = sigma_ratio * min(h, w) / 2.0
    Y, X = np.ogrid[:h, :w]
    D2 = (X - cy) ** 2 + (Y - cx) ** 2
    H_low = np.exp(-D2 / (2.0 * sigma ** 2))
    H = 1.0 - H_low
    return H


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数。"""
    if params is None:
        params = {}

    sigma_ratio = float(params.get("sigma_ratio", 0.10))

    # 转为灰度图处理
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 构建高斯高通滤波器
    H = _gaussian_high_pass(gray.shape, sigma_ratio)

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

    # 滤波器掩模可视化（中心低响应、边缘高响应）
    H_vis = (H * 255).astype(np.uint8)

    steps = [
        {"name": "原始灰度图", "image": cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)},
        {"name": "高斯高通掩模", "image": cv2.cvtColor(H_vis, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波前频谱", "image": cv2.cvtColor(spectrum_orig, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波后频谱", "image": cv2.cvtColor(spectrum_filtered, cv2.COLOR_GRAY2BGR)},
        {"name": "高斯高通滤波结果", "image": result}
    ]

    # 指标计算
    edges_orig = cv2.Canny(gray, 50, 150)
    edges_result = cv2.Canny(filtered_img, 50, 150)
    edge_density_orig = float(np.sum(edges_orig > 0)) / edges_orig.size
    edge_density_result = float(np.sum(edges_result > 0)) / edges_result.size
    mean_intensity = float(np.mean(filtered_img))
    D0_px = sigma_ratio * min(gray.shape) / 2.0

    metrics = {
        "高斯标准差比例": sigma_ratio,
        "截止频率半径(px)": round(D0_px, 1),
        "原图边缘密度(%)": round(edge_density_orig * 100, 2),
        "结果边缘密度(%)": round(edge_density_result * 100, 2),
        "结果平均灰度": round(mean_intensity, 2)
    }

    analysis = (
        f"高斯高通滤波器（sigma比例={sigma_ratio}）由 1 减去高斯低通得到，频率响应从中心向外平滑增强。"
        "与理想高通相比，高斯高通的过渡区域更平滑，不产生振铃效应，边缘提取结果更自然。"
        "由于完全去除直流分量（DC），输出图像整体偏暗，主要呈现各类边缘轮廓和纹理细节。"
        "sigma越小，截止带宽越窄，保留的细节越丰富，包含更多高频噪声。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
