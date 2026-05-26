# 本文件用于实现图像频谱中心化处理，将低频分量移至频谱图中心。

import numpy as np
import cv2

ALGORITHM_META = {
    "module": "frequency_analysis",
    "name": "spectrum_shift",
    "display_name": "频谱中心化",
    "description": "对图像进行傅里叶变换后执行频谱搬移（fftshift），将直流分量（低频）从四角移至图像中心，便于直观分析频率分布和进行频域滤波操作。",
    "params": {
        "show_comparison": {"type": "bool", "default": True, "label": "显示中心化前后对比"}
    }
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数。"""
    if params is None:
        params = {}

    # 转为灰度图
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 执行 DFT
    dft = np.fft.fft2(gray.astype(np.float64))

    # 未中心化幅度谱
    magnitude_raw = np.abs(dft)
    log_raw = np.log1p(magnitude_raw)
    raw_norm = cv2.normalize(log_raw, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 频谱中心化
    dft_shift = np.fft.fftshift(dft)
    magnitude_shift = np.abs(dft_shift)
    log_shift = np.log1p(magnitude_shift)
    shift_norm = cv2.normalize(log_shift, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 结果为中心化后的频谱图（BGR）
    result = cv2.cvtColor(shift_norm, cv2.COLOR_GRAY2BGR)
    raw_bgr = cv2.cvtColor(raw_norm, cv2.COLOR_GRAY2BGR)

    steps = [
        {"name": "原始灰度图", "image": cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)},
        {"name": "中心化前频谱", "image": raw_bgr},
        {"name": "中心化后频谱", "image": result}
    ]

    # 计算中心区域能量占比（低频能量）
    h, w = magnitude_shift.shape
    cx, cy = h // 2, w // 2
    radius = min(h, w) // 8
    Y, X = np.ogrid[:h, :w]
    mask = (X - cy) ** 2 + (Y - cx) ** 2 <= radius ** 2
    low_freq_energy = float(np.sum(magnitude_shift[mask] ** 2))
    total_energy = float(np.sum(magnitude_shift ** 2))
    low_freq_ratio = low_freq_energy / (total_energy + 1e-10)

    metrics = {
        "低频能量占比": round(low_freq_ratio * 100, 2),
        "总能量": round(total_energy, 2),
        "低频区域半径(px)": radius
    }

    analysis = (
        "频谱中心化通过 fftshift 操作将零频率（直流）分量从频谱的四个角落搬移到图像中心。"
        "中心化后的频谱图低频集中于中央，高频分布在周围，便于理解图像的频率结构，"
        "也是后续频域滤波（低通/高通滤波器）设计的必要前置步骤。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
