# 更新日志

## [2026-05-25] 重构后端算法模块目录结构

### 目录结构重构

**删除旧模块目录（8 个空壳）：**
- `anime_recognition/`、`basic_operations/`、`color_processing/`
- `edge_detection/`、`geometry/`、`gray_transform/`
- `morphology/`、`restoration/`

**新建 6 大算法模块（29 个算法文件）：**

| 模块 | 路径 | 文件数 |
|------|------|--------|
| 灰度图像类 | `grayscale_image/` | 8 |
| 彩色图像类 | `color_image/` | 4 |
| 几何变换类 | `geometric_transform/` | 3 |
| 空域滤波类 | `spatial_filter/` | 5 |
| 频域分析类 | `frequency_analysis/` | 3 |
| 频域滤波类 | `frequency_filter/` | 6 |

**新增核心文件：**
- `core/algorithm_framework.py` — 算法通用工具函数与统一运行框架（885 行）
- `algorithms/算法框架填写说明.md` — 算法文件编写规范说明

**新增测试体系：**
- `tests/manual_test_algorithm.py` — 算法手动测试脚本
- `tests/algorithm_test_examples.md` — 测试用例说明
- `tests/sample_test_configs/` — 8 组算法测试配置（JSON）

**新增数据目录：**
- `data/test_images/` — 测试输入图片
- `data/test_outputs/` — 测试输出图片
- `data/uploads/` — 用户上传图片（已规划）
- `data/library/` — 内置图片库（已规划，含 5 个分类子目录）
- `data/outputs/` — 算法处理输出（已规划）

### 文档更新

- **README.md** — 第 4 节目录树与实际项目结构完全同步，修正了过时的文件引用，补充了 `data/` 完整子目录

### 统计

- **63 个文件变更**，+2651 行 / -217 行
- 提交：`1e8e3dd`
