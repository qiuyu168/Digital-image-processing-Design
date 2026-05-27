<template>
  <section id="features" class="section-block feature-section">
    <div class="section-header">
      <span class="section-eyebrow">Highlights</span>
      <h2 class="section-title">项目特色</h2>
      <p class="section-subtitle">精心设计,兼顾功能体验与视觉表现</p>
    </div>

    <div class="feature-grid">
      <div
        v-for="item in featureList"
        :key="item.title"
        class="feature-card"
      >
        <div class="feature-icon">{{ item.icon }}</div>
        <h3>{{ item.title }}</h3>
        <p>{{ item.desc }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
const featureList = [
  {
    icon: '🧩',
    title: '前后端分离',
    desc: 'Vue3 负责页面交互与结果展示,后端 FastAPI 负责图像处理算法和接口服务。'
  },
  {
    icon: '📦',
    title: '算法模块化',
    desc: '每类算法独立管理,便于小组成员分工开发和后续功能扩展。'
  },
  {
    icon: '🔍',
    title: '处理结果对比',
    desc: '支持原图、结果图和中间步骤图展示,便于观察算法处理效果。'
  },
  {
    icon: '🎯',
    title: '交互直观',
    desc: '界面简洁,操作流畅,每一步都有清晰的视觉反馈与引导。'
  }
]
</script>

<style lang="scss" scoped>
@import url(@/styles/index.scss);

.section-block {
  margin-bottom: 64px;
  scroll-margin-top: 80px;
}

.feature-section {
  margin-bottom: 8px;
}

.section-header {
  text-align: left;
  margin-bottom: 32px;
}

.section-eyebrow {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  font-weight: 700;
  color: var(--c-amber);
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.section-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.3px;
}

.section-subtitle {
  margin: 8px 0 0;
  color: var(--c-ink-2);
  font-size: 15px;
}

/* =============== Feature grid =============== */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.feature-card {
  padding: 24px 20px;
  border-radius: var(--radius-lg);
  text-align: left;
  background: #fff;
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
  transition:
    box-shadow var(--dur-fast) var(--ease-standard),
    transform var(--dur-fast) var(--ease-standard);

  animation: cardFadeUp var(--dur-base) var(--ease-standard) both;

  &:hover {
    box-shadow: var(--shadow-2);
    transform: translateY(-1px);
  }
}

@keyframes cardFadeUp {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-icon {
  width: 40px;
  height: 40px;
  margin: 0 0 16px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.feature-card h3 {
  margin: 0 0 8px;
  color: var(--c-ink);
  font-size: 16px;
  font-weight: 700;
}

.feature-card p {
  margin: 0;
  line-height: 1.65;
  color: var(--c-ink-2);
  font-size: 13px;
}

/* =============== Responsive =============== */
@media (max-width: 1100px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 680px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
