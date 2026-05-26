# 本文件用于实现高斯低通滤波器对图像进行频域平滑处理。

import numpy as np
import cv2

ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "gaussian_low_pass",
    "display_name": "高斯低通滤波",
    "description": "使用高斯低通滤波器在频域对图像进行平滑处理，频率响应呈高斯分布，过渡平滑无振铃效应。可用于图像去噪、模糊和预处理，效果优于理想低通滤波器。",
    "params": {
        "sigma_ratio": {"type": "float", "default": 0.15, "min": 0.01, "max": 0.99, "label": "高斯标准差比例（控制截止带宽）"}
    }
}


def _gaussian_low_pass(shape: tuple, sigma_ratio: float) -> np.ndarray:
    """构建高斯低通滤波器掩模。"""
    h, w = shape
    cx, cy = h // 2, w // 2
    sigma = sigma_ratio * min(h, w) / 2.0
    Y, X = np.ogrid[:h, :w]
    D2 = (X - cy) ** 2 + (Y - cx) ** 2
    H = np.exp(-D2 / (2.0 * sigma ** 2))
    return H


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数。"""
    if params is None:
        params = {}

    sigma_ratio = float(params.get("sigma_ratio", 0.15))

    # 转为灰度图处理
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 构建高斯低通滤波器
    H = _gaussian_low_pass(gray.shape, sigma_ratio)

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

    # 滤波器掩模可视化（高斯形状）
    H_vis = (H * 255).astype(np.uint8)

    steps = [
        {"name": "原始灰度图", "image": cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)},
        {"name": "高斯低通掩模", "image": cv2.cvtColor(H_vis, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波前频谱", "image": cv2.cvtColor(spectrum_orig, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波后频谱", "image": cv2.cvtColor(spectrum_filtered, cv2.COLOR_GRAY2BGR)},
        {"name": "高斯低通滤波结果", "image": result}
    ]

    # 指标计算
    psnr = cv2.PSNR(gray, filtered_img)
    edges_orig = cv2.Canny(gray, 50, 150)
    edges_result = cv2.Canny(filtered_img, 50, 150)
    edge_reduction = 1.0 - (np.sum(edges_result > 0) / (np.sum(edges_orig > 0) + 1e-10))

    # 半功率截止频率（sigma 处响应为 e^{-0.5} ≈ 0.607）
    D0_px = sigma_ratio * min(gray.shape) / 2.0

    metrics = {
        "高斯标准差比例": sigma_ratio,
        "截止频率半径(px)": round(D0_px, 1),
        "PSNR(dB)": round(float(psnr), 2),
        "边缘密度降低比(%)": round(float(edge_reduction) * 100, 2)
    }

    analysis = (
        f"高斯低通滤波器（sigma比例={sigma_ratio}）的频率响应呈高斯分布，从中心向外平滑衰减。"
        "由于高斯函数的傅里叶变换仍是高斯函数，空域中等效于高斯核的卷积操作，因此不产生振铃效应。"
        "与理想低通滤波相比，高斯低通的平滑效果更自然；sigma越大，平滑范围越广，图像越模糊。"
        "高斯低通滤波常用于图像预处理、噪声抑制和尺度空间构建。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
