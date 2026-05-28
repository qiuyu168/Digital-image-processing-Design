# 前端全面重设计规格文档

> 日期: 2026-05-28
> 状态: 已确认

## 1. 设计目标

视觉 + 体验双线并进：统一6页面的设计语言和交互规范，建立专业、有辨识度的动漫图像处理系统品牌感。

## 2. 全局设计系统

### 2.1 色彩体系 —— 六色全光谱

六色光谱，每个功能模块用不同强调色区分：

| 令牌 | 色值 | 用途 |
|---|---|---|
| `--bg-primary` | `#0a0014` | 主背景（深紫黑）|
| `--bg-secondary` | `#120024` | 卡片/面板背景 |
| `--bg-glass` | `rgba(255,255,255,0.04)` | 毛玻璃底层 |
| `--accent-pink` | `#ff6b9d → #e04090` | 主CTA、关键强调 |
| `--accent-purple` | `#a78bfa → #7c3aed` | 二级导航、算法分类 |
| `--accent-cyan` | `#38bdf8 → #0ea5e9` | 信息、交互反馈 |
| `--accent-green` | `#34d399 → #10b981` | 成功状态、指标 |
| `--accent-amber` | `#fbbf24 → #f59e0b` | 警告、重要标记 |
| `--accent-rose` | `#fb7185 → #e11d48` | 危险/删除、错误 |
| `--text-primary` | `#f8f4ff` | 主文字（近白）|
| `--text-secondary` | `#c0b8d4` | 次要文字（淡紫灰）|
| `--text-muted` | `#7a7090` | 弱化文字 |
| `--border-glass` | `rgba(255,255,255,0.08)` | 毛玻璃边框 |
| `--border-active` | `rgba(255,107,157,0.4)` | 激活/聚焦边框 |

### 2.2 字体

- **标题**: M PLUS Rounded 1c (Google Fonts, 日系圆体) — 用于页面标题、模块名称
- **正文**: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif

### 2.3 组件风格 —— 全毛玻璃

- 卡片: `bg-glass` + `backdrop-blur(16px)` + 1px `border-glass` + `border-radius: 12px`
- 主按钮: 粉紫渐变 `linear-gradient(135deg, --accent-pink)` + `border-radius: 10px`
- 输入框: 毛玻璃底 + 细边框 + hover时边框微亮
- 标签: 对应强调色 15% 透明度底 + 彩色文字

### 2.4 动效体系

| 令牌 | 值 |
|---|---|
| `--ease-bounce` | `cubic-bezier(0.34, 1.56, 0.64, 1)` |
| `--ease-smooth` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `--dur-fast` | `150ms` |
| `--dur-base` | `250ms` |
| `--dur-slow` | `400ms` |

- 页面入场: fade-up + `scale(0.98→1)`, 300ms
- 卡片 hover: `translateY(-4px)` + glow shadow, 250ms ease-bounce
- 按钮: `scale(0.96)` on press + ripple
- 路由过渡: crossfade 200ms
- 背景粒子: 12-18个, 30-50s浮动, 低透明度

### 2.5 间距体系

4px 基础网格: `--space-xs: 4px | --space-sm: 8px | --space-md: 16px | --space-lg: 24px | --space-xl: 32px | --space-2xl: 48px`

## 3. 页面设计

### 3.1 首页 HomeView — 沉浸式 Hero + 功能卡片网格

- **Hero区**: 大Logo(渐变圆形) + 系统标题 + 副标题(9类75算法) + 双CTA(开始处理/查看图库)
- **算法统计区**: 2xN 网格卡片，每卡显示算法数+分类名，不同类别用不同强调色数字
- **底部引导**: "↓ 向下滚动探索更多" 淡文字 + 浮动箭头动画
- **背景**: 12个粒子 + 径向渐变光晕

### 3.2 工作区 WorkspaceView — 三栏经典布局

- **左栏(25%)**: 算法树 — 9分类折叠列表，当前选中粉色高亮，计数徽章
- **中栏(flex)**: 上传区(拖拽/点击) + 原图/结果左右对比 + 分析文本区
- **右栏(22%)**: 动态参数控件(slider/select/switch) + 执行按钮(固定底部)
- **交互**: 选算法→参数面板刷新→点执行→结果区fade-in动画展示

### 3.3 登录页 LoginView — 居中毛玻璃卡片

- **布局**: 全屏居中，背景模糊彩色光晕(粉+紫+蓝三团大blur圆)
- **卡片**: 毛玻璃悬浮卡 — Logo + 系统名 + 英文副标题 + 输入框 + 登录按钮 + 注册链接
- **交互**: 卡片入场 scale+fade, 输入框focus边框变粉色发光

### 3.4 图像库 LibraryView — 侧栏 + 网格 + 底部抽屉

- **左栏**: 分类列表(头像/人物/场景/素材/其他), 每项带数量徽章
- **右栏**: 图片网格(3-4列)，hover时彩色边框+微放大
- **底部抽屉**: 点击图片弹出指标面板(宽/高/通道/均值/直方图), 可折叠(64px→320px)
- **交互**: 抽屉slide-up动画, 图片入场stagger(每个延迟30ms)

### 3.5 个人中心 UserProfileView — 侧栏 Tab + 内容面板

- **左区**: 头像(渐变圆形+发光边框) + 三个Tab(基本资料/更换头像/设置密码)
- **右区**: 表单面板 — 毛玻璃卡片包裹表单项
- **交互**: Tab切换fade过渡, 保存按钮loading状态, 密码强度指示条(粉→紫→蓝→绿)

### 3.6 404 NotFoundView — 渐变数字 + 浮动粒子

- **内容**: 大号"404"渐变文字(粉→紫→蓝) + "页面飞走了 ✦" 趣味文案
- **按钮**: 渐变"返回首页" + 毛玻璃"返回上一页"
- **动效**: 粒子浮动 + "404"数字呼吸发光 + 按钮弹性入场

## 4. 技术实现规划

### 4.1 文件变更范围

```
frontend/src/styles/index.scss    — 全局设计令牌 + 基础样式
frontend/index.html                — Google Fonts 引入
frontend/src/views/HomeView.vue    — 重写
frontend/src/views/WorkspaceView.vue — 重写
frontend/src/views/LoginView.vue   — 重写
frontend/src/views/LibraryView.vue — 重写
frontend/src/views/UserProfileView.vue — 重写
frontend/src/views/NotFoundView.vue — 重写
frontend/src/components/MainLayout.vue — 更新背景+粒子
frontend/src/components/HeaderNav.vue — 更新配色+动效
frontend/src/components/AppFooter.vue — 更新配色
```

### 4.2 实施顺序

1. `index.scss` 全局令牌 + `index.html` 字体引入
2. `MainLayout.vue` + `HeaderNav.vue` + `AppFooter.vue` 布局壳
3. `HomeView.vue` 首页
4. `WorkspaceView.vue` 工作区
5. `LoginView.vue` 登录页
6. `LibraryView.vue` 图像库
7. `UserProfileView.vue` 个人中心
8. `NotFoundView.vue` 404页面

## 5. 约束与注意

- 保持现有路由结构、API调用、Pinia store 不变
- Element Plus 组件保持使用，通过 SCSS 深度定制主题
- 所有动画尊重 `prefers-reduced-motion`
- 不引入新依赖(echarts暂不启用)
- 保持响应式，min-width 375px 可用
