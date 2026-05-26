# 本文件用于实现图像仿射变换功能，包括平移、旋转、缩放、剪切等线性变换的组合
import cv2
import numpy as np

ALGORITHM_META = {
    "module": "geometry",
    "name": "affine",
    "display_name": "仿射变换",
    "description": "仿射变换是线性变换（旋转、缩放、剪切）和平移的组合，保持图像的平行性和共线性。支持通过变换矩阵或点对进行变换。",
    "params": {
        "transform_type": {
            "type": "choice",
            "default": "rotate_scale",
            "options": ["rotate_scale", "shear", "custom_points", "custom_matrix"],
            "label": "变换类型",
            "description": "rotate_scale: 旋转+缩放; shear: 剪切变换; custom_points: 通过三个点对定义; custom_matrix: 自定义2x3矩阵"
        },
        "angle": {
            "type": "float",
            "default": 30.0,
            "label": "旋转角度（度）",
            "description": "仅 rotate_scale 模式有效"
        },
        "scale": {
            "type": "float",
            "default": 1.0,
            "label": "缩放比例",
            "description": "仅 rotate_scale 模式有效"
        },
        "shear_x": {
            "type": "float",
            "default": 0.5,
            "label": "水平剪切因子",
            "description": "仅 shear 模式有效，表示水平方向的倾斜程度"
        },
        "shear_y": {
            "type": "float",
            "default": 0.0,
            "label": "垂直剪切因子",
            "description": "仅 shear 模式有效，表示垂直方向的倾斜程度"
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
        },
        "auto_crop": {
            "type": "boolean",
            "default": True,
            "label": "自适应裁剪",
            "description": "True: 自动调整输出尺寸包含整个变换后图像; False: 保持原图尺寸"
        }
    }
}

def run(image: np.ndarray, params: dict = None) -> dict:
    """
    对图像进行仿射变换
    :param image: 输入图像
    :param params: 算法参数字典
    :return: 包含 result, steps, analysis 的字典
    """
    # 参数初始化
    if params is None:
        params = {}
    
    transform_type = params.get("transform_type", "rotate_scale")
    angle = params.get("angle", 30.0)
    scale = params.get("scale", 1.0)
    shear_x = params.get("shear_x", 0.5)
    shear_y = params.get("shear_y", 0.0)
    border_mode = params.get("border_mode", "constant")
    border_value = params.get("border_value", 0)
    auto_crop = params.get("auto_crop", True)
    
    # 参数校验（只校验边界颜色范围，其他不设上下限）
    if scale <= 0:
        scale = 1.0
    border_value = max(0, min(255, border_value))
    
    valid_transform_types = ["rotate_scale", "shear", "custom_points", "custom_matrix"]
    if transform_type not in valid_transform_types:
        transform_type = "rotate_scale"
    
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
    center = (w // 2, h // 2)
    
    steps.append({
        "name": f"原始尺寸: {w} x {h}",
        "image": _draw_info_on_image(image, f"原始尺寸: {w} x {h}")
    })
    
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
    
    # 根据变换类型生成仿射矩阵
    if transform_type == "rotate_scale":
        # 旋转 + 缩放
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        transform_matrix = rotation_matrix
        transform_name = f"旋转 {angle:.1f}° + 缩放 {scale:.2f}倍"
        
    elif transform_type == "shear":
        # 剪切变换
        # 剪切矩阵: [1, shear_x, 0; shear_y, 1, 0]
        transform_matrix = np.float32([
            [1, shear_x, 0],
            [shear_y, 1, 0]
        ])
        transform_name = f"剪切变换 (shear_x={shear_x:.2f}, shear_y={shear_y:.2f})"
        
    elif transform_type == "custom_points":
        # 通过三个点对定义仿射变换
        # 默认将原图像三个角点映射到新位置
        pts1 = np.float32([[0, 0], [w - 1, 0], [0, h - 1]])
        
        # 计算变换后的三个点（示例：轻微倾斜）
        offset_x = w * 0.1
        offset_y = h * 0.1
        pts2 = np.float32([
            [offset_x, offset_y],
            [w - 1 - offset_x, offset_y * 0.5],
            [offset_x * 0.5, h - 1 - offset_y]
        ])
        
        transform_matrix = cv2.getAffineTransform(pts1, pts2)
        transform_name = "自定义点对仿射变换"
        
    else:  # custom_matrix
        # 自定义矩阵示例：水平倾斜
        transform_matrix = np.float32([
            [1, 0.3, 0],
            [0, 1, 0]
        ])
        transform_name = "自定义仿射矩阵 (水平倾斜)"
    
    # 计算输出尺寸
    if auto_crop:
        # 计算变换后图像的边界
        corners = np.array([
            [0, 0, 1],
            [w, 0, 1],
            [w, h, 1],
            [0, h, 1]
        ], dtype=np.float32)
        
        transformed_corners = corners @ transform_matrix.T
        min_x = np.min(transformed_corners[:, 0])
        max_x = np.max(transformed_corners[:, 0])
        min_y = np.min(transformed_corners[:, 1])
        max_y = np.max(transformed_corners[:, 1])
        
        new_w = int(np.ceil(max_x - min_x))
        new_h = int(np.ceil(max_y - min_y))
        
        # 调整变换矩阵以将图像平移到正区域
        transform_matrix[0, 2] -= min_x
        transform_matrix[1, 2] -= min_y
        
        output_size = (new_w, new_h)
    else:
        output_size = (w, h)
    
    # 执行仿射变换
    if border_mode == "constant":
        result = cv2.warpAffine(image, transform_matrix, output_size,
                                flags=cv2.INTER_LINEAR,
                                borderMode=border,
                                borderValue=(border_value, border_value, border_value))
    else:
        result = cv2.warpAffine(image, transform_matrix, output_size,
                                flags=cv2.INTER_LINEAR,
                                borderMode=border)
    
    # 显示变换结果
    info_text = f"{transform_name} | 输出尺寸: {result.shape[1]} x {result.shape[0]}"
    result_with_info = _draw_info_on_image(result, info_text)
    
    steps.append({
        "name": f"仿射变换结果",
        "image": result_with_info
    })
    
    # 绘制变换过程示意图
    steps.append({
        "name": "仿射变换示意图",
        "image": _draw_affine_demo(image, transform_matrix, output_size)
    })
    
    # 生成分析文本
    if transform_type == "rotate_scale":
        analysis = f"对图像进行仿射变换：{transform_name}。"
    elif transform_type == "shear":
        analysis = f"对图像进行剪切仿射变换：水平剪切因子={shear_x:.2f}，垂直剪切因子={shear_y:.2f}。剪切变换会使图像产生倾斜效果。"
    elif transform_type == "custom_points":
        analysis = f"通过三个点对定义仿射变换，将原图像的三个角点映射到新位置。仿射变换保持图像的平行性和共线性。"
    else:
        analysis = f"使用自定义仿射矩阵进行变换：{transform_name}。"
    
    if auto_crop:
        analysis += f" 输出尺寸自动调整为 {output_size[0]} x {output_size[1]}，确保完整显示变换后图像。"
    else:
        analysis += f" 输出尺寸保持原图大小 ({w} x {h})，超出部分被裁剪。"
    
    if border_mode == "constant":
        analysis += f" 空白区域使用{border_name}，颜色值为 {border_value}。"
    else:
        analysis += f" 空白区域使用{border_name}填充。"
    
    analysis += " 仿射变换是线性变换（旋转、缩放、剪切）和平移的组合，具有保持平行性和共线性的特点。"
    
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


def _draw_affine_demo(image: np.ndarray, transform_matrix: np.ndarray, output_size: tuple) -> np.ndarray:
    """
    绘制仿射变换示意图（变换前后的网格对比）
    :param image: 原始图像
    :param transform_matrix: 仿射变换矩阵
    :param output_size: 输出尺寸
    :return: 示意图图像
    """
    import matplotlib.pyplot as plt
    
    h, w = image.shape[:2]
    new_w, new_h = output_size
    
    # 创建子图
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # 原始图像
    axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f'原始图像\n尺寸: {w} x {h}')
    axes[0].axis('off')
    
    # 绘制变换后的网格
    # 创建一个空白画布
    transformed_display = np.ones((new_h, new_w, 3), dtype=np.uint8) * 255
    
    # 绘制原始网格点变换后的位置
    step = max(1, min(w, h) // 8)
    for i in range(0, w, step):
        for j in range(0, h, step):
            src_pt = np.array([i, j, 1], dtype=np.float32)
            dst_pt = transform_matrix @ src_pt
            x, y = int(dst_pt[0]), int(dst_pt[1])
            if 0 <= x < new_w and 0 <= y < new_h:
                cv2.circle(transformed_display, (x, y), 1, (0, 0, 255), -1)
    
    # 绘制网格线
    for i in range(0, w, step):
        src_pts_x = np.array([[i, 0, 1], [i, h-1, 1]], dtype=np.float32)
        dst_pts_x = transform_matrix @ src_pts_x.T
        pt1 = (int(dst_pts_x[0, 0]), int(dst_pts_x[1, 0]))
        pt2 = (int(dst_pts_x[0, 1]), int(dst_pts_x[1, 1]))
        if 0 <= pt1[0] < new_w and 0 <= pt1[1] < new_h and 0 <= pt2[0] < new_w and 0 <= pt2[1] < new_h:
            cv2.line(transformed_display, pt1, pt2, (200, 200, 200), 1)
    
    for j in range(0, h, step):
        src_pts_y = np.array([[0, j, 1], [w-1, j, 1]], dtype=np.float32)
        dst_pts_y = transform_matrix @ src_pts_y.T
        pt1 = (int(dst_pts_y[0, 0]), int(dst_pts_y[1, 0]))
        pt2 = (int(dst_pts_y[0, 1]), int(dst_pts_y[1, 1]))
        if 0 <= pt1[0] < new_w and 0 <= pt1[1] < new_h and 0 <= pt2[0] < new_w and 0 <= pt2[1] < new_h:
            cv2.line(transformed_display, pt1, pt2, (200, 200, 200), 1)
    
    axes[1].imshow(cv2.cvtColor(transformed_display, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f'仿射变换后网格\n尺寸: {new_w} x {new_h}')
    axes[1].axis('off')
    
    plt.tight_layout()
    
    # 转换为 OpenCV 格式
    fig.canvas.draw()
    img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    plt.close()
    
    return img