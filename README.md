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

```mermaid
flowchart TB
    subgraph FRONTEND["<b>Vue 3 前端</b>"]
        direction TB
        A["👤 用户"] --> A1["上传图片 / 选择图库 / 选择算法 / 调整参数"]
        A1 --> A2["Views: HomeView · LoginView · UserProfileView · WorkspaceView"]
        A2 --> A3["Components: HeaderNav · MainLayout · AppFooter"]
        A3 --> A4["Axios (http.js)<br/>baseURL + Token 拦截器<br/>Element Plus + ECharts + Pinia"]
    end

    subgraph BACKEND["<b>FastAPI 后端</b>"]
        direction TB

        subgraph API["API 路由层 (12 条路由)"]
            direction LR
            B1["健康检查<br/>GET /api/health"]
            B2["图片上传<br/>POST /api/upload/image<br/>GET /api/upload/preview/{path}"]
            B3["图库<br/>GET /api/library/*"]
            B4["算法元数据<br/>GET /api/algorithms"]
            B5["算法执行<br/>POST /api/process/run<br/>POST /api/algorithms/{cat}/run"]
            B6["指标分析<br/>POST /api/analysis/metrics"]
        end

        subgraph SERVICES["Services 业务层"]
            direction LR
            C1["algorithm_registry<br/>算法注册与动态导入"]
            C2["process_service<br/>load → run → encode"]
            C3["step_service<br/>步骤图编码"]
            C4["analysis_service<br/>像素统计与直方图"]
            C5["image_store<br/>上传/图库/路径安全"]
        end

        subgraph ALGOS["Algorithms 算法模块层 (30 个算法)"]
            direction LR
            D1["灰度图像类<br/>9 个<br/>灰度化/二值化<br/>直方图均衡化<br/>Canny/Sobel<br/>腐蚀/膨胀/开闭运算"]
            D2["彩色图像类<br/>4 个<br/>颜色空间转换<br/>饱和度调整<br/>动漫色彩增强<br/>主色调提取"]
            D3["几何变换类<br/>3 个<br/>缩放/旋转/翻转"]
            D4["空域滤波类<br/>5 个<br/>均值/高斯/中值<br/>双边/拉普拉斯"]
            D5["频域分析类<br/>3 个<br/>DFT/中心化/幅度谱"]
            D6["频域滤波类<br/>6 个<br/>低通/高通<br/>理想/高斯 变种"]
        end

        subgraph CORE["Core 核心工具层"]
            direction LR
            E1["image_codec<br/>numpy ↔ Base64"]
            E2["image_io<br/>中文路径兼容"]
            E3["upload_validator<br/>格式/大小/分辨率"]
            E4["cors · config"]
        end
    end

    subgraph STORAGE["<b>数据存储</b>"]
        direction LR
        F1[("data/uploads/<br/>用户上传")]
        F2[("data/library/<br/>内置图库<br/>5 个分类")]
        F3[("data/outputs/<br/>算法输出")]
    end

    A4 -->|"HTTP 请求"| API
    API --> SERVICES
    SERVICES --> ALGOS
    SERVICES --> CORE
    CORE --> STORAGE
    STORAGE -->|"读取图片"| SERVICES
    ALGOS -->|"run(image, params)"| SERVICES
    SERVICES -->|"JSON + Base64"| A4
    A4 -->|"渲染结果图/分步图/指标/分析"| A2

    style FRONTEND fill:#e3f2fd,stroke:#1565c0,color:#1a237e
    style BACKEND fill:#fff8e1,stroke:#f57f17,color:#3e2723
    style STORAGE fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    style API fill:#fff3e0,stroke:#e65100,color:#bf360c
    style SERVICES fill:#fce4ec,stroke:#c62828,color:#880e4f
    style ALGOS fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c
    style CORE fill:#e0f2f1,stroke:#00695c,color:#004d40
```

---

## 4. 项目目录结构

```text
Digital-image-processing-Design/
├─ README.md
├─ requirements.txt
├─ LICENSE
├─ .gitignore
│
├─ docs/
│  ├─ backend-update-doc/
│  │  ├─ CHANGELOG01.md
│  │  ├─ CHANGELOG02.md
│  │  ├─ CHANGELOG03.md
│  │  ├─ CHANGELOG04.md
│  │  └─ CHANGELOG05.md
│  ├─ prompts/
│  │  └─ algorithm_improvement_prompts_7_models/
│  │     ├─ chatgpt_algorithm_improvement_slider_prompt.md
│  │     ├─ claude_algorithm_improvement_slider_prompt.md
│  │     ├─ deepseek_algorithm_improvement_slider_prompt.md
│  │     ├─ doubao_algorithm_improvement_slider_prompt.md
│  │     ├─ gemini_algorithm_improvement_slider_prompt.md
│  │     ├─ glm_algorithm_improvement_slider_prompt.md
│  │     └─ kimi_algorithm_improvement_slider_prompt.md
│  └─ 算法书写规范说明文档.docx
│
├─ backend/
│  ├─ main.py                                # FastAPI 应用入口
│  ├─ README.md                              # 后端文件说明、前端联调和环境配置
│  │
│  ├─ app/
│  │  ├─ __init__.py
│  │  │
│  │  ├─ core/                               # 核心配置与工具模块
│  │  │  ├─ .gitkeep
│  │  │  ├─ __init__.py
│  │  │  ├─ config.py                        # 应用全局配置
│  │  │  ├─ cors.py                          # CORS 跨域配置
│  │  │  ├─ image_codec.py                   # 图像编解码工具
│  │  │  ├─ image_io.py                      # 图像文件读写（含中文路径支持）
│  │  │  ├─ upload_config.py                 # 上传配置
│  │  │  └─ upload_validator.py              # 上传文件校验
│  │  │
│  │  ├─ api/                                # API 路由层（均委托 services 层处理业务逻辑）
│  │  │  ├─ .gitkeep
│  │  │  ├─ __init__.py
│  │  │  ├─ algorithms.py                    # GET /api/algorithms 算法元数据查询
│  │  │  ├─ analysis.py                      # POST /api/analysis/metrics 图片指标计算
│  │  │  ├─ health.py                        # GET /api/health 健康检查
│  │  │  ├─ library.py                       # 内置图片库分类/列表/文件接口
│  │  │  ├─ process.py                       # POST /api/process/run 算法处理主入口
│  │  │  ├─ upload.py                        # 图片上传与预览接口
│  │  │  └─ algorithm_modules/               # 六大分类独立子路由（GET 列表 + POST 执行）
│  │  │     ├─ __init__.py
│  │  │     ├─ color_image.py
│  │  │     ├─ common.py                     # 共享常量和通用处理逻辑
│  │  │     ├─ frequency_analysis.py
│  │  │     ├─ frequency_filter.py
│  │  │     ├─ geometric_transform.py
│  │  │     ├─ grayscale_image.py
│  │  │     └─ spatial_filter.py
│  │  │
│  │  ├─ schemas/                            # Pydantic 数据校验模型
│  │  │  ├─ .gitkeep
│  │  │  ├─ __init__.py
│  │  │  ├─ algorithm_schema.py
│  │  │  ├─ image_schema.py
│  │  │  ├─ process_schema.py
│  │  │  └─ response_schema.py
│  │  │
│  │  ├─ services/                           # 业务逻辑服务层
│  │  │  ├─ .gitkeep
│  │  │  ├─ __init__.py
│  │  │  ├─ algorithm_registry.py            # 算法注册与发现
│  │  │  ├─ analysis_service.py              # 图像分析服务
│  │  │  ├─ image_store.py                   # 图像存储管理
│  │  │  ├─ process_service.py               # 算法处理调度
│  │  │  └─ step_service.py                  # 分步执行服务
│  │  │
│  │  ├─ analysis/                           # 分析模块（扩展预留）
│  │  │  └─ .gitkeep
│  │  │
│  │  └─ algorithms/                         # 图像处理算法模块
│  │     ├─ __init__.py
│  │     ├─ 算法框架填写说明.md
│  │     ├─ 分工文档.md
│  │     ├─ grayscale_image/                 # 8.1 灰度图像类
│  │     │  ├─ __init__.py
│  │     │  ├─ grayscale.py                  # 灰度化
│  │     │  ├─ binary_threshold.py           # 二值化
│  │     │  ├─ histogram_equalization.py     # 直方图均衡化
│  │     │  ├─ edge_detection_basic.py       # 边缘检测（Canny）
│  │     │  ├─ sobel_edge_detection.py       # 边缘检测（Sobel）
│  │     │  ├─ erode.py                      # 腐蚀
│  │     │  ├─ dilate.py                     # 膨胀
│  │     │  ├─ open_operation.py             # 开运算
│  │     │  └─ close_operation.py            # 闭运算
│  │     │
│  │     ├─ color_image/                     # 8.2 彩色图像类
│  │     │  ├─ __init__.py
│  │     │  ├─ color_space_convert.py        # 颜色空间转换
│  │     │  ├─ saturation_adjust.py          # 饱和度调整
│  │     │  ├─ anime_color_enhance.py        # 动漫色彩增强
│  │     │  └─ dominant_color_extract.py     # 主色调提取
│  │     │
│  │     ├─ geometric_transform/             # 8.3 几何变换类
│  │     │  ├─ __init__.py
│  │     │  ├─ resize.py                     # 图像缩放
│  │     │  ├─ rotate.py                     # 图像旋转
│  │     │  └─ flip.py                       # 图像翻转
│  │     │
│  │     ├─ spatial_filter/                  # 8.4 空域滤波类
│  │     │  ├─ .gitkeep
│  │     │  ├─ __init__.py
│  │     │  ├─ mean_filter.py                # 均值滤波
│  │     │  ├─ gaussian_filter.py            # 高斯滤波
│  │     │  ├─ median_filter.py              # 中值滤波
│  │     │  ├─ bilateral_filter.py           # 双边滤波
│  │     │  └─ laplacian_sharpen.py          # 拉普拉斯锐化
│  │     │
│  │     ├─ frequency_analysis/              # 8.5 频域分析类
│  │     │  ├─ __init__.py
│  │     │  ├─ dft_spectrum.py               # 傅里叶频谱显示
│  │     │  ├─ spectrum_shift.py             # 频谱中心化
│  │     │  └─ magnitude_spectrum.py         # 幅度谱显示
│  │     │
│  │     └─ frequency_filter/                # 8.6 频域滤波类
│  │        ├─ .gitkeep
│  │        ├─ __init__.py
│  │        ├─ low_pass_filter.py            # 低通滤波
│  │        ├─ high_pass_filter.py           # 高通滤波
│  │        ├─ ideal_low_pass.py             # 理想低通滤波
│  │        ├─ ideal_high_pass.py            # 理想高通滤波
│  │        ├─ gaussian_low_pass.py          # 高斯低通滤波
│  │        └─ gaussian_high_pass.py         # 高斯高通滤波
│  │
│  ├─ data/
│  │  ├─ image_limit.md                      # 图片限制说明文档
│  │  ├─ uploads/                            # 用户上传图片运行目录，仅提交 .gitkeep
│  │  ├─ library/                            # 内置图片库
│  │  │  ├─ anime_character/                 #   动漫人物图像
│  │  │  ├─ anime_scene/                     #   动漫场景图像
│  │  │  ├─ anime_avatar/                    #   动漫头像图像
│  │  │  ├─ course_samples/                  #   课程实验素材
│  │  │  └─ other/                           #   其他测试图像
│  │  ├─ test_images/                        # 测试输入图片
│  │  ├─ test_outputs/                       # 测试输出图片运行目录，仅提交 .gitkeep
│  │  └─ outputs/                            # 算法处理输出运行目录，仅提交 .gitkeep
│  │
│  └─ tests/
│     ├─ README.md
│     ├─ manual_test_algorithm.py             # 初学者三路径手动测试脚本
│     ├─ manual_test_algorithm_advanced.py    # 高级参数化手动测试脚本
│     ├─ test_algorithm_completeness.py       # 算法完整性测试
│     ├─ test_backend_framework.py            # 后端框架自动化测试
│     ├─ 算法测试脚本使用说明文档.md
│     └─ sample_test_configs/
│        ├─ saturation_adjust_example.json
│        ├─ grayscale_example.json
│        ├─ binary_threshold_example.json
│        ├─ canny_example.json
│        ├─ sobel_edge_detection_example.json
│        ├─ gaussian_filter_example.json
│        ├─ dft_spectrum_example.json
│        ├─ ideal_low_pass_example.json
│        └─ ideal_high_pass_example.json
│
└─ frontend/
   ├─ .env.development                     # 开发环境变量（后端 API 地址）
   ├─ .gitignore
   ├─ .vscode/
   │  └─ extensions.json
   ├─ README.md
   ├─ package.json
   ├─ pnpm-lock.yaml
   ├─ pnpm-workspace.yaml
   ├─ jsconfig.json
   ├─ vite.config.js
   ├─ index.html
   ├─ public/
   │  └─ favicon.ico
   └─ src/
      ├─ main.js
      ├─ App.vue
      ├─ api/
      │  ├─ .gitkeep
      │  └─ http.js                        # Axios 实例封装（baseURL / 拦截器 / Token）
      ├─ assets/
      │  ├─ .gitkeep
      │  ├─ background/                    # 页面背景图片
      │  │  ├─ bg1.jpg
      │  │  ├─ bg2.jpg
      │  │  ├─ bg3.jpg
      │  │  └─ bg4.jpg
      │  └─ home_bg.jpg                    # 首页背景
      ├─ components/
      │  ├─ .gitkeep
      │  ├─ AppFooter.vue                  # 页脚组件
      │  ├─ HeaderNav.vue                  # 顶部导航组件
      │  └─ MainLayout.vue                 # 主布局组件（Header + RouterView + Footer）
      ├─ router/
      │  └─ index.js                       # 路由配置（首页/登录/个人中心/工作区）
      ├─ stores/
      │  ├─ authStore.js                   # 用户认证状态（Pinia）
      │  └─ counter.js                     # 示例 store
      ├─ styles/
      │  └─ index.scss                      # 全局样式
      ├─ utils/
      │  ├─ .gitkeep
      │  ├─ check_health.js                # 后端健康检查工具
      │  └─ token.js                       # Token 存取工具
      └─ views/
         ├─ .gitkeep
         ├─ HomeView.vue                   # 首页
         ├─ LoginView.vue                  # 登录页
         ├─ UserProfileView.vue             # 个人中心
         └─ WorkspaceView.vue              # 工作区（图像处理主页面）
```

---

## 5. 后端模块化开发要求

### 5.1 一个具体功能一个文件

后端所有具体算法必须拆成单独文件，不允许把多个算法全部堆在一个大文件中。

正确示例：

```text
algorithms/grayscale_image/edge_detection_basic.py
algorithms/grayscale_image/binary_threshold.py
algorithms/spatial_filter/median_filter.py
algorithms/frequency_analysis/dft_spectrum.py
algorithms/frequency_filter/low_pass_filter.py
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
# 本文件用于实现动漫图像的通用边缘检测功能
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
    "module": "grayscale_image",
    "name": "edge_detection_basic",
    "display_name": "基础边缘检测",
    "description": "用于提取动漫人物轮廓、发丝边缘、场景建筑线条等边缘信息。",
    "params": {
        "threshold1": {
            "type": "int",
            "default": 80,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "阈值1",
            "component": "slider"
        },
        "threshold2": {
            "type": "int",
            "default": 160,
            "min": 0,
            "max": 255,
            "step": 1,
            "label": "阈值2",
            "component": "slider"
        },
        "blur_size": {
            "type": "int",
            "default": 3,
            "min": 1,
            "max": 15,
            "step": 2,
            "label": "模糊核大小",
            "component": "slider"
        }
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
            {"name": "边缘检测", "image": edge}
        ],
        "metrics": {
            "threshold1": threshold1,
            "threshold2": threshold2,
            "blur_size": blur_size
        },
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
      "module": "grayscale_image",
      "display_name": "灰度图像类",
      "algorithms": [
        {
          "name": "edge_detection_basic",
          "display_name": "基础边缘检测",
          "params": {
            "threshold1": {
              "type": "int", "default": 80, "min": 0, "max": 255,
              "step": 1, "label": "阈值1", "component": "slider"
            },
            "threshold2": {
              "type": "int", "default": 160, "min": 0, "max": 255,
              "step": 1, "label": "阈值2", "component": "slider"
            }
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
  "image_path": "upload_20260525_001.png",
  "module": "grayscale_image",
  "algorithm": "edge_detection_basic",
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
  "module": "grayscale_image",
  "module_display_name": "灰度图像类",
  "algorithm": "edge_detection_basic",
  "algorithm_display_name": "基础边缘检测",
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

该目录是运行时目录，仓库中只保留 `.gitkeep`。实际上传图片、算法输出图、测试输出图均由 `.gitignore` 忽略，不作为源码提交内容。

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
  "image_path": "upload_xxx.png",
  "filename": "upload_xxx.png",
  "width": 800,
  "height": 600,
  "preview_url": "/api/upload/preview/upload_xxx.png",
  "message": "图片上传成功"
}
```

前后端传递图片时统一使用 `image_path` 作为图片定位字段。上传接口返回的 `image_path` 可继续用于 `/api/upload/preview/{image_path}`、`/api/process/run` 和 `/api/analysis/metrics`，不再保留重复图片编号字段。

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
GET /api/library/image/{image_path}
```

图片库的作用：

1. 防止用户没有合适测试图片时无法演示。
2. 便于课程答辩时快速展示固定案例。
3. 便于小组成员调试同一张图片，保证结果一致。
4. 可将之前上传课程资料中的实验图像整理到 `course_samples` 中作为通用测试样例。

---

## 8. 功能模块清单

当前后端算法主目录按 6 类组织，30 个算法已全部实现。

### 8.1 `grayscale_image/` 灰度图像类

| 功能名称     | 文件名                      | 功能说明                                                     | 状态     |
| ------------ | --------------------------- | ------------------------------------------------------------ | -------- |
| 灰度化       | `grayscale.py`              | 将彩色图像转换为灰度图像，作为二值化、边缘检测、频域分析等算法的基础输入 | 已实现 |
| 二值化       | `binary_threshold.py`       | 将灰度图转换为黑白二值图，可支持固定阈值和自适应阈值         | 已实现 |
| 直方图均衡化 | `histogram_equalization.py` | 增强灰度图像整体对比度，使灰度分布更加均衡                   | 已实现 |
| Canny边缘检测 | `edge_detection_basic.py`   | 使用 Canny 算子提取图像中的主要轮廓和边界                    | 已实现 |
| Sobel边缘检测 | `sobel_edge_detection.py` | 使用 Sobel 一阶梯度算子提取 X/Y/综合方向的边缘强度           | 已实现 |
| 腐蚀         | `erode.py`                  | 缩小前景区域，去除小白点或细小噪声                           | 已实现 |
| 膨胀         | `dilate.py`                 | 扩大前景区域，连接断裂区域或增强目标区域                     | 已实现 |
| 开运算       | `open_operation.py`         | 先腐蚀后膨胀，适合去除小噪声                                 | 已实现 |
| 闭运算       | `close_operation.py`        | 先膨胀后腐蚀，适合填补小孔洞、连接断裂区域                   | 已实现 |

---

### 8.2 `color_image/` 彩色图像类

| 功能名称     | 文件名                      | 功能说明                                                     | 状态   |
| ------------ | --------------------------- | ------------------------------------------------------------ | ------ |
| 颜色空间转换 | `color_space_convert.py`    | 将 BGR 图像转换为灰度、HSV 或 Lab 表示，并生成便于展示的可视化结果 | 已实现 |
| 饱和度调整   | `saturation_adjust.py`      | 基于 HSV 色彩空间调整动漫图像的色相、饱和度和明度，使人物和场景颜色更突出 | 已实现 |
| 动漫色彩增强 | `anime_color_enhance.py`    | 综合调整饱和度、对比度、亮度和轻微锐化，突出动漫图像的明快色彩与线条层次 | 已实现 |
| 主色调提取   | `dominant_color_extract.py` | 使用 K-Means 聚类提取动漫图像中的主要颜色，并生成主色调量化可视化结果 | 已实现 |

---

### 8.3 `geometric_transform/` 几何变换类

| 功能名称 | 文件名      | 功能说明                                   | 状态     |
| -------- | ----------- | ------------------------------------------ | -------- |
| 缩放     | `resize.py` | 改变图像尺寸，支持按比例缩放和指定宽高缩放 | 已实现 |
| 旋转     | `rotate.py` | 按指定角度旋转图像，支持边界填充和中心旋转 | 已实现 |
| 翻转     | `flip.py`   | 实现水平翻转、垂直翻转和中心翻转           | 已实现 |

---

### 8.4 `spatial_filter/` 空域滤波类

| 功能名称     | 文件名                 | 功能说明                                                     | 状态     |
| ------------ | ---------------------- | ------------------------------------------------------------ | -------- |
| 均值滤波     | `mean_filter.py`       | 使用邻域平均值进行平滑处理，可降低随机噪声，但会造成一定模糊 | 已实现 |
| 高斯滤波     | `gaussian_filter.py`   | 使用高斯核进行平滑处理，适合去除一般噪声并保留较自然的过渡   | 已实现 |
| 中值滤波     | `median_filter.py`     | 使用邻域中值替代中心像素，对椒盐噪声有较好去除效果           | 已实现 |
| 双边滤波     | `bilateral_filter.py`  | 在平滑图像的同时尽量保留边缘，适合动漫线条图像降噪           | 已实现 |
| 拉普拉斯锐化 | `laplacian_sharpen.py` | 增强图像边缘和细节，使轮廓更清晰                             | 已实现 |

---

### 8.5 `frequency_analysis/` 频域分析类

| 功能名称           | 文件名                  | 功能说明                                                     | 状态     |
| ------------------ | ----------------------- | ------------------------------------------------------------ | -------- |
| 傅里叶变换显示频谱 | `dft_spectrum.py`       | 将图像转换到频域并显示频谱图，用于观察图像低频和高频信息分布 | 已实现 |
| 频谱中心化         | `spectrum_shift.py`     | 对傅里叶频谱进行中心化，将低频成分移动到频谱中心             | 已实现 |
| 幅度谱显示         | `magnitude_spectrum.py` | 计算并显示图像傅里叶变换后的幅度谱                           | 已实现 |

---

### 8.6 `frequency_filter/` 频域滤波类

| 功能名称     | 文件名                  | 功能说明                                             | 状态     |
| ------------ | ----------------------- | ---------------------------------------------------- | -------- |
| 低通滤波     | `low_pass_filter.py`    | 保留低频信息，抑制高频信息，实现图像平滑和降噪       | 已实现 |
| 高通滤波     | `high_pass_filter.py`   | 保留高频信息，抑制低频信息，用于增强边缘和细节       | 已实现 |
| 理想低通滤波 | `ideal_low_pass.py`     | 使用理想圆形掩膜进行低通滤波，效果直观但可能产生振铃 | 已实现 |
| 理想高通滤波 | `ideal_high_pass.py`    | 使用理想圆形掩膜进行高通滤波，用于突出边缘变化       | 已实现 |
| 高斯低通滤波 | `gaussian_low_pass.py`  | 使用高斯频域掩膜进行平滑，过渡更自然                 | 已实现 |
| 高斯高通滤波 | `gaussian_high_pass.py` | 使用高斯频域掩膜增强边缘，减少理想滤波带来的振铃问题 | 已实现 |

---

## 9. 后端 API 清单

### 9.1 核心接口

| 接口 | 方法 | 功能 | 状态 |
|---|---|---|---|
| `/api/health` | GET | 检查后端是否运行 | 已实现 |
| `/api/upload/image` | POST | 上传用户图片，校验后保存到 data/uploads | 已实现 |
| `/api/upload/preview/{image_path}` | GET | 返回已上传图片文件 | 已实现 |
| `/api/library/categories` | GET | 返回内置图片库所有分类及图片数量 | 已实现 |
| `/api/library/images` | GET | 返回指定分类下的图片列表 | 已实现 |
| `/api/library/image/{image_path}` | GET | 返回内置图片库中的图片文件 | 已实现 |
| `/api/algorithms` | GET | 获取全部可用算法模块和参数元数据 | 已实现 |
| `/api/process/run` | POST | 对指定图片执行选择的算法，返回结果/分步/指标 | 已实现 |
| `/api/analysis/metrics` | POST | 计算图片基础指标（均值/标准差/直方图等） | 已实现 |

### 9.2 分类算法子路由

每个算法分类提供独立的子路由，均包含列表查询和执行接口：

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/algorithms/grayscale-image` | GET | 灰度图像类算法列表 |
| `/api/algorithms/grayscale-image/run` | POST | 执行灰度图像类下的指定算法 |
| `/api/algorithms/color-image` | GET | 彩色图像类算法列表 |
| `/api/algorithms/color-image/run` | POST | 执行彩色图像类下的指定算法 |
| `/api/algorithms/geometric-transform` | GET | 几何变换类算法列表 |
| `/api/algorithms/geometric-transform/run` | POST | 执行几何变换类下的指定算法 |
| `/api/algorithms/spatial-filter` | GET | 空域滤波类算法列表 |
| `/api/algorithms/spatial-filter/run` | POST | 执行空域滤波类下的指定算法 |
| `/api/algorithms/frequency-analysis` | GET | 频域分析类算法列表 |
| `/api/algorithms/frequency-analysis/run` | POST | 执行频域分析类下的指定算法 |
| `/api/algorithms/frequency-filter` | GET | 频域滤波类算法列表 |
| `/api/algorithms/frequency-filter/run` | POST | 执行频域滤波类下的指定算法 |

所有 POST 请求体格式与 `/api/process/run` 一致，其中 `module` 字段由路由自动注入，无需前端传递。

### 9.3 后端请求字段约定

1. 图片定位字段统一使用 `image_path`，上传图片对应 `source_type: "upload"`，内置图库图片对应 `source_type: "library"`。
2. `/api/process/run` 和各分类算法执行接口的核心字段为 `source_type`、`image_path`、`module`、`algorithm`、`params`、`return_steps`。
3. `module_display_name`、`algorithm_display_name` 可作为前端展示辅助字段传入，后端不会依赖它们进行算法定位。
4. 算法结果图和步骤图统一以 PNG Base64 Data URL 返回，前端可直接绑定到图片组件。
5. `/api/analysis/metrics` 支持基础统计指标，开启直方图参数后会返回直方图数据。

---

## 10. 前端页面清单

### 已实现

| 页面 | 文件 | 功能 |
|---|---|---|
| 首页 | `HomeView.vue` | 项目介绍、主题说明、快速导航 |
| 登录页 | `LoginView.vue` | 用户登录认证 |
| 个人中心 | `UserProfileView.vue` | 用户信息与设置 |
| 工作区 | `WorkspaceView.vue` | 图像处理主页面（算法选择/处理/结果展示） |

### 待实现

| 页面 | 功能 |
|---|---|
| 图片上传页 | 用户上传图片并预览 |
| 图片库页 | 用户从项目内置图库中选择图片 |
| 动漫识别页 | 主色调提取、线条风格分析、图库相似度匹配 |
| 分步执行页 | 展示算法中间过程，例如傅里叶变换频谱分解 |
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
cd Digital-image-processing-Design
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
uvicorn main:app --reload --host 127.0.0.1 --port 8050
```

浏览器打开：

```text
http://127.0.0.1:8050/docs
```

后端自动化测试：

```powershell
cd backend
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -q
```

当前后端测试集覆盖算法注册、图片上传与预览、处理请求字段、分析指标、运行目录卫生、手动测试脚本约定和 Sobel 边缘检测接口执行等核心路径。

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

## 13. 协作开发分工

本项目多人协作主要集中在后端算法模块，因此建议直接按照 `backend/app/algorithms/` 下的算法目录进行分工。每个成员负责一个算法类别，并完成该目录下对应 `.py` 文件的算法实现、本地测试和结果检查。

| 成员   | 负责算法目录                      | 需要完成的算法文件          | 对应功能           |
| ------ | --------------------------------- | --------------------------- | ------------------ |
| 任可   | `grayscale_image/` 灰度图像类     | `grayscale.py`              | 灰度化             |
| 任可   | `grayscale_image/` 灰度图像类     | `binary_threshold.py`       | 二值化             |
| 任可   | `grayscale_image/` 灰度图像类     | `histogram_equalization.py` | 直方图均衡化       |
| 雍晨   | `grayscale_image/` 灰度图像类     | `edge_detection_basic.py`   | 边缘检测           |
| 雍晨   | `grayscale_image/` 灰度图像类     | `sobel_edge_detection.py`   | Sobel边缘检测      |
| 雍晨   | `grayscale_image/` 灰度图像类     | `erode.py`                  | 腐蚀               |
| 雍晨   | `grayscale_image/` 灰度图像类     | `dilate.py`                 | 膨胀               |
| 雍晨   | `grayscale_image/` 灰度图像类     | `open_operation.py`         | 开运算             |
| 雍晨   | `grayscale_image/` 灰度图像类     | `close_operation.py`        | 闭运算             |
| 毛思涵 | `color_image/` 彩色图像类         | `color_space_convert.py`    | 颜色空间转换       |
| 毛思涵 | `color_image/` 彩色图像类         | `saturation_adjust.py`      | 饱和度调整         |
| 毛思涵 | `color_image/` 彩色图像类         | `anime_color_enhance.py`    | 动漫色彩增强       |
| 毛思涵 | `color_image/` 彩色图像类         | `dominant_color_extract.py` | 主色调提取         |
| 任可   | `geometric_transform/` 几何变换类 | `resize.py`                 | 缩放               |
| 任可   | `geometric_transform/` 几何变换类 | `rotate.py`                 | 旋转               |
| 任可   | `geometric_transform/` 几何变换类 | `flip.py`                   | 翻转               |
| 周恩丞 | `spatial_filter/` 空域滤波类      | `mean_filter.py`            | 均值滤波           |
| 周恩丞 | `spatial_filter/` 空域滤波类      | `gaussian_filter.py`        | 高斯滤波           |
| 周恩丞 | `spatial_filter/` 空域滤波类      | `median_filter.py`          | 中值滤波           |
| 周恩丞 | `spatial_filter/` 空域滤波类      | `bilateral_filter.py`       | 双边滤波           |
| 周恩丞 | `spatial_filter/` 空域滤波类      | `laplacian_sharpen.py`      | 拉普拉斯锐化       |
| 高艳阳 | `frequency_analysis/` 频域分析类  | `dft_spectrum.py`           | 傅里叶变换显示频谱 |
| 高艳阳 | `frequency_analysis/` 频域分析类  | `spectrum_shift.py`         | 频谱中心化         |
| 高艳阳 | `frequency_analysis/` 频域分析类  | `magnitude_spectrum.py`     | 幅度谱显示         |
| 高艳阳 | `frequency_filter/` 频域滤波类    | `low_pass_filter.py`        | 低通滤波           |
| 高艳阳 | `frequency_filter/` 频域滤波类    | `high_pass_filter.py`       | 高通滤波           |
| 高艳阳 | `frequency_filter/` 频域滤波类    | `ideal_low_pass.py`         | 理想低通滤波       |
| 高艳阳 | `frequency_filter/` 频域滤波类    | `ideal_high_pass.py`        | 理想高通滤波       |
| 高艳阳 | `frequency_filter/` 频域滤波类    | `gaussian_low_pass.py`      | 高斯低通滤波       |
| 高艳阳 | `frequency_filter/` 频域滤波类    | `gaussian_high_pass.py`     | 高斯高通滤波       |

每个成员提交代码时必须保证：

1. 对应算法文件第一行有中文功能说明。
2. 每个算法文件包含 `ALGORITHM_META`。
3. 每个算法文件提供统一的 `run(image, params)` 接口。
4. 返回结果必须包含 `result`、`steps`、`metrics`、`analysis`。
5. 不在算法文件中使用 `cv2.imshow()`。
6. 不使用本机绝对路径。
7. 使用 `backend/tests/manual_test_algorithm.py` 完成初学者三路径本地测试；需要批量参数或复杂配置时再使用 `backend/tests/manual_test_algorithm_advanced.py`。
8. 测试通过后，确认 `backend/data/test_outputs/` 中能够生成结果图片，运行产物不要提交到仓库。

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

### 14.6 后端文档与运行产物

1. 本次后端更新记录见 `docs/backend-update-doc/CHANGELOG05.md`。
2. 算法完善提示词已归档到 `docs/prompts/algorithm_improvement_prompts_7_models/`，不再放在后端算法源码目录中。
3. `backend/data/uploads/`、`backend/data/outputs/`、`backend/data/test_outputs/` 是运行时目录，只保留 `.gitkeep` 占位文件。
4. 后端测试建议使用 `PYTHONDONTWRITEBYTECODE=1`，避免重新生成 `__pycache__` 和 `.pyc` 文件。

---

## 15. 课程报告对应关系

| 报告章节 | 本项目对应内容 |
|---|---|
| 第 1 章 绪论 | 动漫图像处理背景、意义、项目目标、系统框架 |
| 第 2 章 相关方法 | OpenCV、FastAPI、Vue、数字图像处理算法原理 |
| 第 3 章 算法介绍、程序设计、运行结果展示及分析 | 各算法模块、分步结果、处理前后对比、指标分析 |
| 第 4 章 Web 网页开发 | Vue 页面设计、FastAPI 接口、前后端分离、图片上传与图库选择、即时算法处理 |

---

## 16. 开发优先级与实现状态

### P0：必须完成

- [x] 1. Vue + FastAPI 前后端连通（Axios 已封装，页面框架与路由已搭建）
- [x] 2. 图片上传（`POST /api/upload/image`）
- [x] 3. 图片库选择（`GET /api/library/categories` 等）
- [x] 4. 算法列表由后端动态返回（`GET /api/algorithms`）
- [-] 5. 用户选择算法后立即处理并显示结果图（后端已实现，WorkspaceView 待对接算法 API）
- [x] 6. 灰度化、二值化、直方图均衡化
- [x] 7. 均值滤波、高斯滤波、中值滤波
- [x] 8. Canny 边缘检测、Sobel 边缘检测
- [x] 9. 腐蚀、膨胀、开运算、闭运算
- [x] 10. DFT 频谱图与简单低通/高通滤波

### P1：建议完成

- [x] 1. 动漫主色调提取
- [ ] 2. 动漫线条风格分析
- [ ] 3. 动漫图库相似度匹配
- [ ] 4. CLAHE
- [x] 5. 双边滤波
- [x] 6. Laplacian 锐化
- [ ] 7. Hough 直线检测
- [x] 8. 结果指标统计（`POST /api/analysis/metrics`）

### P2：有时间再做

- [ ] 1. 维纳滤波
- [ ] 2. 图像修复
- [ ] 3. 同态滤波
- [ ] 4. 动漫人脸检测
- [ ] 5. 批量处理
- [ ] 6. 报告一键导出
