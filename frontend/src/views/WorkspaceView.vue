<template>
  <div class=”workspace-page page-enter”>
    <!-- 左栏：算法树 -->
    <aside class=”workspace-sidebar glass-card”>
      <div class=”sidebar-header”>
        <span class=”sidebar-title”>✦ 算法分类</span>
        <el-icon class=”sidebar-refresh” @click=”loadAlgorithms”><Refresh /></el-icon>
      </div>
      <div class=”algo-tree”>
        <div v-for=”mod in algorithmModules” :key=”mod.module”
          class=”tree-module”
          :class=”{ 'tree-module--active': activeModule === mod.module }”
          @click=”activeModule = mod.module”>
          <span class=”tree-module-name”>{{ mod.display_name }}</span>
          <span class=”tree-badge”>{{ mod.algorithms?.length || 0 }}</span>
        </div>
      </div>
    </aside>

    <!-- 中栏：主工作区 -->
    <main class=”workspace-main”>
      <!-- 上传区 -->
      <div class=”glass-card upload-section”>
        <input ref=”fileInput” type=”file” accept=”image/*” hidden @change=”onFileChange”>
        <div v-if=”!uploadedImage” class=”upload-placeholder” @click=”triggerUpload”>
          <span class=”upload-icon”>✦</span>
          <span class=”upload-text”>拖拽或点击上传图片</span>
          <span class=”upload-hint”>支持 jpg / png / bmp / webp / tiff</span>
        </div>
        <div v-else class=”image-compare”>
          <div class=”compare-pane”>
            <span class=”compare-label”>原图</span>
            <img :src=”uploadedImage” alt=”原图” class=”compare-image”>
          </div>
          <div class=”compare-pane”>
            <span class=”compare-label”>结果</span>
            <img v-if=”resultInfo.imageUrl” :src=”resultInfo.imageUrl” alt=”结果” class=”compare-image result-image”>
            <div v-else class=”compare-empty”>等待处理...</div>
          </div>
        </div>
      </div>

      <!-- 分析文本 -->
      <div v-if=”resultInfo.analysis” class=”glass-card analysis-section”>
        <p>{{ resultInfo.analysis }}</p>
      </div>
    </main>

    <!-- 右栏：参数面板 -->
    <aside class=”workspace-params glass-card”>
      <div class=”params-header”>
        <span class=”params-title”>{{ selectedAlgorithm?.display_name || '选择算法' }}</span>
      </div>
      <div v-if=”selectedAlgorithm?.params && Object.keys(selectedAlgorithm.params).length > 0” class=”params-list”>
        <div v-for=”(param, key) in selectedAlgorithm.params” :key=”key” class=”param-item”>
          <label class=”param-label”>{{ param.label }}</label>
          <el-slider v-if=”param.component === 'slider'” v-model=”params[key]”
            :min=”param.min” :max=”param.max” :step=”param.step”
            :show-tooltip=”false” />
          <el-select v-else-if=”param.component === 'select'” v-model=”params[key]” style=”width:100%”>
            <el-option v-for=”opt in param.options” :key=”opt” :label=”opt” :value=”opt” />
          </el-select>
          <el-switch v-else-if=”param.component === 'switch'” v-model=”params[key]” />
        </div>
      </div>
      <div v-else class=”params-empty”>
        <span>此算法无可调节参数</span>
      </div>
      <button class=”btn-gradient run-btn”
        :disabled=”running”
        @click=”runAlgorithm”>
        <span v-if=”running”>✦ 处理中...</span>
        <span v-else>▶ 执行算法</span>
      </button>
    </aside>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Delete,
  MagicStick,
  Picture,
  Refresh,
  UploadFilled,
  View
} from '@element-plus/icons-vue'
import http from '@/api/http'
import { getAlgorithmService } from '@/api/algorithms'
import { uploadImageService } from '@/api/upload'

const allowedExtensions = ['jpg', 'jpeg', 'png', 'bmp', 'webp', 'tif', 'tiff']
const minFileSize = 10 * 1024
const maxFileSize = 5 * 1024 * 1024
const minWidth = 128
const minHeight = 128
const maxWidth = 4096
const maxHeight = 4096
const moduleIconList = ['🧮', '🌗', '🎨', '📐', '🫧', '🌌', '⚡', '🌸', '✨']
const moduleIconMap = {
  basic_operation: '🧮',
  grayscale_image: '🌗',
  color_image: '🎨',
  geometric_transform: '📐',
  spatial_filter: '🫧',
  frequency_analysis: '🌌',
  frequency_filter: '⚡',
  image_restoration: '🌸',
  edge_shape_detection: '✨'
}

const twoImageAlgorithmNames = new Set([
  'add_operation',
  'subtract_operation',
  'multiply_operation',
  'divide_operation',
  'and_operation',
  'or_operation',
  'xor_operation',
  'histogram_matching'
])

const moduleRunEndpointMap = {
  basic_operation: '/api/algorithms/basic-operation/run',
  grayscale_image: '/api/algorithms/grayscale-image/run',
  color_image: '/api/algorithms/color-image/run',
  geometric_transform: '/api/algorithms/geometric-transform/run',
  spatial_filter: '/api/algorithms/spatial-filter/run',
  frequency_analysis: '/api/algorithms/frequency-analysis/run',
  frequency_filter: '/api/algorithms/frequency-filter/run',
  image_restoration: '/api/algorithms/image-restoration/run',
  edge_shape_detection: '/api/algorithms/edge-shape-detection/run'
}

const algorithmLoading = ref(false)
const uploadLoading = ref(false)
const secondUploadLoading = ref(false)
const processing = ref(false)

const modules = ref([])
const selectedModuleKey = ref('')
const selectedAlgorithmKey = ref('')
const previewDisplayUrl = ref('')
const secondPreviewDisplayUrl = ref('')

const paramForm = reactive({})

const uploadedImage = reactive({
  id: '',
  localUrl: '',
  serverPreviewUrl: '',
  name: '',
  size: 0,
  width: 0,
  height: 0
})

const secondUploadedImage = reactive({
  id: '',
  localUrl: '',
  serverPreviewUrl: '',
  name: '',
  size: 0,
  width: 0,
  height: 0
})

const resultInfo = reactive({
  status: 'idle',
  imageUrl: '',
  message: '',
  endpoint: '',
  steps: [],
  metrics: {},
  analysis: ''
})

const selectedModule = computed(() => {
  return modules.value.find((item) => item.key === selectedModuleKey.value) || null
})

const selectedAlgorithm = computed(() => {
  if (!selectedModule.value) return null
  return selectedModule.value.algorithms.find((item) => item.key === selectedAlgorithmKey.value) || null
})

const paramList = computed(() => selectedAlgorithm.value?.paramsList || [])

const requiresSecondImage = computed(() => {
  return Boolean(selectedAlgorithm.value && twoImageAlgorithmNames.has(selectedAlgorithm.value.name))
})

const activeMenuKey = computed(() => {
  if (!selectedModuleKey.value || !selectedAlgorithmKey.value) return ''
  return `${selectedModuleKey.value}::${selectedAlgorithmKey.value}`
})

const openModuleKeys = computed(() => modules.value.map((item) => item.key))

const selectedRunEndpoint = computed(() => {
  if (!selectedAlgorithm.value) return ''
  return getRunEndpoint(selectedAlgorithm.value.module)
})

const canProcess = computed(() => {
  return Boolean(
    selectedAlgorithm.value &&
      uploadedImage.id &&
      previewDisplayUrl.value &&
      (!requiresSecondImage.value || secondUploadedImage.id) &&
      !uploadLoading.value &&
      !secondUploadLoading.value &&
      !processing.value
  )
})

const uploadedImageSizeText = computed(() => {
  if (!uploadedImage.width || !uploadedImage.height) return '已上传'
  return `${uploadedImage.width} × ${uploadedImage.height}`
})

const secondUploadedImageSizeText = computed(() => {
  if (!secondUploadedImage.width || !secondUploadedImage.height) return '已上传'
  return `${secondUploadedImage.width} × ${secondUploadedImage.height}`
})

const processHintText = computed(() => {
  if (requiresSecondImage.value) {
    return '选择算法并上传主图与参考图后，点击“开始处理”即可调用后端算法运行接口。'
  }

  return '选择算法并上传图片后，点击“开始处理”即可调用后端算法运行接口。'
})

const parameterSummary = computed(() => {
  return paramList.value.map((param) => ({
    key: param.key,
    label: param.label,
    value: formatParamValue(param, paramForm[param.key])
  }))
})

const metricSummary = computed(() => {
  if (!isPlainObject(resultInfo.metrics)) return []

  return Object.entries(resultInfo.metrics).map(([key, value]) => ({
    key,
    value: formatMetricValue(value)
  }))
})

watch(selectedAlgorithm, () => {
  resetParamForm()
  resetResult()
  if (!requiresSecondImage.value) {
    clearSecondUploadedImage({ silent: true })
  }
})

onMounted(() => {
  loadAlgorithms()
})

onBeforeUnmount(() => {
  revokeLocalPreviewUrl(uploadedImage)
  revokeLocalPreviewUrl(secondUploadedImage)
})

async function loadAlgorithms() {
  algorithmLoading.value = true

  try {
    const data = await getAlgorithmService()
    const parsedModules = normalizeModules(data)

    modules.value = parsedModules

    if (parsedModules.length === 0) {
      selectedModuleKey.value = ''
      selectedAlgorithmKey.value = ''
      ElMessage.warning('后端算法列表为空，请检查接口返回值')
      return
    } 
    
    ElMessage.success('算法列表加载成功！')

    selectFirstAlgorithm()
  } catch (error) {
    modules.value = []
    selectedModuleKey.value = ''
    selectedAlgorithmKey.value = ''
  } finally {
    algorithmLoading.value = false
  }
}

function normalizeModules(data) {
  const rawModules = Array.isArray(data?.modules) ? data.modules : []

  return rawModules.map((rawModule, moduleIndex) => {
    const moduleName = toText(rawModule?.module, `module_${moduleIndex}`)
    const rawAlgorithms = Array.isArray(rawModule?.algorithms) ? rawModule.algorithms : []

    return {
      key: createStableKey(moduleName, moduleIndex),
      module: moduleName,
      displayName: toText(rawModule?.display_name, moduleName),
      algorithms: rawAlgorithms.map((rawAlgorithm, algorithmIndex) => {
        return normalizeAlgorithm(rawAlgorithm, moduleName, moduleIndex, algorithmIndex)
      })
    }
  })
}

function normalizeAlgorithm(rawAlgorithm, fallbackModuleName, moduleIndex, algorithmIndex) {
  const algorithmName = toText(rawAlgorithm?.name, `algorithm_${algorithmIndex}`)

  return {
    key: createStableKey(algorithmName, algorithmIndex),
    module: toText(rawAlgorithm?.module, fallbackModuleName),
    name: algorithmName,
    displayName: toText(rawAlgorithm?.display_name, algorithmName),
    description: toText(rawAlgorithm?.description, '暂无算法说明'),
    paramsList: normalizeParams(rawAlgorithm?.params, moduleIndex, algorithmIndex)
  }
}

function normalizeParams(params, moduleIndex, algorithmIndex) {
  if (!isPlainObject(params)) return []

  return Object.entries(params).map(([paramKey, rawParam], paramIndex) => {
    const safeParam = isPlainObject(rawParam) ? rawParam : {}
    const type = normalizeType(safeParam.type)
    const component = normalizeComponent(safeParam.component, type)

    const normalizedParam = {
      key: paramKey,
      label: toText(safeParam.label, paramKey),
      type,
      component,
      default: safeParam.default,
      min: normalizeNumber(safeParam.min, undefined),
      max: normalizeNumber(safeParam.max, undefined),
      step: normalizeNumber(safeParam.step, undefined),
      options: normalizeOptions(safeParam.options),
      orderKey: `${moduleIndex}_${algorithmIndex}_${paramIndex}`
    }

    fillParamDefaultConfig(normalizedParam)
    return normalizedParam
  })
}

function fillParamDefaultConfig(param) {
  if (param.component === 'slider' || isNumberType(param.type)) {
    if (!Number.isFinite(param.min)) param.min = 0
    if (!Number.isFinite(param.max)) param.max = 100
    if (!Number.isFinite(param.step) || param.step <= 0) {
      param.step = param.type === 'float' ? 0.1 : 1
    }
  }

  if (param.type === 'odd_int') {
    if (!Number.isFinite(param.step) || param.step <= 0) param.step = 2
    param.min = normalizeOddIntIfNeeded(param, param.min)
    param.max = normalizeOddIntIfNeeded(param, param.max)
  }
}

function normalizeType(type) {
  const allowedTypes = ['int', 'float', 'odd_int', 'select', 'bool']
  return allowedTypes.includes(type) ? type : 'input'
}

function normalizeComponent(component, type) {
  const allowedComponents = ['slider', 'select', 'switch', 'input']

  if (allowedComponents.includes(component)) return component
  if (type === 'select') return 'select'
  if (type === 'bool') return 'switch'
  if (isNumberType(type)) return 'slider'
  return 'input'
}

function normalizeOptions(options) {
  if (!Array.isArray(options)) return []

  return options.map((option, index) => {
    if (isPlainObject(option)) {
      return {
        label: toText(option.label, option.value ?? `选项 ${index + 1}`),
        value: option.value
      }
    }

    return {
      label: String(option),
      value: option
    }
  })
}

function selectFirstAlgorithm() {
  const firstModule = modules.value[0]
  const firstAlgorithm = firstModule?.algorithms?.[0]

  selectedModuleKey.value = firstModule?.key || ''
  selectedAlgorithmKey.value = firstAlgorithm?.key || ''
}

function handleSelectAlgorithm(index) {
  const [moduleKey, algorithmKey] = index.split('::')
  selectedModuleKey.value = moduleKey
  selectedAlgorithmKey.value = algorithmKey
}

function resetParamForm() {
  Object.keys(paramForm).forEach((key) => {
    delete paramForm[key]
  })

  paramList.value.forEach((param) => {
    paramForm[param.key] = getInitialParamValue(param)
  })
}

function getInitialParamValue(param) {
  if (param.component === 'select') {
    const hasDefault = param.options.some((option) => option.value === param.default)
    return hasDefault ? param.default : param.options[0]?.value ?? ''
  }

  if (param.type === 'bool') return Boolean(param.default)

  if (param.type === 'int' || param.type === 'odd_int') {
    const value = Number.parseInt(param.default, 10)
    const safeValue = Number.isNaN(value) ? param.min : value
    return normalizeOddIntIfNeeded(param, safeValue)
  }

  if (param.type === 'float') {
    const value = Number.parseFloat(param.default)
    return Number.isNaN(value) ? param.min : value
  }

  return param.default ?? ''
}

function handleParamChange(param) {
  if (param.type === 'odd_int') {
    paramForm[param.key] = normalizeOddIntIfNeeded(param, paramForm[param.key])
  }
}

function normalizeOddIntIfNeeded(param, value) {
  if (param.type !== 'odd_int') return value

  let numberValue = Number.parseInt(value, 10)
  if (Number.isNaN(numberValue)) numberValue = 1

  if (numberValue % 2 === 0) numberValue += 1

  if (Number.isFinite(param.max) && numberValue > param.max) {
    numberValue = param.max % 2 === 1 ? param.max : param.max - 1
  }

  if (Number.isFinite(param.min) && numberValue < param.min) {
    numberValue = param.min % 2 === 1 ? param.min : param.min + 1
  }

  return numberValue
}

async function handleFileChange(uploadFile) {
  await uploadSelectedFile({
    uploadFile,
    imageRecord: uploadedImage,
    previewRef: previewDisplayUrl,
    loadingRef: uploadLoading,
    successMessage: '主图上传成功'
  })
}

async function handleSecondFileChange(uploadFile) {
  await uploadSelectedFile({
    uploadFile,
    imageRecord: secondUploadedImage,
    previewRef: secondPreviewDisplayUrl,
    loadingRef: secondUploadLoading,
    successMessage: '参考图上传成功'
  })
}

async function uploadSelectedFile({
  uploadFile,
  imageRecord,
  previewRef,
  loadingRef,
  successMessage
}) {
  const file = uploadFile.raw
  if (!file) return

  const checkResult = await validateImageFile(file)
  if (!checkResult.valid) {
    ElMessage.error(checkResult.message)
    return
  }

  loadingRef.value = true

  try {
    const formData = new FormData()
    formData.append('file', file, file.name)

    const data = await uploadImageService(formData)

    if (!data?.success) {
      ElMessage.error(data?.message || '图片上传失败')
      return
    }

    const imagePath = data.image_path
    if (!imagePath) {
      ElMessage.error('图片上传成功，但后端未返回 image_path')
      return
    }

    revokeLocalPreviewUrl(imageRecord)

    imageRecord.id = imagePath
    imageRecord.localUrl = URL.createObjectURL(file)
    imageRecord.serverPreviewUrl = normalizePreviewUrl(data.preview_url)
    imageRecord.name = data.original_filename || file.name
    imageRecord.size = file.size
    imageRecord.width = Number(data.width) || checkResult.width
    imageRecord.height = Number(data.height) || checkResult.height

    previewRef.value = imageRecord.serverPreviewUrl || imageRecord.localUrl

    await nextTick()
    resetResult()
    ElMessage.success(successMessage)
  } finally {
    loadingRef.value = false
  }
}

async function validateImageFile(file) {
  const extension = getFileExtension(file.name)

  if (!allowedExtensions.includes(extension)) {
    return {
      valid: false,
      message: '文件格式不支持，请上传 jpg、jpeg、png、bmp、webp、tif、tiff 图片'
    }
  }

  if (file.size < minFileSize) {
    return { valid: false, message: '图片不能小于 10KB' }
  }

  if (file.size > maxFileSize) {
    return { valid: false, message: '图片不能大于 5MB' }
  }

  try {
    const sizeInfo = await readImageSize(file)

    if (sizeInfo.width < minWidth || sizeInfo.height < minHeight) {
      return { valid: false, message: '图片分辨率不能小于 128×128' }
    }

    if (sizeInfo.width > maxWidth || sizeInfo.height > maxHeight) {
      return { valid: false, message: '图片分辨率不能大于 4096×4096' }
    }

    return { valid: true, width: sizeInfo.width, height: sizeInfo.height }
  } catch (error) {
    return { valid: false, message: '无法读取图片分辨率，请确认图片没有损坏' }
  }
}

function readImageSize(file) {
  return new Promise((resolve, reject) => {
    const objectUrl = URL.createObjectURL(file)
    const image = new Image()

    image.onload = () => {
      const result = { width: image.width, height: image.height }
      URL.revokeObjectURL(objectUrl)
      resolve(result)
    }

    image.onerror = () => {
      URL.revokeObjectURL(objectUrl)
      reject(new Error('image load error'))
    }

    image.src = objectUrl
  })
}

function handleImagePreviewError() {
  if (previewDisplayUrl.value !== uploadedImage.localUrl && uploadedImage.localUrl) {
    previewDisplayUrl.value = uploadedImage.localUrl
  }
}

function handleSecondImagePreviewError() {
  if (
    secondPreviewDisplayUrl.value !== secondUploadedImage.localUrl &&
    secondUploadedImage.localUrl
  ) {
    secondPreviewDisplayUrl.value = secondUploadedImage.localUrl
  }
}

function clearUploadedImage() {
  clearImageRecord(uploadedImage, previewDisplayUrl)
  resetResult()
  ElMessage.info('已移除当前图片')
}

function clearSecondUploadedImage(options = {}) {
  clearImageRecord(secondUploadedImage, secondPreviewDisplayUrl)
  resetResult()

  if (!options.silent) {
    ElMessage.info('已移除参考图')
  }
}

function clearImageRecord(imageRecord, previewRef) {
  revokeLocalPreviewUrl(imageRecord)

  imageRecord.id = ''
  imageRecord.localUrl = ''
  imageRecord.serverPreviewUrl = ''
  imageRecord.name = ''
  imageRecord.size = 0
  imageRecord.width = 0
  imageRecord.height = 0
  previewRef.value = ''
}

async function handleProcess() {
  if (!selectedAlgorithm.value) {
    ElMessage.warning('请先选择算法')
    return
  }

  if (!uploadedImage.id) {
    ElMessage.warning('请先上传图片')
    return
  }

  if (requiresSecondImage.value && !secondUploadedImage.id) {
    ElMessage.warning('当前算法需要先上传参考图')
    return
  }

  const endpoint = getRunEndpoint(selectedAlgorithm.value.module)
  const payload = {
    source_type: 'upload',
    image_path: uploadedImage.id,
    algorithm: selectedAlgorithm.value.name,
    algorithm_display_name: selectedAlgorithm.value.displayName,
    params: buildProcessParams(),
    return_steps: true
  }

  if (requiresSecondImage.value) {
    payload.second_image_path = secondUploadedImage.id
  }

  processing.value = true
  resultInfo.status = 'processing'
  resultInfo.imageUrl = ''
  resultInfo.endpoint = endpoint
  resultInfo.steps = []
  resultInfo.metrics = {}
  resultInfo.analysis = ''
  resultInfo.message = `正在调用 ${endpoint} 运行算法...`

  try {
    const data = await http.post(endpoint, payload)

    if (!data?.success) {
      resultInfo.status = 'error'
      resultInfo.message = data?.message || '算法运行失败'
      ElMessage.error(resultInfo.message)
      return
    }

    resultInfo.status = 'done'
    resultInfo.imageUrl = normalizeResultImageUrl(data.result_image)
    resultInfo.steps = normalizeResultSteps(data.steps)
    resultInfo.metrics = isPlainObject(data.metrics) ? data.metrics : {}
    resultInfo.analysis = toText(data.analysis, '')
    resultInfo.message = `${toText(data.algorithm_display_name, selectedAlgorithm.value.displayName)} 运行完成，已返回处理结果。`

    ElMessage.success('算法运行成功')
  } catch (error) {
    resultInfo.status = 'error'
    resultInfo.imageUrl = ''
    resultInfo.message = extractErrorMessage(error) || '算法运行失败，请查看浏览器控制台和后端日志。'
  } finally {
    processing.value = false
  }
}

function buildProcessParams() {
  const params = {}

  paramList.value.forEach((param) => {
    params[param.key] = castParamValue(param, paramForm[param.key])
  })

  return params
}

function castParamValue(param, value) {
  if (param.type === 'bool') return Boolean(value)

  if (param.type === 'int' || param.type === 'odd_int') {
    const numberValue = Number.parseInt(value, 10)
    const safeValue = Number.isNaN(numberValue) ? getInitialParamValue(param) : numberValue
    return normalizeOddIntIfNeeded(param, safeValue)
  }

  if (param.type === 'float') {
    const numberValue = Number.parseFloat(value)
    return Number.isNaN(numberValue) ? getInitialParamValue(param) : numberValue
  }

  return value
}

function getRunEndpoint(moduleName) {
  const normalizedModuleName = String(moduleName || '')

  if (moduleRunEndpointMap[normalizedModuleName]) {
    return moduleRunEndpointMap[normalizedModuleName]
  }

  return `/api/algorithms/${normalizedModuleName.replaceAll('_', '-')}/run`
}

function normalizeResultImageUrl(image) {
  if (!image) return ''

  const imageText = String(image).trim()

  if (
    imageText.startsWith('data:image/') ||
    imageText.startsWith('http://') ||
    imageText.startsWith('https://') ||
    imageText.startsWith('blob:')
  ) {
    return imageText
  }

  return `data:image/png;base64,${imageText}`
}

function normalizeResultSteps(steps) {
  if (!Array.isArray(steps)) return []

  return steps.map((step, index) => {
    const safeStep = isPlainObject(step) ? step : {}
    return {
      name: toText(safeStep.name, `步骤 ${index + 1}`),
      image: safeStep.image ? normalizeResultImageUrl(safeStep.image) : '',
      error: toText(safeStep.error, '')
    }
  })
}

function extractErrorMessage(error) {
  return (
    error?.response?.data?.message ||
    error?.response?.data?.detail ||
    error?.message ||
    ''
  )
}

function getResultStatusText(status) {
  const statusMap = {
    processing: '处理中',
    done: '运行完成',
    error: '运行失败'
  }

  return statusMap[status] || '未开始'
}

function getResultTagType(status) {
  if (status === 'done') return 'success'
  if (status === 'error') return 'danger'
  return 'warning'
}

function formatMetricValue(value) {
  if (value === null || value === undefined) return ''
  if (typeof value === 'number') return Number.isInteger(value) ? String(value) : String(Number(value.toFixed(6)))
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

function resetResult() {
  resultInfo.status = 'idle'
  resultInfo.imageUrl = ''
  resultInfo.message = ''
  resultInfo.endpoint = ''
  resultInfo.steps = []
  resultInfo.metrics = {}
  resultInfo.analysis = ''
  processing.value = false
}

function revokeLocalPreviewUrl(imageRecord) {
  if (imageRecord.localUrl) {
    URL.revokeObjectURL(imageRecord.localUrl)
  }
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

  if (baseURL.startsWith('http://') || baseURL.startsWith('https://')) {
    const origin = new URL(baseURL).origin

    if (url.startsWith('/api/')) {
      return `${origin}${url}`
    }

    if (url.startsWith('/')) {
      return `${baseURL}${url}`
    }

    return `${baseURL}/${url}`
  }

  if (baseURL.endsWith('/api') && url.startsWith('/api/')) {
    return url
  }

  if (baseURL.endsWith('/api') && url.startsWith('/')) {
    return `${baseURL}${url}`
  }

  return url.startsWith('/') ? url : `/${url}`
}

function formatParamValue(param, value) {
  if (param.type === 'bool') return value ? '开启' : '关闭'

  if (param.component === 'select') {
    const target = param.options.find((option) => option.value === value)
    return target?.label ?? value
  }

  return value
}

function getParamTypeText(type) {
  const textMap = {
    int: '整数',
    float: '小数',
    odd_int: '奇数',
    select: '选择',
    bool: '开关',
    input: '输入'
  }

  return textMap[type] || '参数'
}

function isNumberType(type) {
  return ['int', 'float', 'odd_int'].includes(type)
}

function getPrecision(step) {
  const text = String(step ?? 1)
  if (!text.includes('.')) return 0
  return text.split('.')[1].length
}

function getFileExtension(filename) {
  return filename.split('.').pop()?.toLowerCase() || ''
}

function formatFileSize(size) {
  if (!size) return '0 KB'
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(2)} MB`
}

function getModuleIcon(moduleName, index) {
  return moduleIconMap[moduleName] || moduleIconList[index % moduleIconList.length]
}

function createStableKey(value, index) {
  return `${String(value)}_${index}`
}

function toText(value, fallback = '') {
  if (value === undefined || value === null || value === '') return String(fallback)
  return String(value)
}

function normalizeNumber(value, fallback) {
  const numberValue = Number(value)
  return Number.isNaN(numberValue) ? fallback : numberValue
}

function isPlainObject(value) {
  return Object.prototype.toString.call(value) === '[object Object]'
}
</script>

<style lang="scss" scoped>
.workspace-page {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  height: calc(100vh - 64px - 80px);
  max-width: 1600px;
  margin: 0 auto;
}

.workspace-sidebar {
  width: 220px;
  flex-shrink: 0;
  padding: var(--space-md);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-title {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--accent-purple);
}

.sidebar-refresh {
  color: var(--text-muted);
  cursor: pointer;
  &:hover { color: var(--accent-cyan); }
}

.tree-module {
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all var(--dur-fast) var(--ease-smooth);
  font-size: 13px;
  color: var(--text-secondary);

  &:hover { background: rgba(255,255,255,0.04); }
  &--active { background: rgba(255,107,157,0.1); color: var(--accent-pink); }
}

.tree-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  background: rgba(255,255,255,0.06);
}

.workspace-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  min-width: 0;
}

.upload-section {
  flex: 1;
  padding: var(--space-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-placeholder {
  text-align: center;
  cursor: pointer;
}

.upload-icon { font-size: 40px; display: block; margin-bottom: var(--space-sm); color: var(--accent-pink); }
.upload-text { color: var(--text-secondary); font-size: 14px; }
.upload-hint { color: var(--text-muted); font-size: 12px; display: block; margin-top: var(--space-xs); }

.image-compare { display: flex; gap: var(--space-md); width: 100%; height: 100%; }
.compare-pane { flex: 1; display: flex; flex-direction: column; align-items: center; }
.compare-label { font-size: 12px; color: var(--text-muted); margin-bottom: var(--space-sm); }
.compare-image { max-width: 100%; max-height: 300px; border-radius: 8px; object-fit: contain; }
.result-image { border: 1px solid rgba(56,189,248,0.3); box-shadow: 0 0 12px rgba(56,189,248,0.1); }
.compare-empty { flex: 1; display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: 13px; }

.analysis-section {
  padding: var(--space-md);
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.workspace-params {
  width: 240px;
  flex-shrink: 0;
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.params-header {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--accent-purple);
}

.params-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.param-label {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: var(--space-xs);
}

.params-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 13px;
}

.run-btn {
  width: 100%;
  padding: 12px 0;
  font-size: 15px;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
</style>
