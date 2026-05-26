# 本文件用于实现理想低通滤波器对图像进行频域滤波。

import numpy as np
import cv2

ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "ideal_low_pass",
    "display_name": "理想低通滤波",
    "description": "使用理想低通滤波器在频域对图像进行滤波，完全阻断截止频率以外的高频成分，保留圆形截止区域内的低频成分。由于频域硬截断，结果图像会出现明显的振铃效应（Gibbs现象）。",
    "params": {
        "cutoff_ratio": {"type": "float", "default": 0.15, "min": 0.01, "max": 0.99, "label": "截止频率比例"}
    }
}


def _ideal_low_pass(shape: tuple, cutoff_ratio: float) -> np.ndarray:
    """构建理想低通滤波器掩模（圆形二值掩模）。"""
    h, w = shape
    cx, cy = h // 2, w // 2
    D0 = cutoff_ratio * min(h, w) / 2.0
    Y, X = np.ogrid[:h, :w]
    D = np.sqrt((X - cy) ** 2 + (Y - cx) ** 2)
    H = (D <= D0).astype(np.float64)
    return H


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数。"""
    if params is None:
        params = {}

    cutoff_ratio = float(params.get("cutoff_ratio", 0.15))

    # 转为灰度图处理
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 构建理想低通滤波器
    H = _ideal_low_pass(gray.shape, cutoff_ratio)

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

    # 滤波器掩模可视化（二值圆形）
    H_vis = (H * 255).astype(np.uint8)

    steps = [
        {"name": "原始灰度图", "image": cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)},
        {"name": "理想低通掩模（圆形）", "image": cv2.cvtColor(H_vis, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波前频谱", "image": cv2.cvtColor(spectrum_orig, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波后频谱", "image": cv2.cvtColor(spectrum_filtered, cv2.COLOR_GRAY2BGR)},
        {"name": "理想低通滤波结果", "image": result}
    ]

    # 计算通过频率比例和振铃评估
    pass_ratio = float(np.sum(H)) / H.size
    psnr = cv2.PSNR(gray, filtered_img)

    # 振铃效应评估：检测滤波结果中的局部震荡（与原图差异）
    diff = cv2.absdiff(gray, filtered_img)
    ringing_strength = float(np.mean(diff))

    metrics = {
        "截止频率比例": cutoff_ratio,
        "通过频率点占比(%)": round(pass_ratio * 100, 2),
        "PSNR(dB)": round(float(psnr), 2),
        "振铃强度（均值差异）": round(ringing_strength, 2)
    }

    analysis = (
        f"理想低通滤波器（截止频率比例={cutoff_ratio}）在频域使用圆形二值掩模，"
        "完全保留截止频率以内的低频成分，完全阻断截止频率以外的高频成分。"
        "由于频域的硬截断对应空域的 sinc 函数，因此结果图像会在边缘附近产生明显的振铃效应（Gibbs现象）。"
        "截止频率越小，平滑越强，振铃越明显；相比巴特沃斯滤波器，理想低通的振铃效应更严重。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
