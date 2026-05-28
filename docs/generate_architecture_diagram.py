# 本文件用于生成系统架构图并保存为 PNG 图片
from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, fontManager
import os

matplotlib.use("Agg")

# Windows 中文字体配置
_chinese_font_paths = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
]
for _fp in _chinese_font_paths:
    if os.path.exists(_fp):
        fontManager.addfont(_fp)
        _prop = FontProperties(fname=_fp)
        plt.rcParams["font.family"] = _prop.get_name()
        break
plt.rcParams["axes.unicode_minus"] = False


def draw_architecture_diagram(output_path: str = "docs/architecture.png") -> None:
    fig, ax = plt.subplots(1, 1, figsize=(12, 14), facecolor="#f8f9fa")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.axis("off")
    ax.set_facecolor("#f8f9fa")

    box_style = dict(
        boxstyle="round,pad=0.5",
        facecolor="white",
        edgecolor="#333333",
        linewidth=1.5,
    )
    arrow_color = "#555555"

    texts_and_positions = [
        (5.0, 15.0, "用户", "#e8f5e9", "#2e7d32", 14, "bold"),
        (5.0, 14.0, "上传图片 / 选择图库图片 / 选择算法 / 调整参数", None, "#666666", 9, "normal"),
        (5.0, 12.5, "Vue 3 前端页面\n(Element Plus + ECharts + Pinia)", "#e3f2fd", "#1565c0", 12, "bold"),
        (5.0, 11.5, "Axios HTTP 请求", None, "#666666", 9, "normal"),
        (5.0, 9.5, "FastAPI 后端接口层\n(参数校验 / 图片读取 / 算法路由)", "#fff3e0", "#e65100", 12, "bold"),
        (5.0, 8.5, "模块路由 → 算法注册表 → 动态导入", None, "#666666", 9, "normal"),
        (5.0, 6.5, "后端算法模块层\n灰度图像 | 彩色图像 | 几何变换 | 空域滤波 | 频域分析 | 频域滤波", "#fce4ec", "#c62828", 12, "bold"),
        (5.0, 5.5, "统一接口: run(image, params) → result/steps/metrics/analysis", None, "#666666", 9, "normal"),
        (5.0, 3.5, "结果分析层\n(指标统计 / 直方图 / 分步结果 / 文字分析)", "#f3e5f5", "#7b1fa2", 12, "bold"),
        (5.0, 2.5, "图像编码 → Base64 / JSON 序列化", None, "#666666", 9, "normal"),
        (5.0, 1.0, "JSON 响应\n(Base64 结果图 / 分步图 / 指标 / 分析文本)", "#e8eaf6", "#283593", 11, "bold"),
    ]

    for x, y, text, bg_color, text_color, fontsize, weight in texts_and_positions:
        if bg_color:
            ax.text(
                x, y, text,
                ha="center", va="center",
                fontsize=fontsize, fontweight=weight, color=text_color,
                bbox=dict(
                    boxstyle="round,pad=0.5",
                    facecolor=bg_color,
                    edgecolor=text_color,
                    linewidth=1.2,
                    alpha=0.9,
                ),
                zorder=5,
            )
        else:
            ax.text(
                x, y, text,
                ha="center", va="center",
                fontsize=fontsize, fontweight=weight, color=text_color,
                zorder=4,
            )

    arrows = [
        (5.0, 14.0, 5.0, 13.2),
        (5.0, 11.8, 5.0, 10.2),
        (5.0, 8.8, 5.0, 7.2),
        (5.0, 5.8, 5.0, 4.2),
        (5.0, 2.8, 5.0, 1.7),
    ]
    for x1, y1, x2, y2 in arrows:
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                color=arrow_color,
                lw=2.0,
                connectionstyle="arc3,rad=0",
            ),
            zorder=3,
        )

    arrow_down_left = [
        (5.0, 0.5, 5.0, -0.3),
    ]
    ax.text(5.0, 0.3, "▼ 前端即时展示处理结果", ha="center", fontsize=10, color="#333333", fontweight="bold")

    plt.tight_layout(pad=2)
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="#f8f9fa", edgecolor="none")
    plt.close(fig)
    print(f"架构图已保存到: {output_path}")


if __name__ == "__main__":
    draw_architecture_diagram()
