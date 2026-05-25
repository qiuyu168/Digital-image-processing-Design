# 本文件用于实现图像伽马变换功能，通过非线性变换校正图像亮度
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "gray_transform",
    "name": "gamma_transform",
    "display_name": "伽马变换",
    "description": "通过伽马校正调整图像亮度，公式为 g = c * f^γ，γ<1 增加暗部细节（变亮），γ>1 增加亮部细节（变暗）。常用于图像曝光校正和对比度增强。",
    "params": {
        "gamma": {
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 5.0,
            "label": "伽马值 γ",
            "description": "γ<1 图像变亮（增强暗部细节），γ>1 图像变暗（增强亮部细节），γ=1 无变化"
        },
        "c": {
            "type": "float",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "label": "缩放常数 c",
            "description": "整体缩放系数，默认1.0"
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
    对图像进行伽马变换（伽马校正）
    :param image: 输入图像 (BGR或灰度图)
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    gamma = params.get("gamma", 1.0)
    c = params.get("c", 1.0)
    apply_to_color = params.get("apply_to_color", "luminance")
    
    # 参数校验
    gamma = max(0.1, min(5.0, gamma))
    c = max(0.1, min(3.0, c))
    
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
    
    # 预计算伽马查找表（提高效率）
    # 公式: output = c * (input / 255)^gamma * 255
    gamma_table = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        gamma_table[i] = np.clip(c * (i / 255.0) ** gamma * 255.0, 0, 255)
    
    steps.append({
        "name": f"伽马映射曲线 (γ={gamma:.2f}, c={c:.2f})",
        "image": _draw_gamma_curve(gamma, c)
    })
    
    if not is_color:
        # 灰度图像：直接应用伽马变换
        gray = image.copy()
        
        steps.append({
            "name": "灰度图像",
            "image": gray.copy()
        })
        
        result = cv2.LUT(gray, gamma_table)
        
        steps.append({
            "name": f"伽马变换结果 (γ={gamma:.2f})",
            "image": result.copy()
        })
        
        if gamma < 1.0:
            analysis = f"使用伽马值 γ={gamma:.2f}（<1）进行伽马变换，图像整体变亮，暗部细节得到增强。"
        elif gamma > 1.0:
            analysis = f"使用伽马值 γ={gamma:.2f}（>1）进行伽马变换，图像整体变暗，亮部细节得到增强。"
        else:
            analysis = f"使用伽马值 γ={gamma:.2f}（=1）进行伽马变换，图像无变化。"
        analysis += f" 伽马变换公式为 g = c·f^γ，常用于图像曝光校正和对比度调整。"
    
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
            
            v_corrected = cv2.LUT(v, gamma_table)
            hsv_result = cv2.merge([h, s, v_corrected])
            result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            
            steps.append({
                "name": f"亮度通道伽马校正 (γ={gamma:.2f})",
                "image": result.copy()
            })
            
        elif apply_to_color == "rgb":
            # 方式2：分别处理RGB三通道
            b, g, r = cv2.split(image)
            
            steps.append({
                "name": "分离RGB通道",
                "image": _combine_rgb_preview(b, g, r)
            })
            
            b_corrected = cv2.LUT(b, gamma_table)
            g_corrected = cv2.LUT(g, gamma_table)
            r_corrected = cv2.LUT(r, gamma_table)
            result = cv2.merge([b_corrected, g_corrected, r_corrected])
            
            steps.append({
                "name": f"RGB三通道伽马校正 (γ={gamma:.2f})",
                "image": result.copy()
            })
            
        else:  # "hsv"
            # 方式3：转换到HSV，处理所有通道（较少用）
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            steps.append({
                "name": "转换到HSV空间",
                "image": cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            })
            
            h_corrected = cv2.LUT(h, gamma_table)
            s_corrected = cv2.LUT(s, gamma_table)
            v_corrected = cv2.LUT(v, gamma_table)
            hsv_result = cv2.merge([h_corrected, s_corrected, v_corrected])
            result = cv2.cvtColor(hsv_result, cv2.COLOR_HSV2BGR)
            
            steps.append({
                "name": f"HSV三通道伽马校正 (γ={gamma:.2f})",
                "image": result.copy()
            })
        
        if gamma < 1.0:
            analysis = f"使用伽马值 γ={gamma:.2f}（<1）进行伽马变换，图像整体变亮，暗部细节得到增强。处理方式："
        elif gamma > 1.0:
            analysis = f"使用伽马值 γ={gamma:.2f}（>1）进行伽马变换，图像整体变暗，亮部细节得到增强。处理方式："
        else:
            analysis = f"使用伽马值 γ={gamma:.2f}（=1）进行伽马变换，图像无变化。处理方式："
        
        mode_names = {"luminance": "仅处理亮度通道（保持色彩）", 
                      "rgb": "分别处理RGB三通道", 
                      "hsv": "处理HSV所有通道"}
        analysis += mode_names.get(apply_to_color, "仅处理亮度通道")
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }


def _draw_gamma_curve(gamma: float, c: float) -> np.ndarray:
    """
    绘制伽马变换曲线图（用于步骤展示）
    :param gamma: 伽马值
    :param c: 缩放常数
    :return: 曲线图图像 (BGR格式)
    """
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(6, 4))
    
    x = np.linspace(0, 255, 256)
    y = c * (x / 255.0) ** gamma * 255.0
    y = np.clip(y, 0, 255)
    
    plt.plot(x, y, 'b-', linewidth=2)
    plt.plot([0, 255], [0, 255], 'r--', linewidth=1, alpha=0.5)
    plt.xlim([0, 255])
    plt.ylim([0, 255])
    plt.xlabel('输入像素值')
    plt.ylabel('输出像素值')
    plt.title(f'伽马变换曲线 (γ={gamma:.2f}, c={c:.2f})')
    plt.grid(True, alpha=0.3)
    plt.legend(['伽马变换', '恒等变换'])
    
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
    # 创建并排预览图
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