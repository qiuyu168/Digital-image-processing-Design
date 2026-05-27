<template>
  <section id="flow" class="section-block">
    <div class="section-header">
      <span class="section-eyebrow">Workflow</span>
      <h2 class="section-title">功能流程</h2>
      <p class="section-subtitle">简单几步,完成动漫图像的处理与预览</p>
    </div>

    <div class="flow-indicator">
      <template v-for="(item, index) in flowList" :key="item.title">
        <div class="flow-step" :style="{ '--step-delay': `${index * 60}ms` }">
          <div class="flow-circle">
            <span>{{ index + 1 }}</span>
          </div>
          <div class="flow-text">
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
          </div>
        </div>
        <!-- Connecting line between steps -->
        <div
          v-if="index < flowList.length - 1"
          class="flow-connector"
          :class="{ 'connector-active': index === 0 }"
        />
      </template>
    </div>
  </section>
</template>

<script setup>
const flowList = [
  { icon: '📤', title: '上传图片', desc: '选择本地动漫图片、头像或插画素材。' },
  { icon: '🪄', title: '选择算法', desc: '从灰度、彩色、几何、空域、频域等模块中选择算法。' },
  { icon: '🎚️', title: '调整参数', desc: '设置阈值、滤波核、旋转角度等参数。' },
  { icon: '🖼️', title: '查看结果', desc: '展示处理前后对比、分步过程与指标分析。' }
]
</script>

<style lang="scss" scoped>
@import url(@/styles/index.scss);

.section-block {
  margin-bottom: 64px;
  scroll-margin-top: 80px;
}

.section-header {
  text-align: left;
  margin-bottom: 40px;
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

/* =============== Horizontal step indicator =============== */
.flow-indicator {
  display: flex;
  align-items: flex-start;
  gap: 0;
}

.flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  flex: 1;
  animation: flowStepFadeUp var(--dur-base) var(--ease-standard) both;
  animation-delay: var(--step-delay, 0ms);
}

@keyframes flowStepFadeUp {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.flow-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  font-family: 'SF Mono', 'Consolas', monospace;
  background: #fff;
  border: 2px solid var(--c-line);
  color: var(--c-ink-2);
  flex-shrink: 0;
  transition:
    background var(--dur-fast) var(--ease-standard),
    border-color var(--dur-fast) var(--ease-standard),
    color var(--dur-fast) var(--ease-standard),
    box-shadow var(--dur-fast) var(--ease-standard);
}

.flow-step:hover .flow-circle {
  background: var(--c-amber);
  border-color: var(--c-amber);
  color: #fff;
  box-shadow: 0 0 0 4px rgba(217, 119, 6, 0.12);
}

.flow-text {
  text-align: center;
  max-width: 200px;
}

.flow-text h3 {
  margin: 0 0 8px;
  font-size: 16px;
  color: var(--c-ink);
  font-weight: 700;
}

.flow-text p {
  margin: 0;
  line-height: 1.65;
  color: var(--c-ink-2);
  font-size: 13px;
}

/* =============== Connecting line =============== */
.flow-connector {
  flex: 0 0 48px;
  height: 2px;
  align-self: center;
  background: var(--c-line);
  margin: 0 8px;
  margin-bottom: 64px; /* offset to align with circles */
  border-radius: 1px;
  transition: background var(--dur-fast) var(--ease-standard);

  &.connector-active {
    background: var(--c-amber);
    height: 3px;
  }

  &:hover {
    background: var(--c-amber);
    height: 3px;
  }
}

/* =============== Responsive =============== */
@media (max-width: 1100px) {
  .flow-indicator {
    flex-wrap: wrap;
    gap: 24px;
  }

  .flow-step {
    flex-direction: row;
    flex: 1 1 45%;
    animation-delay: 0ms;
  }

  .flow-text {
    text-align: left;
  }

  .flow-connector {
    display: none;
  }
}

@media (max-width: 680px) {
  .flow-step {
    flex: 1 1 100%;
  }
}
</style>
