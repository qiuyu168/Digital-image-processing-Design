<template>
  <section
    class="metrics-panel"
    :class="{ expanded: !!selectedImage }"
  >
    <!-- Collapsed state: prompt bar -->
    <div v-if="!selectedImage" class="metrics-collapsed">
      <el-icon class="collapsed-icon"><DataAnalysis /></el-icon>
      <p>请选择一张图片查看参数</p>
    </div>

    <!-- Expanded state: metrics content -->
    <template v-else>
      <div class="metrics-header">
        <div class="selected-image-summary">
          <div class="thumb-frame">
            <el-image
              class="thumb-image"
              :src="selectedImage.displayUrl"
              fit="contain"
              :preview-src-list="previewUrls"
              :initial-index="0"
              preview-teleported
              hide-on-click-modal
            >
              <template #error>
                <div class="image-error small-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>
          <div class="summary-text">
            <h4>{{ selectedImage.displayName }}</h4>
            <p>{{ selectedImage.imagePath }}</p>
          </div>
        </div>

        <el-button
          class="close-btn"
          size="small"
          circle
          @click="$emit('close')"
        >
          <el-icon><Close /></el-icon>
        </el-button>
      </div>

      <el-skeleton v-if="isLoading" :rows="4" animated />

      <el-empty
        v-else-if="metricRows.length === 0"
        description="暂无图像参数"
        :image-size="72"
      />

      <el-scrollbar v-else class="metrics-horizontal-scroll">
        <div class="metrics-row">
          <div
            v-for="item in metricRows"
            :key="item.key"
            class="metric-chip"
          >
            <span class="chip-label">{{ item.label }}</span>
            <strong class="chip-value">{{ item.value }}</strong>
          </div>
        </div>
      </el-scrollbar>
    </template>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { Close, DataAnalysis, Picture } from '@element-plus/icons-vue'

const props = defineProps({
  selectedImage: { type: Object, default: null },
  metrics: { type: Object, default: null }
})

defineEmits(['close'])

const previewUrls = computed(() => {
  return props.selectedImage?.displayUrl ? [props.selectedImage.displayUrl] : []
})

const isLoading = computed(() => {
  return !!props.selectedImage && !props.metrics
})

const metricRows = computed(() => {
  if (!props.metrics) return []

  const orderedKeys = ['width', 'height', 'channels', 'dtype', 'mean', 'std', 'min', 'max']
  const rows = []

  orderedKeys.forEach((key) => {
    if (Object.prototype.hasOwnProperty.call(props.metrics, key)) {
      rows.push({
        key,
        label: getMetricLabel(key),
        value: formatMetricValue(key, props.metrics[key])
      })
    }
  })

  Object.entries(props.metrics).forEach(([key, value]) => {
    if (orderedKeys.includes(key)) return
    rows.push({
      key,
      label: getMetricLabel(key),
      value: formatMetricValue(key, value)
    })
  })

  return rows
})

function getMetricLabel(key) {
  const labelMap = {
    width: '图像宽度',
    height: '图像高度',
    channels: '通道数量',
    dtype: '数据类型',
    mean: '像素均值',
    std: '像素标准差',
    min: '最小像素值',
    max: '最大像素值',
    histogram: '灰度直方图',
    bins: '直方图分箱数',
    pixel_count: '像素数量',
    peak_value: '峰值灰度',
    peak_count: '峰值数量'
  }
  return labelMap[key] || key
}

function formatMetricValue(key, value) {
  if (value === null || value === undefined) return '无'
  if (key === 'width' || key === 'height') {
    return `${value} 像素`
  }
  if (key === 'channels') {
    return `${value} 通道`
  }
  if (typeof value === 'number') {
    return Number.isInteger(value) ? String(value) : value.toFixed(4)
  }
  if (Array.isArray(value)) {
    return `${value.length} 项数据`
  }
  if (typeof value === 'object') {
    return '已获取，可用于后续图表展示'
  }
  return String(value)
}
</script>

<style scoped>
.metrics-panel {
  max-height: 64px;
  overflow: hidden;
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-1);
  transition: max-height var(--dur-base) var(--ease-standard);
}

.metrics-panel.expanded {
  max-height: 320px;
}

/* =============== Collapsed state =============== */
.metrics-collapsed {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--c-ink-2);
  background: var(--c-cream-2);
  border: 1px dashed var(--c-line);
  border-radius: var(--radius-md);
  margin: -1px;
}

.collapsed-icon {
  color: var(--c-amber);
  font-size: 22px;
  opacity: 0.6;
}

.metrics-collapsed p {
  margin: 0;
  font-size: 13px;
  font-weight: 500;
}

/* =============== Header =============== */
.metrics-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px 0;
}

.selected-image-summary {
  flex: 1;
  display: flex;
  gap: 12px;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.thumb-frame {
  width: 84px;
  height: 64px;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: #fff;
  border: 1px solid var(--c-line);
}

.thumb-image {
  width: 100%;
  height: 100%;
}

.summary-text {
  min-width: 0;
}

.summary-text h4 {
  margin: 2px 0 6px;
  color: var(--c-ink);
  font-size: 14px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-text p {
  margin: 0;
  color: var(--c-ink-2);
  font-size: 11px;
  line-height: 1.5;
  word-break: break-all;
  font-family: 'SF Mono', 'Consolas', monospace;
}

.close-btn {
  flex-shrink: 0;
  margin-top: 4px;
  color: var(--c-ink-2);
  background: #fff;
  border-color: var(--c-line);
}

.close-btn:hover {
  color: var(--c-amber);
  border-color: rgba(217, 119, 6, 0.35);
  background: var(--c-cream-2);
}

/* =============== Horizontal metrics row =============== */
.metrics-horizontal-scroll {
  padding: 12px 20px 16px;
}

.metrics-row {
  display: flex;
  gap: 12px;
}

.metric-chip {
  flex-shrink: 0;
  padding: 10px 16px;
  border-radius: var(--radius-sm);
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 110px;
}

.chip-label {
  color: var(--c-ink-2);
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
}

.chip-value {
  color: var(--c-ink);
  font-size: 13px;
  font-weight: 600;
  font-family: 'SF Mono', 'Consolas', monospace;
  white-space: nowrap;
}

/* =============== Error state =============== */
.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-error .el-icon {
  color: var(--c-amber);
  font-size: 20px;
  opacity: 0.6;
}

.small-error {
  min-height: 60px;
}

:deep(.el-image__inner) {
  object-fit: contain;
}
</style>
