<template>
  <section class="panel-card algorithm-info-card">
    <div class="panel-title">
      <div class="title-left">
        <span class="title-icon">🪄</span>
        <div>
          <h3>{{ algorithm?.displayName || '请选择算法' }}</h3>
          <p>
            {{
              algorithm?.description ||
              '请从左侧选择一个具体算法。'
            }}
          </p>
        </div>
      </div>

      <el-tag v-if="moduleDisplayName" class="soft-tag">
        {{ moduleDisplayName }}
      </el-tag>
    </div>
  </section>
</template>

<script setup>
defineProps({
  algorithm: { type: Object, default: null },
  moduleDisplayName: { type: String, default: '' }
})
</script>

<style lang="scss" scoped>
.panel-card {
  padding: 24px;
  border-radius: var(--radius-lg);
  background: #fff;
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
}

.algorithm-info-card {
  margin-bottom: 0;
}

.panel-title {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 0;
}

.title-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.panel-title h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.2px;
}

.panel-title p {
  margin: 4px 0 0;
  color: var(--c-ink-2);
  font-size: 13px;
  line-height: 1.6;
}

.soft-tag {
  border: 1px solid var(--c-line);
  color: var(--c-amber);
  background: var(--c-peach);
  border-radius: var(--radius-sm);
  font-weight: 600;
}

@media (max-width: 680px) {
  .panel-card {
    padding: 18px;
  }

  .panel-title {
    flex-direction: column;
  }
}
</style>
