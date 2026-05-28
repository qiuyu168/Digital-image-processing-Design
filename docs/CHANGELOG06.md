# CHANGELOG06 — 前端元素分布重写 + 组件拆分 + Apple HIG 动效

更新时间：2026-05-28

## 更新范围

本次更新围绕前端的页面元素分布进行全面重写，将所有 View 文件拆分为功能区子组件，引入 Apple HIG 动效系统。**后端文件零修改，所有算法文本、参数 label、按钮文案、团队名单一字未改。**

## 新增文件（22 个）

### 工作区子组件 (`frontend/src/components/workspace/`)
| 文件 | 说明 |
| --- | --- |
| `AlgorithmSidebar.vue` | 左侧算法树侧栏，el-menu + 模块图标 + 算法计数徽章，sticky 顶部 |
| `AlgorithmInfoCard.vue` | 当前选中算法名称与描述信息卡 |
| `UploadPanel.vue` | 图片上传面板，预览 + hover 遮罩重上传提示 + 元数据展示 |
| `ParamsPanel.vue` | 参数设置面板，slider/select/switch/input 动态生成，执行按钮固定底部 |
| `NoParamCard.vue` | 无可变参数时的 SVG 插图占位卡 |
| `ResultPanel.vue` | 处理结果展示，原图/结果对比 + 步骤图 + 指标 + 分析 |

### 首页子组件 (`frontend/src/components/home/`)
| 文件 | 说明 |
| --- | --- |
| `HeroSection.vue` | Hero 区，左文本 + 右层叠步骤卡片 |
| `FlowSection.vue` | 功能流程横向步骤指示器（圆形编号 + 连线，首段 amber 高亮） |
| `AlgorithmModuleGrid.vue` | 算法模块展示，主推大卡 + 紧凑卡列表联动 |
| `FeatureSection.vue` | 项目特色卡片网格 |

### 图像库子组件 (`frontend/src/components/library/`)
| 文件 | 说明 |
| --- | --- |
| `CategorySidebar.vue` | 左侧分类侧栏，含刷新按钮和骨架加载态 |
| `LibraryHero.vue` | 图库顶部信息区 |
| `ImageGrid.vue` | 图片网格，hover 右上角滑入操作图标组（Apple Finder 风格） |
| `MetricsPanel.vue` | 底部内联抽屉，折叠 64px / 展开 320px，横滚显示指标 |

### 登录页子组件 (`frontend/src/components/login/`)
| 文件 | 说明 |
| --- | --- |
| `LoginHero.vue` | 左侧品牌展示区，层叠步骤卡片视觉 |
| `LoginCard.vue` | 右侧表单卡片，顶部 tab 切换 + amber focus ring |

### 个人信息子组件 (`frontend/src/components/profile/`)
| 文件 | 说明 |
| --- | --- |
| `ProfileTabSidebar.vue` | 左侧竖排 tab 侧栏 |
| `InfoForm.vue` | 基本资料表单（8pt 网格对齐） |
| `AvatarForm.vue` | 头像更换区（左预览右操作两栏） |
| `PasswordForm.vue` | 密码修改表单 + 三段密码强度指示条 |

## 修改文件（8 个）

| 文件 | 变更 |
| --- | --- |
| `frontend/src/views/WorkspaceView.vue` | 三栏装配层（算法树 260px / 工作区 1fr / 参数 340px），保留全部 script 逻辑 |
| `frontend/src/views/HomeView.vue` | 四子组件装配 + TOC 侧栏，保留 scrollSpy 逻辑 |
| `frontend/src/views/LibraryView.vue` | 三区装配 + 底部 MetricsPanel 抽屉，保留全部 API 调用逻辑 |
| `frontend/src/views/LoginView.vue` | hero + card 装配，保留全部登录/注册/表单逻辑 |
| `frontend/src/views/UserProfileView.vue` | sidebar + 三 form 分条件装配，保留全部状态和校验逻辑 |
| `frontend/src/views/NotFoundView.vue` | 增加 404 数字 + accent line  stagger 入场动画 |
| `frontend/src/styles/index.scss` | 追加 Apple HIG 缓动 Token（`--ease-*`、`--dur-*`）+ `prefers-reduced-motion` + route-fade 类 |
| `frontend/src/components/MainLayout.vue` | RouterView 外包 `<Transition name="route-fade">` |

## 已调整组件（3 个）

| 文件 | 变更 |
| --- | --- |
| `frontend/src/components/HeaderNav.vue` | nav-item active underline 改为 left-origin scale 滑动；user-box 折叠为头像 hover 展开 |
| `frontend/src/components/AppFooter.vue` | 从 3 栏竖直改为两行水平流向（品牌 + 团队）；member-tag 加 hover 微高亮 |
| `frontend/src/components/MainLayout.vue` | 路由切换增加 fade-up Transition |

## Apple HIG 动效系统

| Token | 值 | 用途 |
| --- | --- | --- |
| `--ease-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | 常规 hover、状态切换 |
| `--ease-emphasized` | `cubic-bezier(0.25, 0.1, 0.25, 1)` | 强调入场 |
| `--ease-decel` | `cubic-bezier(0, 0, 0.2, 1)` | 减速入场（大组件） |
| `--dur-fast` | `180ms` | 微交互 |
| `--dur-base` | `240ms` | 面板/tab 切换 |
| `--dur-slow` | `340ms` | 大组件进场 |

全局尊重 `prefers-reduced-motion: reduce`。

## 原则验证

- `pnpm build` 构建通过
- `git diff --stat backend/` 后端零变更
- 所有算法名、模块名、参数 label、按钮文案、团队名单一字未改
