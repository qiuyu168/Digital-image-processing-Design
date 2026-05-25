# 本文件用于实现图像对数变换功能，扩展暗区细节，压缩亮区范围
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "gray_transform",
    "name": "log_transform",
    "display_name": "对数变换",
    "description": "通过对数变换增强图像暗部细节，压缩亮部范围，公式为 g = c * log(1 + f)。常用于显示傅里叶频谱、增强低灰度图像细节。",
    "params": {
        "c": {
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 5.0,
            "label": "缩放常数 c",
            "description": "控制变换强度，值越大效果越明显"
        },
        "base": {
            "type": "choice",
            "default": "e",
            "options": ["e", "10", "2"],
            "label": "对数底数",
            "description": "e: 自然对数; 10: 常用对数; 2: 以2为底的对数"
        },
        "apply_to_color": {
            "type": "choice",
            "default": "luminance",
            "options": ["luminance", "rgb", "hsv"],
            "label": "彩色图像处理方式",
            "description": "luminance: 只处理亮度通道; rgb: 分别处理RGB三通道; hsv: 处理HSV的V通道"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行对数变换，增强暗部细节
    :param image: 输入图像 (BGR或灰度图)
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    c = params.get("c", 1.0)
    base = params.get("base", "e")
    apply_to_color = params.get("apply_to_color", "luminance")
    
    # 参数校验
    c = max(0.1, min(5.0, c))
    
    valid_bases = ["e", "10", "2"]
    if base not in valid_bases:
        base = "e"
    
    valid_modes = ["luminance", "rgb", "hsv"]
    if apply_to_color not in valid_modes:
        apply_to_color = "luminance"
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 根据底数选择对数函数
    if base == "e":
        log_func = np.log
        base_name = "自然对数 (ln)"
        log_factor = 1.0
    elif base == "10":
        log_func = np.log10
        base_name = "常用对数 (log10)"
        log_factor = 1.0
    else:  # base == "2"
        log_func = np.log2
        base_name = "以2为底对数 (log2)"
        log_factor = 1.0
    
    steps.append({
        "name": f"对数变换曲线 ({base_name}, c={c:.2f})",
        "image": _draw_log_curve(c, base)
    })
    
    # 判断图像类型
    is_color = len(image.shape) == 3
    
    if not is_color:
        # 灰度图像：直接应用对数变换
        gray = image.copy()
        
        steps.append({
            "name": "灰度图像",
            "image": gray.copy()
        })
        
        # 对数变换公式: output = c * log(1 + input)
        # 输入归一化到 0-1 范围，输出映射回 0-255
        gray_norm = gray.astype(np.float32) / 255.0
        result_norm = c * log_func(1 + gray_norm)
        
        # 归一化到 0-255
        result_norm = result_norm / (c * log_func(2))  # log(1+1) = log(2)
        result = np.clip(result_norm * 255, 0, 255).astype(np.uint8)
        
        steps.append({
            "name": f"对数变换结果 (c={c:.2f}, {base_name})",
            "image": result.copy()
        })
        
        analysis = f"使用对数变换处理灰度图像，缩放常数 c={c:.2f}，底数为{base_name}。对数变换能显著增强暗部细节，压缩高亮区域，特别适用于整体偏暗的图像。"
    
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
            
            # 对亮度通道进行对数变换
            v_norm = v.astype(np.float32) / 255.0
            v_corrected_norm = c * log_func(1 + v_norm)
            v_corrected_norm = v_corrected_norm / (c * log_func(2))
            v_corrected = np.clip(v_corrected_norm * 255, 0, 255).astype(np.uint8)
            
            hsv_result = cv2.merge([h, s, v_corrected])
            result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            
            steps.append({
                "name": f"亮度通道对数变换 (c={c:.2f})",
                "image": result.copy()
            })
            
            analysis = f"使用对数变换处理彩色图像，仅调整亮度通道（保持色彩）。缩放常数 c={c:.2f}，底数为{base_name}。"
            
        elif apply_to_color == "rgb":
            # 方式2：分别处理RGB三通道
            b, g, r = cv2.split(image)
            
            steps.append({
                "name": "分离RGB通道",
                "image": _combine_rgb_preview(b, g, r)
            })
            
            def log_transform_channel(channel):
                ch_norm = channel.astype(np.float32) / 255.0
                result_norm = c * log_func(1 + ch_norm)
                result_norm = result_norm / (c * log_func(2))
                return np.clip(result_norm * 255, 0, 255).astype(np.uint8)
            
            b_corrected = log_transform_channel(b)
            g_corrected = log_transform_channel(g)
            r_corrected = log_transform_channel(r)
            result = cv2.merge([b_corrected, g_corrected, r_corrected])
            
            steps.append({
                "name": f"RGB三通道对数变换 (c={c:.2f})",
                "image": result.copy()
            })
            
            analysis = f"使用对数变换分别处理RGB三个通道，缩放常数 c={c:.2f}，底数为{base_name}。"
            
        else:  # "hsv"
            # 方式3：转换到HSV，处理所有通道
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            steps.append({
                "name": "转换到HSV空间",
                "image": cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            })
            
            def log_transform_channel(channel):
                ch_norm = channel.astype(np.float32) / 255.0
                result_norm = c * log_func(1 + ch_norm)
                result_norm = result_norm / (c * log_func(2))
                return np.clip(result_norm * 255, 0, 255).astype(np.uint8)
            
            h_corrected = log_transform_channel(h)
            s_corrected = log_transform_channel(s)
            v_corrected = log_transform_channel(v)
            hsv_result = cv2.merge([h_corrected, s_corrected, v_corrected])
            result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            
            steps.append({
                "name": f"HSV三通道对数变换 (c={c:.2f})",
                "image": result.copy()
            })
            
            analysis = f"使用对数变换处理HSV三个通道，缩放常数 c={c:.2f}，底数为{base_name}。"
        
        analysis += " 对数变换能有效扩展暗区细节，压缩亮区范围，常用于显示频谱或增强欠曝光图像。"
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }


def _draw_log_curve(c: float, base: str) -> np.ndarray:
    """
    绘制对数变换曲线图（用于步骤展示）
    :param c: 缩放常数
    :param base: 对数底数
    :return: 曲线图图像 (BGR格式)
    """
    import matplotlib.pyplot as plt
    
    # 选择对数函数
    if base == "e":
        log_func = np.log
        base_name = "ln"
    elif base == "10":
        log_func = np.log10
        base_name = "log₁₀"
    else:  # base == "2"
        log_func = np.log2
        base_name = "log₂"
    
    plt.figure(figsize=(6, 4))
    
    x = np.linspace(0, 255, 256)
    x_norm = x / 255.0
    y_norm = c * log_func(1 + x_norm)
    y_norm = y_norm / (c * log_func(2))  # 归一化
    y = y_norm * 255
    
    plt.plot(x, y, 'b-', linewidth=2)
    plt.plot([0, 255], [0, 255], 'r--', linewidth=1, alpha=0.5)
    plt.xlim([0, 255])
    plt.ylim([0, 255])
    plt.xlabel('输入像素值')
    plt.ylabel('输出像素值')
    plt.title(f'对数变换曲线 (g = c·log(1+f), c={c:.2f}, 底={base_name})')
    plt.grid(True, alpha=0.3)
    plt.legend(['对数变换', '恒等变换'])
    
    # 转换为 OpenCV 格式
    fig = plt.gcf()
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