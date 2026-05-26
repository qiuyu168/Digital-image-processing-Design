# 本文件用于实现动漫图像的 Canny 边缘检测功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "grayscale_image",
    "name": "edge_detection_basic",
    "display_name": "边缘检测",
    "description": "用于提取动漫人物轮廓、头发边缘、场景建筑线条等边缘信息。",
    "params": {
        "threshold1": {
            "type": "int",
            "default": 80,
            "min": 0,
            "max": 255,
            "label": "低阈值"
        },
        "threshold2": {
            "type": "int",
            "default": 160,
            "min": 0,
            "max": 255,
            "label": "高阈值"
        },
        "blur_size": {
            "type": "odd_int",
            "default": 3,
            "min": 1,
            "max": 15,
            "label": "高斯核大小"
        }
    }
}


def run(image: np.ndarray, params: dict | None = None) -> dict:
    """统一算法入口函数"""

    if params is None:
        params = {}

    threshold1 = int(params.get("threshold1", 80))
    threshold2 = int(params.get("threshold2", 160))
    blur_size = int(params.get("blur_size", 3))

    threshold1 = max(0, min(255, threshold1))
    threshold2 = max(0, min(255, threshold2))

    if blur_size < 1:
        blur_size = 1

    if blur_size % 2 == 0:
        blur_size += 1

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(
        gray,
        (blur_size, blur_size),
        0
    )

    edge = cv2.Canny(
        blurred,
        threshold1,
        threshold2
    )

    edge_density = float(np.count_nonzero(edge)) / float(edge.size)

    result = edge

    steps = [
        {
            "name": "灰度化",
            "image": gray
        },
        {
            "name": "高斯平滑",
            "image": blurred
        },
        {
            "name": "Canny边缘检测",
            "image": edge
        }
    ]

    metrics = {
        "threshold1": threshold1,
        "threshold2": threshold2,
        "blur_size": blur_size,
        "edge_density": round(edge_density, 4)
    }

    analysis = (
        "Canny算法能够有效提取动漫人物轮廓、头发边缘和场景线条。"
        "较低阈值会检测更多边缘，但可能引入噪声。"
    )

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis
    }