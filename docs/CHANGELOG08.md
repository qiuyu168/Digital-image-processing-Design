# CHANGELOG08 — 前端适配后端 + 图像库分页 + bug 修复

更新时间：2026-05-28

## 更新范围

本次更新完成前端与后端的全面适配（njk-branch 前端 → backend-develop），修复运行时 bug，改进图像库页面（分页 + 排除 other 分类），统一端口为 8050。

---

## 一、前端从 njk-branch 拉取

前端目录从 `njk-branch` 完整拉取，替换原有前端代码。基于现有页面结构进行拓展适配。

---

## 二、前端适配后端（4 文件）

### 1. `frontend/src/utils/check_health.js`
- 修复：添加缺失的 `ElMessage` 导入（运行时报错修复）

### 2. `frontend/src/api/run.js`
- 新建：实现 `runAlgorithmService(moduleSlug, payload)` 函数
- 自动将模块名（下划线）转换为 URL slug（短横线）
- POST 到 `/api/algorithms/{slug}/run`

### 3. `frontend/src/views/WorkspaceView.vue`
- 移除硬编码的 `moduleRunEndpointMap`（仅 6 个模块）→ 动态计算全部 9 个模块端点
- 用 `runAlgorithmService` 替换内联 `http.post()`
- 新增第二张图片选择器：`basic_operation` 模块从图像库选第二张图
- 修复 `canProcess` 双图校验逻辑
- 修复 `normalizePreviewUrl` 中对已删除 `http` 导入的引用

### 4. `frontend/src/views/HomeView.vue`
- 算法模块卡片从硬编码 6 个 → 后端 API 动态获取 9 个模块
- 新增 skeleton loading 状态 + 硬编码数据 fallback

---

## 三、图像库分页 + 排除 other 分类

### 后端 (`backend/app/services/image_store.py` + `backend/app/api/library.py`)

| 变更 | 说明 |
|------|------|
| 排除 other 分类 | `list_library_categories()` 跳过 `other`，侧栏仅显示 4 个分类 |
| 分页参数 | `GET /api/library/images` 新增 `page`(ge=1)、`page_size`(ge=1, le=100) 参数 |
| 分页响应 | 返回 `{ success, category, images, total, page, page_size }` |

### 前端 (`frontend/src/views/LibraryView.vue`)

| 变更 | 说明 |
|------|------|
| 分页 UI | `el-pagination` 组件，`layout="prev, pager, next"`，6 张/页 |
| 删除标题栏 | 移除"图片列表"标题模块，图片区域直接展示 |
| 3 列网格 | 固定 `repeat(3, 1fr)` 布局，6 张图 2 行 × 3 列 |
| 高度自适应 | 移除固定 `max-height`/`min-height`，内容自然撑开 |
| 分类切换 | 自动重置 `currentPage = 1` |
| 刷新按钮 | 移至左侧分类栏 |

---

## 四、Bug 修复

| Bug | 文件 | 修复 |
|-----|------|------|
| `ElMessage` 未定义 | `check_health.js` | 添加 `import { ElMessage } from 'element-plus'` |
| `selectedAlgorithm` TDZ | `WorkspaceView.vue` | `secondImageEnabled` 移至 `selectedAlgorithm` 声明之后 |
| `http` 引用残留 | `WorkspaceView.vue` | `normalizePreviewUrl` 移除已删除的 `http.defaults.baseURL` |
| 双图未强制选择 | `WorkspaceView.vue` | `canProcess` 增加 `(!secondImageEnabled \|\| selectedSecondImagePath)` 校验 |

---

## 五、端口统一

`.env.development` 中 `VITE_API_BASE_URL` 从 `8000` 改为 `8050`，后端同步启动在 8050 端口。

---

## 六、文档更新

- 根目录 `README.md`：更新前端组件结构、页面描述、API 模块说明
- `frontend/README.md`：更新接口表格（全部 9 模块）、页面描述、run.js 说明
- 新增 `docs/superpowers/specs/2026-05-28-frontend-backend-adaptation-design.md`
- 新增 `docs/superpowers/plans/2026-05-28-frontend-backend-adaptation.md`
