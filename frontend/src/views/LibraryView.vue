<template>
  <div class="library-page">
    <section class="library-shell">
      <CategorySidebar
        :categories="categories"
        :active-category="activeCategoryName"
        :loading="categoryLoading"
        @select-category="handleSelectCategory"
        @refresh="loadCategories"
      />

      <main class="library-main">
        <LibraryHero
          :total-count="images.length"
          :active-category-name="activeCategory?.displayName || '图像库'"
        />

        <ImageGrid
          :images="images"
          :loading="imageLoading"
          :selected-image-id="selectedImage?.imagePath || ''"
          @select-image="handleViewMetrics"
          @download-image="downloadImage"
          @refresh="activeCategoryName && loadImages(activeCategoryName)"
        />

        <MetricsPanel
          :selected-image="selectedImage"
          :metrics="metrics"
          @close="handleCloseMetrics"
        />
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

import CategorySidebar from '@/components/library/CategorySidebar.vue'
import LibraryHero from '@/components/library/LibraryHero.vue'
import ImageGrid from '@/components/library/ImageGrid.vue'
import MetricsPanel from '@/components/library/MetricsPanel.vue'

const categoryLoading = ref(false)
const imageLoading = ref(false)
const metricsLoading = ref(false)

const categories = ref([])
const images = ref([])
const activeCategoryName = ref('')
const selectedImage = ref(null)
const metrics = ref(null)

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
  await loadImages(categoryName)
}

async function loadImages(categoryName) {
  if (!categoryName) return

  imageLoading.value = true

  try {
    const data = await getDetailImageService({ params: {category: categoryName} })

    if (!data?.success) {
      ElMessage.error('获取图像列表失败')
      return
    }

    images.value = normalizeImages(data.images)
  } finally {
    imageLoading.value = false
  }
}

async function handleViewMetrics(image) {
  selectedImage.value = image
  metrics.value = null
  await loadImageMetrics(image)
}

function handleCloseMetrics() {
  selectedImage.value = null
  metrics.value = null
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
</script>

<style lang="scss" scoped>
.library-page {
  color: var(--c-ink);
  font-family: var(--font-stack);
}

.library-shell {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 24px;
  align-items: flex-start;
}

.library-main {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

:deep(.el-image-viewer__wrapper) {
  z-index: 4000 !important;
}

/* =============== Responsive =============== */
@media (max-width: 1200px) {
  .library-shell {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 680px) {
  .library-main {
    gap: 16px;
  }
}
</style>
