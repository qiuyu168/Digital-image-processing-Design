<template>
  <section class="panel-card image-list-card">
    <div class="panel-title compact-title">
      <div class="title-left">
        <div>
          <h3>图片列表</h3>
          <p>点击图片全屏预览，按钮用于查看参数或下载图片</p>
        </div>
      </div>

      <el-button
        class="refresh-btn small-refresh"
        circle
        :loading="loading"
        @click="$emit('refresh')"
      >
        <el-icon><Refresh /></el-icon>
      </el-button>
    </div>

    <el-skeleton v-if="loading && images.length === 0" :rows="10" animated />

    <el-empty
      v-else-if="images.length === 0"
      description="该分类下暂无图片"
      :image-size="110"
    />

    <TransitionGroup
      v-else
      name="grid"
      tag="div"
      class="image-grid"
    >
      <article
        v-for="(image, index) in images"
        :key="image.imagePath"
        class="image-card"
        :class="{ active: image.imagePath === selectedImageId }"
        :style="{ '--stagger-delay': Math.min(index, 9) * 30 + 'ms' }"
        @click="handleCardClick(image)"
      >
        <div class="image-frame" @click.stop>
          <el-image
            class="library-image"
            :src="image.displayUrl"
            fit="contain"
            :preview-src-list="imagePreviewUrls"
            :initial-index="getImagePreviewIndex(image)"
            preview-teleported
            hide-on-click-modal
          >
            <template #error>
              <div class="image-error">
                <el-icon><Picture /></el-icon>
                <span>图片加载失败</span>
              </div>
            </template>
          </el-image>

          <div class="preview-mask">
            <el-icon><View /></el-icon>
            <span>全屏预览</span>
          </div>

          <div class="hover-actions">
            <el-tooltip content="查看参数" placement="top">
              <el-button
                class="action-icon-btn"
                size="small"
                circle
                @click.stop="handleSelectMetrics(image)"
              >
                <el-icon><DataAnalysis /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip content="获取图片" placement="top">
              <el-button
                class="action-icon-btn"
                size="small"
                circle
                @click.stop="handleDownload(image)"
              >
                <el-icon><Download /></el-icon>
              </el-button>
            </el-tooltip>
          </div>
        </div>

        <div class="image-info">
          <h4>{{ image.displayName }}</h4>
          <p>{{ image.filename }}</p>
        </div>
      </article>
    </TransitionGroup>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import {
  DataAnalysis,
  Download,
  Picture,
  Refresh,
  View
} from '@element-plus/icons-vue'

const props = defineProps({
  images: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  selectedImageId: { type: String, default: '' }
})

const emit = defineEmits(['select-image', 'view-image', 'download-image', 'refresh'])

const imagePreviewUrls = computed(() => {
  return props.images.map((item) => item.displayUrl).filter(Boolean)
})

function getImagePreviewIndex(image) {
  if (!image?.displayUrl) return 0
  const index = imagePreviewUrls.value.findIndex((url) => url === image.displayUrl)
  return index >= 0 ? index : 0
}

function handleCardClick(image) {
  emit('select-image', image)
}

function handleSelectMetrics(image) {
  emit('select-image', image)
}

function handleDownload(image) {
  emit('download-image', image)
}
</script>

<style scoped>
.panel-card {
  padding: 24px;
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-1);
}

.image-list-card {
  min-width: 0;
}

.panel-title {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.compact-title {
  margin-bottom: 16px;
}

.title-left {
  min-width: 0;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.panel-title h3 {
  margin: 0 0 6px;
  color: var(--c-ink);
  font-size: 18px;
  font-weight: 700;
}

.panel-title p {
  margin: 0;
  color: var(--c-ink-2);
  font-size: 13px;
  line-height: 1.65;
}

.small-refresh {
  width: 32px;
  height: 32px;
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

/* =============== Grid =============== */
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 16px;
}

.image-card {
  position: relative;
  min-width: 0;
  padding: 12px;
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-1);
  cursor: pointer;
  transition: box-shadow var(--dur-fast) var(--ease-standard),
              transform var(--dur-fast) var(--ease-standard),
              border-color var(--dur-fast) var(--ease-standard);
}

.image-card:hover {
  box-shadow: var(--shadow-2);
  transform: translateY(-1px);
}

.image-card.active {
  border-color: rgba(217, 119, 6, 0.35);
  box-shadow: var(--shadow-2);
}

.image-frame {
  position: relative;
  width: 100%;
  min-height: 170px;
  max-height: 260px;
  aspect-ratio: 4 / 3;
  border-radius: var(--radius-sm);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.library-image {
  width: 100%;
  height: 100%;
  min-height: 170px;
  max-height: 260px;
}

.preview-mask {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #fff;
  font-weight: 600;
  font-size: 13px;
  background: rgba(43, 36, 25, 0.4);
  opacity: 0;
  transition: opacity var(--dur-fast) var(--ease-standard);
  pointer-events: none;
}

.preview-mask .el-icon {
  font-size: 24px;
}

.image-card:hover .preview-mask {
  opacity: 1;
}

/* =============== Apple Finder style hover action icons =============== */
.hover-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 6px;
  opacity: 0;
  transform: translateX(8px);
  transition: opacity var(--dur-fast) var(--ease-standard),
              transform var(--dur-fast) var(--ease-standard);
  pointer-events: none;
  z-index: 2;
}

.image-card:hover .hover-actions {
  opacity: 1;
  transform: translateX(0);
  pointer-events: auto;
}

.action-icon-btn {
  backdrop-filter: blur(4px);
  background: rgba(255, 255, 255, 0.85) !important;
  border-color: rgba(0, 0, 0, 0.08) !important;
  color: var(--c-ink-2) !important;
  transition: all var(--dur-fast) var(--ease-standard);
}

.action-icon-btn:hover {
  background: rgba(255, 255, 255, 0.95) !important;
  border-color: rgba(217, 119, 6, 0.35) !important;
  color: var(--c-amber) !important;
  transform: scale(1.08);
}

.action-icon-btn .el-icon {
  font-size: 14px;
}

/* =============== Image info =============== */
.image-info {
  padding: 12px 2px 2px;
}

.image-info h4 {
  margin: 0 0 4px;
  color: var(--c-ink);
  font-size: 14px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.image-info p {
  margin: 0;
  color: var(--c-ink-2);
  font-size: 11px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: 'SF Mono', 'Consolas', monospace;
}

/* =============== Image error fallback =============== */
.image-error {
  width: 100%;
  height: 100%;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--c-ink-2);
  font-size: 12px;
}

.image-error .el-icon {
  color: var(--c-amber);
  font-size: 28px;
  opacity: 0.6;
}

/* =============== TransitionGroup stagger =============== */
.grid-enter-active {
  transition: opacity var(--dur-base) var(--ease-standard),
              transform var(--dur-base) var(--ease-standard);
  transition-delay: var(--stagger-delay, 0ms);
}

.grid-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.grid-leave-active {
  transition: opacity var(--dur-fast) var(--ease-standard),
              transform var(--dur-fast) var(--ease-standard);
}

.grid-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.grid-move {
  transition: transform var(--dur-base) var(--ease-standard);
}

:deep(.el-image__inner) {
  object-fit: contain;
}
</style>
