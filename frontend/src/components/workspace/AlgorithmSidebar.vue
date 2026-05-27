<template>
  <aside class="algorithm-sidebar">
    <div class="sidebar-header">
      <div>
        <h2>算法模块</h2>
      </div>

      <el-button
        class="refresh-btn"
        circle
        :loading="algorithmLoading"
        @click="$emit('refresh')"
      >
        <el-icon><Refresh /></el-icon>
      </el-button>
    </div>

    <el-skeleton v-if="algorithmLoading" :rows="9" animated />

    <el-empty
      v-else-if="modules.length === 0"
      description="暂无算法数据，请检查后端接口"
      :image-size="96"
    />

    <el-scrollbar v-else class="menu-scroll">
      <el-menu
        class="algorithm-menu"
        :default-active="activeMenuKey"
        :default-openeds="openModuleKeys"
        @select="(idx) => $emit('select', idx)"
      >
        <el-sub-menu
          v-for="(moduleItem, moduleIndex) in modules"
          :key="moduleItem.key"
          :index="moduleItem.key"
        >
          <template #title>
            <span class="module-title">
              <span class="module-icon">{{ getModuleIcon(moduleIndex) }}</span>
              <span class="module-name">{{ moduleItem.displayName }}</span>
              <span class="module-count">{{ moduleItem.algorithms.length }}</span>
              <span class="module-spacer"></span>
            </span>
          </template>

          <el-menu-item
            v-for="algorithm in moduleItem.algorithms"
            :key="algorithm.key"
            :index="`${moduleItem.key}::${algorithm.key}`"
          >
            <span class="algorithm-name">{{ algorithm.displayName }}</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-scrollbar>
  </aside>
</template>

<script setup>
import { Refresh } from '@element-plus/icons-vue'

const moduleIconList = ['🌗', '🎨', '📐', '🫧', '🌌', '⚡', '🌸', '✨']

defineProps({
  modules: { type: Array, required: true },
  activeMenuKey: { type: String, default: '' },
  openModuleKeys: { type: Array, default: () => [] },
  algorithmLoading: { type: Boolean, default: false }
})

defineEmits(['select', 'refresh'])

function getModuleIcon(index) {
  return moduleIconList[index % moduleIconList.length]
}
</script>

<style lang="scss" scoped>
.algorithm-sidebar {
  position: sticky;
  top: 88px;
  min-height: 640px;
  max-height: calc(100vh - 112px);
  padding: 20px 14px;
  overflow: hidden;
  border-radius: var(--radius-lg);
  background: #fff;
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 4px 8px 16px;
  border-bottom: 1px solid var(--c-line);
  margin-bottom: 12px;
  flex-shrink: 0;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.2px;
}

.refresh-btn {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  color: var(--c-ink-2);
  background: transparent;
  border: 1px solid var(--c-line);
  transition: color var(--dur-fast) var(--ease-standard),
              border-color var(--dur-fast) var(--ease-standard),
              background var(--dur-fast) var(--ease-standard);
}

.refresh-btn:hover {
  color: var(--c-amber);
  border-color: rgba(217, 119, 6, 0.3);
  background: rgba(217, 119, 6, 0.06);
}

.menu-scroll {
  flex: 1;
  min-height: 0;
}

.algorithm-menu {
  border-right: none;
  background: transparent;
}

.module-title {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-right: 22px;
}

.module-icon {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  background: var(--c-cream-2);
}

.module-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--c-ink);
}

.module-spacer {
  flex: 1;
}

.module-count {
  min-width: 22px;
  height: 20px;
  padding: 0 7px;
  margin-left: 4px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--c-amber);
  font-size: 11px;
  font-weight: 700;
  font-family: 'SF Mono', 'Consolas', monospace;
  background: var(--c-peach);
}

.algorithm-name {
  font-size: 13px;
}

:deep(.el-menu) {
  background: transparent;
}

:deep(.el-sub-menu__title) {
  height: 42px;
  padding: 0 10px !important;
  border-radius: var(--radius-md);
  color: var(--c-ink);
  transition: background var(--dur-fast) var(--ease-standard);
}

:deep(.el-sub-menu__title:hover) {
  background: var(--c-cream-2);
}

:deep(.el-menu-item) {
  height: 36px;
  margin: 2px 0;
  padding-left: 44px !important;
  border-radius: var(--radius-md);
  color: var(--c-ink-2);
  font-size: 13px;
  transition: color var(--dur-fast) var(--ease-standard),
              background var(--dur-fast) var(--ease-standard);
}

:deep(.el-menu-item:hover) {
  color: var(--c-ink);
  background: var(--c-cream-2);
}

:deep(.el-menu-item.is-active) {
  color: var(--c-amber);
  font-weight: 600;
  background: rgba(217, 119, 6, 0.08);
}

:deep(.el-sub-menu__icon-arrow) {
  color: var(--c-ink-2);
}
</style>
