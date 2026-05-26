# 本文件用于实现高斯滤波平滑图像的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "gaussian_filter",
    "display_name": "高斯滤波",
    "description": "使用高斯核进行平滑处理，适合去除一般噪声并保留较自然的过渡。",
    "params": {
        "kernel_size": {
            "type": "odd_int",
            "default": 5,
            "min": 1,
            "max": 31,
            "label": "滤波核大小"
        },
        "sigma": {
            "type": "float",
            "default": 1.0,
            "min": 0.0,
            "max": 10.0,
            "label": "高斯标准差"
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """
    高斯滤波统一算法入口函数
    """

    # =========================
    # 输入检查
    # =========================
    if image is None:
        raise ValueError("输入图像不能为空")

    if not isinstance(image, np.ndarray):
        raise TypeError("输入图像必须为 numpy.ndarray 类型")

    if params is None:
        params = {}

    # =========================
    # 获取参数
    # =========================
    kernel_size = int(params.get("kernel_size", 5))
    sigma = float(params.get("sigma", 1.0))

    # 保证卷积核大小合法
    kernel_size = max(1, kernel_size)

    # OpenCV 高斯核要求奇数
    if kernel_size % 2 == 0:
        kernel_size += 1

    # =========================
    # 保存原图
    # =========================
    original = image.copy()

    # =========================
    # 执行高斯滤波
    # =========================
    result = cv2.GaussianBlur(
        src=image,
        ksize=(kernel_size, kernel_size),
        sigmaX=sigma
    )

    # =========================
    # 构建步骤图
    # =========================
    steps = [
        {
            "name": "原始图像",
            "image": original
        },
        {
            "name": "高斯滤波结果",
            "image": result
        }
    ]

    # =========================
    # 计算指标
    # =========================
    gray_before = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray_after = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    average_difference = float(
        np.mean(
            np.abs(
                gray_before.astype(np.float32) -
                gray_after.astype(np.float32)
            )
        )
    )

    metrics = {
        "kernel_size": kernel_size,
        "sigma": sigma,
        "average_difference": round(average_difference, 2)
    }

    # =========================
    # 中文分析
    # =========================
    analysis = (
        f"高斯滤波处理完成。"
        f"当前卷积核大小为 {kernel_size}×{kernel_size}，"
        f"高斯标准差为 {sigma}。"
        f"该算法能够有效减少随机噪声，使图像更加平滑，"
        f"同时保持较自然的图像过渡效果，"
        f"适合普通图像降噪和预处理任务。"
    )

    # =========================
    # 返回统一结构
    # =========================
    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }