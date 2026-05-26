# 本文件用于实现双边滤波平滑并保留边缘的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "bilateral_filter",
    "display_name": "双边滤波",
    "description": "在平滑图像的同时尽量保留边缘，适合动漫线条图像降噪。",
    "params": {
        "diameter": {
            "type": "int",
            "default": 9,
            "min": 1,
            "max": 31,
            "label": "邻域直径"
        },
        "sigma_color": {
            "type": "float",
            "default": 75.0,
            "min": 1.0,
            "max": 200.0,
            "label": "颜色标准差"
        },
        "sigma_space": {
            "type": "float",
            "default": 75.0,
            "min": 1.0,
            "max": 200.0,
            "label": "空间标准差"
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """
    双边滤波统一算法入口
    :param image: OpenCV BGR 图像
    :param params: 参数字典
    :return: 标准算法返回结构
    """

    # =========================
    # 输入检查
    # =========================
    if image is None:
        raise ValueError("输入图像不能为空")

    if not isinstance(image, np.ndarray):
        raise TypeError("输入图像必须是 numpy.ndarray 类型")

    if params is None:
        params = {}

    # =========================
    # 读取参数
    # =========================
    diameter = int(params.get("diameter", 9))
    sigma_color = float(params.get("sigma_color", 75.0))
    sigma_space = float(params.get("sigma_space", 75.0))

    # 防止非法参数
    diameter = max(1, diameter)

    # OpenCV 要求直径最好为奇数
    if diameter % 2 == 0:
        diameter += 1

    # =========================
    # 保存原图
    # =========================
    original = image.copy()

    # =========================
    # 执行双边滤波
    # =========================
    filtered = cv2.bilateralFilter(
        src=image,
        d=diameter,
        sigmaColor=sigma_color,
        sigmaSpace=sigma_space
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
            "name": "双边滤波结果",
            "image": filtered
        }
    ]

    # =========================
    # 指标信息
    # =========================
    gray_before = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray_after = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

    noise_difference = float(
        np.mean(
            np.abs(
                gray_before.astype(np.float32) -
                gray_after.astype(np.float32)
            )
        )
    )

    metrics = {
        "diameter": diameter,
        "sigma_color": sigma_color,
        "sigma_space": sigma_space,
        "average_difference": round(noise_difference, 2)
    }

    # =========================
    # 中文分析
    # =========================
    analysis = (
        f"双边滤波处理完成。"
        f"当前邻域直径为 {diameter}，"
        f"颜色标准差为 {sigma_color}，"
        f"空间标准差为 {sigma_space}。"
        f"该算法能够在降低图像噪声的同时较好保留边缘信息，"
        f"适合动漫图像、人物线条和平滑区域处理。"
    )

    # =========================
    # 返回统一结构
    # =========================
    return {
        "result": filtered,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }