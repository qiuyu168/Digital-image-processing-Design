<template>
  <div class="library-page">
    <section class="library-shell">
      <!-- 左侧分类栏 -->
      <aside class="category-sidebar">
        <div class="sidebar-header">
          <div>
            <h2>图像分类</h2>
          </div>

          <el-button
            class="refresh-btn"
            circle
            :loading="categoryLoading"
            @click="loadCategories"
          >
            <el-icon><Refresh /></el-icon>
          </el-button>
        </div>

        <el-skeleton v-if="categoryLoading" :rows="8" animated />

        <el-empty
          v-else-if="categories.length === 0"
          description="暂无图像分类"
          :image-size="92"
        />

        <el-scrollbar v-else class="category-scroll">
          <el-menu
            class="category-menu"
            :default-active="activeCategoryName"
            @select="handleSelectCategory"
          >
            <el-menu-item
              v-for="(category, index) in categories"
              :key="category.name"
              :index="category.name"
            >
              <span class="category-title">
                <span class="category-icon">{{ getCategoryIcon(index) }}</span>
                <span class="category-name">{{ category.displayName }}</span>
                <span class="category-count">{{ category.count }}</span>
              </span>
            </el-menu-item>
          </el-menu>
        </el-scrollbar>
      </aside>

      <!-- 右侧图库与指标 -->
      <main class="library-main">
        <section class="panel-card library-header-card">
          <div class="panel-title">
            <div class="title-left">
              <span class="title-icon">🖼️</span>
              <div>
                <h3>{{ activeCategory?.displayName || '图像库' }}</h3>
              </div>
            </div>

            <el-tag v-if="activeCategory" class="soft-tag">
              {{ totalImages }} 张图片
            </el-tag>
          </div>
        </section>

        <div class="content-grid">
          <!-- 图片列表 -->
          <section class="panel-card image-list-card">
            <el-skeleton v-if="imageLoading" :rows="10" animated />

            <el-empty
              v-else-if="images.length === 0"
              description="该分类下暂无图片"
              :image-size="110"
            />

            <template v-else>
              <div class="image-grid">
                  <article
                    v-for="image in images"
                    :key="image.imagePath"
                    class="image-card"
                    :class="{ active: selectedImage?.imagePath === image.imagePath }"
                  >
                    <div class="image-frame">
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
                    </div>

                    <div class="image-info">
                      <h4>{{ image.displayName }}</h4>
                      <p>{{ image.filename }}</p>
                    </div>

                    <div class="image-actions">
                      <el-button
                        class="image-action-btn"
                        size="small"
                        plain
                        :loading="metricsLoading && selectedImage?.imagePath === image.imagePath"
                        @click.stop="handleViewMetrics(image)"
                      >
                        <el-icon><DataAnalysis /></el-icon>
                        查看参数
                      </el-button>

                      <el-button
                        class="image-action-btn download-btn"
                        size="small"
                        plain
                        @click.stop="downloadImage(image)"
                      >
                        <el-icon><Download /></el-icon>
                        获取图片
                      </el-button>
                    </div>
                  </article>
                </div>

              <div v-if="totalImages > pageSize" class="pagination-wrapper">
                <el-pagination
                  background
                  layout="prev, pager, next"
                  :total="totalImages"
                  :page-size="pageSize"
                  :current-page="currentPage"
                  @current-change="handlePageChange"
                />
              </div>
            </template>
          </section>

          <!-- 参数展示 -->
          <section class="panel-card metrics-card">
            <div class="panel-title compact-title">
              <div class="title-left">
                <span class="title-icon">📊</span>
                <div>
                  <h3>图像参数</h3>
                </div>
              </div>
            </div>

            <div v-if="!selectedImage" class="metrics-empty">
              <el-icon><DataAnalysis /></el-icon>
              <p>请选择一张图片查看参数</p>
            </div>

            <template v-else>
              <div class="selected-image-summary">
                <div class="thumb-frame">
                  <el-image
                    class="thumb-image"
                    :src="selectedImage.displayUrl"
                    fit="contain"
                    :preview-src-list="imagePreviewUrls"
                    :initial-index="getImagePreviewIndex(selectedImage)"
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

              <el-skeleton v-if="metricsLoading" :rows="8" animated />

              <el-scrollbar v-else class="metrics-scroll">
                <div v-if="metricRows.length > 0" class="metrics-list">
                  <div
                    v-for="item in metricRows"
                    :key="item.key"
                    class="metric-item"
                  >
                    <span>{{ item.label }}</span>
                    <strong>{{ item.value }}</strong>
                  </div>
                </div>

                <el-empty
                  v-else
                  description="暂无图像参数"
                  :image-size="90"
                />
              </el-scrollbar>
            </template>
          </section>
        </div>
      </main>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  DataAnalysis,
  Download,
  Picture,
  Refresh,
  View
} from '@element-plus/icons-vue'
import http from '@/api/http'
import { getCategoriesService, getDetailImageService, getImageMetricsService } from '@/api/library'

const categoryIcons = ['🌸', '🎨', '🌆', '✨', '📚', '🖌️', '🫧', '🌙']

const categoryLoading = ref(false)
const imageLoading = ref(false)
const metricsLoading = ref(false)

const categories = ref([])
const images = ref([])
const activeCategoryName = ref('')
const selectedImage = ref(null)
const metrics = ref(null)

const currentPage = ref(1)
const totalImages = ref(0)
const pageSize = ref(6)

const activeCategory = computed(() => {
  return categories.value.find((item) => item.name === activeCategoryName.value) || null
})

const imagePreviewUrls = computed(() => {
  return images.value.map((item) => item.displayUrl).filter(Boolean)
})

const metricRows = computed(() => {
  if (!metrics.value) return []

  const orderedKeys = ['width', 'height', 'channels', 'dtype', 'mean', 'std', 'min', 'max']
  const rows = []

  orderedKeys.forEach((key) => {
    if (Object.prototype.hasOwnProperty.call(metrics.value, key)) {
      rows.push({
        key,
        label: getMetricLabel(key),
        value: formatMetricValue(key, metrics.value[key])
      })
    }
  })

  Object.entries(metrics.value).forEach(([key, value]) => {
    if (orderedKeys.includes(key)) return

    rows.push({
      key,
      label: getMetricLabel(key),
      value: formatMetricValue(key, value)
    })
  })

  return rows
})

onMounted(() => {
  loadCategories()
})

async function loadCategories() {
  categoryLoading.value = true

  try {
    const data = await getCategoriesService()

    if (!data?.success) {
      ElMessage.error('获取图像分类失败')
      return
    }

    categories.value = normalizeCategories(data.categories)

    if (categories.value.length === 0) {
      activeCategoryName.value = ''
      images.value = []
      selectedImage.value = null
      metrics.value = null
      return
    }

    const firstCategory = categories.value.find((item) => item.count > 0) || categories.value[0]
    await handleSelectCategory(firstCategory.name)
  } finally {
    categoryLoading.value = false
  }
}

async function handleSelectCategory(categoryName) {
  if (!categoryName) return

  activeCategoryName.value = categoryName
  selectedImage.value = null
  metrics.value = null
  currentPage.value = 1
  await loadImages(categoryName)
}

async function loadImages(categoryName) {
  if (!categoryName) return

  imageLoading.value = true

  try {
    const data = await getDetailImageService({
      params: {
        category: categoryName,
        page: currentPage.value,
        page_size: pageSize.value
      }
    })

    if (!data?.success) {
      ElMessage.error('获取图像列表失败')
      return
    }

    images.value = normalizeImages(data.images)
    totalImages.value = data.total || 0
  } finally {
    imageLoading.value = false
  }
}

async function handlePageChange(page) {
  currentPage.value = page
  selectedImage.value = null
  metrics.value = null
  await loadImages(activeCategoryName.value)
}

async function handleViewMetrics(image) {
  selectedImage.value = image
  metrics.value = null
  await loadImageMetrics(image)
}

function getImagePreviewIndex(image) {
  if (!image?.displayUrl) return 0

  const index = imagePreviewUrls.value.findIndex((url) => url === image.displayUrl)
  return index >= 0 ? index : 0
}

function downloadImage(image) {
  if (!image?.displayUrl) {
    ElMessage.warning('图片地址不存在，无法下载')
    return
  }

  const link = document.createElement('a')

  link.href = image.displayUrl
  link.download = image.filename || `${image.name || 'library-image'}.png`
  link.target = '_blank'
  link.rel = 'noopener noreferrer'

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  ElMessage.success('已打开图片下载地址')
}

async function loadImageMetrics(image) {
  if (!image?.imagePath) return

  metricsLoading.value = true

  try {
    const data = await getImageMetricsService({
      source_type: 'library',
      image_path: image.imagePath,
      include_histogram: false
    })

    if (!data?.success) {
      ElMessage.error('获取图像参数失败')
      return
    }

    metrics.value = data.metrics || {}
  } finally {
    metricsLoading.value = false
  }
}

function normalizeCategories(rawCategories) {
  if (!Array.isArray(rawCategories)) return []

  return rawCategories
    .filter((item) => item && item.name)
    .map((item) => ({
      name: String(item.name),
      displayName: item.display_name || item.displayName || item.name,
      count: Number.isFinite(Number(item.count)) ? Number(item.count) : 0
    }))
}

function normalizeImages(rawImages) {
  if (!Array.isArray(rawImages)) return []

  return rawImages
    .filter((item) => item && item.image_path)
    .map((item) => {
      const imagePath = String(item.image_path)
      const previewUrl = item.preview_url || `/api/library/image/${encodeURI(imagePath)}`

      return {
        name: item.name || imagePath,
        displayName: item.display_name || item.displayName || item.name || item.filename || imagePath,
        filename: item.filename || imagePath.split('/').pop(),
        category: item.category || activeCategoryName.value,
        imagePath,
        previewUrl,
        displayUrl: normalizePreviewUrl(previewUrl)
      }
    })
}

function normalizePreviewUrl(url) {
  if (!url) return ''

  if (
    url.startsWith('http://') ||
    url.startsWith('https://') ||
    url.startsWith('data:') ||
    url.startsWith('blob:')
  ) {
    return url
  }

  const baseURL = String(http.defaults.baseURL || import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

  if (!baseURL || baseURL === '/api') {
    return url
  }

  if (baseURL.endsWith('/api') && url.startsWith('/api/')) {
    return `${baseURL.slice(0, -4)}${url}`
  }

  if (url.startsWith('/')) {
    return `${baseURL}${url}`
  }

  return `${baseURL}/${url}`
}

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

function getCategoryIcon(index) {
  return categoryIcons[index % categoryIcons.length]
}
</script>

<style lang="scss" scoped>
.library-page {
  color: #1a1a1a;
  font-family: 'M PLUS Rounded 1c', 'Quicksand', 'Noto Sans JP', sans-serif;
}

.library-shell {
  display: flex;
  align-items: flex-start;
  gap: 22px;
  position: relative;
}

.category-sidebar,
.panel-card {
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.category-sidebar {
  position: sticky;
  top: 96px;
  flex: 0 0 280px;
  width: 280px;
  align-self: flex-start;
  max-height: calc(100vh - 112px);
  min-height: 520px;
  padding: 20px 14px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 4px 8px 18px;
}

.sidebar-header h2 {
  margin: 0 0 6px;
  color: #1a1a1a;
  font-size: 22px;
  font-weight: 800;
}

.sidebar-header p {
  margin: 0;
  color: #555;
  font-size: 13px;
  line-height: 1.6;
}

.refresh-btn {
  flex-shrink: 0;
  color: #ff6b8b;
  background: rgba(255, 107, 139, 0.08);
  border-color: rgba(255, 107, 139, 0.2);
}

.category-scroll {
  flex: 1;
  height: calc(100vh - 230px);
  min-height: 360px;
  max-height: 560px;
}

.category-menu {
  border-right: none;
  background: transparent;
}

.category-title {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
}

.category-icon {
  width: 30px;
  height: 30px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 107, 139, 0.1);
}

.category-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 700;
}

.category-count {
  min-width: 24px;
  height: 22px;
  padding: 0 6px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #ff5277;
  font-size: 12px;
  background: rgba(255, 82, 119, 0.1);
}

:deep(.el-menu) {
  background: transparent;
}

:deep(.el-menu-item) {
  height: 48px;
  margin: 5px 0;
  padding: 0 12px !important;
  border-radius: 16px;
  color: #333;
}

:deep(.el-menu-item:hover) {
  color: #ff5277;
  background: rgba(255, 107, 139, 0.08);
}

:deep(.el-menu-item.is-active) {
  color: #ff5277;
  font-weight: 700;
  background: rgba(255, 107, 139, 0.12);
}

.library-main {
  flex: 1 1 auto;
  min-width: 0;
  align-self: flex-start;
}

.panel-card {
  padding: 22px;
}

.library-header-card {
  margin-bottom: 22px;
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

.title-icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  border-radius: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  background: rgba(255, 107, 139, 0.1);
}

.panel-title h3 {
  margin: 0 0 6px;
  color: #1a1a1a;
  font-size: 20px;
  font-weight: 800;
}

.panel-title p {
  margin: 0;
  color: #555;
  font-size: 14px;
  line-height: 1.7;
}

.soft-tag {
  flex-shrink: 0;
  border: none;
  color: #ff5277;
  background: rgba(255, 82, 119, 0.1);
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 22px;
  align-items: start;
}

.image-list-card {
  min-width: 0;
}

.small-refresh {
  width: 34px;
  height: 34px;
}

.image-scroll {
  padding-right: 4px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 20px;
  padding-bottom: 4px;
}

.image-card {
  min-width: 0;
  padding: 12px;
  border-radius: 20px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.62);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.28s ease;
}

.image-card:hover,
.image-card.active {
  transform: translateY(-3px);
  border-color: rgba(255, 82, 119, 0.32);
  box-shadow: 0 12px 26px rgba(255, 107, 139, 0.16);
  background: rgba(255, 255, 255, 0.78);
}

.image-frame {
  position: relative;
  width: 100%;
  min-height: 170px;
  max-height: 260px;
  aspect-ratio: 4 / 3;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(circle at 20% 10%, rgba(255, 182, 193, 0.18), transparent 35%),
    rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(255, 107, 139, 0.12);
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
  gap: 8px;
  color: #fff;
  font-weight: 800;
  background: rgba(0, 0, 0, 0.34);
  opacity: 0;
  transition: opacity 0.25s ease;
  pointer-events: none;
}

.preview-mask .el-icon {
  font-size: 30px;
}

.image-card:hover .preview-mask {
  opacity: 1;
}

.image-info {
  padding: 12px 2px 2px;
}

.image-info h4 {
  margin: 0 0 6px;
  color: #1a1a1a;
  font-size: 15px;
  font-weight: 800;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.image-info p {
  margin: 0;
  color: #666;
  font-size: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.image-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  padding-top: 10px;
}

.image-action-btn {
  width: 100%;
  margin: 0;
  border-radius: 999px;
  color: #ff5277;
  border-color: rgba(255, 82, 119, 0.26);
  background: rgba(255, 255, 255, 0.72);
  font-weight: 700;
}

.image-action-btn:hover,
.image-action-btn:focus {
  color: #fff;
  border-color: #ff6b8b;
  background: #ff6b8b;
}

.download-btn {
  color: #5d8cff;
  border-color: rgba(93, 140, 255, 0.26);
}

.download-btn:hover,
.download-btn:focus {
  color: #fff;
  border-color: #5d8cff;
  background: #5d8cff;
}

.metrics-card {
  position: sticky;
  top: 96px;
  max-height: calc(100vh - 110px);
  overflow: hidden;
}

.metrics-empty {
  min-height: 460px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  color: #888;
  background: rgba(255, 255, 255, 0.58);
  border: 1px dashed rgba(255, 107, 139, 0.25);
}

.metrics-empty .el-icon {
  color: #ff9aae;
  font-size: 54px;
}

.metrics-empty p {
  margin: 0;
  font-size: 14px;
}

.selected-image-summary {
  display: flex;
  gap: 12px;
  padding: 12px;
  margin-bottom: 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.62);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.thumb-frame {
  width: 92px;
  height: 72px;
  flex-shrink: 0;
  border-radius: 14px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.72);
}

.thumb-image {
  width: 100%;
  height: 100%;
}

.summary-text {
  min-width: 0;
}

.summary-text h4 {
  margin: 2px 0 8px;
  color: #1a1a1a;
  font-size: 15px;
  font-weight: 800;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-text p {
  margin: 0;
  color: #666;
  font-size: 12px;
  line-height: 1.5;
  word-break: break-all;
}

.metrics-scroll {
  max-height: calc(100vh - 320px);
  padding-right: 4px;
}

.metrics-list {
  display: grid;
  gap: 10px;
}

.metric-item {
  padding: 12px 14px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: rgba(255, 255, 255, 0.66);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.metric-item span {
  flex-shrink: 0;
  color: #666;
  font-size: 13px;
}

.metric-item strong {
  min-width: 0;
  color: #1a1a1a;
  font-size: 14px;
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.image-error {
  width: 100%;
  height: 100%;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #999;
  font-size: 13px;
}

.image-error .el-icon {
  color: #ff9aae;
  font-size: 34px;
}

.small-error {
  min-height: 72px;
}

:deep(.el-image__inner) {
  object-fit: contain;
}

:global(.el-image-viewer__wrapper) {
  z-index: 4000 !important;
}

@media (max-width: 1200px) {
  .library-shell {
    display: grid;
    grid-template-columns: 1fr;
  }

  .category-sidebar,
  .metrics-card {
    position: relative;
    top: 0;
    min-height: auto;
  }

  .category-sidebar {
    width: auto;
    flex: none;
    height: auto;
    max-height: none;
    min-height: auto;
  }

  .category-scroll {
    height: 320px;
    flex: none;
    min-height: auto;
  }
}

@media (max-width: 960px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .metrics-card {
    max-height: none;
  }

  .metrics-scroll {
    max-height: none;
  }
}

@media (max-width: 680px) {
  .panel-card {
    padding: 18px;
  }

  .panel-title {
    flex-direction: column;
  }

  .image-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
