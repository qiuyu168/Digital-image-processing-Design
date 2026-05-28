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
