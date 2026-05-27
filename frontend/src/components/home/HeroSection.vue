<template>
  <section id="hero" class="hero-section">
    <div class="hero-layout">
      <!-- Left 60%: Carousel text -->
      <div class="hero-content-col">
        <el-carousel
          height="420px"
          indicator-position="outside"
          arrow="always"
          class="hero-carousel"
        >
          <el-carousel-item
            v-for="item in carouselList"
            :key="item.title"
          >
            <div class="hero-slide">
              <div class="hero-content">
                <div class="hero-tag">{{ item.tag }}</div>
                <h1>{{ item.title }}</h1>
                <p>{{ item.desc }}</p>
                <div class="hero-actions">
                  <el-button class="btn-primary" @click="$router.push('/workspace')">
                    开始处理图像
                  </el-button>
                  <el-button class="btn-ghost" @click="$router.push('/profile')">
                    查看个人信息
                  </el-button>
                </div>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>

      <!-- Right 40%: Stacked step-cards -->
      <div class="hero-panel-col">
        <div class="step-card-stack">
          <div class="step-card">
            <div
              v-for="(step, stepIndex) in panelSteps"
              :key="step"
              class="step-row"
            >
              <span class="step-no">0{{ stepIndex + 1 }}</span>
              <span class="step-label">{{ step }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const panelSteps = ['上传图片', '选择算法', '参数调节', '查看结果']

const carouselList = [
  {
    tag: 'Anime Image Processing',
    title: '基于动漫图像识别的交互式数字图像处理系统',
    desc: '支持动漫人物、头像、插画、场景截图等图片的上传、算法处理、结果展示与分析。',
    panelSteps: ['上传图片', '选择算法', '参数调节', '查看结果']
  },
  {
    tag: 'Digital Image Processing',
    title: '覆盖多类数字图像处理算法',
    desc: '集成灰度、彩色、几何、空域、频域等经典模块,满足多种处理需求。',
    panelSteps: ['灰度处理', '空域滤波', '频域分析', '边缘增强']
  },
  {
    tag: 'Visual Experience',
    title: '直观的交互与可视化反馈',
    desc: '每一步操作都配有即时预览与对比,帮助你直观理解图像处理效果。',
    panelSteps: ['原图预览', '处理过程', '结果对比', '细节查看']
  }
]
</script>

<style lang="scss" scoped>
@import url(@/styles/index.scss);

.hero-section {
  margin-bottom: 56px;
  animation: heroFadeUp var(--dur-base) var(--ease-standard) both;
}

@keyframes heroFadeUp {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 40px;
  align-items: stretch;
}

.hero-content-col {
  min-width: 0;
}

.hero-panel-col {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* =============== Carousel =============== */
.hero-carousel {
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-2);
  background: #fff;
  border: 1px solid var(--c-line);
}

.hero-slide {
  position: relative;
  height: 100%;
  padding: 0 56px;
  display: flex;
  align-items: center;
  background:
    radial-gradient(circle at 88% 18%, rgba(217, 119, 6, 0.08), transparent 40%),
    #fff;
}

.hero-content {
  flex: 1;
  min-width: 0;
}

.hero-tag {
  display: inline-flex;
  padding: 4px 12px;
  margin-bottom: 20px;
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.6px;
  color: var(--c-amber);
  background: transparent;
  border: 1px solid var(--c-line);
}

.hero-content h1 {
  max-width: 600px;
  margin: 0 0 16px;
  font-size: 32px;
  line-height: 1.3;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.3px;
}

.hero-content p {
  max-width: 560px;
  margin: 0 0 28px;
  color: var(--c-ink-2);
  font-size: 15px;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  gap: 12px;
}

.btn-primary {
  border: none;
  background: var(--c-amber);
  color: #fff;
  font-weight: 600;
  border-radius: var(--radius-md);
  padding: 12px 22px;
  height: auto;
  transition: background var(--dur-fast) ease;

  &:hover, &:focus {
    background: var(--c-amber-2);
    color: #fff;
  }
}

.btn-ghost {
  color: var(--c-ink);
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-md);
  padding: 12px 22px;
  height: auto;
  font-weight: 600;
  transition: border-color var(--dur-fast) ease, background var(--dur-fast) ease;

  &:hover, &:focus {
    background: var(--c-cream-2);
    border-color: rgba(43, 36, 25, 0.18);
    color: var(--c-ink);
  }
}

/* =============== Stacked step-cards =============== */
.step-card-stack {
  position: relative;
  width: 100%;
}

.step-card-stack::before,
.step-card-stack::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-lg);
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
  pointer-events: none;
}

.step-card-stack::after {
  /* bottom card */
  background: var(--c-cream);
  z-index: 1;
  transform: translate(8px, 8px);
}

.step-card-stack::before {
  /* middle card */
  background: var(--c-cream-2);
  z-index: 2;
  transform: translate(4px, 4px);
}

.step-card {
  position: relative;
  z-index: 3;
  background: #fff;
  border: 2px solid var(--c-amber);
  border-radius: var(--radius-lg);
  padding: 16px;
  box-shadow: var(--shadow-2);
  display: grid;
  gap: 8px;
}

.step-row {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: var(--c-cream);
  border-radius: var(--radius-md);
  border: 1px solid var(--c-line);

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 10px;
    bottom: 10px;
    width: 3px;
    border-radius: 2px;
    background: var(--c-amber);
  }
}

.step-no {
  font-size: 12px;
  font-weight: 700;
  color: var(--c-amber);
  font-family: 'SF Mono', 'Consolas', monospace;
}

.step-label {
  color: var(--c-ink);
  font-weight: 600;
  font-size: 14px;
}

/* =============== Carousel indicators =============== */
:deep(.el-carousel__indicators--outside) {
  margin-top: 16px;
}

:deep(.el-carousel__button) {
  width: 20px;
  height: 3px;
  border-radius: 999px;
  background-color: rgba(43, 36, 25, 0.18);
  opacity: 1;
}

:deep(.el-carousel__button.is-active) {
  background-color: var(--c-amber);
}

:deep(.el-carousel__arrow) {
  background-color: rgba(255, 255, 255, 0.85);
  color: var(--c-ink);
  border: 1px solid var(--c-line);
}

:deep(.el-carousel__arrow:hover) {
  background-color: #fff;
  color: var(--c-amber);
}

/* =============== Responsive =============== */
@media (max-width: 1100px) {
  .hero-layout {
    grid-template-columns: 1fr;
  }

  .hero-panel-col {
    display: none;
  }

  .hero-slide {
    padding: 0 32px;
  }

  .hero-content h1 {
    font-size: 28px;
  }
}

@media (max-width: 680px) {
  .hero-slide {
    padding: 0 20px;
  }

  .hero-content h1 {
    font-size: 24px;
  }

  .hero-content p {
    font-size: 14px;
  }

  .hero-actions {
    flex-direction: column;
  }
}
</style>
