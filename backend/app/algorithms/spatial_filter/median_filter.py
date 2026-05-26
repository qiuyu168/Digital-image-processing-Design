# 本文件用于实现中值滤波去除噪声的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "median_filter",
    "display_name": "中值滤波",
    "description": "使用邻域中值替代中心像素，对椒盐噪声有较好去除效果。",
    "params": {
        "kernel_size": {
            "type": "odd_int",
            "default": 5,
            "min": 1,
            "max": 31,
            "label": "滤波核大小"
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """
    中值滤波统一算法入口函数
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

    # 防止非法参数
    kernel_size = max(1, kernel_size)

    # OpenCV 中值滤波要求必须为奇数
    if kernel_size % 2 == 0:
        kernel_size += 1

    # =========================
    # 保存原图
    # =========================
    original = image.copy()

    # =========================
    # 执行中值滤波
    # =========================
    result = cv2.medianBlur(
        src=image,
        ksize=kernel_size
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
            "name": "中值滤波结果",
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
        "average_difference": round(average_difference, 2)
    }

    # =========================
    # 中文分析
    # =========================
    analysis = (
        f"中值滤波处理完成。"
        f"当前滤波核大小为 {kernel_size}×{kernel_size}。"
        f"该算法通过使用邻域像素的中值替代中心像素，"
        f"能够有效去除椒盐噪声和孤立噪点，"
        f"同时较好保留图像边缘信息。"
        f"适用于动漫图像、老照片和含噪图像预处理。"
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