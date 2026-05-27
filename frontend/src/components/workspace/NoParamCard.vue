<template>
  <div class="no-param-card" :class="`module-tone-${moduleName}`">
    <div class="no-param-illust" aria-hidden="true">
      <svg viewBox="0 0 64 64" width="56" height="56">
        <circle cx="32" cy="32" r="28" fill="none" stroke="#5a4f43" stroke-width="1.5" opacity="0.35" />
        <polyline points="20,33 28,41 44,24" fill="none" stroke="#d97706" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </div>
    <h4>无可变参数</h4>
    <p>该算法直接对图像执行处理，无需手动调节，点击下方「开始处理」即可。</p>
  </div>
</template>

<script setup>
defineProps({
  moduleName: { type: String, default: '' }
})
</script>

<style lang="scss" scoped>
.no-param-card {
  position: relative;
  margin: 4px 0 20px;
  padding: 32px 24px;
  border-radius: var(--radius-lg);
  text-align: center;
  background: var(--c-cream);
  border: 1px solid var(--c-line);
  animation: noParamIn var(--dur-slow) var(--ease-decel) both;
}

@keyframes noParamIn {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}

.no-param-illust {
  position: relative;
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.no-param-card h4 {
  position: relative;
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.1px;
}

.no-param-card h4::after {
  content: "";
  display: block;
  width: 32px;
  height: 2px;
  margin: 8px auto 0;
  background: var(--c-amber);
  border-radius: 2px;
}

.no-param-card p {
  position: relative;
  margin: 12px auto 0;
  max-width: 320px;
  color: var(--c-ink-2);
  font-size: 13px;
  line-height: 1.7;
}

.module-tone-grayscale_image,
.module-tone-color_image,
.module-tone-geometric_transform,
.module-tone-spatial_filter,
.module-tone-frequency_analysis,
.module-tone-frequency_filter {
  border-left: 3px solid var(--c-amber);
}
</style>
