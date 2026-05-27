<template>
  <section id="modules" class="section-block">
    <div class="section-header">
      <span class="section-eyebrow">Algorithms</span>
      <h2 class="section-title">算法模块</h2>
      <p class="section-subtitle">六大图像处理方向,覆盖数字图像处理核心算法</p>
    </div>

    <div class="algorithm-showcase">
      <!-- Featured large card -->
      <div class="featured-card" :style="{ '--card-delay': '0ms' }">
        <div class="featured-icon">{{ currentModule.icon }}</div>
        <div class="featured-body">
          <h3>{{ currentModule.title }}</h3>
          <p>{{ currentModule.desc }}</p>
          <div class="featured-tags">
            <span v-for="tag in currentModule.tags" :key="tag">{{ tag }}</span>
          </div>
          <el-button class="featured-cta" @click="handleCTA">
            进入处理
            <span class="arrow">&rarr;</span>
          </el-button>
        </div>
      </div>

      <!-- Compact card list -->
      <div class="compact-list">
        <div
          v-for="(mod, index) in modules"
          :key="mod.title"
          class="compact-card"
          :class="{ 'is-selected': selectedIndex === index }"
          @mouseenter="selectedIndex = index"
          @click="handleSelect(index)"
        >
          <div class="compact-icon">{{ mod.icon }}</div>
          <div class="compact-info">
            <h4>{{ mod.title }}</h4>
            <div class="compact-tags">
              <span v-for="tag in mod.tags" :key="tag">{{ tag }}</span>
            </div>
          </div>
          <div class="compact-arrow">&rarr;</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  modules: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['select-module'])

const router = useRouter()
const selectedIndex = ref(0)

const currentModule = computed(() => props.modules[selectedIndex.value])

function handleCTA() {
  router.push('/workspace')
}

function handleSelect(index) {
  emit('select-module', index)
  router.push('/workspace')
}
</script>

<style lang="scss" scoped>
@import url(@/styles/index.scss);

.section-block {
  margin-bottom: 64px;
  scroll-margin-top: 80px;
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

/* =============== Algorithm showcase =============== */
.algorithm-showcase {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  align-items: flex-start;
}

/* =============== Featured large card =============== */
.featured-card {
  display: flex;
  gap: 24px;
  padding: 28px 24px;
  border-radius: var(--radius-lg);
  background: #fff;
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
  animation: cardFadeUp var(--dur-base) var(--ease-standard) both;
  animation-delay: var(--card-delay, 0ms);
  transition:
    box-shadow var(--dur-fast) var(--ease-standard),
    border-color var(--dur-fast) var(--ease-standard);
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

.featured-icon {
  width: 64px;
  height: 64px;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  background: var(--c-peach);
}

.featured-body {
  flex: 1;
  min-width: 0;
}

.featured-body h3 {
  margin: 0 0 10px;
  font-size: 20px;
  font-weight: 700;
  color: var(--c-ink);
}

.featured-body p {
  margin: 0 0 16px;
  color: var(--c-ink-2);
  line-height: 1.65;
  font-size: 14px;
}

.featured-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 20px;
}

.featured-tags span {
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  color: var(--c-ink-2);
  font-size: 12px;
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.featured-cta {
  border: none;
  background: var(--c-amber);
  color: #fff;
  font-weight: 600;
  border-radius: var(--radius-md);
  padding: 10px 20px;
  height: auto;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: background var(--dur-fast) ease;

  .arrow {
    transition: transform var(--dur-fast) var(--ease-standard);
  }

  &:hover {
    background: var(--c-amber-2);
    color: #fff;

    .arrow {
      transform: translateX(3px);
    }
  }
}

/* =============== Compact card list =============== */
.compact-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.compact-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: var(--radius-md);
  background: #fff;
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
  cursor: pointer;
  transition:
    box-shadow var(--dur-fast) var(--ease-standard),
    border-color var(--dur-fast) var(--ease-standard),
    transform var(--dur-fast) var(--ease-standard);

  animation: cardFadeUp var(--dur-base) var(--ease-standard) both;
  animation-delay: calc(var(--card-delay, 0ms) + 60ms);

  &:hover {
    box-shadow: var(--shadow-2);
    border-color: rgba(217, 119, 6, 0.25);
    transform: translateY(-1px);
  }

  &.is-selected {
    border-color: var(--c-amber);
    background: var(--c-cream);
  }
}

.compact-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  background: var(--c-cream-2);
}

.compact-info {
  flex: 1;
  min-width: 0;
}

.compact-info h4 {
  margin: 0 0 4px;
  font-size: 13px;
  font-weight: 700;
  color: var(--c-ink);
}

.compact-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.compact-tags span {
  padding: 2px 8px;
  border-radius: 4px;
  color: var(--c-ink-2);
  font-size: 10px;
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.compact-arrow {
  color: var(--c-ink-2);
  font-size: 14px;
  transition: transform var(--dur-fast) var(--ease-standard), color var(--dur-fast) var(--ease-standard);
}

.compact-card:hover .compact-arrow {
  transform: translateX(3px);
  color: var(--c-amber);
}

.compact-card.is-selected .compact-arrow {
  color: var(--c-amber);
}

/* =============== Responsive =============== */
@media (max-width: 1100px) {
  .algorithm-showcase {
    grid-template-columns: 1fr;
  }

  .compact-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
}

@media (max-width: 680px) {
  .featured-card {
    flex-direction: column;
    gap: 16px;
  }

  .compact-list {
    grid-template-columns: 1fr;
  }
}
</style>
