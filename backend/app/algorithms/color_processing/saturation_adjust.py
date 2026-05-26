# 本文件用于实现动漫图像的饱和度调整功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "color_image",
    "name": "saturation_adjust",
    "display_name": "饱和度调整",
    "description": "调整动漫图像色彩鲜艳程度，使人物和场景颜色更突出。通过 HSV 颜色空间的饱和度通道缩放实现。",
    "params": {
        "saturation_factor": {
            "type": "float",
            "default": 1.5,
            "min": 0.0,
            "max": 3.0,
            "step": 0.1,
            "label": "饱和度系数",
            "component": "slider"
        }
    }
}


def run(image: np.ndarray, params: dict = None) -> dict:
    """统一算法入口函数。"""
    if image is None:
        raise ValueError("输入图像不能为空")

    # 防御：params 可能为 None
    if params is None:
        params = {}

    # 1. 读取并校验参数，使用与 ALGORITHM_META 一致的默认值
    factor = float(params.get("saturation_factor", 1.5))
    factor = max(0.0, min(3.0, factor))

    # 2. 灰度图处理：直接返回原图，不做调整
    if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
        return {
            "result": image.copy(),
            "steps": [
                {"name": "原始图像（灰度）", "image": image}
            ],
            "metrics": {
                "mean_saturation_before": 0.0,
                "mean_saturation_after": 0.0
            },
            "analysis": "输入为灰度图像，无饱和度通道，不进行任何调整，直接返回原图。"
        }

    # 3. Alpha 通道处理：分离并保留
    has_alpha = (image.shape[2] == 4)
    if has_alpha:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]
    else:
        bgr = image
        alpha = None

    # 4. BGR 转 HSV，使用浮点计算避免溢出
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV).astype(np.float32)

    # 5. 记录调整前的平均饱和度
    mean_s_before = float(np.mean(hsv[:, :, 1]))

    # 6. 缩放饱和度通道并截断到有效范围
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0.0, 255.0)

    # 7. 记录调整后的平均饱和度
    mean_s_after = float(np.mean(hsv[:, :, 1]))

    # 8. 提取饱和度通道图像（转为 uint8 供步骤图显示）
    s_channel_display = np.clip(hsv[:, :, 1], 0, 255).astype(np.uint8)

    # 9. 转换回 BGR
    hsv = np.clip(hsv, 0.0, 255.0).astype(np.uint8)
    result_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 10. 如有 Alpha 通道，重新合并
    if has_alpha:
        result = np.dstack((result_bgr, alpha))
    else:
        result = result_bgr

    # 11. 组织分步结果
    steps = [
        {"name": "原始图像", "image": image.copy()},
        {"name": "饱和度通道（S 通道）", "image": s_channel_display},
        {"name": "饱和度调整结果", "image": result}
    ]

    # 12. 生成中文分析
    analysis = (
        f"饱和度系数为 {factor:.1f}，"
        f"平均饱和度从 {mean_s_before:.1f} 变化为 {mean_s_after:.1f}。"
        f"系数大于 1 时颜色更加鲜艳，小于 1 时颜色趋于柔和。"
        f"动漫图像中适当提高饱和度可以让角色发色、服装和场景色彩更加突出。"
    )

    # 13. 返回统一结构
    return {
        "result": result,
        "steps": steps,
        "metrics": {
            "mean_saturation_before": round(mean_s_before, 2),
            "mean_saturation_after": round(mean_s_after, 2)
        },
        "analysis": analysis
    }