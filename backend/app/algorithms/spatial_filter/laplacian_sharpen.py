# 本文件用于实现拉普拉斯锐化增强边缘的功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "spatial_filter",
    "name": "laplacian_sharpen",
    "display_name": "拉普拉斯锐化",
    "description": "增强图像边缘和细节，使轮廓更清晰。",
    "params": {
        "amount": {
            "type": "float",
            "default": 0.5,
            "min": 0.0,
            "max": 3.0,
            "label": "锐化强度"
        },
    },
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """
    拉普拉斯锐化统一算法入口函数
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
    amount = float(params.get("amount", 0.5))

    # 防止负值
    amount = max(0.0, amount)

    # =========================
    # 保存原图
    # =========================
    original = image.copy()

    # =========================
    # 转换为 float 防止溢出
    # =========================
    image_float = image.astype(np.float32)

    # =========================
    # 拉普拉斯边缘检测
    # =========================
    laplacian = cv2.Laplacian(
        image_float,
        cv2.CV_32F,
        ksize=3
    )

    # =========================
    # 锐化处理
    # 原图 - 拉普拉斯结果
    # =========================
    sharpened = image_float - amount * laplacian

    # 限制范围到 0~255
    sharpened = np.clip(sharpened, 0, 255)

    # 转回 uint8
    result = sharpened.astype(np.uint8)

    # =========================
    # 构建步骤图
    # =========================
    laplacian_display = cv2.convertScaleAbs(laplacian)

    steps = [
        {
            "name": "原始图像",
            "image": original
        },
        {
            "name": "拉普拉斯边缘",
            "image": laplacian_display
        },
        {
            "name": "锐化结果",
            "image": result
        }
    ]

    # =========================
    # 计算指标
    # =========================
    gray_original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    sharpness_difference = float(
        np.mean(
            np.abs(
                gray_result.astype(np.float32) -
                gray_original.astype(np.float32)
            )
        )
    )

    metrics = {
        "amount": amount,
        "average_difference": round(sharpness_difference, 2)
    }

    # =========================
    # 中文分析
    # =========================
    analysis = (
        f"拉普拉斯锐化处理完成。"
        f"当前锐化强度为 {amount}。"
        f"该算法通过增强图像中的高频边缘信息，"
        f"提升人物轮廓、纹理和场景细节清晰度。"
        f"适用于动漫图像、边缘增强和细节突出处理。"
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