# 基于动漫图像识别的交互式数字图像处理系统

## 1. 项目定位

本项目是一个面向数字图像处理课程设计的 Web 交互式系统，主题确定为：

> **基于动漫图像识别的交互式数字图像处理系统**

项目围绕"动漫相关图像"展开，用户可以上传动漫人物、动漫场景、二次元插画、头像、截图等图片，也可以从项目内置图片库中选择示例图片。系统通过后端图像处理算法对图片进行实时处理，并在前端页面即时展示处理后的结果、算法参数、分步过程和结果分析。

本项目需要同时满足两类目标：

1. **课程设计目标**：覆盖数字图像处理中的基础运算、灰度变换、几何变换、空域滤波、频域滤波、彩色图像处理、图像复原、形态学处理、边缘检测等内容。
2. **项目开发目标**：采用 Vue + FastAPI 前后端分离架构，后端算法高度模块化，便于多人协作开发和前端自由组合调用。

---

## 2. 已确定技术路线

| 类型 | 技术选型 | 说明 |
|---|---|---|
| 项目主题 | 动漫相关图像识别 | 以动漫人物、头像、插画、场景截图为主要处理对象 |
| 前端框架 | Vue 3 + Vite | 用于实现交互式 Web 页面 |
| 前端请求 | Axios | 用于请求 FastAPI 后端接口 |
| 前端 UI | Element Plus / Naive UI 二选一 | 推荐 Element Plus，组件成熟，适合课程展示 |
| 前端图表 | ECharts | 用于展示直方图、指标曲线、对比图 |
| 后端框架 | FastAPI | 提供图片上传、图库读取、算法处理、结果返回接口 |
| 后端语言 | Python | 所有图像处理与识别功能均使用 Python 实现 |
| 图像处理库 | OpenCV、Pillow、scikit-image、SciPy | 覆盖主要数字图像处理算法 |
| 图像识别方式 | OpenCV 特征 + scikit-learn 轻量分类/匹配 | 先不强制使用深度学习，降低部署难度 |
| 开发系统 | Windows 11 | 全体成员统一 Windows 11 环境 |
| Python 环境 | venv 虚拟环境 | 保证每名成员环境一致，避免依赖冲突 |
| 部署方式 | 本地运行 | 不使用 Docker |
| 协作重点 | 后端算法模块 | 每个具体功能独立文件，按分类划归到小模块 |

---

## 3. 总体系统架构

```text
用户
 │
 │  上传图片 / 选择图库图片 / 选择算法 / 调整参数
 ▼
Vue 前端页面
 │
 │  Axios 请求
 ▼
FastAPI 后端接口层
 │
 │  参数校验、图片读取、算法路由
 ▼
后端算法模块层
 │
 │  基础运算 / 灰度变换 / 滤波 / 频域 / 彩色处理 / 复原 / 形态学 / 边缘检测 / 动漫识别
 ▼
结果分析层
 │
 │  指标统计、直方图、分步结果、文字分析
 ▼
FastAPI 返回 JSON
 │
 │  Base64 结果图 / 分步图 / 指标 / 分析文本
 ▼
Vue 前端即时展示处理结果
```

---

## 4. 项目目录结构

```text
anime-image-processing/
├─ README.md
├─ requirements.txt
│
├─ backend/
│  ├─ main.py
│  ├─ run_backend.bat
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ api/
│  │  │  ├─ __init__.py
│  │  │  ├─ health.py
│  │  │  ├─ upload.py
│  │  │  ├─ library.py
│  │  │  ├─ algorithms.py
│  │  │  └─ process.py
│  │  │
│  │  ├─ core/
│  │  │  ├─ __init__.py
│  │  │  ├─ config.py
│  │  │  ├─ cors.py
│  │  │  ├─ image_io.py
│  │  │  ├─ image_codec.py
│  │  │  └─ validators.py
│  │  │
│  │  ├─ schemas/
│  │  │  ├─ __init__.py
│  │  │  ├─ image_schema.py
│  │  │  ├─ algorithm_schema.py
│  │  │  └─ response_schema.py
│  │  │
│  │  ├─ services/
│  │  │  ├─ __init__.py
│  │  │  ├─ image_store.py
│  │  │  ├─ algorithm_registry.py
│  │  │  ├─ process_service.py
│  │  │  ├─ step_service.py
│  │  │  └─ analysis_service.py
│  │  │
│  │  ├─ algorithms/
│  │  │  ├─ __init__.py
│  │  │  │
│  │  │  ├─ basic_operations/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ image_add.py
│  │  │  │  ├─ image_subtract.py
│  │  │  │  ├─ image_blend.py
│  │  │  │  ├─ logic_and.py
│  │  │  │  ├─ logic_or.py
│  │  │  │  ├─ logic_not.py
│  │  │  │  └─ mask_apply.py
│  │  │  │
│  │  │  ├─ geometry/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ resize.py
│  │  │  │  ├─ rotate.py
│  │  │  │  ├─ translate.py
│  │  │  │  ├─ affine.py
│  │  │  │  └─ perspective.py
│  │  │  │
│  │  │  ├─ gray_transform/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ grayscale.py
│  │  │  │  ├─ binary_threshold.py
│  │  │  │  ├─ linear_transform.py
│  │  │  │  ├─ gamma_transform.py
│  │  │  │  ├─ log_transform.py
│  │  │  │  ├─ histogram_equalization.py
│  │  │  │  └─ clahe.py
│  │  │  │
│  │  │  ├─ spatial_filter/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ mean_filter.py
│  │  │  │  ├─ gaussian_filter.py
│  │  │  │  ├─ median_filter.py
│  │  │  │  ├─ bilateral_filter.py
│  │  │  │  ├─ laplacian_sharpen.py
│  │  │  │  └─ unsharp_mask.py
│  │  │  │
│  │  │  ├─ frequency_filter/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ dft_spectrum.py
│  │  │  │  ├─ ideal_low_pass.py
│  │  │  │  ├─ ideal_high_pass.py
│  │  │  │  ├─ gaussian_low_pass.py
│  │  │  │  ├─ gaussian_high_pass.py
│  │  │  │  └─ homomorphic_filter.py
│  │  │  │
│  │  │  ├─ color_processing/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ rgb_channel.py
│  │  │  │  ├─ hsv_adjust.py
│  │  │  │  ├─ color_balance.py
│  │  │  │  ├─ pseudo_color.py
│  │  │  │  └─ anime_color_enhance.py
│  │  │  │
│  │  │  ├─ restoration/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ motion_blur.py
│  │  │  │  ├─ inverse_filter.py
│  │  │  │  ├─ wiener_filter.py
│  │  │  │  ├─ denoise.py
│  │  │  │  └─ inpaint.py
│  │  │  │
│  │  │  ├─ morphology/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ erode.py
│  │  │  │  ├─ dilate.py
│  │  │  │  ├─ open_operation.py
│  │  │  │  ├─ close_operation.py
│  │  │  │  ├─ top_hat.py
│  │  │  │  ├─ black_hat.py
│  │  │  │  └─ connected_components.py
│  │  │  │
│  │  │  ├─ edge_detection/
│  │  │  │  ├─ __init__.py
│  │  │  │  ├─ sobel.py
│  │  │  │  ├─ scharr.py
│  │  │  │  ├─ laplace.py
│  │  │  │  ├─ log_edge.py
│  │  │  │  ├─ canny.py
│  │  │  │  ├─ hough_line.py
│  │  │  │  └─ hough_circle.py
│  │  │  │
│  │  │  └─ anime_recognition/
│  │  │     ├─ __init__.py
│  │  │     ├─ anime_face_detect.py
│  │  │     ├─ dominant_color_extract.py
│  │  │     ├─ line_style_analyze.py
│  │  │     ├─ feature_extract.py
│  │  │     └─ gallery_match.py
│  │  │
│  │  └─ analysis/
│  │     ├─ __init__.py
│  │     ├─ histogram.py
│  │     ├─ metrics.py
│  │     ├─ image_quality.py
│  │     └─ text_explanation.py
│  │
│  ├─ data/
│  │  ├─ library/
│  │  │  ├─ anime_character/
│  │  │  ├─ anime_scene/
│  │  │  ├─ anime_avatar/
│  │  │  ├─ course_samples/
│  │  │  └─ other/
│  │  ├─ uploads/
│  │  └─ outputs/
│  │
│  └─ tests/
│     ├─ test_health.py
│     ├─ test_image_io.py
│     ├─ test_algorithms_basic.py
│     └─ test_process_api.py
│
└─ frontend/
   ├─ package.json
   ├─ vite.config.js
   ├─ index.html
   ├─ src/
   │  ├─ main.js
   │  ├─ App.vue
   │  ├─ api/
   │  │  ├─ http.js
   │  │  ├─ uploadApi.js
   │  │  ├─ libraryApi.js
   │  │  ├─ algorithmApi.js
   │  │  └─ processApi.js
   │  ├─ router/
   │  │  └─ index.js
   │  ├─ stores/
   │  │  ├─ imageStore.js
   │  │  └─ algorithmStore.js
   │  ├─ views/
   │  │  ├─ HomeView.vue
   │  │  ├─ UploadView.vue
   │  │  ├─ LibraryView.vue
   │  │  ├─ ProcessView.vue
   │  │  ├─ AnimeRecognitionView.vue
   │  │  └─ ReportView.vue
   │  └─ components/
   │     ├─ ImageUploader.vue
   │     ├─ ImageLibrary.vue
   │     ├─ AlgorithmSelector.vue
   │     ├─ ParameterPanel.vue
   │     ├─ ImageCompare.vue
   │     ├─ StepViewer.vue
   │     └─ MetricPanel.vue
   └─ public/
      └─ favicon.ico
```

---

## 5. 后端模块化开发要求

### 5.1 一个具体功能一个文件

后端所有具体算法必须拆成单独文件，不允许把多个算法全部堆在一个大文件中。

正确示例：

```text
algorithms/edge_detection/canny.py
algorithms/edge_detection/sobel.py
algorithms/spatial_filter/median_filter.py
algorithms/gray_transform/gamma_transform.py
```

错误示例：

```text
algorithms/all_filters.py
algorithms/all_algorithms.py
```

### 5.2 每个文件第一行必须是中文功能说明

所有 `.py`、`.js`、`.vue`、`.md`、`.txt` 文件第一行都必须写中文功能说明。

Python 文件示例：

```python
# 本文件用于实现动漫图像的 Canny 边缘检测功能
```

Vue 文件示例：

```vue
<!-- 本文件用于实现图像处理页面的算法选择与结果展示功能 -->
```

JavaScript 文件示例：

```javascript
// 本文件用于封装图像处理相关的后端接口请求
```

Markdown 文件示例：

```markdown
# 本文件用于说明项目整体架构与协作开发规范
```

### 5.3 每个算法文件的统一接口规范

每个算法文件建议统一提供 `run` 函数，方便前端动态选择算法后，后端可以通过注册表统一调用。

```python
# 本文件用于实现动漫图像的 Canny 边缘检测功能

import cv2
import numpy as np


ALGORITHM_META = {
    "module": "edge_detection",
    "name": "canny",
    "display_name": "Canny 边缘检测",
    "description": "用于提取动漫人物轮廓、发丝边缘、场景建筑线条等边缘信息。",
    "params": {
        "threshold1": {"type": "int", "default": 80, "min": 0, "max": 255},
        "threshold2": {"type": "int", "default": 160, "min": 0, "max": 255},
        "blur_size": {"type": "odd_int", "default": 3, "min": 1, "max": 15}
    }
}


def run(image: np.ndarray, params: dict) -> dict:
    threshold1 = int(params.get("threshold1", 80))
    threshold2 = int(params.get("threshold2", 160))
    blur_size = int(params.get("blur_size", 3))

    if blur_size % 2 == 0:
        blur_size += 1

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)
    edge = cv2.Canny(blurred, threshold1, threshold2)

    return {
        "result": edge,
        "steps": [
            {"name": "灰度化", "image": gray},
            {"name": "高斯平滑", "image": blurred},
            {"name": "Canny 边缘检测", "image": edge}
        ],
        "analysis": "Canny 算法可以突出动漫图像中的人物轮廓、头发边缘和服装线条。阈值越低，边缘越丰富，但噪声也越明显。"
    }
```

---

## 6. 前端即时选择算法的实现逻辑

前端页面不应该写死算法按钮，而应该从后端读取算法清单。

### 6.1 前端启动后读取算法列表

```text
GET /api/algorithms
```

返回示例：

```json
{
  "modules": [
    {
      "module": "edge_detection",
      "display_name": "边缘检测",
      "algorithms": [
        {
          "name": "canny",
          "display_name": "Canny 边缘检测",
          "params": {
            "threshold1": {"type": "int", "default": 80, "min": 0, "max": 255},
            "threshold2": {"type": "int", "default": 160, "min": 0, "max": 255}
          }
        }
      ]
    }
  ]
}
```

### 6.2 用户选择算法后立即请求处理

```text
POST /api/process/run
```

请求示例：

```json
{
  "source_type": "upload",
  "image_id": "upload_20260525_001.png",
  "module": "edge_detection",
  "algorithm": "canny",
  "params": {
    "threshold1": 80,
    "threshold2": 160,
    "blur_size": 3
  },
  "return_steps": true
}
```

返回示例：

```json
{
  "success": true,
  "result_image": "data:image/png;base64,...",
  "steps": [
    {
      "name": "灰度化",
      "image": "data:image/png;base64,..."
    },
    {
      "name": "Canny 边缘检测",
      "image": "data:image/png;base64,..."
    }
  ],
  "metrics": {
    "mean": 126.5,
    "std": 42.1,
    "edge_density": 0.18
  },
  "analysis": "处理后图像中的人物轮廓更加清晰，适合用于动漫角色线稿提取。"
}
```

---

## 7. 图片来源设计

系统必须为用户提供两种图片来源。

### 7.1 用户实时上传图片

用户上传本地图片，后端保存到：

```text
backend/data/uploads/
```

推荐接口：

```text
POST /api/upload/image
```

支持格式：

```text
jpg、jpeg、png、bmp、tif、tiff、webp
```

上传后返回：

```json
{
  "success": true,
  "image_id": "upload_xxx.png",
  "preview_url": "/api/upload/preview/upload_xxx.png"
}
```

### 7.2 项目内置图片库

项目内置图片库保存到：

```text
backend/data/library/
```

推荐分类：

```text
anime_character/     动漫人物图像
anime_scene/         动漫场景图像
anime_avatar/        动漫头像图像
course_samples/      课程实验素材图像
other/               其他测试图像
```

推荐接口：

```text
GET /api/library/categories
GET /api/library/images?category=anime_character
GET /api/library/image/{image_id}
```

图片库的作用：

1. 防止用户没有合适测试图片时无法演示。
2. 便于课程答辩时快速展示固定案例。
3. 便于小组成员调试同一张图片，保证结果一致。
4. 可将之前上传课程资料中的实验图像整理到 `course_samples` 中作为通用测试样例。

---

## 8. 推荐功能清单

### 8.1 基础图像处理功能

| 分类 | 功能文件 | 功能说明 | 是否必做 |
|---|---|---|---|
| 基础运算 | `image_add.py` | 图像加法、亮度增加 | 必做 |
| 基础运算 | `image_subtract.py` | 图像减法、差异检测 | 必做 |
| 基础运算 | `image_blend.py` | 图像融合 | 必做 |
| 逻辑运算 | `logic_and.py` | 图像与运算 | 必做 |
| 逻辑运算 | `logic_or.py` | 图像或运算 | 必做 |
| 逻辑运算 | `logic_not.py` | 图像反相 | 必做 |
| 几何变换 | `resize.py` | 缩放 | 必做 |
| 几何变换 | `rotate.py` | 旋转 | 必做 |
| 几何变换 | `translate.py` | 平移 | 必做 |
| 几何变换 | `affine.py` | 仿射变换 | 推荐 |
| 几何变换 | `perspective.py` | 透视变换 | 推荐 |
| 灰度变换 | `grayscale.py` | 灰度化 | 必做 |
| 灰度变换 | `binary_threshold.py` | 二值化 | 必做 |
| 灰度变换 | `gamma_transform.py` | 伽马变换 | 必做 |
| 灰度变换 | `histogram_equalization.py` | 直方图均衡化 | 必做 |
| 灰度变换 | `clahe.py` | 自适应直方图均衡化 | 推荐 |

### 8.2 滤波、复原、形态学与边缘检测

| 分类 | 功能文件 | 功能说明 | 是否必做 |
|---|---|---|---|
| 空域滤波 | `mean_filter.py` | 均值滤波 | 必做 |
| 空域滤波 | `gaussian_filter.py` | 高斯滤波 | 必做 |
| 空域滤波 | `median_filter.py` | 中值滤波 | 必做 |
| 空域滤波 | `bilateral_filter.py` | 双边滤波 | 推荐 |
| 空域锐化 | `laplacian_sharpen.py` | 拉普拉斯锐化 | 必做 |
| 空域锐化 | `unsharp_mask.py` | 反锐化掩蔽 | 推荐 |
| 频域滤波 | `dft_spectrum.py` | 傅里叶频谱显示 | 必做 |
| 频域滤波 | `ideal_low_pass.py` | 理想低通滤波 | 必做 |
| 频域滤波 | `ideal_high_pass.py` | 理想高通滤波 | 必做 |
| 频域滤波 | `gaussian_low_pass.py` | 高斯低通滤波 | 推荐 |
| 频域滤波 | `homomorphic_filter.py` | 同态滤波 | 推荐 |
| 图像复原 | `motion_blur.py` | 运动模糊模拟 | 推荐 |
| 图像复原 | `wiener_filter.py` | 维纳滤波 | 推荐 |
| 图像复原 | `inpaint.py` | 图像修复 | 推荐 |
| 形态学 | `erode.py` | 腐蚀 | 必做 |
| 形态学 | `dilate.py` | 膨胀 | 必做 |
| 形态学 | `open_operation.py` | 开运算 | 必做 |
| 形态学 | `close_operation.py` | 闭运算 | 必做 |
| 形态学 | `connected_components.py` | 连通域分析 | 推荐 |
| 边缘检测 | `sobel.py` | Sobel 边缘检测 | 必做 |
| 边缘检测 | `laplace.py` | Laplace 边缘检测 | 必做 |
| 边缘检测 | `canny.py` | Canny 边缘检测 | 必做 |
| 边缘检测 | `hough_line.py` | Hough 直线检测 | 推荐 |

### 8.3 动漫图像识别与主题化功能

| 功能文件 | 功能说明 | 实现难度 | 建议 |
|---|---|---:|---|
| `anime_face_detect.py` | 检测动漫头像或人物主体区域 | 中 | 可先用边缘、肤色/亮色区域、轮廓近似实现 |
| `dominant_color_extract.py` | 提取动漫角色主色调 | 低 | 适合分析头发、服装、背景色彩 |
| `line_style_analyze.py` | 分析动漫线稿边缘密度和线条风格 | 低 | 可基于 Canny + 边缘密度实现 |
| `feature_extract.py` | 提取颜色直方图、HOG、边缘特征 | 中 | 为图库匹配服务 |
| `gallery_match.py` | 将上传图片与图库图片做相似度匹配 | 中 | 可用颜色直方图 + ORB/SIFT/HOG 特征 |
| `anime_color_enhance.py` | 动漫图像色彩增强 | 低 | 用 HSV 饱和度、亮度和 CLAHE 实现 |

推荐先实现轻量级识别，不要一开始引入深度学习大模型。课程设计重点是数字图像处理，识别模块主要用于强化主题，不要让项目复杂到难以完成。

---

## 9. 后端 API 清单

| 接口 | 方法 | 功能 |
|---|---|---|
| `/api/health` | GET | 检查后端是否运行 |
| `/api/upload/image` | POST | 上传用户图片 |
| `/api/upload/preview/{image_id}` | GET | 获取上传图片预览 |
| `/api/library/categories` | GET | 获取图库分类 |
| `/api/library/images` | GET | 获取指定分类下的图片列表 |
| `/api/library/image/{image_id}` | GET | 获取图库图片 |
| `/api/algorithms` | GET | 获取全部可用算法模块和参数 |
| `/api/process/run` | POST | 对指定图片执行当前选择的算法 |
| `/api/process/steps` | POST | 返回算法分步执行过程 |
| `/api/analysis/metrics` | POST | 返回图像指标与分析结果 |

---

## 10. 前端页面清单

| 页面 | 功能 |
|---|---|
| 首页 | 项目介绍、主题说明、快速开始 |
| 图片上传页 | 用户上传图片并预览 |
| 图片库页 | 用户从项目内置图库中选择图片 |
| 图像处理页 | 选择算法分类、算法名称、参数并即时处理 |
| 动漫识别页 | 主色调提取、线条风格分析、图库相似度匹配 |
| 分步执行页 | 展示算法中间过程，例如傅里叶变换频谱分解 |
| 结果分析页 | 展示直方图、指标、文字分析 |
| 报告辅助页 | 汇总原图、结果图、参数、分析文字，便于写课程报告 |

---

## 11. 依赖说明

### 11.1 后端 Python 依赖

后端依赖已经整理到 `requirements.txt`，主要包括：

| 依赖 | 用途 |
|---|---|
| FastAPI | 后端接口服务 |
| Uvicorn | FastAPI 本地运行服务器 |
| python-multipart | 支持图片文件上传 |
| pydantic | 请求参数与响应数据校验 |
| opencv-contrib-python | 核心图像处理算法 |
| Pillow | 图片读取、格式转换、兼容部分特殊格式 |
| NumPy | 图像矩阵与像素运算 |
| SciPy | 卷积、滤波、频域、复原算法支持 |
| scikit-image | 补充图像处理算法、SSIM、形态学等 |
| scikit-learn | 轻量图像识别、相似度分类、特征匹配 |
| matplotlib | 直方图、频谱图、结果图生成 |
| pandas | 结果指标表格整理 |
| plotly | 交互式图表展示 |
| imageio | 动图、视频帧或部分特殊格式读取 |
| tifffile | `.tif`、`.tiff` 图像支持 |
| pytest | 后端测试 |
| httpx | API 测试 |
| ruff | 代码格式与静态检查 |

### 11.2 前端依赖建议

前端不写入 `requirements.txt`，需要单独写入 `frontend/package.json`。

推荐前端依赖：

```json
{
  "dependencies": {
    "@vitejs/plugin-vue": "latest",
    "vite": "latest",
    "vue": "latest",
    "vue-router": "latest",
    "pinia": "latest",
    "axios": "latest",
    "element-plus": "latest",
    "echarts": "latest"
  },
  "devDependencies": {}
}
```

---

## 12. Windows 11 开发与启动流程

### 12.1 后端启动

进入项目根目录：

```bat
cd anime-image-processing
```

创建虚拟环境：

```bat
python -m venv .venv
```

激活虚拟环境：

```bat
.venv\Scripts\activate
```

升级 pip：

```bat
python -m pip install --upgrade pip
```

安装依赖：

```bat
pip install -r requirements.txt
```

启动 FastAPI：

```bat
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

浏览器打开：

```text
http://127.0.0.1:8000/docs
```

### 12.2 前端启动

进入前端目录：

```bat
cd frontend
```

安装依赖：

```bat
npm install
```

启动开发服务器：

```bat
npm run dev
```

默认访问：

```text
http://127.0.0.1:5173
```

---

## 13. 协作开发分工建议

本项目多人协作主要集中在后端，因此建议按算法模块分工：

| 成员 | 负责模块 | 主要任务 |
|---|---|---|
| 成员 A | 基础运算、灰度变换 | 图像加减、逻辑运算、灰度化、二值化、直方图均衡化 |
| 成员 B | 空域滤波、图像复原 | 均值、高斯、中值、双边、锐化、维纳滤波 |
| 成员 C | 频域滤波 | DFT、频谱图、低通、高通、同态滤波 |
| 成员 D | 形态学、边缘检测 | 腐蚀、膨胀、开闭运算、Sobel、Canny、Hough |
| 成员 E | 动漫识别、结果分析 | 主色调、线条风格、图库匹配、指标与分析文本 |
| 成员 F | 前端整合 | 页面、接口调用、参数面板、结果展示 |

每个成员提交代码时必须保证：

1. 文件第一行有中文功能说明。
2. 新算法文件有 `ALGORITHM_META`。
3. 新算法文件有统一 `run(image, params)` 接口。
4. 不在算法文件中写前端逻辑。
5. 不在算法文件中使用 `cv2.imshow()`。
6. 不修改其他成员负责模块的接口格式。
7. 至少准备 1 张测试图片和 1 个测试参数组合。

---

## 14. 关键实现注意事项

### 14.1 OpenCV 的 BGR 与前端 RGB 问题

OpenCV 默认读取图片为 BGR，而前端页面显示通常需要 RGB。因此：

1. 后端算法内部可以统一使用 BGR。
2. 返回给前端前必须转成 RGB 或 PNG/JPEG Base64。
3. Matplotlib 绘图时必须注意通道转换。

### 14.2 中文路径读取问题

Windows 下 OpenCV 读取中文路径可能失败，建议统一使用以下方式读取：

```python
# 本文件用于提供支持中文路径的图像读取函数

import cv2
import numpy as np


def imread_unicode(path: str, flags=cv2.IMREAD_COLOR):
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, flags)
```

### 14.3 参数合法性问题

所有参数必须在后端校验：

| 参数 | 要求 |
|---|---|
| 滤波核大小 | 必须是正奇数 |
| 阈值 | 必须在 0-255 |
| 缩放比例 | 必须大于 0 |
| 旋转角度 | 建议限制在 -360 到 360 |
| 频域滤波半径 | 必须大于 0 且小于图像尺寸 |
| 形态学结构元素大小 | 必须是正奇数 |
| 图片大小 | 建议限制最大分辨率，避免接口过慢 |

### 14.4 图片返回格式

后端推荐将结果图转为 Base64 返回给前端：

```json
{
  "result_image": "data:image/png;base64,..."
}
```

这样前端可以直接使用：

```html
<img :src="resultImage" />
```

### 14.5 分步执行展示

课程设计要求体现算法执行过程，因此重点算法必须返回步骤图。

优先支持分步执行的功能：

1. 傅里叶变换。
2. 频域低通/高通滤波。
3. Canny 边缘检测。
4. 直方图均衡化。
5. 形态学开闭运算。
6. 动漫图库相似度匹配。
7. 动漫主色调提取。

---

## 15. 课程报告对应关系

| 报告章节 | 本项目对应内容 |
|---|---|
| 第 1 章 绪论 | 动漫图像处理背景、意义、项目目标、系统框架 |
| 第 2 章 相关方法 | OpenCV、FastAPI、Vue、数字图像处理算法原理 |
| 第 3 章 算法介绍、程序设计、运行结果展示及分析 | 各算法模块、分步结果、处理前后对比、指标分析 |
| 第 4 章 Web 网页开发 | Vue 页面设计、FastAPI 接口、前后端分离、图片上传与图库选择、即时算法处理 |

---

## 16. 开发优先级

### P0：必须完成

1. Vue + FastAPI 前后端连通。
2. 图片上传。
3. 图片库选择。
4. 算法列表由后端动态返回。
5. 用户选择算法后立即处理并显示结果图。
6. 灰度化、二值化、直方图均衡化。
7. 均值滤波、高斯滤波、中值滤波。
8. Sobel、Canny 边缘检测。
9. 腐蚀、膨胀、开运算、闭运算。
10. DFT 频谱图与简单低通/高通滤波。

### P1：建议完成

1. 动漫主色调提取。
2. 动漫线条风格分析。
3. 动漫图库相似度匹配。
4. CLAHE。
5. 双边滤波。
6. Laplacian 锐化。
7. Hough 直线检测。
8. 结果指标统计。

### P2：有时间再做

1. 维纳滤波。
2. 图像修复。
3. 同态滤波。
4. 动漫人脸检测。
5. 批量处理。
6. 报告一键导出。

---

## 17. 最终验收标准

项目最终至少应达到以下效果：

1. 用户可以选择"上传图片"或"项目图库图片"。
2. 用户可以在前端自由选择算法分类和算法名称。
3. 用户调整参数后，可以立即看到处理后的图片。
4. 后端每个具体算法都是单独文件。
5. 每个文件第一行都有中文功能说明。
6. 系统可以展示处理前后对比图。
7. 系统可以展示部分算法的分步执行过程。
8. 系统可以输出基本结果分析。
9. 项目可以在 Windows 11 + Python venv 环境下运行。
10. 不依赖 Docker。
11. 项目结构适合多人协作开发。
12. 课程报告可以直接引用系统页面截图、算法结果和分析文字。

---

## 18. 不建议做的内容

为了保证项目可落地，不建议一开始加入以下内容：

1. 不建议使用 Docker。
2. 不建议一开始接入大型深度学习模型。
3. 不建议把所有算法写在一个文件里。
4. 不建议前端写死算法列表。
5. 不建议直接使用 `cv2.imshow()` 展示结果。
6. 不建议使用绝对路径读取图片。
7. 不建议只做网页，不做结果分析。
8. 不建议只做动漫识别，不覆盖数字图像处理课程要求。
