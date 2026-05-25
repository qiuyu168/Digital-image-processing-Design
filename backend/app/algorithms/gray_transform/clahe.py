# 本文件用于实现CLAHE自适应直方图均衡化功能，限制对比度增强，避免噪声放大
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "gray_transform",
    "name": "clahe",
    "display_name": "CLAHE 自适应直方图均衡化",
    "description": "CLAHE（限制对比度自适应直方图均衡化）将图像分成小块进行局部均衡化，并通过限制对比度来避免噪声放大。特别适合动漫图像等需要增强细节但保持自然感的场景。",
    "params": {
        "clip_limit": {
            "type": "float",
            "default": 2.0,
            "min": 0.0,
            "max": 10.0,
            "label": "裁剪限制",
            "description": "限制对比度放大的阈值，值越大对比度越强，推荐范围1.0-4.0"
        },
        "tile_grid_size": {
            "type": "int",
            "default": 8,
            "min": 2,
            "max": 32,
            "label": "网格大小",
            "description": "将图像分成的网格数量（tile_grid_size x tile_grid_size），值越小局部适应性越强"
        },
        "apply_to_color": {
            "type": "choice",
            "default": "luminance",
            "options": ["luminance", "rgb", "hsv"],
            "label": "彩色图像处理方式",
            "description": "luminance: 只处理亮度通道（推荐）; rgb: 分别处理RGB三通道; hsv: 处理HSV的V通道"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行CLAHE自适应直方图均衡化，增强对比度同时控制噪声
    :param image: 输入图像 (BGR或灰度图)
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    clip_limit = params.get("clip_limit", 2.0)
    tile_grid_size = params.get("tile_grid_size", 8)
    apply_to_color = params.get("apply_to_color", "luminance")
    
    # 参数校验
    clip_limit = max(0.0, min(10.0, clip_limit))
    tile_grid_size = max(2, min(32, tile_grid_size))
    tile_grid_size = int(tile_grid_size)
    
    valid_modes = ["luminance", "rgb", "hsv"]
    if apply_to_color not in valid_modes:
        apply_to_color = "luminance"
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 判断图像类型
    is_color = len(image.shape) == 3
    
    # 创建CLAHE对象
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
    
    if not is_color:
        # 灰度图像：直接应用CLAHE
        gray = image.copy()
        
        steps.append({
            "name": "灰度图像",
            "image": gray.copy()
        })
        
        # 计算原始直方图
        hist_original = cv2.calcHist([gray], [0], None, [256], [0, 256])
        
        steps.append({
            "name": "原始直方图",
            "image": _draw_histogram(hist_original, "原始直方图")
        })
        
        # 应用CLAHE
        result = clahe.apply(gray)
        
        # 计算均衡化后直方图
        hist_result = cv2.calcHist([result], [0], None, [256], [0, 256])
        
        steps.append({
            "name": f"CLAHE处理 (clip={clip_limit}, grid={tile_grid_size}x{tile_grid_size})",
            "image": result.copy()
        })
        
        steps.append({
            "name": "CLAHE后直方图",
            "image": _draw_histogram(hist_result, "CLAHE后直方图")
        })
        
        steps.append({
            "name": "直方图对比",
            "image": _draw_histogram_comparison(hist_original, hist_result)
        })
        
        analysis = f"使用CLAHE处理灰度图像，裁剪限制={clip_limit}，网格大小={tile_grid_size}x{tile_grid_size}。CLAHE在增强局部对比度的同时限制了噪声放大，效果优于全局直方图均衡化。"
    
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
            
            # 计算原始亮度直方图
            hist_original = cv2.calcHist([v], [0], None, [256], [0, 256])
            
            steps.append({
                "name": "原始亮度直方图",
                "image": _draw_histogram(hist_original, "原始亮度直方图")
            })
            
            # 对亮度通道应用CLAHE
            v_equalized = clahe.apply(v)
            
            # 计算均衡化后直方图
            hist_result = cv2.calcHist([v_equalized], [0], None, [256], [0, 256])
            
            # 合并通道并转回BGR
            hsv_result = cv2.merge([h, s, v_equalized])
            result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            
            steps.append({
                "name": f"亮度通道CLAHE (clip={clip_limit}, grid={tile_grid_size}x{tile_grid_size})",
                "image": cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            })
            
            steps.append({
                "name": "CLAHE后亮度直方图",
                "image": _draw_histogram(hist_result, "CLAHE后亮度直方图")
            })
            
            steps.append({
                "name": "亮度直方图对比",
                "image": _draw_histogram_comparison(hist_original, hist_result)
            })
            
            analysis = f"使用CLAHE处理彩色图像，仅调整亮度通道（保持色彩）。裁剪限制={clip_limit}，网格大小={tile_grid_size}x{tile_grid_size}。该方法在增强动漫图像局部对比度的同时，能有效避免色彩失真。"
        
        elif apply_to_color == "rgb":
            # 方式2：分别处理RGB三通道
            b, g, r = cv2.split(image)
            
            steps.append({
                "name": "分离RGB通道",
                "image": _combine_rgb_preview(b, g, r)
            })
            
            # 计算原始灰度直方图（用于对比）
            gray_for_hist = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            hist_original = cv2.calcHist([gray_for_hist], [0], None, [256], [0, 256])
            
            steps.append({
                "name": "原始灰度直方图",
                "image": _draw_histogram(hist_original, "原始灰度直方图")
            })
            
            # 对每个通道应用CLAHE
            b_equalized = clahe.apply(b)
            g_equalized = clahe.apply(g)
            r_equalized = clahe.apply(r)
            
            result = cv2.merge([b_equalized, g_equalized, r_equalized])
            
            # 计算均衡化后灰度直方图
            gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            hist_result = cv2.calcHist([gray_result], [0], None, [256], [0, 256])
            
            steps.append({
                "name": f"RGB三通道CLAHE (clip={clip_limit}, grid={tile_grid_size}x{tile_grid_size})",
                "image": result.copy()
            })
            
            steps.append({
                "name": "CLAHE后灰度直方图",
                "image": _draw_histogram(hist_result, "CLAHE后灰度直方图")
            })
            
            steps.append({
                "name": "灰度直方图对比",
                "image": _draw_histogram_comparison(hist_original, hist_result)
            })
            
            analysis = f"使用CLAHE分别处理RGB三个通道，裁剪限制={clip_limit}，网格大小={tile_grid_size}x{tile_grid_size}。注意：该方法可能改变图像色彩平衡，通常不推荐用于彩色图像。"
        
        else:  # "hsv"
            # 方式3：转换到HSV，只处理V通道（与luminance类似，但展示不同）
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            steps.append({
                "name": "转换到HSV空间",
                "image": cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            })
            
            steps.append({
                "name": "分离HSV通道",
                "image": _combine_hsv_preview(h, s, v)
            })
            
            # 计算原始亮度直方图
            hist_original = cv2.calcHist([v], [0], None, [256], [0, 256])
            
            steps.append({
                "name": "原始V通道直方图",
                "image": _draw_histogram(hist_original, "原始V通道直方图")
            })
            
            # 对亮度通道应用CLAHE
            v_equalized = clahe.apply(v)
            
            # 计算均衡化后直方图
            hist_result = cv2.calcHist([v_equalized], [0], None, [256], [0, 256])
            
            # 合并通道并转回BGR
            hsv_result = cv2.merge([h, s, v_equalized])
            result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            
            steps.append({
                "name": f"V通道CLAHE (clip={clip_limit}, grid={tile_grid_size}x{tile_grid_size})",
                "image": result.copy()
            })
            
            steps.append({
                "name": "CLAHE后V通道直方图",
                "image": _draw_histogram(hist_result, "CLAHE后V通道直方图")
            })
            
            steps.append({
                "name": "V通道直方图对比",
                "image": _draw_histogram_comparison(hist_original, hist_result)
            })
            
            analysis = f"使用CLAHE处理HSV空间的V通道（亮度），裁剪限制={clip_limit}，网格大小={tile_grid_size}x{tile_grid_size}。该方法在增强动漫图像局部细节的同时，保持了原始色调。"
    
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
    :param hist2: 处理后直方图
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
    axes[1].set_title('CLAHE后直方图')
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
    将三个RGB单通道合并为预览图（用于步骤展示）
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


def _combine_hsv_preview(h: np.ndarray, s: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    将三个HSV单通道合并为预览图（用于步骤展示）
    """
    h, w = h.shape
    preview = np.zeros((h, w * 3, 3), dtype=np.uint8)
    
    # H通道 -> 伪彩色显示（色相映射）
    h_color = cv2.applyColorMap(h, cv2.COLORMAP_JET)
    preview[:, 0:w] = h_color
    
    # S通道 -> 灰度显示
    s_gray = cv2.cvtColor(cv2.merge([s, s, s]), cv2.COLOR_GRAY2BGR)
    preview[:, w:2*w] = s_gray
    
    # V通道 -> 灰度显示
    v_gray = cv2.cvtColor(cv2.merge([v, v, v]), cv2.COLOR_GRAY2BGR)
    preview[:, 2*w:3*w] = v_gray
    
    # 添加文字标签
    cv2.putText(preview, "H (色相)", (w//2 - 40, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(preview, "S (饱和度)", (w + w//2 - 45, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(preview, "V (亮度)", (2*w + w//2 - 35, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return preview