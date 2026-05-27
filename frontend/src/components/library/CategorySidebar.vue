<template>
  <aside class="category-sidebar">
    <div class="sidebar-header">
      <div>
        <span class="eyebrow">Categories</span>
        <h2>图像分类</h2>
      </div>

      <el-button
        class="refresh-btn"
        circle
        :loading="loading"
        @click="$emit('refresh')"
      >
        <el-icon><Refresh /></el-icon>
      </el-button>
    </div>

    <el-skeleton v-if="loading" :rows="8" animated />

    <el-empty
      v-else-if="categories.length === 0"
      description="暂无图像分类"
      :image-size="92"
    />

    <el-scrollbar v-else class="category-scroll">
      <el-menu
        class="category-menu"
        :default-active="activeCategory"
        @select="(index) => $emit('select-category', index)"
      >
        <el-menu-item
          v-for="category in categories"
          :key="category.name"
          :index="category.name"
        >
          <span class="category-title">
            <span class="category-dot"></span>
            <span class="category-name">{{ category.displayName }}</span>
            <span class="category-count">{{ category.count }}</span>
          </span>
        </el-menu-item>
      </el-menu>
    </el-scrollbar>
  </aside>
</template>

<script setup>
import { Refresh } from '@element-plus/icons-vue'

defineProps({
  categories: { type: Array, default: () => [] },
  activeCategory: { type: String, default: '' },
  loading: { type: Boolean, default: false }
})

defineEmits(['select-category', 'refresh'])
</script>

<style scoped>
.category-sidebar {
  position: sticky;
  top: 88px;
  align-self: flex-start;
  padding: 20px 14px;
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-1);
  max-height: calc(100vh - 112px);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 4px 8px 16px;
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

.sidebar-header h2 {
  margin: 0;
  color: var(--c-ink);
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.2px;
}

.refresh-btn {
  flex-shrink: 0;
  color: var(--c-amber);
  background: #fff;
  border-color: var(--c-line);
}

.refresh-btn:hover,
.refresh-btn:focus {
  color: var(--c-amber-2);
  background: var(--c-cream-2);
  border-color: rgba(217, 119, 6, 0.25);
}

.category-scroll {
  flex: 1;
  min-height: 320px;
}

.category-menu {
  border-right: none;
  background: transparent;
}

.category-title {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--c-line);
  flex-shrink: 0;
  transition: background var(--dur-fast);
}

.category-name {
  flex: 0 1 auto;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
  font-size: 14px;
}

.category-count {
  margin-left: 4px;
  padding: 1px 8px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--c-ink-2);
  font-size: 11px;
  font-weight: 600;
  background: var(--c-peach);
  border: 1px solid var(--c-line);
}

:deep(.el-menu) {
  background: transparent;
}

:deep(.el-menu-item) {
  height: 40px;
  margin: 2px 0;
  padding: 0 12px !important;
  border-radius: var(--radius-sm);
  color: var(--c-ink-2);
  position: relative;
}

:deep(.el-menu-item)::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2px;
  height: 0;
  background: var(--c-amber);
  border-radius: 2px;
  transition: height var(--dur-fast);
}

:deep(.el-menu-item:hover) {
  color: var(--c-ink);
  background: var(--c-cream-2);
}

:deep(.el-menu-item:hover) .category-dot {
  background: var(--c-amber);
}

:deep(.el-menu-item.is-active) {
  color: var(--c-ink);
  font-weight: 600;
  background: var(--c-cream-2);
}

:deep(.el-menu-item.is-active)::before {
  height: 18px;
}

:deep(.el-menu-item.is-active) .category-dot {
  background: var(--c-amber);
}
</style>
