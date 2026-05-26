# 更新日志

## [2026-05-26] 算法模块框架化重构与文档整理

### algorithm_framework.py 精简

将集中式算法调度框架（885 行）精简为纯工具函数模块（74 行），移除：
- `HANDLERS` 调度字典（含 50+ 个算法实现映射）
- `MODULE_DESCRIPTIONS`、`DISPLAY_NAMES`、`PARAMS_BY_NAME` 等集中式元数据中心
- `build_algorithm_meta()`、`run_standard_algorithm()` 调度函数
- 全部 `_run_*` 算法实现函数

保留 10 个通用工具函数：`clamp_int`、`clamp_float`、`ensure_odd_int`、`ensure_color`、`as_gray`、`clip_uint8`、`normalize_uint8`、`make_step`、`make_response`

### 26 个算法文件框架化

所有算法文件从调用集中式框架改为独立自包含结构，每个文件包含：

- 首行中文功能说明
- 独立的 `ALGORITHM_META` 字典（module / name / display_name / description / params）
- 统一的 `run(image, params)` 占位函数（参数校验 + 返回原图 + 提示文本）

影响范围（6 个模块）：

| 模块 | 文件数 | 变更类型 |
|------|--------|---------|
| `grayscale_image/` | 7 | 重写为框架占位 |
| `color_image/` | 4 | 重写为框架占位 |
| `geometric_transform/` | 3 | 重写为框架占位 |
| `spatial_filter/` | 5 | 重写为框架占位 |
| `frequency_analysis/` | 1 | 重写为框架占位 |
| `frequency_filter/` | 6 | 重写为框架占位 |

已包含实现的文件不受影响：`edge_detection_basic.py`、`magnitude_spectrum.py`、`spectrum_shift.py`

### 依赖与环境配置更新

- **requirements.txt** — 精简为 18 个依赖、6 个功能分组，Python 版本对齐为 3.10/3.11/3.12
- **后端运行环境配置说明.md** — 重写为 16 节完整版，新增依赖分类表、目录结构总览、测试配置表、常见问题表格、环境验证清单
- **README.md** — 第 5.1 节示例文件名修正

### Git 管理优化

- **新增 `.gitignore`** — 过滤 venv、\_\_pycache\_\_、IDE 配置、node_modules、系统文件等

### 清理

- 删除 `backend/tests/algorithm_test_examples.md`

### 统计

- **33 个文件变更**，+765 行 / -1396 行（净减 631 行）
- 核心变更：algorithm_framework.py 从 885 行精简到 74 行
