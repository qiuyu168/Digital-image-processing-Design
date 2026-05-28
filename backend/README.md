# 后端 README

> 更新日期：2026-05-28

本文档根据当前本地项目文件扫描生成，面向后端维护者和前端联调人员。后端运行缓存目录 `.pytest_cache/` 不属于业务文件，本文不作为功能文件记录。

---

## 1. 后端概览

后端使用 FastAPI 提供图像上传、内置图库、算法列表、算法执行、图像指标分析等接口。算法统一放在 `app/algorithms/`，每个算法文件通过 `ALGORITHM_META` 暴露前端参数元数据，并通过 `run(image, params)` 执行处理。

默认本地服务地址：

```text
http://127.0.0.1:8050
```

接口文档地址：

```text
http://127.0.0.1:8050/docs
```

前端开发服务器默认允许来源：

```text
http://localhost:5173
http://127.0.0.1:5173
```

---

## 2. 目录结构与文件功能

### 2.1 根目录

| 文件 | 功能 |
|---|---|
| `main.py` | FastAPI 应用入口，创建 `app`，注册 CORS、数据目录初始化、全部 API 路由和统一异常处理。 |
| `README.md` | 当前后端说明文档，包含文件功能、前端使用方式和环境配置。 |

### 2.2 `app/` 应用包

| 文件 | 功能 |
|---|---|
| `app/__init__.py` | 标记 `app` 为 Python 包。 |
| `app/analysis/__init__.py` | 标记 `analysis` 为 Python 包（扩展预留）。 |

### 2.3 `app/core/` 核心工具

| 文件 | 功能 |
|---|---|
| `app/core/__init__.py` | 标记 `core` 为 Python 包。 |
| `app/core/config.py` | 定义后端根目录、数据目录、上传目录、图库目录、输出目录和测试目录，并提供 `ensure_data_directories()` 自动创建运行目录。 |
| `app/core/cors.py` | 配置跨域来源，允许 Vite 前端本地开发地址访问后端。 |
| `app/core/image_codec.py` | 在 OpenCV 图像数组和前端 PNG Base64 Data URL 之间转换，并规范化灰度、BGR、BGRA、float、bool 图像。 |
| `app/core/image_io.py` | 使用 OpenCV 编解码方式读写图片，兼容 Windows 中文路径。 |
| `app/core/upload_config.py` | 定义上传文件格式、MIME 类型、文件大小、分辨率限制。 |
| `app/core/upload_validator.py` | 校验上传图片的扩展名、MIME、大小、解码结果、分辨率和通道格式。 |

### 2.4 `app/schemas/` 数据模型

| 文件 | 功能 |
|---|---|
| `app/schemas/__init__.py` | 标记 `schemas` 为 Python 包。 |
| `app/schemas/algorithm_schema.py` | 定义算法参数、算法元数据、算法分类和算法列表响应模型。 |
| `app/schemas/image_schema.py` | 定义上传图片响应、图库分类和图库图片信息模型。 |
| `app/schemas/process_schema.py` | 定义统一算法处理请求、分类算法处理请求、步骤图和处理响应模型。图片定位字段统一为 `image_path`。 |
| `app/schemas/response_schema.py` | 定义通用基础响应模型 `BaseResponse`。 |

### 2.5 `app/services/` 业务服务

| 文件 | 功能 |
|---|---|
| `app/services/__init__.py` | 标记 `services` 为 Python 包。 |
| `app/services/algorithm_registry.py` | 维护九大算法分类、算法顺序和中文名称，动态导入算法文件并生成前端可用的算法元数据。 |
| `app/services/analysis_service.py` | 计算图像宽高、通道数、数据类型、均值、标准差、最大最小值和可选直方图。 |
| `app/services/image_store.py` | 管理上传图片保存、上传图片预览路径、图库分类列表、图库图片列表、图片来源读取和路径安全校验。 |
| `app/services/process_service.py` | 加载图片、调度算法 `run(image, params)`、校验算法返回结构，并组装前端处理响应。 |
| `app/services/step_service.py` | 将算法步骤图列表转换为前端可显示的 PNG Base64 Data URL。 |

### 2.6 `app/api/` API 路由

| 文件 | 功能 |
|---|---|
| `app/api/__init__.py` | 标记 `api` 为 Python 包。 |
| `app/api/health.py` | 提供 `GET /api/health` 健康检查接口。 |
| `app/api/upload.py` | 提供 `POST /api/upload/image` 图片上传接口和 `GET /api/upload/preview/{image_path}` 上传图片预览接口。 |
| `app/api/library.py` | 提供内置图库分类、图片列表和图片文件读取接口。 |
| `app/api/algorithms.py` | 提供 `GET /api/algorithms`，返回全部算法分类和参数元数据。 |
| `app/api/process.py` | 提供 `POST /api/process/run`，按 `module` 与 `algorithm` 执行算法。 |
| `app/api/analysis.py` | 提供 `POST /api/analysis/metrics`，返回图片基础指标和可选直方图。 |

### 2.7 `app/api/algorithm_modules/` 分类算法路由

| 文件 | 功能 |
|---|---|
| `app/api/algorithm_modules/__init__.py` | 标记分类算法路由目录为 Python 包。 |
| `app/api/algorithm_modules/common.py` | 定义九类算法名称、分类中文名、分类算法查询、分类算法运行和算法归属校验逻辑。 |
| `app/api/algorithm_modules/basic_operation.py` | 提供图像基本运算类算法列表和分类运行接口。 |
| `app/api/algorithm_modules/grayscale_image.py` | 提供灰度图像类算法列表和分类运行接口。 |
| `app/api/algorithm_modules/color_image.py` | 提供彩色图像类算法列表和分类运行接口。 |
| `app/api/algorithm_modules/geometric_transform.py` | 提供几何变换类算法列表和分类运行接口。 |
| `app/api/algorithm_modules/spatial_filter.py` | 提供空域滤波类算法列表和分类运行接口。 |
| `app/api/algorithm_modules/frequency_analysis.py` | 提供频域分析类算法列表和分类运行接口。 |
| `app/api/algorithm_modules/frequency_filter.py` | 提供频域滤波类算法列表和分类运行接口。 |
| `app/api/algorithm_modules/image_restoration.py` | 提供图像复原类算法列表和分类运行接口。 |
| `app/api/algorithm_modules/edge_shape_detection.py` | 提供边缘与形状检测类算法列表和分类运行接口。 |

分类路由统一格式：

| 分类 | 列表接口 | 执行接口 |
|---|---|---|
| 图像基本运算类 | `GET /api/algorithms/basic-operation` | `POST /api/algorithms/basic-operation/run` |
| 灰度图像类 | `GET /api/algorithms/grayscale-image` | `POST /api/algorithms/grayscale-image/run` |
| 彩色图像类 | `GET /api/algorithms/color-image` | `POST /api/algorithms/color-image/run` |
| 几何变换类 | `GET /api/algorithms/geometric-transform` | `POST /api/algorithms/geometric-transform/run` |
| 空域滤波类 | `GET /api/algorithms/spatial-filter` | `POST /api/algorithms/spatial-filter/run` |
| 频域分析类 | `GET /api/algorithms/frequency-analysis` | `POST /api/algorithms/frequency-analysis/run` |
| 频域滤波类 | `GET /api/algorithms/frequency-filter` | `POST /api/algorithms/frequency-filter/run` |
| 图像复原类 | `GET /api/algorithms/image-restoration` | `POST /api/algorithms/image-restoration/run` |
| 边缘与形状检测类 | `GET /api/algorithms/edge-shape-detection` | `POST /api/algorithms/edge-shape-detection/run` |

### 2.8 `app/algorithms/` 算法文件

| 文件 | 功能 |
|---|---|
| `app/algorithms/__init__.py` | 标记算法根目录为 Python 包。 |
| `app/algorithms/common.py` | 算法共享工具函数（图像格式转换、参数提取、频域工具等）。 |
| `app/algorithms/算法框架填写说明.md` | 算法文件编写规范，说明 `ALGORITHM_META` 和 `run(image, params)` 要求。 |
| `app/algorithms/分工文档.md` | 小组算法开发分工与提交要求。 |

#### 图像基本运算类 `app/algorithms/basic_operation/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记图像基本运算类目录为 Python 包。 | - |
| `add_operation.py` | 图像加法，两张图像加权相加。 | `alpha`、`beta`、`gamma` |
| `subtract_operation.py` | 图像减法，逐像素差值计算。 | `scale` |
| `multiply_operation.py` | 图像乘法，归一化相乘增强。 | `scale` |
| `divide_operation.py` | 图像除法，第一张除以第二张。 | `scale`、`epsilon` |
| `and_operation.py` | 按位与运算，掩膜提取。 | 无 |
| `or_operation.py` | 按位或运算，区域合并。 | 无 |
| `not_operation.py` | 按位取反，负片/反色效果。 | 无 |
| `xor_operation.py` | 按位异或，差异高亮。 | 无 |

#### 灰度图像类 `app/algorithms/grayscale_image/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记灰度图像类目录为 Python 包。 | - |
| `linear_gray_transform.py` | 线性灰度变换，g = alpha*f + beta。 | `alpha`、`beta` |
| `gamma_correction.py` | 伽马校正，幂律变换增强暗部或亮部。 | `gamma` |
| `log_transform.py` | 对数变换，动态范围压缩。 | `gain` |
| `exponential_transform.py` | 指数变换，动态范围扩展。 | `gain`、`base` |
| `negative_transform.py` | 负片变换，灰度反转。 | `keep_color` |
| `grayscale.py` | 灰度化，将 BGR 彩色图像转换为单通道灰度图。 | 无 |
| `binary_threshold.py` | 二值化，按固定阈值转换黑白图。 | `threshold` |
| `histogram_equalization.py` | 直方图均衡化，提升低对比图像明暗层次。 | 无 |
| `clahe_equalization.py` | 对比度受限自适应直方图均衡化，增强局部细节。 | `clip_limit`、`tile_grid_size` |
| `histogram_matching.py` | 直方图匹配，根据 `second_image_path` 参考图规定化灰度分布。 | `strength`、`color_mode` |
| `erode.py` | 腐蚀，缩小前景区域并去除细小白色噪声。 | `kernel_size`、`threshold` |
| `dilate.py` | 膨胀，扩大白色前景并连接断裂结构。 | `kernel_size`、`threshold` |
| `open_operation.py` | 开运算，先腐蚀后膨胀以去除小白点噪声。 | `kernel_size`、`threshold` |
| `close_operation.py` | 闭运算，先膨胀后腐蚀以填补孔洞和连接断裂区域。 | `kernel_size`、`threshold` |

#### 彩色图像类 `app/algorithms/color_image/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记彩色图像类目录为 Python 包。 | - |
| `color_space_convert.py` | 颜色空间转换，支持灰度、HSV、Lab 等展示。 | `target_space` |
| `saturation_adjust.py` | 饱和度调整，基于 HSV 调整色相、饱和度和明度。 | `hue_shift`、`saturation_factor`、`value_factor` |
| `anime_color_enhance.py` | 动漫色彩增强，调整饱和度、对比度、亮度和锐化。 | `saturation_factor`、`contrast`、`brightness`、`sharpen_strength` |
| `dominant_color_extract.py` | 主色调提取，使用 K-Means 提取主要颜色。 | `color_count` |
| `region_mosaic.py` | 对指定比例区域进行马赛克处理。 | `x_ratio`、`y_ratio`、`width_ratio`、`height_ratio`、`block_size` |
| `color_comprehensive_processing.py` | 彩色图像综合增强入口。 | `brightness`、`contrast`、`saturation`、`hue_shift`、`sharpen_strength` |

#### 几何变换类 `app/algorithms/geometric_transform/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记几何变换类目录为 Python 包。 | - |
| `resize.py` | 图像缩放。 | `scale` |
| `rotate.py` | 图像旋转，支持任意比例旋转中心。 | `angle`、`scale`、`center_x_ratio`、`center_y_ratio` |
| `flip.py` | 图像翻转。 | `flip_code` |
| `translate.py` | 图像平移。 | `tx`、`ty`、`border_mode` |
| `affine_transform.py` | 仿射变换。 | `dx1`、`dy1`、`dx2`、`dy2`、`dx3`、`dy3` |
| `perspective_transform.py` | 投影变换。 | `top_left_x`、`top_left_y`、`top_right_x`、`top_right_y`、`bottom_right_x`、`bottom_right_y`、`bottom_left_x`、`bottom_left_y` |

#### 空域滤波类 `app/algorithms/spatial_filter/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记空域滤波类目录为 Python 包。 | - |
| `mean_filter.py` | 均值滤波，使用邻域平均值平滑图像。 | `kernel_size` |
| `gaussian_filter.py` | 高斯滤波，使用高斯核进行自然平滑。 | `kernel_size`、`sigma` |
| `median_filter.py` | 中值滤波，抑制椒盐噪声。 | `kernel_size` |
| `bilateral_filter.py` | 双边滤波，在平滑同时尽量保留边缘。 | `diameter`、`sigma_color`、`sigma_space` |
| `laplacian_sharpen.py` | 拉普拉斯锐化，增强边缘和细节。 | `amount` |
| `statistical_order_filter.py` | 统计排序滤波统一入口。 | `kernel_size`、`mode`、`percentile` |
| `max_filter.py` | 最大值滤波。 | `kernel_size` |
| `min_filter.py` | 最小值滤波。 | `kernel_size` |
| `adaptive_median_filter.py` | 自适应中值滤波。 | `initial_kernel_size`、`max_kernel_size` |
| `unsharp_masking.py` | USM 锐化。 | `amount`、`radius`、`threshold` |
| `add_noise.py` | 添加噪声，用于退化模拟和滤波测试。 | `noise_type`、`amount`、`mean`、`sigma` |

#### 频域分析类 `app/algorithms/frequency_analysis/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记频域分析类目录为 Python 包。 | - |
| `dft_spectrum.py` | 傅里叶频谱显示。 | 无 |
| `spectrum_shift.py` | 频谱中心化。 | 无 |
| `magnitude_spectrum.py` | 幅度谱显示。 | `shift_center` |

#### 频域滤波类 `app/algorithms/frequency_filter/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记频域滤波类目录为 Python 包。 | - |
| `low_pass_filter.py` | 低通滤波，保留低频信息并抑制高频信息。 | `radius` |
| `high_pass_filter.py` | 高通滤波，保留高频信息并增强边缘细节。 | `radius` |
| `ideal_low_pass.py` | 理想低通滤波。 | `radius` |
| `ideal_high_pass.py` | 理想高通滤波。 | `radius` |
| `gaussian_low_pass.py` | 高斯低通滤波。 | `radius` |
| `gaussian_high_pass.py` | 高斯高通滤波。 | `radius` |
| `butterworth_low_pass.py` | 巴特沃斯低通滤波。 | `cutoff`、`order` |
| `butterworth_high_pass.py` | 巴特沃斯高通滤波。 | `cutoff`、`order` |
| `frequency_laplacian_sharpen.py` | 频域拉普拉斯锐化。 | `amount` |
| `homomorphic_filter.py` | 同态滤波。 | `gamma_low`、`gamma_high`、`cutoff`、`order` |

#### 图像复原类 `app/algorithms/image_restoration/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记图像复原类目录为 Python 包。 | - |
| `defocus_blur_simulation.py` | 散焦模糊模拟，使用圆盘 PSF。 | `radius` |
| `lens_distortion_blur_simulation.py` | 镜头畸变模糊模拟，径向畸变+模糊。 | `distortion_strength`、`blur_kernel_size` |
| `motion_blur_simulation.py` | 运动模糊模拟，线性 PSF 匀速直线运动。 | `length`、`angle` |
| `atmospheric_turbulence_blur_simulation.py` | 大气湍流模糊模拟，频域湍流传递函数。 | `k` |
| `inverse_filter_restoration.py` | 逆滤波复原，频域直接反卷积。 | `k`、`epsilon` |
| `windowed_inverse_filter_restoration.py` | 加窗逆滤波复原，限制高频噪声放大。 | `k`、`epsilon`、`window_radius` |
| `wiener_filter_restoration.py` | 维纳滤波复原，信噪比自适应最优滤波。 | `k`、`noise_power` |
| `constrained_least_squares_restoration.py` | 约束最小二乘复原，拉普拉斯正则化。 | `k`、`gamma` |

#### 边缘与形状检测类 `app/algorithms/edge_shape_detection/`

| 文件 | 算法 | 参数 |
|---|---|---|
| `__init__.py` | 标记边缘与形状检测类目录为 Python 包。 | - |
| `basic_edge_detection.py` | 基础边缘检测统一入口。 | `method`、`threshold1`、`threshold2`、`kernel_size` |
| `canny_edge_detection.py` | Canny 边缘检测。 | `threshold1`、`threshold2`、`blur_size` |
| `sobel_edge_detection.py` | Sobel 边缘检测。 | `direction`、`kernel_size`、`scale`、`delta` |
| `roberts_cross.py` | Roberts 交叉算子边缘检测。 | `scale` |
| `prewitt_edge_detection.py` | Prewitt 边缘检测。 | `direction`、`kernel_size` |
| `scharr_edge_detection.py` | Scharr 边缘检测。 | `direction`、`scale` |
| `log_edge_detection.py` | LoG 边缘检测。 | `blur_size`、`sigma`、`threshold` |
| `hough_shape_detection.py` | Hough 直线/圆形检测。 | `shape_type`、`threshold`、`min_line_length`、`max_line_gap` |
| `corner_detection.py` | Harris / Shi-Tomasi 角点检测。 | `method`、`max_corners`、`quality_level`、`min_distance` |

### 2.9 `data/` 数据目录

| 文件或目录 | 功能 |
|---|---|
| `data/image_limit.md` | 图片上传限制说明。 |
| `data/uploads/.gitkeep` | 保留用户上传目录。实际上传图片是运行产物，不提交。 |
| `data/outputs/.gitkeep` | 保留算法输出目录。实际输出图片是运行产物，不提交。 |
| `data/test_images/.gitkeep` | 保留本地测试输入图片目录。 |
| `data/test_outputs/.gitkeep` | 保留本地测试输出目录。实际测试结果图片不提交。 |
| `data/library/anime_avatar/.gitkeep` | 保留动漫头像图库分类目录。 |
| `data/library/anime_character/.gitkeep` | 保留动漫人物图库分类目录。 |
| `data/library/anime_scene/.gitkeep` | 保留动漫场景图库分类目录。 |
| `data/library/course_samples/.gitkeep` | 保留课程示例图库分类目录。 |
| `data/library/other/.gitkeep` | 保留其他图库分类目录。 |

### 2.10 `tests/` 测试文件

| 文件 | 功能 |
|---|---|
| `tests/README.md` | 后端本地算法测试工具说明。 |
| `tests/算法测试脚本使用说明文档.md` | 简化版手动测试脚本的路径配置示例。 |
| `tests/manual_test_algorithm.py` | 初学者三路径手动测试脚本，只需配置输入图、输出图、算法导入路径。 |
| `tests/manual_test_algorithm_advanced.py` | 高级手动测试脚本，支持 `--config` 配置文件、`--input` 输入图、`--params` 临时参数和 `--second-input` 第二张图。 |
| `tests/test_algorithm_completeness.py` | 自动检查所有算法文件是否可导入、元数据是否完整、`run` 是否可执行。 |
| `tests/test_backend_framework.py` | 后端框架测试，覆盖上传校验、接口联调、算法注册、分析指标、schema 和目录卫生。 |
| `tests/sample_test_configs/add_operation_example.json` | 图像加法测试配置示例。 |
| `tests/sample_test_configs/binary_threshold_example.json` | 二值化测试配置示例。 |
| `tests/sample_test_configs/canny_example.json` | Canny 边缘检测测试配置示例。 |
| `tests/sample_test_configs/dft_spectrum_example.json` | DFT 频谱测试配置示例。 |
| `tests/sample_test_configs/gamma_correction_example.json` | 伽马校正测试配置示例。 |
| `tests/sample_test_configs/gaussian_filter_example.json` | 高斯滤波测试配置示例。 |
| `tests/sample_test_configs/grayscale_example.json` | 灰度化测试配置示例。 |
| `tests/sample_test_configs/ideal_high_pass_example.json` | 理想高通滤波测试配置示例。 |
| `tests/sample_test_configs/ideal_low_pass_example.json` | 理想低通滤波测试配置示例。 |
| `tests/sample_test_configs/motion_blur_simulation_example.json` | 运动模糊模拟测试配置示例。 |
| `tests/sample_test_configs/saturation_adjust_example.json` | 饱和度调整测试配置示例。 |
| `tests/sample_test_configs/sobel_edge_detection_example.json` | Sobel 边缘检测测试配置示例。 |
| `tests/sample_test_configs/wiener_filter_restoration_example.json` | 维纳滤波复原测试配置示例。 |

---

## 3. 前端联调手册

### 3.1 推荐联调配置

前端 `frontend/src/api/http.js` 使用 Axios。建议前端在 `.env.development` 中写入：

```env
VITE_API_BASE_URL=http://127.0.0.1:8050
```

然后请求路径继续使用后端完整 API 路径，例如：

```js
const data = await http.get('/api/health')
```

如果不配置该环境变量，当前前端默认 `baseURL` 为 `/api`，需要额外配置 Vite 代理或把调用路径改成不重复的相对路径。

### 3.2 通用响应规则

后端成功响应通常包含：

```json
{ "success": true }
```

后端错误响应统一为：

```json
{ "success": false, "message": "错误说明" }
```

请求体验证失败会返回：

```json
{ "success": false, "message": "请求参数校验失败", "errors": [] }
```

前端应优先读取 `message` 做错误提示。

### 3.3 健康检查

```http
GET /api/health
```

返回示例：

```json
{ "success": true, "message": "后端服务运行正常" }
```

### 3.4 上传图片

```http
POST /api/upload/image
Content-Type: multipart/form-data
```

前端示例：

```js
const formData = new FormData()
formData.append('file', file, file.name)

const data = await http.post('/api/upload/image', formData)
const imagePath = data.image_path
const previewUrl = data.preview_url
```

返回示例：

```json
{
  "success": true,
  "image_path": "upload_6f4f0b8d2a0c4f31a79d5d9a9a4b8e11.png",
  "filename": "upload_6f4f0b8d2a0c4f31a79d5d9a9a4b8e11.png",
  "width": 800,
  "height": 600,
  "preview_url": "/api/upload/preview/upload_6f4f0b8d2a0c4f31a79d5d9a9a4b8e11.png",
  "message": "图片上传成功"
}
```

前端后续处理图片时必须保存并传递 `image_path`。不要再使用旧的重复图片编号字段。

上传限制：

| 项目 | 规则 |
|---|---|
| 扩展名 | `jpg`、`jpeg`、`png`、`bmp`、`webp`、`tif`、`tiff` |
| MIME | `image/jpeg`、`image/png`、`image/bmp`、`image/webp`、`image/tiff` |
| 文件大小 | 10KB 到 5MB |
| 分辨率 | 最小 128 x 128，最大 4096 x 4096 |

### 3.5 预览上传图片

```http
GET /api/upload/preview/{image_path}
```

`preview_url` 已由上传接口返回，前端可以直接将完整地址绑定到图片组件。若 `preview_url` 是 `/api/...` 相对路径，拼接规则应以 `VITE_API_BASE_URL` 为准。

### 3.6 使用内置图库

获取图库分类：

```http
GET /api/library/categories
```

获取分类下图片：

```http
GET /api/library/images?category=anime_character
```

获取图库图片文件：

```http
GET /api/library/image/{image_path}
```

图库图片列表会返回 `image_path` 和 `preview_url`。使用图库图片执行算法时，`source_type` 应传 `"library"`。

图库分类：

| category | 中文名 |
|---|---|
| `anime_character` | 动漫人物图像 |
| `anime_scene` | 动漫场景图像 |
| `anime_avatar` | 动漫头像图像 |
| `course_samples` | 课程示例图像 |
| `other` | 其他图像 |

### 3.7 获取算法列表和渲染参数面板

```http
GET /api/algorithms
```

返回结构：

```json
{
  "success": true,
  "modules": [
    {
      "module": "grayscale_image",
      "display_name": "灰度图像类",
      "algorithms": [
        {
          "module": "grayscale_image",
          "module_display_name": "灰度图像类",
          "name": "binary_threshold",
          "display_name": "二值化",
          "description": "按固定阈值转换黑白图",
          "params": {
            "threshold": {
              "type": "int",
              "default": 128,
              "min": 0,
              "max": 255,
              "step": 1,
              "label": "阈值",
              "component": "slider"
            }
          }
        }
      ]
    }
  ],
  "algorithms": []
}
```

前端参数渲染建议：

| 字段 | 用途 |
|---|---|
| `type` | 参数类型，常见值为 `int`、`float`、`odd_int`、`select`、`bool`。 |
| `component` | 推荐控件，常见值为 `slider`、`select`、`switch`、`input`。 |
| `default` | 初始值。 |
| `min`、`max`、`step` | 数值控件边界和步长。 |
| `label` | 前端显示名称。 |
| `options` | 下拉选项。 |

### 3.8 执行算法

统一处理接口：

```http
POST /api/process/run
```

请求示例：

```json
{
  "source_type": "upload",
  "image_path": "upload_6f4f0b8d2a0c4f31a79d5d9a9a4b8e11.png",
  "module": "edge_shape_detection",
  "algorithm": "canny_edge_detection",
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
  "module": "edge_shape_detection",
  "module_display_name": "边缘与形状检测类",
  "algorithm": "canny_edge_detection",
  "algorithm_display_name": "Canny边缘检测",
  "result_image": "data:image/png;base64,...",
  "steps": [
    { "name": "灰度化", "image": "data:image/png;base64,..." }
  ],
  "metrics": {},
  "analysis": "算法分析文本"
}
```

前端展示规则：

1. `result_image` 可直接作为 `<img>` 的 `src`。
2. `steps` 中每个 `image` 也是 PNG Base64 Data URL。
3. 不需要前端再做 BGR/RGB 转换。
4. `return_steps` 传 `false` 时，后端只返回结果图，`steps` 为空数组。

分类执行接口也可以使用，例如：

```http
POST /api/algorithms/edge-shape-detection/run
```

分类执行接口请求体不需要传 `module`，后端会根据路由自动注入分类。

### 3.9 计算图片指标

```http
POST /api/analysis/metrics
```

请求示例：

```json
{
  "source_type": "upload",
  "image_path": "upload_6f4f0b8d2a0c4f31a79d5d9a9a4b8e11.png",
  "include_histogram": true
}
```

返回内容包括：

| 字段 | 说明 |
|---|---|
| `width`、`height` | 图像宽高。 |
| `channels` | 通道数。 |
| `dtype` | 图像数组类型。 |
| `mean`、`std` | 像素均值和标准差。 |
| `min`、`max` | 像素最小值和最大值。 |
| `histogram` | 开启 `include_histogram` 后返回 256 bins 通道直方图。 |

### 3.10 前端联调顺序建议

1. `GET /api/health` 确认后端可访问。
2. `GET /api/algorithms` 渲染左侧算法分类、算法列表和参数面板。
3. `POST /api/upload/image` 上传图片，保存 `image_path`。
4. 使用 `preview_url` 展示上传图片预览。
5. `POST /api/process/run` 传入 `source_type`、`image_path`、`module`、`algorithm`、`params`。
6. 用 `result_image` 展示处理结果，用 `steps` 展示分步过程。
7. 需要统计面板时调用 `POST /api/analysis/metrics`。

---

## 4. 环境配置

### 4.1 环境要求

| 项目 | 要求 |
|---|---|
| 操作系统 | Windows 11 |
| Python | Python >= 3.11，推荐 Python 3.11 或 3.12 |
| 虚拟环境 | `venv` |
| 后端端口 | `8050` |
| 前端开发端口 | `5173` |

### 4.2 创建并激活虚拟环境

在项目根目录执行：

```powershell
python -m venv .venv
.venv\Scripts\activate
```

升级 pip：

```powershell
python -m pip install --upgrade pip
```

安装依赖：

```powershell
pip install -r requirements.txt
```

如果下载慢，可以使用清华源：

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4.3 启动后端服务

```powershell
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8050
```

启动后访问：

```text
http://127.0.0.1:8050/docs
```

### 4.4 运行测试

建议使用以下命令避免生成 `__pycache__` 和 `.pyc` 文件：

```powershell
cd backend
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -q
```

### 4.5 本地手动测试单个算法

编辑：

```text
backend/tests/manual_test_algorithm.py
```

只需要改 3 个路径：

```python
INPUT_IMAGE_PATH = "data/test_images/anime_test.png"
OUTPUT_IMAGE_PATH = "data/test_outputs/result.png"
ALGORITHM_IMPORT_PATH = "app.algorithms.color_image.saturation_adjust"
```

运行：

```powershell
cd backend
python tests/manual_test_algorithm.py
```

高级配置测试使用：

```powershell
python tests/manual_test_algorithm_advanced.py --config tests/sample_test_configs/canny_example.json
```

### 4.6 运行目录和提交规则

以下目录是运行时目录，只提交 `.gitkeep`：

```text
backend/data/uploads/
backend/data/outputs/
backend/data/test_outputs/
```

以下内容不要提交：

```text
__pycache__/
*.pyc
.pytest_cache/
backend/data/uploads/*
backend/data/outputs/*
backend/data/test_outputs/*
```

### 4.7 依赖说明

依赖文件在项目根目录：

```text
requirements.txt
```

主要依赖：

| 依赖 | 用途 |
|---|---|
| `fastapi` | API 服务框架。 |
| `uvicorn[standard]` | 本地 ASGI 服务。 |
| `python-multipart` | 解析图片上传表单。 |
| `pydantic`、`pydantic-settings` | 请求与响应数据校验。 |
| `opencv-contrib-python` | 核心图像处理。 |
| `numpy` | 图像数组计算。 |
| `Pillow`、`imageio`、`tifffile` | 图片格式兼容。 |
| `scipy`、`scikit-image`、`scikit-learn` | 算法和轻量特征分析支持。 |
| `matplotlib`、`pandas`、`plotly` | 统计、图表和结果分析。 |
| `pytest`、`httpx` | 后端测试。 |
| `ruff` | 代码格式和静态检查。 |

---

## 5. 开发约定

### 5.1 新增或修改算法时的后端约定

1. 算法文件必须放在 `app/algorithms/<module>/` 下。
2. 算法名必须加入 `app/services/algorithm_registry.py` 与 `app/api/algorithm_modules/common.py` 对应分类列表。
3. 如需新增算法分类子路由，在 `app/api/algorithm_modules/` 下添加对应文件并在 `main.py` 注册。
4. 每个算法文件必须提供 `ALGORITHM_META`。
5. 每个算法文件必须提供 `run(image, params)`。
6. `run` 返回值必须是包含 `result`、`steps`、`metrics`、`analysis` 的 `dict`。
7. `result` 和每个步骤 `image` 必须是 `numpy.ndarray`。
8. 后端统一把结果图编码为 PNG Base64，算法内部不要返回文件路径。
9. 不要在算法代码中使用 `cv2.imshow()`，不要写个人电脑绝对路径。

### 5.2 算法文件规范模板

```python
# 本文件用于实现 xxx 功能

ALGORITHM_META = {
    "module": "模块名",
    "name": "算法名",
    "display_name": "中文显示名",
    "description": "功能描述",
    "params": { ... }
}

def run(image: np.ndarray, params: dict | None = None) -> dict:
    return {
        "result": np.ndarray,
        "steps": [{ "name": "...", "image": np.ndarray }],
        "metrics": { ... },
        "analysis": "文字分析"
    }
```
