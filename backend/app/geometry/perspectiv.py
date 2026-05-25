# 本文件用于实现图像透视变换功能，通过4个点对将图像投影到新的视角
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "geometry",
    "name": "perspective",
    "display_name": "透视变换",
    "description": "透视变换通过4个点对将图像投影到新的视角，可用于校正倾斜图像、模拟不同视角等。透视变换会改变图像的平行线关系，产生近大远小的效果。",
    "params": {
        "preset": {
            "type": "choice",
            "default": "tilt",
            "options": ["tilt", "corner", "custom"],
            "label": "预设模式",
            "description": "tilt: 向后倾斜效果; corner: 角点透视; custom: 自定义四个点"
        },
        "top_offset": {
            "type": "float",
            "default": 0.2,
            "min": 0.0,
            "max": 0.5,
            "label": "顶部偏移比例",
            "description": "仅 tilt 模式有效，控制顶部收缩程度"
        },
        "bottom_offset": {
            "type": "float",
            "default": 0.0,
            "min": 0.0,
            "max": 0.5,
            "label": "底部偏移比例",
            "description": "仅 tilt 模式有效，控制底部收缩程度"
        },
        "side_offset": {
            "type": "float",
            "default": 0.15,
            "min": 0.0,
            "max": 0.5,
            "label": "侧边偏移比例",
            "description": "仅 corner 模式有效，控制侧边收缩程度"
        },
        "border_mode": {
            "type": "choice",
            "default": "constant",
            "options": ["constant", "replicate", "reflect", "wrap"],
            "label": "边界填充模式",
            "description": "constant: 常数填充; replicate: 边缘复制; reflect: 镜像反射; wrap: 环绕重复"
        },
        "border_value": {
            "type": "int",
            "default": 0,
            "min": 0,
            "max": 255,
            "label": "边界填充颜色",
            "description": "仅 constant 模式有效，0=黑色，255=白色"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行透视变换
    :param image: 输入图像
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    preset = params.get("preset", "tilt")
    top_offset = params.get("top_offset", 0.2)
    bottom_offset = params.get("bottom_offset", 0.0)
    side_offset = params.get("side_offset", 0.15)
    border_mode = params.get("border_mode", "constant")
    border_value = params.get("border_value", 0)
    
    # 参数校验
    top_offset = max(0.0, min(0.5, top_offset))
    bottom_offset = max(0.0, min(0.5, bottom_offset))
    side_offset = max(0.0, min(0.5, side_offset))
    border_value = max(0, min(255, border_value))
    
    valid_presets = ["tilt", "corner", "custom"]
    if preset not in valid_presets:
        preset = "tilt"
    
    valid_border_modes = ["constant", "replicate", "reflect", "wrap"]
    if border_mode not in valid_border_modes:
        border_mode = "constant"
    
    steps = []
    
    # 记录原始图像
    steps.append({
        "name": "原始图像",
        "image": image.copy()
    })
    
    # 获取图像尺寸
    h, w = image.shape[:2]
    
    steps.append({
        "name": f"原始尺寸: {w} x {h}",
        "image": _draw_info_on_image(image, f"原始尺寸: {w} x {h}")
    })
    
    # 定义源点（原始图像的四个角点）
    pts_src = np.float32([
        [0, 0],           # 左上
        [w - 1, 0],       # 右上
        [w - 1, h - 1],   # 右下
        [0, h - 1]        # 左下
    ])
    
    # 根据预设模式计算目标点
    if preset == "tilt":
        # 向后倾斜效果：顶部收缩
        top_width = w * (1 - top_offset * 2)
        top_x_offset = w * top_offset
        
        bottom_width = w * (1 - bottom_offset * 2)
        bottom_x_offset = w * bottom_offset
        
        pts_dst = np.float32([
            [top_x_offset, 0],                      # 左上
            [top_x_offset + top_width, 0],          # 右上
            [bottom_x_offset + bottom_width, h - 1],# 右下
            [bottom_x_offset, h - 1]                # 左下
        ])
        transform_name = f"向后倾斜透视 (顶部收缩 {top_offset*100:.0f}%)"
        
    elif preset == "corner":
        # 角点透视：模拟从角点观看的效果
        offset = w * side_offset
        pts_dst = np.float32([
            [offset, offset],                        # 左上
            [w - 1 - offset, offset * 0.5],          # 右上
            [w - 1 - offset, h - 1 - offset],        # 右下
            [offset, h - 1 - offset * 1.5]           # 左下
        ])
        transform_name = f"角点透视 (侧边收缩 {side_offset*100:.0f}%)"
        
    else:  # custom
        # 自定义：用户可以传入自定义点对（这里提供可调整的示例）
        # 实际使用中，前端可以传递 pts_src 和 pts_dst
        custom_offset = w * 0.15
        custom_offset_bottom = w * 0.1
        pts_dst = np.float32([
            [custom_offset, custom_offset * 0.5],
            [w - 1 - custom_offset, custom_offset * 0.3],
            [w - 1 - custom_offset_bottom, h - 1 - custom_offset_bottom],
            [custom_offset_bottom, h - 1 - custom_offset_bottom * 1.2]
        ])
        transform_name = "自定义透视变换"
    
    # 绘制源点和目标点示意图
    steps.append({
        "name": "透视变换点对示意图",
        "image": _draw_points_demo(image, pts_src, pts_dst)
    })
    
    # 计算透视变换矩阵
    perspective_matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
    
    # 计算输出图像尺寸（包含整个变换后图像）
    corners = np.array([
        [0, 0, 1],
        [w - 1, 0, 1],
        [w - 1, h - 1, 1],
        [0, h - 1, 1]
    ], dtype=np.float32)
    
    transformed_corners = corners @ perspective_matrix.T
    # 齐次坐标归一化
    transformed_corners = transformed_corners[:, :2] / transformed_corners[:, 2:3]
    
    min_x = np.min(transformed_corners[:, 0])
    max_x = np.max(transformed_corners[:, 0])
    min_y = np.min(transformed_corners[:, 1])
    max_y = np.max(transformed_corners[:, 1])
    
    new_w = int(np.ceil(max_x - min_x))
    new_h = int(np.ceil(max_y - min_y))
    
    # 调整变换矩阵以将图像平移到正区域
    translation_matrix = np.array([
        [1, 0, -min_x],
        [0, 1, -min_y],
        [0, 0, 1]
    ])
    perspective_matrix = translation_matrix @ perspective_matrix
    
    output_size = (new_w, new_h)
    
    # 边界填充模式映射
    border_mode_map = {
        "constant": cv2.BORDER_CONSTANT,
        "replicate": cv2.BORDER_REPLICATE,
        "reflect": cv2.BORDER_REFLECT,
        "wrap": cv2.BORDER_WRAP
    }
    border = border_mode_map.get(border_mode, cv2.BORDER_CONSTANT)
    
    border_names = {
        "constant": "常数填充",
        "replicate": "边缘复制",
        "reflect": "镜像反射",
        "wrap": "环绕重复"
    }
    border_name = border_names.get(border_mode, "常数填充")
    
    # 执行透视变换
    if border_mode == "constant":
        result = cv2.warpPerspective(image, perspective_matrix, output_size,
                                     flags=cv2.INTER_LINEAR,
                                     borderMode=border,
                                     borderValue=(border_value, border_value, border_value))
    else:
        result = cv2.warpPerspective(image, perspective_matrix, output_size,
                                     flags=cv2.INTER_LINEAR,
                                     borderMode=border)
    
    # 显示变换结果
    info_text = f"{transform_name} | 输出尺寸: {result.shape[1]} x {result.shape[0]}"
    result_with_info = _draw_info_on_image(result, info_text)
    
    steps.append({
        "name": "透视变换结果",
        "image": result_with_info
    })
    
    # 绘制透视变换示意图（网格变形）
    steps.append({
        "name": "透视变换网格示意图",
        "image": _draw_perspective_grid(w, h, perspective_matrix, output_size)
    })
    
    # 生成分析文本
    if preset == "tilt":
        analysis = f"对图像进行透视变换：{transform_name}。顶部收缩 {top_offset*100:.0f}%，底部收缩 {bottom_offset*100:.0f}%。这种变换模拟了向后倾斜的视角效果。"
    elif preset == "corner":
        analysis = f"对图像进行透视变换：{transform_name}。侧边收缩 {side_offset*100:.0f}%，模拟从角点观看图像的透视效果。"
    else:
        analysis = f"对图像进行透视变换：{transform_name}。通过自定义四个点对的映射关系实现视角变换。"
    
    analysis += f" 输出尺寸自动调整为 {output_size[0]} x {output_size[1]}，确保完整显示变换后图像。"
    
    if border_mode == "constant":
        analysis += f" 空白区域使用{border_name}，颜色值为 {border_value}。"
    else:
        analysis += f" 空白区域使用{border_name}填充。"
    
    analysis += " 透视变换与仿射变换的区别在于：透视变换使用4个点对，可以改变平行线关系，产生近大远小的三维投影效果。"
    
    return {
        "result": result,
        "steps": steps,
        "analysis": analysis
    }


def _draw_info_on_image(image: np.ndarray, text: str) -> np.ndarray:
    """
    在图像上绘制信息文本
    :param image: 输入图像
    :param text: 要显示的文本
    :return: 添加了文本的图像
    """
    img_copy = image.copy()
    h, w = img_copy.shape[:2]
    
    # 添加半透明背景
    overlay = img_copy.copy()
    cv2.rectangle(overlay, (10, 10), (w - 10, 60), (0, 0, 0), -1)
    img_copy = cv2.addWeighted(img_copy, 0.7, overlay, 0.3, 0)
    
    # 添加文字
    cv2.putText(img_copy, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return img_copy


def _draw_points_demo(image: np.ndarray, pts_src: np.ndarray, pts_dst: np.ndarray) -> np.ndarray:
    """
    绘制源点和目标点示意图
    :param image: 原始图像
    :param pts_src: 源点坐标
    :param pts_dst: 目标点坐标
    :return: 示意图图像
    """
    import matplotlib.pyplot as plt
    
    h, w = image.shape[:2]
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 原始图像 + 源点标记
    img_src = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    axes[0].imshow(img_src)
    # 绘制源点
    for i, pt in enumerate(pts_src):
        axes[0].plot(pt[0], pt[1], 'ro', markersize=8)
        axes[0].text(pt[0] + 5, pt[1] + 5, str(i+1), fontsize=10, color='red')
    axes[0].set_title('原始图像（源点）')
    axes[0].axis('off')
    
    # 目标点示意图（空白画布）
    new_w = int(np.max(pts_dst[:, 0]) - np.min(pts_dst[:, 0])) + w
    new_h = int(np.max(pts_dst[:, 1]) - np.min(pts_dst[:, 1])) + h
    img_dst = np.ones((new_h, new_w, 3), dtype=np.uint8) * 240
    img_dst = cv2.cvtColor(img_dst, cv2.COLOR_RGB2BGR)
    
    # 绘制目标点
    for i, pt in enumerate(pts_dst):
        cv2.circle(img_dst, (int(pt[0]), int(pt[1])), 5, (0, 0, 255), -1)
        cv2.putText(img_dst, str(i+1), (int(pt[0]) + 5, int(pt[1]) + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # 连接目标点形成四边形
    pts_int = pts_dst.astype(np.int32)
    cv2.polylines(img_dst, [pts_int], True, (0, 255, 0), 2)
    
    axes[1].imshow(cv2.cvtColor(img_dst, cv2.COLOR_BGR2RGB))
    axes[1].set_title('目标点位置（投影区域）')
    axes[1].axis('off')
    
    plt.tight_layout()
    
    # 转换为 OpenCV 格式
    fig.canvas.draw()
    result = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    result = result.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    plt.close()
    
    return result


def _draw_perspective_grid(w: int, h: int, perspective_matrix: np.ndarray, output_size: tuple) -> np.ndarray:
    """
    绘制透视变换网格示意图
    :param w: 原始宽度
    :param h: 原始高度
    :param perspective_matrix: 透视变换矩阵
    :param output_size: 输出尺寸
    :return: 网格示意图
    """
    import matplotlib.pyplot as plt
    
    new_w, new_h = output_size
    
    # 创建输出画布
    grid_display = np.ones((new_h, new_w, 3), dtype=np.uint8) * 255
    
    # 绘制变换后的网格
    step_x = max(1, w // 10)
    step_y = max(1, h // 10)
    
    # 绘制垂直网格线变换后的位置
    for i in range(0, w, step_x):
        # 创建线上的点
        pts = np.array([[i, 0, 1], [i, h-1, 1]], dtype=np.float32).reshape(-1, 3)
        transformed = perspective_matrix @ pts.T
        transformed = transformed[:2, :] / transformed[2, :]
        
        pt1 = (int(transformed[0, 0]), int(transformed[1, 0]))
        pt2 = (int(transformed[0, 1]), int(transformed[1, 1]))
        
        if 0 <= pt1[0] < new_w and 0 <= pt1[1] < new_h and 0 <= pt2[0] < new_w and 0 <= pt2[1] < new_h:
            cv2.line(grid_display, pt1, pt2, (100, 100, 100), 1)
    
    # 绘制水平网格线变换后的位置
    for j in range(0, h, step_y):
        pts = np.array([[0, j, 1], [w-1, j, 1]], dtype=np.float32).reshape(-1, 3)
        transformed = perspective_matrix @ pts.T
        transformed = transformed[:2, :] / transformed[2, :]
        
        pt1 = (int(transformed[0, 0]), int(transformed[1, 0]))
        pt2 = (int(transformed[0, 1]), int(transformed[1, 1]))
        
        if 0 <= pt1[0] < new_w and 0 <= pt1[1] < new_h and 0 <= pt2[0] < new_w and 0 <= pt2[1] < new_h:
            cv2.line(grid_display, pt1, pt2, (100, 100, 100), 1)
    
    # 在网格图上绘制边框
    cv2.rectangle(grid_display, (0, 0), (new_w - 1, new_h - 1), (0, 0, 255), 2)
    
    # 使用 matplotlib 显示
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.imshow(cv2.cvtColor(grid_display, cv2.COLOR_BGR2RGB))
    ax.set_title(f'透视变换网格示意图\n输出尺寸: {new_w} x {new_h}')
    ax.axis('off')
    
    plt.tight_layout()
    
    # 转换为 OpenCV 格式
    fig.canvas.draw()
    result = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    result = result.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    plt.close()
    
    return result