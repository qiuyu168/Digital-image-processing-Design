# 本文件用于实现巴特沃斯低通滤波器对图像进行频域低通滤波。

import numpy as np
import cv2

ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "low_pass_filter",
    "display_name": "低通滤波",
    "description": "使用巴特沃斯低通滤波器在频域对图像进行平滑处理，保留低频成分（整体轮廓），抑制高频成分（噪声、细节），可控制截止频率和滤波阶数。",
    "params": {
        "cutoff_ratio": {"type": "float", "default": 0.15, "min": 0.01, "max": 0.99, "label": "截止频率比例"},
        "order": {"type": "int", "default": 2, "min": 1, "max": 10, "label": "巴特沃斯阶数"}
    }
}


def _butterworth_low_pass(shape: tuple, cutoff_ratio: float, order: int) -> np.ndarray:
    """构建巴特沃斯低通滤波器掩模。"""
    h, w = shape
    cx, cy = h // 2, w // 2
    D0 = cutoff_ratio * min(h, w) / 2.0
    Y, X = np.ogrid[:h, :w]
    D = np.sqrt((X - cy) ** 2 + (Y - cx) ** 2)
    H = 1.0 / (1.0 + (D / (D0 + 1e-10)) ** (2 * order))
    return H


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数。"""
    if params is None:
        params = {}

    cutoff_ratio = float(params.get("cutoff_ratio", 0.15))
    order = int(params.get("order", 2))

    # 转为灰度图处理
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 构建滤波器
    H = _butterworth_low_pass(gray.shape, cutoff_ratio, order)

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

    # 滤波器掩模可视化
    H_vis = (H * 255).astype(np.uint8)

    steps = [
        {"name": "原始灰度图", "image": cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)},
        {"name": "低通滤波器掩模", "image": cv2.cvtColor(H_vis, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波前频谱", "image": cv2.cvtColor(spectrum_orig, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波后频谱", "image": cv2.cvtColor(spectrum_filtered, cv2.COLOR_GRAY2BGR)},
        {"name": "低通滤波结果", "image": result}
    ]

    # 计算平滑程度（边缘强度降低量）
    edges_orig = cv2.Canny(gray, 50, 150)
    edges_result = cv2.Canny(filtered_img, 50, 150)
    edge_reduction = 1.0 - (np.sum(edges_result > 0) / (np.sum(edges_orig > 0) + 1e-10))
    psnr = cv2.PSNR(gray, filtered_img)

    metrics = {
        "截止频率比例": cutoff_ratio,
        "巴特沃斯阶数": order,
        "边缘密度降低比(%)": round(float(edge_reduction) * 100, 2),
        "PSNR(dB)": round(float(psnr), 2)
    }

    analysis = (
        f"巴特沃斯低通滤波器（截止频率比例={cutoff_ratio}，阶数={order}）对图像进行了频域平滑处理。"
        "低通滤波保留了图像的整体结构和低频轮廓，同时有效抑制了高频噪声和细节。"
        "截止频率越小，平滑程度越强，图像越模糊；阶数越高，截止特性越陡峭，越接近理想低通滤波器。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
