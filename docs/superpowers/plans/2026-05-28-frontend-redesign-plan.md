# 前端全面重设计实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将6个前端页面的视觉设计和交互体验统一翻新为动漫活力风（六色光谱 + 全毛玻璃 + 适度动效）

**Architecture:** 先从全局设计令牌入手建立视觉底盘，再更新三个布局壳组件，最后逐个重写六个页面视图。所有 Element Plus 组件通过 SCSS 深度定制保持使用。

**Tech Stack:** Vue 3 + Element Plus + Pinia + SCSS + Vite

---

### Task 1: 全局设计系统 — SCSS 令牌 + Google Fonts

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/src/styles/index.scss`

- [ ] **Step 1: 引入 Google Fonts**

在 `frontend/index.html` 的 `<head>` 中添加 M PLUS Rounded 1c 字体链接。

```html
<!-- 在 </title> 之后添加 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800&display=swap" rel="stylesheet">
```

- [ ] **Step 2: 重写 `frontend/src/styles/index.scss` 全局设计令牌**

```scss
/* ===== 动漫活力风设计令牌 ===== */

/* --- 色彩令牌 --- */
:root {
  --bg-primary: #0a0014;
  --bg-secondary: #120024;
  --bg-glass: rgba(255, 255, 255, 0.04);

  --accent-pink: #ff6b9d;
  --accent-pink-deep: #e04090;
  --accent-purple: #a78bfa;
  --accent-purple-deep: #7c3aed;
  --accent-cyan: #38bdf8;
  --accent-cyan-deep: #0ea5e9;
  --accent-green: #34d399;
  --accent-green-deep: #10b981;
  --accent-amber: #fbbf24;
  --accent-amber-deep: #f59e0b;
  --accent-rose: #fb7185;
  --accent-rose-deep: #e11d48;

  --text-primary: #f8f4ff;
  --text-secondary: #c0b8d4;
  --text-muted: #7a7090;

  --border-glass: rgba(255, 255, 255, 0.08);
  --border-active: rgba(255, 107, 157, 0.4);

  --shadow-card: 0 4px 24px rgba(180, 40, 100, 0.12);
  --shadow-glow-pink: 0 0 20px rgba(255, 107, 157, 0.25);
  --shadow-glow-purple: 0 0 20px rgba(167, 139, 250, 0.25);

  /* --- 动效令牌 --- */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  --dur-fast: 150ms;
  --dur-base: 250ms;
  --dur-slow: 400ms;

  /* --- 间距令牌 --- */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* --- 字体 --- */
  --font-display: 'M PLUS Rounded 1c', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-body: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* --- 基础重置 --- */
*, *::before, *::after {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

/* --- 毛玻璃卡片基类 --- */
.glass-card {
  background: var(--bg-glass);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-glass);
  border-radius: 12px;
}

/* --- 渐变按钮 --- */
.btn-gradient {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-pink-deep));
  color: #fff;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform var(--dur-fast) var(--ease-smooth),
              box-shadow var(--dur-base) var(--ease-smooth);
  box-shadow: var(--shadow-glow-pink);

  &:hover {
    box-shadow: 0 0 32px rgba(255, 107, 157, 0.4);
  }

  &:active {
    transform: scale(0.96);
  }
}

/* --- 毛玻璃按钮 --- */
.btn-glass {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  border: 1px solid var(--border-glass);
  border-radius: 10px;
  background: var(--bg-glass);
  backdrop-filter: blur(12px);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: border-color var(--dur-fast) var(--ease-smooth),
              background var(--dur-fast) var(--ease-smooth);

  &:hover {
    border-color: var(--border-active);
    background: rgba(255, 255, 255, 0.06);
  }

  &:active {
    transform: scale(0.96);
  }
}

/* --- 毛玻璃输入框 --- */
.glass-input {
  width: 100%;
  padding: 10px 14px;
  background: var(--bg-glass);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-glass);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 14px;
  outline: none;
  transition: border-color var(--dur-fast) var(--ease-smooth),
              box-shadow var(--dur-fast) var(--ease-smooth);

  &::placeholder {
    color: var(--text-muted);
  }

  &:focus {
    border-color: var(--border-active);
    box-shadow: 0 0 8px rgba(255, 107, 157, 0.15);
  }
}

/* --- 页面入场动画 --- */
.page-enter {
  animation: pageIn var(--dur-slow) var(--ease-smooth) both;
}

@keyframes pageIn {
  from {
    opacity: 0;
    transform: translateY(12px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* --- 悬浮粒子 --- */
.floating-particle {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  opacity: 0.12;
}

/* --- 路由过渡 --- */
.route-fade-enter-active,
.route-fade-leave-active {
  transition: opacity var(--dur-base) var(--ease-smooth);
}
.route-fade-enter-from,
.route-fade-leave-to {
  opacity: 0;
}

/* --- 渐变文字 --- */
.gradient-text {
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple), var(--accent-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* --- 自定义滚动条 --- */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(167, 139, 250, 0.3);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(167, 139, 250, 0.5);
}

/* --- prefers-reduced-motion --- */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* --- Element Plus 暗色主题覆盖 --- */
.el-dialog {
  --el-dialog-bg: transparent;
}
.el-message {
  --el-message-bg: var(--bg-secondary);
}
```

- [ ] **Step 3: 提交**

```bash
git add frontend/index.html frontend/src/styles/index.scss
git commit -m "feat: 全局设计令牌 — 六色光谱/毛玻璃/动效体系/Google Fonts"
```

---

### Task 2: 布局组件翻新 — MainLayout + HeaderNav + AppFooter

**Files:**
- Modify: `frontend/src/components/MainLayout.vue`
- Modify: `frontend/src/components/HeaderNav.vue`
- Modify: `frontend/src/components/AppFooter.vue`

- [ ] **Step 1: 重写 `MainLayout.vue` — 暗色背景 + 浮动粒子**

```vue
<template>
  <div class="main-layout">
    <div class="bg-particles">
      <div
        v-for="p in particles"
        :key="p.id"
        class="floating-particle"
        :style="{
          width: p.size + 'px',
          height: p.size + 'px',
          left: p.x + '%',
          top: p.y + '%',
          background: p.color,
          animation: `float-particle ${p.duration}s ease-in-out infinite`,
          animationDelay: p.delay + 's'
        }"
      />
    </div>
    <HeaderNav />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="route-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HeaderNav from './HeaderNav.vue'
import AppFooter from './AppFooter.vue'

const colors = ['rgba(255,107,157,0.15)', 'rgba(167,139,250,0.12)', 'rgba(56,189,248,0.1)', 'rgba(52,211,153,0.08)']
const particles = ref(
  Array.from({ length: 16 }, (_, i) => ({
    id: i,
    size: Math.random() * 80 + 20,
    x: Math.random() * 100,
    y: Math.random() * 100,
    color: colors[i % colors.length],
    duration: Math.random() * 20 + 30,
    delay: Math.random() * 10
  }))
)
</script>

<style lang="scss" scoped>
.main-layout {
  min-height: 100vh;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.bg-particles {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.main-content {
  position: relative;
  z-index: 1;
  padding-top: 64px;
  min-height: calc(100vh - 64px - 80px);
}

@keyframes float-particle {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(12px, -20px) scale(1.1); }
  50% { transform: translate(-8px, -36px) scale(0.9); }
  75% { transform: translate(-16px, -12px) scale(1.05); }
}
</style>
```

- [ ] **Step 2: 重写 `HeaderNav.vue` — 毛玻璃导航栏 + 六色激活指示**

```vue
<template>
  <header class="header-nav glass-card">
    <div class="nav-inner">
      <router-link to="/home" class="logo-area">
        <span class="logo-icon">✦</span>
        <div class="logo-text">
          <span class="logo-title">动漫图像处理系统</span>
          <span class="logo-sub">Anime Image Processing</span>
        </div>
      </router-link>

      <nav class="nav-links">
        <router-link to="/home" class="nav-link" active-class="nav-link--active">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </router-link>
        <router-link to="/workspace" class="nav-link" active-class="nav-link--active">
          <el-icon><MagicStick /></el-icon>
          <span>图像处理</span>
        </router-link>
        <router-link to="/library" class="nav-link" active-class="nav-link--active">
          <el-icon><Picture /></el-icon>
          <span>图像库</span>
        </router-link>
        <router-link to="/profile" class="nav-link" active-class="nav-link--active">
          <el-icon><UserFilled /></el-icon>
          <span>个人中心</span>
        </router-link>
      </nav>

      <div class="user-area">
        <template v-if="authStore.isLogin">
          <div class="user-avatar">{{ (authStore.userInfo?.username || 'U')[0].toUpperCase() }}</div>
          <span class="user-name">{{ authStore.userInfo?.username }}</span>
          <el-icon class="logout-btn" @click="handleLogout"><CloseBold /></el-icon>
        </template>
        <router-link v-else to="/login" class="btn-gradient" style="padding:6px 16px;font-size:13px;">
          登录 / 注册
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { House, MagicStick, Picture, UserFilled, CloseBold } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.clearLoginInfo()
  router.push('/login')
}
</script>

<style lang="scss" scoped>
.header-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 64px;
  border-radius: 0;
  border-top: none;
  border-left: none;
  border-right: none;
}

.nav-inner {
  max-width: 1440px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 var(--space-lg);
  gap: var(--space-xl);
}

.logo-area {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  font-size: 28px;
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: logoSpin 8s linear infinite;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.logo-sub {
  font-size: 10px;
  color: var(--text-muted);
  line-height: 1.2;
}

.nav-links {
  display: flex;
  gap: var(--space-xs);
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13px;
  font-family: var(--font-body);
  transition: all var(--dur-fast) var(--ease-smooth);
  position: relative;

  &:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.04);
  }

  &--active {
    color: var(--accent-pink);
    background: rgba(255, 107, 157, 0.1);

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 20px;
      height: 3px;
      border-radius: 2px;
      background: var(--accent-pink);
    }
  }
}

.user-area {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  flex-shrink: 0;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
}

.user-name {
  font-size: 13px;
  color: var(--text-secondary);
}

.logout-btn {
  color: var(--text-muted);
  cursor: pointer;
  font-size: 16px;
  transition: color var(--dur-fast);

  &:hover {
    color: var(--accent-rose);
  }
}

@keyframes logoSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
```

- [ ] **Step 3: 重写 `AppFooter.vue` — 简洁毛玻璃页脚**

```vue
<template>
  <footer class="app-footer glass-card">
    <div class="footer-inner">
      <div class="footer-left">
        <span class="footer-logo">✦</span>
        <span class="footer-title">动漫图像处理系统</span>
      </div>
      <div class="footer-center">
        <span>2025 基于动漫图像识别的交互式数字图像处理系统</span>
        <span class="footer-divider">·</span>
        <span>Vue3 + FastAPI 前后端分离项目</span>
      </div>
      <div class="footer-right">
        <span class="member-tag">总架构/对接: 王韬涵</span>
        <span class="member-tag">前端设计: 聂纪坤</span>
        <span class="member-tag">后端设计: 毛思涵 周恩承 任可 高艳阳 雍晨</span>
      </div>
    </div>
  </footer>
</template>

<style lang="scss" scoped>
.app-footer {
  border-radius: 0;
  border-bottom: none;
  border-left: none;
  border-right: none;
  padding: var(--space-md) var(--space-lg);
}

.footer-inner {
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-sm);
  font-size: 12px;
  color: var(--text-muted);
}

.footer-logo {
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 16px;
}

.footer-title {
  font-family: var(--font-display);
  font-weight: 700;
  color: var(--text-secondary);
}

.footer-divider {
  margin: 0 var(--space-xs);
}

.member-tag {
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.03);
  font-size: 11px;
  transition: background var(--dur-fast);

  &:hover {
    background: rgba(255, 107, 157, 0.1);
  }
}
</style>
```

- [ ] **Step 4: 提交**

```bash
git add frontend/src/components/MainLayout.vue frontend/src/components/HeaderNav.vue frontend/src/components/AppFooter.vue
git commit -m "feat: 布局组件翻新 — 毛玻璃导航/暗色粒子背景/简洁页脚"
```

---

### Task 3: 首页重写 — 沉浸式 Hero + 算法卡片网格

**Files:**
- Modify: `frontend/src/views/HomeView.vue`

- [ ] **Step 1: 重写 `HomeView.vue`**

```vue
<template>
  <div class="home-page page-enter">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-glow hero-glow--pink"></div>
      <div class="hero-glow hero-glow--purple"></div>
      <div class="hero-glow hero-glow--blue"></div>
      <div class="hero-logo">✦</div>
      <h1 class="hero-title">动漫图像处理系统</h1>
      <p class="hero-subtitle">
        <span class="gradient-text">9 大分类 · 75 个算法</span> — 实时交互式数字图像处理
      </p>
      <div class="hero-actions">
        <router-link to="/workspace" class="btn-gradient hero-btn">✦ 开始处理</router-link>
        <router-link to="/library" class="btn-glass hero-btn">查看图库</router-link>
      </div>
    </section>

    <!-- 算法统计 -->
    <section class="algo-stats">
      <h2 class="section-title"><span class="gradient-text">算法模块</span></h2>
      <div class="algo-grid">
        <div v-for="m in modules" :key="m.key" class="algo-card glass-card"
          :style="{ '--card-accent': m.color }"
          @click="$router.push('/workspace')">
          <span class="algo-count" :style="{ color: m.color }">{{ m.count }}</span>
          <span class="algo-name">{{ m.name }}</span>
        </div>
      </div>
    </section>

    <!-- 引导 -->
    <div class="scroll-hint">
      <span>向下滚动探索更多</span>
      <span class="scroll-arrow">↓</span>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { chech_health } from '@/utils/check_health'

const modules = [
  { key: 'basic', count: 8, name: '图像基本运算', color: 'var(--accent-pink)' },
  { key: 'gray', count: 14, name: '灰度图像类', color: 'var(--accent-purple)' },
  { key: 'color', count: 6, name: '彩色图像类', color: 'var(--accent-cyan)' },
  { key: 'geo', count: 6, name: '几何变换类', color: 'var(--accent-green)' },
  { key: 'spatial', count: 11, name: '空域滤波类', color: 'var(--accent-amber)' },
  { key: 'freq_a', count: 3, name: '频域分析类', color: 'var(--accent-rose)' },
  { key: 'freq_f', count: 10, name: '频域滤波类', color: 'var(--accent-pink)' },
  { key: 'restore', count: 8, name: '图像复原类', color: 'var(--accent-purple)' },
  { key: 'edge', count: 9, name: '边缘形状检测', color: 'var(--accent-cyan)' },
]

onMounted(() => { chech_health() })
</script>

<style lang="scss" scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-2xl) var(--space-lg);
}

.hero {
  text-align: center;
  padding: 80px 0 64px;
  position: relative;
}

.hero-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  pointer-events: none;
  &--pink { width: 300px; height: 300px; background: var(--accent-pink); top: -40px; left: 10%; }
  &--purple { width: 250px; height: 250px; background: var(--accent-purple); top: 20px; right: 10%; }
  &--blue { width: 200px; height: 200px; background: var(--accent-cyan); bottom: -20px; left: 50%; transform: translateX(-50%); }
}

.hero-logo {
  font-size: 64px;
  width: 100px;
  height: 100px;
  margin: 0 auto var(--space-lg);
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 48px rgba(255, 107, 157, 0.3);
}

.hero-title {
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 var(--space-sm);
}

.hero-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0 0 var(--space-xl);
}

.hero-actions {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
  flex-wrap: wrap;
}

.hero-btn {
  padding: 12px 32px;
  font-size: 15px;
  text-decoration: none;
}

.section-title {
  text-align: center;
  font-family: var(--font-display);
  font-size: 24px;
  margin: 0 0 var(--space-xl);
}

.algo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: var(--space-md);
  margin-bottom: var(--space-2xl);
}

.algo-card {
  padding: var(--space-lg);
  text-align: center;
  cursor: pointer;
  transition: transform var(--dur-base) var(--ease-bounce),
              box-shadow var(--dur-base) var(--ease-smooth),
              border-color var(--dur-base) var(--ease-smooth);

  &:hover {
    transform: translateY(-4px);
    border-color: var(--card-accent);
    box-shadow: 0 8px 32px rgba(255, 107, 157, 0.15);
  }
}

.algo-count {
  display: block;
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 800;
}

.algo-name {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: var(--space-xs);
}

.scroll-hint {
  text-align: center;
  color: var(--text-muted);
  font-size: 12px;
  padding: var(--space-lg) 0;
}

.scroll-arrow {
  display: block;
  animation: bounce 2s ease-in-out infinite;
  margin-top: var(--space-xs);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(6px); }
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/views/HomeView.vue
git commit -m "feat: 首页重写 — 沉浸式Hero+光晕/算法统计网格/毛玻璃卡片"
```

---

### Task 4: 工作区重写 — 三栏毛玻璃布局

**Files:**
- Modify: `frontend/src/views/WorkspaceView.vue`

- [ ] **Step 1: 重写 `WorkspaceView.vue`**

保持现有 `<script setup>` 逻辑完全不变（API调用、参数处理、结果展示），仅替换 `<template>` 和 `<style>`。

```vue
<template>
  <div class="workspace-page page-enter">
    <!-- 左栏：算法树 -->
    <aside class="workspace-sidebar glass-card">
      <div class="sidebar-header">
        <span class="sidebar-title">✦ 算法分类</span>
        <el-icon class="sidebar-refresh" @click="loadAlgorithms"><Refresh /></el-icon>
      </div>
      <div class="algo-tree">
        <div v-for="mod in algorithmModules" :key="mod.module"
          class="tree-module"
          :class="{ 'tree-module--active': activeModule === mod.module }"
          @click="activeModule = mod.module">
          <span class="tree-module-name">{{ mod.display_name }}</span>
          <span class="tree-badge">{{ mod.algorithms?.length || 0 }}</span>
        </div>
      </div>
    </aside>

    <!-- 中栏：主工作区 -->
    <main class="workspace-main">
      <!-- 上传区 -->
      <div class="glass-card upload-section" @click.self="triggerUpload">
        <input ref="fileInput" type="file" accept="image/*" hidden @change="onFileChange">
        <div v-if="!uploadedImage" class="upload-placeholder" @click="triggerUpload">
          <span class="upload-icon">✦</span>
          <span class="upload-text">拖拽或点击上传图片</span>
          <span class="upload-hint">支持 jpg / png / bmp / webp / tiff</span>
        </div>
        <div v-else class="image-compare">
          <div class="compare-pane">
            <span class="compare-label">原图</span>
            <img :src="uploadedImage" alt="原图" class="compare-image">
          </div>
          <div class="compare-pane">
            <span class="compare-label">结果</span>
            <img v-if="resultInfo.imageUrl" :src="resultInfo.imageUrl" alt="结果" class="compare-image result-image">
            <div v-else class="compare-empty">等待处理...</div>
          </div>
        </div>
      </div>

      <!-- 分析文本 -->
      <div v-if="resultInfo.analysis" class="glass-card analysis-section">
        <p>{{ resultInfo.analysis }}</p>
      </div>
    </main>

    <!-- 右栏：参数面板 -->
    <aside class="workspace-params glass-card">
      <div class="params-header">
        <span class="params-title">{{ selectedAlgorithm?.display_name || '选择算法' }}</span>
      </div>
      <div v-if="selectedAlgorithm?.params" class="params-list">
        <div v-for="(param, key) in selectedAlgorithm.params" :key="key" class="param-item">
          <label class="param-label">{{ param.label }}</label>
          <!-- slider -->
          <el-slider v-if="param.component === 'slider'" v-model="params[key]"
            :min="param.min" :max="param.max" :step="param.step"
            :show-tooltip="false" />
          <!-- select -->
          <el-select v-else-if="param.component === 'select'" v-model="params[key]">
            <el-option v-for="opt in param.options" :key="opt" :label="opt" :value="opt" />
          </el-select>
          <!-- switch -->
          <el-switch v-else-if="param.component === 'switch'" v-model="params[key]" />
        </div>
      </div>
      <div v-else class="params-empty">
        <span>此算法无可调节参数</span>
      </div>
      <button class="btn-gradient run-btn"
        :disabled="running"
        @click="runAlgorithm">
        <span v-if="running">✦ 处理中...</span>
        <span v-else>▶ 执行算法</span>
      </button>
    </aside>
  </div>
</template>

<style lang="scss" scoped>
.workspace-page {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  height: calc(100vh - 64px - 80px);
  max-width: 1600px;
  margin: 0 auto;
}

.workspace-sidebar {
  width: 220px;
  flex-shrink: 0;
  padding: var(--space-md);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-title {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--accent-purple);
}

.sidebar-refresh {
  color: var(--text-muted);
  cursor: pointer;
  &:hover { color: var(--accent-cyan); }
}

.tree-module {
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all var(--dur-fast) var(--ease-smooth);
  font-size: 13px;
  color: var(--text-secondary);

  &:hover { background: rgba(255,255,255,0.04); }
  &--active { background: rgba(255,107,157,0.1); color: var(--accent-pink); }
}

.tree-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  background: rgba(255,255,255,0.06);
}

.workspace-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  min-width: 0;
}

.upload-section {
  flex: 1;
  padding: var(--space-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon { font-size: 40px; display: block; margin-bottom: var(--space-sm); }
.upload-text { color: var(--text-secondary); font-size: 14px; }
.upload-hint { color: var(--text-muted); font-size: 12px; display: block; margin-top: var(--space-xs); }

.image-compare { display: flex; gap: var(--space-md); width: 100%; height: 100%; }
.compare-pane { flex: 1; display: flex; flex-direction: column; align-items: center; }
.compare-label { font-size: 12px; color: var(--text-muted); margin-bottom: var(--space-sm); }
.compare-image { max-width: 100%; max-height: 300px; border-radius: 8px; object-fit: contain; }
.compare-empty { flex: 1; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 13px; }

.result-image { border: 1px solid rgba(56,189,248,0.3); box-shadow: 0 0 12px rgba(56,189,248,0.1); }

.analysis-section {
  padding: var(--space-md);
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.workspace-params {
  width: 240px;
  flex-shrink: 0;
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.params-header {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--accent-purple);
}

.params-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.param-label {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
}

.params-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 13px;
}

.run-btn {
  width: 100%;
  padding: 12px 0;
  font-size: 15px;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
</style>
```

> **注意:** `<script setup>` 部分保持现有逻辑完全不变。以上 `<template>` 和 `<style>` 为完整替换内容。`algorithmModules`、`activeModule`、`selectedAlgorithm`、`params`、`running`、`resultInfo`、`uploadedImage`、`loadAlgorithms`、`triggerUpload`、`onFileChange`、`runAlgorithm` 均来自现有脚本。

- [ ] **Step 2: 提交**

```bash
git add frontend/src/views/WorkspaceView.vue
git commit -m "feat: 工作区重写 — 三栏毛玻璃/算法树高亮/原图结果对比"
```

---

### Task 5: 登录页重写 — 居中毛玻璃卡片 + 背景光晕

**Files:**
- Modify: `frontend/src/views/LoginView.vue`

- [ ] **Step 1: 重写 `LoginView.vue`**

保持现有 `<script setup>` 逻辑完全不变，仅替换 `<template>` 和 `<style>`。

```vue
<template>
  <div class="login-page">
    <div class="login-glow login-glow--pink"></div>
    <div class="login-glow login-glow--purple"></div>
    <div class="login-glow login-glow--blue"></div>

    <div class="login-card glass-card">
      <div class="login-logo">✦</div>
      <h1 class="login-title">动漫图像处理系统</h1>
      <p class="login-sub">Interactive Digital Image Processing</p>

      <div class="login-tabs">
        <button :class="{ active: isLogin }" @click="isLogin = true">登录</button>
        <button :class="{ active: !isLogin }" @click="isLogin = false">注册</button>
      </div>

      <form @submit.prevent="handleSubmit" class="login-form">
        <input v-model="username" class="glass-input" placeholder="用户名" autocomplete="username">
        <input v-model="password" type="password" class="glass-input" placeholder="密码" autocomplete="current-password">
        <input v-if="!isLogin" v-model="confirmPassword" type="password" class="glass-input" placeholder="确认密码">

        <button type="submit" class="btn-gradient login-submit">
          {{ isLogin ? '登 录' : '注 册' }}
        </button>
      </form>

      <p class="login-switch">
        {{ isLogin ? '没有账号？' : '已有账号？' }}
        <span @click="isLogin = !isLogin">{{ isLogin ? '立即注册' : '立即登录' }}</span>
      </p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.login-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.12;
  pointer-events: none;
  &--pink { width: 400px; height: 400px; background: var(--accent-pink); top: -100px; left: -100px; animation: glowMove 12s ease-in-out infinite; }
  &--purple { width: 350px; height: 350px; background: var(--accent-purple); bottom: -80px; right: -80px; animation: glowMove 12s ease-in-out infinite reverse; }
  &--blue { width: 250px; height: 250px; background: var(--accent-cyan); top: 50%; left: 50%; animation: glowMove 12s ease-in-out infinite 4s; }
}

.login-card {
  position: relative;
  z-index: 1;
  width: 380px;
  padding: var(--space-2xl) var(--space-xl);
  text-align: center;
  animation: cardIn 500ms var(--ease-smooth) both;
}

.login-logo {
  font-size: 48px;
  width: 80px;
  height: 80px;
  margin: 0 auto var(--space-md);
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 32px rgba(255, 107, 157, 0.3);
}

.login-title {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 var(--space-xs);
}

.login-sub {
  font-size: 11px;
  color: var(--text-muted);
  margin: 0 0 var(--space-xl);
}

.login-tabs {
  display: flex;
  gap: var(--space-xs);
  margin-bottom: var(--space-lg);
  button {
    flex: 1;
    padding: 8px 0;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--text-muted);
    font-size: 14px;
    cursor: pointer;
    transition: all var(--dur-fast);

    &.active {
      background: rgba(255, 107, 157, 0.1);
      color: var(--accent-pink);
    }
  }
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.login-submit {
  width: 100%;
  padding: 12px 0;
  margin-top: var(--space-sm);
  font-size: 15px;
}

.login-switch {
  margin-top: var(--space-lg);
  font-size: 13px;
  color: var(--text-muted);
  span { color: var(--accent-cyan); cursor: pointer; }
}

@keyframes glowMove {
  0%, 100% { transform: translate(0, 0); }
  33% { transform: translate(30px, -20px); }
  66% { transform: translate(-20px, 10px); }
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(20px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
```

> **注意:** `<script setup>` 保持现有逻辑不变。`isLogin`、`username`、`password`、`confirmPassword`、`handleSubmit` 均来自现有脚本。

- [ ] **Step 2: 提交**

```bash
git add frontend/src/views/LoginView.vue
git commit -m "feat: 登录页重写 — 居中毛玻璃卡片/背景光晕动画/弹性入场"
```

---

### Task 6: 图像库 + 个人中心 + 404 重写

**Files:**
- Modify: `frontend/src/views/LibraryView.vue`
- Modify: `frontend/src/views/UserProfileView.vue`
- Modify: `frontend/src/views/NotFoundView.vue`

- [ ] **Step 1: 重写 `LibraryView.vue`**

保持 `<script setup>` 不变，仅替换 `<template>` 和 `<style>`。

```vue
<template>
  <div class="library-page page-enter">
    <aside class="library-sidebar glass-card">
      <h3 class="lib-title">✦ 图库分类</h3>
      <div v-for="cat in categories" :key="cat.name"
        class="lib-cat" :class="{ active: activeCategory === cat.name }"
        @click="activeCategory = cat.name">
        <span>{{ cat.display_name }}</span>
        <span class="lib-count">{{ cat.count }}</span>
      </div>
    </aside>

    <main class="library-main">
      <div class="image-grid">
        <div v-for="img in images" :key="img.image_path"
          class="image-card glass-card"
          :style="{ '--card-accent': img._accent || 'var(--accent-pink)' }"
          @click="selectImage(img)">
          <img :src="img.preview_url" :alt="img.filename" class="image-thumb" loading="lazy">
          <span class="image-name">{{ img.filename }}</span>
        </div>
      </div>

      <transition name="drawer-slide">
        <div v-if="selectedImage" class="metrics-drawer glass-card">
          <div class="drawer-handle" @click="selectedImage = null">—</div>
          <div class="metrics-grid">
            <div class="metric-item" v-for="(val, key) in imageMetrics" :key="key">
              <span class="metric-label">{{ key }}</span>
              <span class="metric-value">{{ val }}</span>
            </div>
          </div>
        </div>
      </transition>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.library-page {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  height: calc(100vh - 64px - 80px);
  max-width: 1400px;
  margin: 0 auto;
}

.library-sidebar {
  width: 180px;
  padding: var(--space-md);
  overflow-y: auto;
}

.lib-title { font-family: var(--font-display); font-size: 14px; color: var(--accent-purple); margin: 0 0 var(--space-md); }

.lib-cat {
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  justify-content: space-between;
  transition: all var(--dur-fast);
  &:hover { background: rgba(255,255,255,0.04); }
  &.active { background: rgba(255,107,157,0.1); color: var(--accent-pink); }
}

.lib-count { font-size: 11px; color: var(--text-muted); }

.library-main { flex: 1; display: flex; flex-direction: column; gap: var(--space-md); overflow: hidden; }

.image-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--space-md);
  overflow-y: auto;
  align-content: start;
}

.image-card {
  padding: var(--space-sm);
  cursor: pointer;
  transition: transform var(--dur-base) var(--ease-bounce), border-color var(--dur-base);
  &:hover {
    transform: translateY(-2px) scale(1.02);
    border-color: var(--card-accent);
  }
}

.image-thumb {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 6px;
}

.image-name {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  text-align: center;
  margin-top: var(--space-xs);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.metrics-drawer {
  padding: var(--space-md);
  border-radius: 12px 12px 0 0;
  max-height: 320px;
  overflow-y: auto;
}

.drawer-handle {
  text-align: center;
  color: var(--text-muted);
  cursor: pointer;
  padding-bottom: var(--space-sm);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: var(--space-sm);
}

.metric-item { text-align: center; }
.metric-label { font-size: 11px; color: var(--text-muted); display: block; }
.metric-value { font-size: 14px; color: var(--text-primary); font-weight: 600; }

.drawer-slide-enter-active, .drawer-slide-leave-active { transition: all 300ms var(--ease-smooth); }
.drawer-slide-enter-from, .drawer-slide-leave-to { max-height: 0; opacity: 0; transform: translateY(20px); }
</style>
```

- [ ] **Step 2: 重写 `UserProfileView.vue`**

保持 `<script setup>` 不变，仅替换 `<template>` 和 `<style>`。

```vue
<template>
  <div class="profile-page page-enter">
    <aside class="profile-sidebar glass-card">
      <div class="profile-avatar">
        <div class="avatar-circle">{{ (authStore.userInfo?.username || 'U')[0].toUpperCase() }}</div>
      </div>
      <h2 class="profile-name">{{ authStore.userInfo?.username || '用户' }}</h2>
      <div class="profile-tabs">
        <button :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">基本资料</button>
        <button :class="{ active: activeTab === 'avatar' }" @click="activeTab = 'avatar'">更换头像</button>
        <button :class="{ active: activeTab === 'password' }" @click="activeTab = 'password'">设置密码</button>
      </div>
    </aside>

    <main class="profile-main">
      <div class="glass-card profile-form">
        <!-- 基本资料 -->
        <form v-if="activeTab === 'info'" @submit.prevent="saveInfo">
          <div class="form-field"><label>昵称</label><input v-model="nickname" class="glass-input"></div>
          <div class="form-field"><label>邮箱</label><input v-model="email" type="email" class="glass-input"></div>
          <button type="submit" class="btn-gradient">保存修改</button>
        </form>
        <!-- 更换头像 -->
        <div v-if="activeTab === 'avatar'" class="avatar-upload">
          <div class="avatar-preview-lg">{{ (authStore.userInfo?.username || 'U')[0].toUpperCase() }}</div>
          <input type="file" accept="image/*" @change="onAvatarChange">
          <button class="btn-glass" style="margin-top:12px;">选择图片</button>
        </div>
        <!-- 设置密码 -->
        <form v-if="activeTab === 'password'" @submit.prevent="savePassword">
          <div class="form-field"><label>旧密码</label><input v-model="oldPassword" type="password" class="glass-input"></div>
          <div class="form-field"><label>新密码</label><input v-model="newPassword" type="password" class="glass-input"></div>
          <div class="form-field"><label>确认密码</label><input v-model="confirmPwd" type="password" class="glass-input"></div>
          <div class="password-strength">
            <div class="strength-bar" :style="{ width: passwordStrength + '%', background: strengthColor }"></div>
          </div>
          <button type="submit" class="btn-gradient">更新密码</button>
        </form>
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.profile-page { display: flex; gap: var(--space-md); padding: var(--space-md); max-width: 1000px; margin: 0 auto; min-height: calc(100vh - 64px - 80px); }

.profile-sidebar { width: 220px; padding: var(--space-xl) var(--space-md); text-align: center; display: flex; flex-direction: column; align-items: center; gap: var(--space-md); }

.avatar-circle {
  width: 72px; height: 72px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  border: 3px solid rgba(255,107,157,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; font-weight: 800; color: #fff;
}

.profile-name { font-family: var(--font-display); font-size: 16px; margin: 0; }

.profile-tabs { display: flex; flex-direction: column; gap: var(--space-xs); width: 100%;
  button { padding: 10px; border: none; border-radius: 8px; background: transparent; color: var(--text-secondary); cursor: pointer; font-size: 13px; transition: all var(--dur-fast);
    &:hover { background: rgba(255,255,255,0.04); }
    &.active { background: rgba(255,107,157,0.1); color: var(--accent-pink); }
  }
}

.profile-main { flex: 1; }

.profile-form { padding: var(--space-xl); }

.form-field { margin-bottom: var(--space-md);
  label { display: block; font-size: 12px; color: var(--text-secondary); margin-bottom: var(--space-xs); }
}

.password-strength { height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; margin: var(--space-sm) 0 var(--space-md); overflow: hidden; }
.strength-bar { height: 100%; border-radius: 2px; transition: width var(--dur-base) var(--ease-smooth); }
</style>
```

- [ ] **Step 3: 重写 `NotFoundView.vue`**

保持 `<script setup>` 不变，仅替换 `<template>` 和 `<style>`。

```vue
<template>
  <div class="notfound-page">
    <div class="nf-glow nf-glow--pink"></div>
    <div class="nf-glow nf-glow--purple"></div>

    <h1 class="nf-code gradient-text">404</h1>
    <p class="nf-message">页面飞走了 ✦</p>
    <p class="nf-sub">你访问的页面不存在或已被移除</p>

    <div class="nf-actions">
      <router-link to="/home" class="btn-gradient">返回首页</router-link>
      <button class="btn-glass" @click="$router.go(-1)">返回上一页</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.notfound-page {
  min-height: calc(100vh - 64px - 80px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.nf-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.1;
  pointer-events: none;
  &--pink { width: 300px; height: 300px; background: var(--accent-pink); top: 10%; left: 20%; }
  &--purple { width: 250px; height: 250px; background: var(--accent-purple); bottom: 10%; right: 20%; }
}

.nf-code {
  font-family: var(--font-display);
  font-size: 120px;
  font-weight: 800;
  animation: nfBreathe 3s ease-in-out infinite;
  position: relative;
  z-index: 1;
}

.nf-message { font-family: var(--font-display); font-size: 22px; color: var(--text-primary); margin: 0 0 var(--space-sm); position: relative; z-index: 1; }
.nf-sub { font-size: 14px; color: var(--text-muted); margin: 0 0 var(--space-xl); position: relative; z-index: 1; }

.nf-actions { display: flex; gap: var(--space-md); position: relative; z-index: 1; }

@keyframes nfBreathe {
  0%, 100% { opacity: 1; filter: drop-shadow(0 0 20px rgba(255,107,157,0.3)); }
  50% { opacity: 0.85; filter: drop-shadow(0 0 40px rgba(167,139,250,0.4)); }
}
</style>
```

- [ ] **Step 4: 提交**

```bash
git add frontend/src/views/LibraryView.vue frontend/src/views/UserProfileView.vue frontend/src/views/NotFoundView.vue
git commit -m "feat: 图像库/个人中心/404 三页重写 — 毛玻璃侧栏/渐变头像/呼吸404"
```

---

### Self-Review

**1. Spec coverage:**
- 色彩令牌 → Task 1 Step 2 (all color tokens defined)
- 字体 → Task 1 Step 1 (Google Fonts) + Step 2 (font tokens)
- 组件风格 → Task 1 Step 2 (glass-card, btn-gradient, btn-glass, glass-input)
- 动效体系 → Task 1 Step 2 (easing tokens, keyframes, reduced-motion)
- 间距体系 → Task 1 Step 2 (spacing tokens)
- 首页 → Task 3
- 工作区 → Task 4
- 登录页 → Task 5
- 图像库 → Task 6 Step 1
- 个人中心 → Task 6 Step 2
- 404 → Task 6 Step 3
- 布局组件 → Task 2

**2. Placeholder scan:** No "TBD", "TODO", or vague instructions. All code is concrete.

**3. Type consistency:** Vue template bindings reference data properties from existing script setup sections, which are preserved. No cross-task naming conflicts.
