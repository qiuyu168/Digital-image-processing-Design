# 本文件用于实现颜色空间转换功能（RGB↔HSV、RGB→CMYK）

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "color_processing",
    "name": "color_space_convert",
    "display_name": "颜色空间转换",
    "description": "实现 RGB 与 HSV 之间的相互转换，以及 RGB 到 CMYK 的转换，并自动提取主色调及其 HSV、CMYK 数值对照表。",
    "params": {
        "conversion_type": {
            "type": "select",
            "default": "bgr_to_hsv",
            "options": [
                {"value": "bgr_to_hsv", "label": "RGB → HSV"},
                {"value": "hsv_to_bgr", "label": "HSV → RGB"},
                {"value": "bgr_to_cmyk", "label": "RGB → CMYK"}
            ],
            "label": "转换类型"
        },
        "n_colors": {
            "type": "int",
            "default": 5,
            "min": 2,
            "max": 10,
            "label": "主色调数量",
            "description": "提取的主色调个数，用于生成 HSV/CMYK 数值对照表"
        }
    }
}


def _channel_to_bgr(channel: np.ndarray) -> np.ndarray:
    """单通道灰度图转为 BGR 三通道图像，便于前端统一展示。"""
    return cv2.cvtColor(channel, cv2.COLOR_GRAY2BGR)


def _bgr_to_hsv_impl(image: np.ndarray):
    """BGR → HSV 转换，返回 HSV 图像及各通道。"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    return hsv, h, s, v


def _hsv_to_bgr_impl(image: np.ndarray) -> np.ndarray:
    """HSV → BGR 转换。"""
    return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)


def _bgr_to_cmyk_impl(image: np.ndarray):
    """BGR → CMYK 转换，返回 CMYK 可视化预览图及各通道。

    公式（基于归一化 RGB）：
        K = 1 - max(R', G', B')
        C = (1 - R' - K) / (1 - K)   (K ≠ 1 时)
        M = (1 - G' - K) / (1 - K)
        Y = (1 - B' - K) / (1 - K)

    可视化使用减色模型逆变换，模拟白色纸张上的油墨叠加效果。
    """
    # BGR → RGB 再归一化到 [0, 1]
    rgb = image.astype(np.float32)
    b, g, r = cv2.split(rgb)
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    k_channel = 1.0 - np.maximum(np.maximum(r_norm, g_norm), b_norm)
    denom = 1.0 - k_channel
    zero_mask = denom == 0.0
    denom_safe = np.where(zero_mask, 1.0, denom)

    c_channel = np.where(zero_mask, 0.0, (1.0 - r_norm - k_channel) / denom_safe)
    m_channel = np.where(zero_mask, 0.0, (1.0 - g_norm - k_channel) / denom_safe)
    y_channel = np.where(zero_mask, 0.0, (1.0 - b_norm - k_channel) / denom_safe)

    c_u8 = (c_channel * 255.0).astype(np.uint8)
    m_u8 = (m_channel * 255.0).astype(np.uint8)
    y_u8 = (y_channel * 255.0).astype(np.uint8)
    k_u8 = (k_channel * 255.0).astype(np.uint8)

    # ---- 修正：使用减色模型逆变换生成正确的预览图 ----
    # 模拟油墨叠加效果：C' = C*(1-K) + K，M'、Y' 同理
    c_with_k = np.clip(c_channel * (1.0 - k_channel) + k_channel, 0.0, 1.0)
    m_with_k = np.clip(m_channel * (1.0 - k_channel) + k_channel, 0.0, 1.0)
    y_with_k = np.clip(y_channel * (1.0 - k_channel) + k_channel, 0.0, 1.0)

    # 从 CMY 反算 RGB（减色模型：R=1-C, G=1-M, B=1-Y）
    r_show = ((1.0 - c_with_k) * 255.0).astype(np.uint8)
    g_show = ((1.0 - m_with_k) * 255.0).astype(np.uint8)
    b_show = ((1.0 - y_with_k) * 255.0).astype(np.uint8)

    cmyk_vis = cv2.merge([b_show, g_show, r_show])  # BGR 顺序
    # -------------------------------------------------

    return cmyk_vis, c_u8, m_u8, y_u8, k_u8


def _extract_color_table(image_bgr: np.ndarray, n_colors: int = 5) -> list:
    """
    基于 BGR 图像提取主色调，并给出 BGR、HSV、CMYK 对照表。
    参数:
        image_bgr: 输入 BGR 彩色图像 (uint8, shape=(H,W,3))
        n_colors: 聚类的主色调数量
    返回:
        列表，每个元素为字典：
        {
            "bgr": [B, G, R],
            "hsv": [H, S, V],
            "cmyk": [C, M, Y, K],   # 百分比值 (0-100)
            "percentage": 面积占比 (%)，保留一位小数
        }
    """
    if len(image_bgr.shape) != 3 or image_bgr.shape[2] != 3:
        # 如果不是三通道，直接返回空表
        return []

    pixels = image_bgr.reshape(-1, 3).astype(np.float32)

    # K-Means 聚类主色调
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(
        pixels, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    centers = centers.astype(np.uint8)
    labels = labels.flatten()
    total_pixels = len(labels)

    color_table = []
    for i, bgr in enumerate(centers):
        # 面积占比
        ratio = np.sum(labels == i) / total_pixels

        # BGR → HSV
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        # BGR → CMYK (百分比)
        r, g, b_val = bgr[2] / 255.0, bgr[1] / 255.0, bgr[0] / 255.0
        k = 1.0 - max(r, g, b_val)
        if k < 1.0:
            c = (1.0 - r - k) / (1.0 - k)
            m = (1.0 - g - k) / (1.0 - k)
            y = (1.0 - b_val - k) / (1.0 - k)
        else:
            c = m = y = 0.0

        cmyk_percent = [
            round(c * 100, 1),
            round(m * 100, 1),
            round(y * 100, 1),
            round(k * 100, 1)
        ]

        color_table.append({
            "bgr": [int(bgr[0]), int(bgr[1]), int(bgr[2])],
            "hsv": [int(hsv[0]), int(hsv[1]), int(hsv[2])],
            "cmyk": cmyk_percent,
            "percentage": round(ratio * 100, 1)
        })

    # 按面积占比降序排列
    color_table.sort(key=lambda x: x["percentage"], reverse=True)
    return color_table


def run(image: np.ndarray, params: dict) -> dict:
    """统一算法入口函数。"""
    if image is None:
        raise ValueError("输入图像不能为空")

    conversion_type = params.get("conversion_type", "bgr_to_hsv")
    n_colors = params.get("n_colors", 5)

    valid_types = ["bgr_to_hsv", "hsv_to_bgr", "bgr_to_cmyk"]
    if conversion_type not in valid_types:
        conversion_type = "bgr_to_hsv"

    steps = [{"name": "原始图像", "image": image}]
    metrics = {}
    analysis = ""

    # ---------- 颜色转换 ----------
    if conversion_type == "bgr_to_hsv":
        if len(image.shape) == 2:
            raise ValueError("BGR → HSV 转换需要输入三通道彩色图像")
        hsv, h, s, v = _bgr_to_hsv_impl(image)
        result = image  # HSV 数据不可直接显示，保留原图作为 result
        steps.extend([
            {"name": "HSV 色调通道（H）", "image": _channel_to_bgr(h)},
            {"name": "HSV 饱和度通道（S）", "image": _channel_to_bgr(s)},
            {"name": "HSV 明度通道（V）", "image": _channel_to_bgr(v)}
        ])
        metrics = {
            "mean_hue": round(float(np.mean(h)), 2),
            "mean_saturation": round(float(np.mean(s)), 2),
            "mean_value": round(float(np.mean(v)), 2)
        }
        analysis = (
            "RGB → HSV 转换完成。H 通道表示色调（色相角），S 通道表示饱和度（颜色纯度），"
            "V 通道表示明度（亮度）。HSV 空间将颜色与亮度分离，更符合人眼感知习惯，"
            "适合进行颜色分析和饱和度、亮度调整。动漫图像在 HSV 空间中通常具有较高的饱和度值。"
            "注意：HSV 为数据处理空间，结果图像不可直接显示，此处显示原图。"
        )
        # 颜色表基于原始 BGR 图像
        src_for_table = image

    elif conversion_type == "hsv_to_bgr":
        if len(image.shape) != 3 or image.shape[2] != 3:
            raise ValueError("HSV → RGB 转换需要输入三通道图像")
        result = _hsv_to_bgr_impl(image)
        steps.append({"name": "HSV → RGB 结果", "image": result})
        analysis = (
            "HSV → RGB 转换完成。将 HSV 颜色空间的图像还原为 RGB（BGR 通道序）格式，"
            "可在图像处理管线中继续后续操作或直接用于显示。"
        )
        # 颜色表基于转换后的 BGR 图像
        src_for_table = result

    elif conversion_type == "bgr_to_cmyk":
        if len(image.shape) == 2:
            raise ValueError("RGB → CMYK 转换需要输入三通道彩色图像")
        cmyk_vis, c, m, y, k = _bgr_to_cmyk_impl(image)
        result = cmyk_vis
        steps.extend([
            {"name": "CMYK 青色通道（C）", "image": _channel_to_bgr(c)},
            {"name": "CMYK 品红通道（M）", "image": _channel_to_bgr(m)},
            {"name": "CMYK 黄色通道（Y）", "image": _channel_to_bgr(y)},
            {"name": "CMYK 黑色通道（K）", "image": _channel_to_bgr(k)}
        ])
        metrics = {
            "mean_cyan": round(float(np.mean(c)), 2),
            "mean_magenta": round(float(np.mean(m)), 2),
            "mean_yellow": round(float(np.mean(y)), 2),
            "mean_black": round(float(np.mean(k)), 2)
        }
        analysis = (
            "RGB → CMYK 转换完成。CMYK 是印刷行业使用的减色模型："
            "C（青）、M（品红）、Y（黄）为三原色，K（黑）用于加深暗部层次。"
            "动漫图像的暗部（如阴影区域）K 值较高，鲜艳区域的 C/M/Y 组合值较高。"
            "注意：CMYK 为设备相关颜色空间，实际印刷效果需结合 ICC 色彩配置文件。"
        )
        src_for_table = image

    else:
        # 理论上不会走到这里，但保留兜底
        result = image
        src_for_table = image

    # ---------- 生成主色调对照表 ----------
    color_table = _extract_color_table(src_for_table, n_colors=n_colors)

    return {
        "result": result,
        "steps": steps,
        "metrics": metrics,
        "analysis": analysis,
        "color_table": color_table
    }