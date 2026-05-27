<template>
  <section class="panel-card library-header-card">
    <div class="header-hero">
      <div class="hero-left">
        <span class="eyebrow">Library</span>
        <h3>{{ activeCategoryName }}</h3>
      </div>

      <div v-if="activeCategoryName" class="hero-metric">
        <div class="metric-number">{{ totalCount }}</div>
        <div class="metric-label">张图片</div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  totalCount: { type: Number, default: 0 },
  activeCategoryName: { type: String, default: '' }
})
</script>

<style scoped>
.panel-card {
  padding: 24px;
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-1);
}

.library-header-card {
  margin-bottom: 0;
}

.header-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.eyebrow {
  display: block;
  margin-bottom: 6px;
  font-size: 11px;
  font-weight: 700;
  color: var(--c-amber);
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.hero-left h3 {
  margin: 0;
  color: var(--c-ink);
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.hero-metric {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.metric-number {
  color: var(--c-amber);
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -1px;
  font-family: 'SF Mono', 'Consolas', monospace;
}

.metric-label {
  color: var(--c-ink-2);
  font-size: 12px;
  font-weight: 500;
}
</style>
