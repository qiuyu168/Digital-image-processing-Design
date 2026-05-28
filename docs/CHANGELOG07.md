# CHANGELOG07 - Backend Algorithm Classification Refactor

更新时间：2026-05-28

## 更新范围

本次更新完成后端算法分类重构和缺失算法补齐，后端活动分类调整为最终 9 类：

```text
basic_operation
grayscale_image
color_image
geometric_transform
spatial_filter
frequency_analysis
frequency_filter
image_restoration
edge_shape_detection
```

未修改前端文件，未引入 Docker、数据库或大型深度学习模型依赖。运行时图片字段继续使用 `image_path`；两图算法通过 `second_image_path` 传入第二张图。

## 新增和调整的算法文件

### `grayscale_image`

新增：

```text
clahe_equalization.py
histogram_matching.py
```

灰度变换算法已统一保留在 `grayscale_image/`，不再设置独立 `gray_transform` 分类。

### `color_image`

新增：

```text
region_mosaic.py
color_comprehensive_processing.py
```

### `geometric_transform`

新增：

```text
translate.py
affine_transform.py
perspective_transform.py
```

修改：

```text
rotate.py
```

`rotate.py` 新增任意比例旋转中心参数 `center_x_ratio`、`center_y_ratio`。

### `spatial_filter`

新增：

```text
statistical_order_filter.py
max_filter.py
min_filter.py
adaptive_median_filter.py
unsharp_masking.py
add_noise.py
```

空间域锐化继续保留在 `laplacian_sharpen.py` 和 `unsharp_masking.py`。

### `frequency_filter`

新增：

```text
butterworth_low_pass.py
butterworth_high_pass.py
frequency_laplacian_sharpen.py
homomorphic_filter.py
```

频域拉普拉斯锐化放在 `frequency_filter/frequency_laplacian_sharpen.py`。

### `image_restoration`

新增：

```text
windowed_inverse_filter_restoration.py
```

### `edge_shape_detection`

新增分类目录：

```text
backend/app/algorithms/edge_shape_detection/
```

新增/迁移算法：

```text
basic_edge_detection.py
canny_edge_detection.py
sobel_edge_detection.py
roberts_cross.py
prewitt_edge_detection.py
scharr_edge_detection.py
log_edge_detection.py
hough_shape_detection.py
corner_detection.py
```

Canny 已迁移为 `edge_shape_detection/canny_edge_detection.py`；Sobel 已迁移到 `edge_shape_detection/sobel_edge_detection.py`。旧灰度目录下的两个边缘检测文件已删除，不再注册为活动算法。

## API 与服务更新

新增分类路由：

```text
GET  /api/algorithms/edge-shape-detection
POST /api/algorithms/edge-shape-detection/run
```

更新文件：

```text
backend/app/services/algorithm_registry.py
backend/app/api/algorithm_modules/common.py
backend/app/api/algorithm_modules/edge_shape_detection.py
backend/app/schemas/process_schema.py
backend/app/services/process_service.py
backend/main.py
```

关键变化：

- `MODULE_ORDER` 和 `ALGORITHM_MODULES` 已对齐最终 9 类。
- `/api/algorithms` 应返回 9 个分类。
- `grayscale_image` 不再暴露 Canny 或 Sobel。
- `edge_shape_detection` 暴露 Canny、Sobel 和形状检测相关算法。
- `ProcessRequest` 与 `CategoryProcessRequest` 都支持 `second_image_path`。
- `process_service.py` 会加载第二张图并注入 `params["_second_image"]`。
- 旧字段 `image_id` 继续通过 Pydantic `extra="forbid"` 拒绝。

## 测试和文档更新

更新测试：

```text
backend/tests/test_algorithm_completeness.py
backend/tests/test_backend_framework.py
backend/tests/sample_test_configs/canny_example.json
backend/tests/sample_test_configs/sobel_edge_detection_example.json
backend/tests/manual_test_algorithm_advanced.py
```

测试覆盖：

- `/api/algorithms` 返回 9 个分类。
- `edge_shape_detection` 分类存在并可运行。
- Canny/Sobel 不再注册到 `grayscale_image`。
- 最终注册算法均可导入、可运行，并返回统一结构。
- 参数元数据满足前端 slider/select 渲染要求。
- 双图像算法和 `histogram_matching` 支持 `second_image_path`。
- 旧 `image_id` 字段仍被拒绝。

更新文档：

```text
README.md
backend/README.md
backend/app/README.md
backend/app/algorithms/分工文档.md
backend/app/algorithms/算法框架填写说明.md
backend/tests/README.md
backend/tests/算法测试脚本使用说明文档.md
```

## 验证结果

执行命令：

```bat
cd backend
pytest -q
```

结果：

```text
16 passed
```

## 前端联调说明

- 前端应从 `/api/algorithms` 动态读取 9 个分类和算法参数。
- 需要运行边缘检测时，使用 `edge_shape_detection` 或分类接口 `/api/algorithms/edge-shape-detection/run`。
- Canny 算法名为 `canny_edge_detection`，Sobel 算法名为 `sobel_edge_detection`。
- 两图算法需要传 `second_image_path`，不要把 `_second_image` 暴露给前端参数面板。
- 不要提交旧字段 `image_id`。
