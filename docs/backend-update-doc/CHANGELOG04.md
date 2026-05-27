# 本文件用于记录 P0/P1 后端问题修复与运行产物清理更新

# CHANGELOG04 - P0/P1 Backend Issues Fix

更新时间：2026-05-27

## 修复范围

本次根据 `codex_fix_p0_p1_backend_issues_prompt.md` 完成后端 P0/P1 问题修复，范围限定在后端、测试和文档，不修改前端，不引入 Docker、数据库或大模型依赖。

## P0 修复

1. 删除误放在 `app/core/` 下的 `backend/app/core/algorithm_framework.py`。
2. 清理 `backend` 下 Python 运行缓存，验证无 `__pycache__`、`*.pyc`、`*.pyo` 残留。
3. 清理 `backend/data/uploads/` 的运行上传图片，仅保留 `.gitkeep`。
4. 更新 `.gitignore`，忽略 Python 缓存、pytest 缓存、上传目录、输出目录和测试输出目录中的运行产物。
5. 修复 `bilateral_filter.py` 对 BGRA、灰度、BGR、0.0-1.0 float、非连续数组输入的兼容性。

## P1 修复

1. 将 `backend/tests/manual_test_algorithm.py` 恢复为初学者友好的三路径版本，只需修改：
   - `INPUT_IMAGE_PATH`
   - `OUTPUT_IMAGE_PATH`
   - `ALGORITHM_IMPORT_PATH`
2. 将复杂手动测试脚本保留为 `backend/tests/manual_test_algorithm_advanced.py`。
3. 将算法改进提示词目录移出运行时代码目录：
   - 原路径：`backend/app/algorithms/algorithm_improvement_prompts_7_models/`
   - 新路径：`docs/prompts/algorithm_improvement_prompts_7_models/`
4. `ProcessRequest` 新增可选字段：
   - `module_display_name`
   - `algorithm_display_name`
5. `CategoryProcessRequest` 新增可选字段：
   - `algorithm_display_name`
6. README 当前接口示例统一使用 `image_path`，不再使用运行时 `image_id`。

## 测试覆盖

新增或更新的测试覆盖：

1. `bilateral_filter.py` 可处理 BGRA float 非连续图像。
2. `ProcessRequest` 可接收前端显示名字段，并继续拒绝 legacy `image_id`。
3. `CategoryProcessRequest` 可接收 `algorithm_display_name`。
4. `manual_test_algorithm.py` 是三路径初学者版本，不依赖 argparse、命令行参数或 PARAMS。
5. `algorithm_framework.py` 已移出 `app/core/`。
6. prompt 文档已移到 `docs/prompts/`。
7. 上传运行产物未保留在 `backend/data/uploads/`。
8. `.gitignore` 已包含运行产物防提交规则。

## 验证结果

已运行：

```bat
python -m pytest backend\tests -q
```

结果：

```text
13 passed in 0.53s
```

补充验证：

```text
backend 下 __pycache__ 数量：0
backend 下 *.pyc/*.pyo 数量：0
backend/data/uploads/ 仅保留 .gitkeep
```

## 当前约束

1. 当前运行时图片标识只使用 `image_path`。
2. `image_id` 仅保留在 legacy 字段拒绝测试中。
3. 本次没有进行 push。
