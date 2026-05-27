<script setup>
// Static content component — no props or emits.
</script>

<template>
  <aside class="hero-pane">
    <div class="hero-inner">
      <div class="brand-row">
        <span class="brand-dot" />
        <span class="brand-name">动漫图像处理系统</span>
      </div>

      <span class="hero-tag">Anime Image Processing</span>
      <h1 class="hero-title">基于动漫图像识别的交互式数字图像处理系统</h1>
      <p class="hero-desc">
        支持动漫人物、头像、插画、场景截图等图片的上传、算法处理、结果展示与分析。
      </p>

      <!-- 3 cascading step cards (overlapping visual) -->
      <div class="cascade-steps">
        <div class="cascade-card card-front">
          <div class="step-row">
            <span class="step-no">01</span>
            <span class="step-label">上传图片</span>
          </div>
          <div class="step-row">
            <span class="step-no">02</span>
            <span class="step-label">选择算法</span>
          </div>
        </div>
        <div class="cascade-card card-mid">
          <div class="step-row">
            <span class="step-no">03</span>
            <span class="step-label">参数调节</span>
          </div>
        </div>
        <div class="cascade-card card-back">
          <div class="step-row">
            <span class="step-no">04</span>
            <span class="step-label">查看结果</span>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<style lang="scss" scoped>
.hero-pane {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 56px;
}

.hero-inner {
  max-width: 460px;
  width: 100%;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 40px;
  color: var(--c-ink);
  font-size: 16px;
  font-weight: 700;
}

.brand-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--c-amber);
}

.hero-tag {
  display: inline-flex;
  padding: 4px 12px;
  margin-bottom: 20px;
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.6px;
  color: var(--c-amber);
  border: 1px solid var(--c-line);
}

.hero-title {
  margin: 0 0 16px;
  font-size: 28px;
  line-height: 1.35;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.3px;
}

.hero-desc {
  margin: 0 0 32px;
  color: var(--c-ink-2);
  font-size: 14px;
  line-height: 1.7;
}

/* ============== Cascade step cards ============== */
.cascade-steps {
  display: flex;
  flex-direction: column;
}

.cascade-card {
  position: relative;
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all var(--dur-fast) var(--ease-standard);
}

.card-front {
  z-index: 3;
  box-shadow: var(--shadow-2);
  border-left: 3px solid var(--c-amber);
}

.card-mid {
  z-index: 2;
  margin-top: -16px;
  margin-left: 20px;
  opacity: 0.68;
  box-shadow: var(--shadow-1);
}

.card-back {
  z-index: 1;
  margin-top: -16px;
  margin-left: 40px;
  opacity: 0.44;
  box-shadow: var(--shadow-1);
}

.step-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 0;
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
  font-size: 13px;
}
</style>
