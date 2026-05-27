<!-- 极淡暖色尘埃漂浮,WWDC chrome 风格,几乎不可察觉 -->
<template>
  <div class="warm-dust" aria-hidden="true">
    <span class="dust dust-1"></span>
    <span class="dust dust-2"></span>
    <span class="dust dust-3"></span>
    <span class="dust dust-4"></span>
    <span class="dust dust-5"></span>
  </div>
</template>

<script setup>
</script>

<style lang="scss" scoped>
.warm-dust {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.dust {
  position: absolute;
  border-radius: 50%;
  filter: blur(8px);
  will-change: transform, opacity;
}

.dust-1 {
  left: 6%;
  top: 18%;
  width: 18px;
  height: 18px;
  background: var(--c-amber);
  animation: warmDustDrift 32s ease-in-out infinite;
}

.dust-2 {
  left: 78%;
  top: 12%;
  width: 14px;
  height: 14px;
  background: var(--c-peach);
  animation: warmDustDriftAlt 44s ease-in-out infinite;
}

.dust-3 {
  left: 22%;
  top: 72%;
  width: 16px;
  height: 16px;
  background: var(--c-peach);
  animation: warmDustDriftAlt 38s ease-in-out infinite;
  animation-delay: -8s;
}

.dust-4 {
  left: 62%;
  top: 60%;
  width: 12px;
  height: 12px;
  background: var(--c-amber);
  animation: warmDustDrift 40s ease-in-out infinite;
  animation-delay: -12s;
}

.dust-5 {
  left: 88%;
  top: 82%;
  width: 14px;
  height: 14px;
  background: var(--c-peach);
  animation: warmDustDriftAlt 50s ease-in-out infinite;
  animation-delay: -20s;
}
</style>
