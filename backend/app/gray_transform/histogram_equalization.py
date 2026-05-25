# 本文件用于实现图像直方图均衡化功能，增强灰度图像整体对比度
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "gray_transform",
    "name": "histogram_equalization",
    "display_name": "直方图均衡化",
    "description": "通过重新分配像素灰度值，使图像的直方图分布更加均匀，从而增强整体对比度。适用于曝光不足或过度的图像。",
    "params": {
        "apply_to_color": {
            "type": "choice",
            "default": "luminance",
            "options": ["luminance", "rgb", "hsv"],
            "label": "彩色图像处理方式",
            "description": "luminance: 只处理亮度通道（推荐）; rgb: 分别处理RGB三通道; hsv: 处理HSV的V通道"
        },
        "clip_limit": {
            "type": "float",
            "default": 0.0,
            "min": 0.0,
            "max": 10.0,
            "label": "裁剪限制 (CLAHE)",
            "description": "0表示使用全局均衡化，>0表示使用自适应均衡化(CLAHE)，值越大对比度越强"
        },
        "tile_grid_size": {
            "type": "int",
            "default": 8,
            "min": 2,
            "max": 32,
            "label": "网格大小 (CLAHE)",
            "description": "CLAHE算法的网格大小，仅在clip_limit>0时有效"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行直方图均衡化，增强对比度
    :param image: 输入图像 (BGR或灰度图)
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    apply_to_color = params.get("apply_to_color", "luminance")
    clip_limit = params.get("clip_limit", 0.0)
    tile_grid_size = params.get("tile_grid_size", 8)
    
    # 参数校验
    valid_modes = ["luminance", "rgb", "hsv"]
    if apply_to_color not in valid_modes:
        apply_to_color = "luminance"
    
    clip_limit = max(0.0, min(10.0, clip_limit))
    tile_grid_size = max(2, min(32, tile_grid_size))
    
    # 确保 tile_grid_size 为正整数
    tile_grid_size = int(tile_grid_size)
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 判断图像类型
    is_color = len(image.shape) == 3
    
    # 计算原始直方图（用于对比展示）
    if not is_color:
        gray = image.copy()
        hist_original = cv2.calcHist([gray], [0], None, [256], [0, 256])
    else:
        gray_for_hist = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist_original = cv2.calcHist([gray_for_hist], [0], None, [256], [0, 256])
    
    if not is_color:
        # 灰度图像：直接处理
        gray = image.copy()
        
        steps.append({
            "name": "灰度图像",
            "image": gray.copy()
        })
        
        steps.append({
            "name": "原始直方图",
            "image": _draw_histogram(hist_original, "原始直方图")
        })
        
        # 直方图均衡化
        if clip_limit == 0.0:
            # 全局直方图均衡化
            result = cv2.equalizeHist(gray)
            method_name = "全局直方图均衡化"
            analysis = "使用全局直方图均衡化，将灰度分布拉伸到整个0-255范围，增强整体对比度。"
        else:
            # CLAHE (限制对比度自适应直方图均衡化)
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
            result = clahe.apply(gray)
            method_name = f"CLAHE自适应均衡化 (clip={clip_limit}, grid={tile_grid_size})"
            analysis = f"使用CLAHE自适应直方图均衡化，裁剪限制={clip_limit}，网格大小={tile_grid_size}。该方法能避免全局均衡化带来的噪声放大问题。"
        
        # 计算均衡化后直方图
        hist_result = cv2.calcHist([result], [0], None, [256], [0, 256])
        
        steps.append({
            "name": f"{method_name}",
            "image": result.copy()
        })
        
        steps.append({
            "name": "均衡化后直方图",
            "image": _draw_histogram(hist_result, "均衡化后直方图")
        })
        
        steps.append({
            "name": "直方图对比",
            "image": _draw_histogram_comparison(hist_original, hist_result)
        })
    
    else:
        # 彩色图像：根据模式选择处理方式
        if apply_to_color == "luminance":
            # 方式1：转换到HSV，只处理V通道（亮度）
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            steps.append({
                "name": "转换到HSV空间",
                "image": cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            })
            
            steps.append({
                "name": "亮度通道(V)",
                "image": cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2BGR)
            })
            
            # 直方图均衡化
            if clip_limit == 0.0:
                v_equalized = cv2.equalizeHist(v)
                method_name = "全局直方图均衡化"
            else:
                clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
                v_equalized = clahe.apply(v)
                method_name = f"CLAHE自适应均衡化"
            
            hsv_result = cv2.merge([h, s, v_equalized])
            result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            
            steps.append({
                "name": f"亮度通道均衡化 ({method_name})",
                "image": cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            })
            
            # 计算均衡化后直方图
            hist_result = cv2.calcHist([v_equalized], [0], None, [256], [0, 256])
            
            steps.append({
                "name": "直方图对比",
                "image": _draw_histogram_comparison(hist_original, hist_result)
            })
            
            analysis = f"使用{method_name}处理彩色图像，仅调整亮度通道（保持色彩）。"
            if clip_limit == 0.0:
                analysis += " 全局均衡化将亮度分布拉伸到整个范围，整体对比度得到增强。"
            else:
                analysis += f" CLAHE通过限制对比度放大，避免噪声放大问题。"
        
        elif apply_to_color == "rgb":
            # 方式2：分别处理RGB三通道
            b, g, r = cv2.split(image)
            
            steps.append({
                "name": "分离RGB通道",
                "image": _combine_rgb_preview(b, g, r)
            })
            
            # 对每个通道进行均衡化
            if clip_limit == 0.0:
                b_eq = cv2.equalizeHist(b)
                g_eq = cv2.equalizeHist(g)
                r_eq = cv2.equalizeHist(r)
                method_name = "全局直方图均衡化"
            else:
                clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
                b_eq = clahe.apply(b)
                g_eq = clahe.apply(g)
                r_eq = clahe.apply(r)
                method_name = f"CLAHE自适应均衡化"
            
            result = cv2.merge([b_eq, g_eq, r_eq])
            
            steps.append({
                "name": f"RGB通道均衡化 ({method_name})",
                "image": result.copy()
            })
            
            # 计算均衡化后直方图（亮度近似）
            gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            hist_result = cv2.calcHist([gray_result], [0], None, [256], [0, 256])
            
            steps.append({
                "name": "直方图对比",
                "image": _draw_histogram_comparison(hist_original, hist_result)
            })
            
            analysis = f"使用{method_name}分别处理RGB三个通道。注意：该方法可能改变图像色彩平衡。"
        
        else:  # "hsv"
            # 方式3：转换到HSV，处理所有通道
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            steps.append({
                "name": "转换到HSV空间",
                "image": cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            })
            
            # 对亮度通道进行均衡化
            if clip_limit == 0.0:
                v_eq = cv2.equalizeHist(v)
                method_name = "全局直方图均衡化"
            else:
                clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
                v_eq = clahe.apply(v)
                method_name = f"CLAHE自适应均衡化"
            
            hsv_result = cv2.merge([h, s, v_eq])
            result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            
            steps.append({
                "name": f"HSV空间均衡化 ({method_name})",
                "image": result.copy()
            })
            
            # 计算均衡化后直方图
            hist_result = cv2.calcHist([v_eq], [0], None, [256], [0, 256])
            
            steps.append({
                "name": "直方图对比",
                "image": _draw_histogram_comparison(hist_original, hist_result)
            })
            
            analysis = f"使用{method_name}处理HSV空间，仅调整亮度通道V，保持色相和饱和度不变。"
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }


def _draw_histogram(hist: np.ndarray, title: str) -> np.ndarray:
    """
    绘制直方图（用于步骤展示）
    :param hist: 直方图数据
    :param title: 图表标题
    :return: 直方图图像 (BGR格式)
    """
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(6, 3))
    plt.bar(range(256), hist.flatten(), width=1.0, color='black', alpha=0.7)
    plt.title(title)
    plt.xlabel('像素值')
    plt.ylabel('像素数量')
    plt.xlim([0, 255])
    plt.grid(True, alpha=0.3)
    
    # 转换为 OpenCV 格式
    fig = plt.gcf()
    fig.canvas.draw()
    img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    plt.close()
    
    return img


def _draw_histogram_comparison(hist1: np.ndarray, hist2: np.ndarray) -> np.ndarray:
    """
    绘制直方图对比（用于步骤展示）
    :param hist1: 原始直方图
    :param hist2: 均衡化后直方图
    :return: 对比图图像 (BGR格式)
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    axes[0].bar(range(256), hist1.flatten(), width=1.0, color='black', alpha=0.7)
    axes[0].set_title('原始直方图')
    axes[0].set_xlim([0, 256])
    axes[0].set_xlabel('像素值')
    axes[0].set_ylabel('像素数量')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].bar(range(256), hist2.flatten(), width=1.0, color='black', alpha=0.7)
    axes[1].set_title('均衡化后直方图')
    axes[1].set_xlim([0, 256])
    axes[1].set_xlabel('像素值')
    axes[1].set_ylabel('像素数量')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 转换为 OpenCV 格式
    fig.canvas.draw()
    img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    plt.close()
    
    return img


def _combine_rgb_preview(b: np.ndarray, g: np.ndarray, r: np.ndarray) -> np.ndarray:
    """
    将三个单通道合并为RGB预览图（用于步骤展示）
    """
    h, w = b.shape
    preview = np.zeros((h, w * 3, 3), dtype=np.uint8)
    
    # B通道 -> 蓝色
    preview[:, 0:w, 0] = b
    # G通道 -> 绿色
    preview[:, w:2*w, 1] = g
    # R通道 -> 红色
    preview[:, 2*w:3*w, 2] = r
    
    # 添加文字标签
    cv2.putText(preview, "B", (w//2 - 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(preview, "G", (w + w//2 - 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(preview, "R", (2*w + w//2 - 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return preview