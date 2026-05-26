# 本文件用于实现巴特沃斯高通滤波器对图像进行频域高通滤波。

import numpy as np
import cv2

ALGORITHM_META = {
    "module": "frequency_filter",
    "name": "high_pass_filter",
    "display_name": "高通滤波",
    "description": "使用巴特沃斯高通滤波器在频域对图像进行边缘增强处理，抑制低频成分（平滑区域），保留高频成分（边缘、细节、纹理），可控制截止频率和滤波阶数。",
    "params": {
        "cutoff_ratio": {"type": "float", "default": 0.10, "min": 0.01, "max": 0.99, "label": "截止频率比例"},
        "order": {"type": "int", "default": 2, "min": 1, "max": 10, "label": "巴特沃斯阶数"}
    }
}


def _butterworth_high_pass(shape: tuple, cutoff_ratio: float, order: int) -> np.ndarray:
    """构建巴特沃斯高通滤波器掩模（= 1 - 低通）。"""
    h, w = shape
    cx, cy = h // 2, w // 2
    D0 = cutoff_ratio * min(h, w) / 2.0
    Y, X = np.ogrid[:h, :w]
    D = np.sqrt((X - cy) ** 2 + (Y - cx) ** 2)
    H_low = 1.0 / (1.0 + (D / (D0 + 1e-10)) ** (2 * order))
    H = 1.0 - H_low
    return H


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数。"""
    if params is None:
        params = {}

    cutoff_ratio = float(params.get("cutoff_ratio", 0.10))
    order = int(params.get("order", 2))

    # 转为灰度图处理
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 构建高通滤波器
    H = _butterworth_high_pass(gray.shape, cutoff_ratio, order)

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
        {"name": "高通滤波器掩模", "image": cv2.cvtColor(H_vis, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波前频谱", "image": cv2.cvtColor(spectrum_orig, cv2.COLOR_GRAY2BGR)},
        {"name": "滤波后频谱", "image": cv2.cvtColor(spectrum_filtered, cv2.COLOR_GRAY2BGR)},
        {"name": "高通滤波结果", "image": result}
    ]

    # 计算边缘增强效果
    edges_orig = cv2.Canny(gray, 50, 150)
    edges_result = cv2.Canny(filtered_img, 50, 150)
    edge_ratio_orig = np.sum(edges_orig > 0) / edges_orig.size
    edge_ratio_result = np.sum(edges_result > 0) / edges_result.size
    mean_intensity = float(np.mean(filtered_img))

    metrics = {
        "截止频率比例": cutoff_ratio,
        "巴特沃斯阶数": order,
        "原图边缘密度(%)": round(float(edge_ratio_orig) * 100, 2),
        "结果边缘密度(%)": round(float(edge_ratio_result) * 100, 2),
        "结果平均灰度": round(mean_intensity, 2)
    }

    analysis = (
        f"巴特沃斯高通滤波器（截止频率比例={cutoff_ratio}，阶数={order}）对图像进行了频域边缘增强处理。"
        "高通滤波抑制了图像的低频平滑区域，突出了边缘、轮廓和纹理细节等高频成分。"
        "截止频率越大，保留的细节越少，仅保留最突出的边缘；阶数越高，过渡区域越窄，振铃效应越明显。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }
