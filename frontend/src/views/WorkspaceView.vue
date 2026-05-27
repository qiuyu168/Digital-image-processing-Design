<template>
  <div class="workspace-page">
    <section class="workspace-shell">
      <AlgorithmSidebar
        :modules="modules"
        :active-menu-key="activeMenuKey"
        :open-module-keys="openModuleKeys"
        :algorithm-loading="algorithmLoading"
        @select="handleSelectAlgorithm"
        @refresh="loadAlgorithms"
      />

      <main class="workspace-main">
        <AlgorithmInfoCard
          :algorithm="selectedAlgorithm"
          :module-display-name="selectedModule?.displayName || ''"
        />

        <div class="middle-stack">
          <UploadPanel
            :uploaded-image="uploadedImage"
            :upload-loading="uploadLoading"
            :preview-display-url="previewDisplayUrl"
            :uploaded-image-size-text="uploadedImageSizeText"
            @file-change="handleFileChange"
            @clear="clearUploadedImage"
            @preview-error="handleImagePreviewError"
          />

          <ResultPanel
            :result-info="resultInfo"
            :preview-display-url="previewDisplayUrl"
            :selected-algorithm="selectedAlgorithm"
            :selected-module-display-name="selectedModule?.displayName || ''"
            :selected-run-endpoint="selectedRunEndpoint"
            :parameter-summary="parameterSummary"
            :metric-summary="metricSummary"
            @preview-error="handleImagePreviewError"
          />
        </div>

        <ParamsPanel
          class="params-column"
          :selected-algorithm="selectedAlgorithm"
          :param-list="paramList"
          :param-form="paramForm"
          :can-process="canProcess"
          :processing="processing"
          @param-change="handleParamChange"
          @process="handleProcess"
          @reset="resetParamForm"
        />
      </main>
    </section>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import http from '@/api/http'
import { getAlgorithmService } from '@/api/algorithms'
import { uploadImageService } from '@/api/upload'
import AlgorithmSidebar from '@/components/workspace/AlgorithmSidebar.vue'
import AlgorithmInfoCard from '@/components/workspace/AlgorithmInfoCard.vue'
import UploadPanel from '@/components/workspace/UploadPanel.vue'
import ParamsPanel from '@/components/workspace/ParamsPanel.vue'
import ResultPanel from '@/components/workspace/ResultPanel.vue'

const allowedExtensions = ['jpg', 'jpeg', 'png', 'bmp', 'webp', 'tif', 'tiff']
const minFileSize = 10 * 1024
const maxFileSize = 5 * 1024 * 1024
const minWidth = 128
const minHeight = 128
const maxWidth = 4096
const maxHeight = 4096

const moduleRunEndpointMap = {
  grayscale_image: '/api/algorithms/grayscale-image/run',
  color_image: '/api/algorithms/color-image/run',
  geometric_transform: '/api/algorithms/geometric-transform/run',
  spatial_filter: '/api/algorithms/spatial-filter/run',
  frequency_analysis: '/api/algorithms/frequency-analysis/run',
  frequency_filter: '/api/algorithms/frequency-filter/run'
}

const algorithmLoading = ref(false)
const uploadLoading = ref(false)
const processing = ref(false)

const modules = ref([])
const selectedModuleKey = ref('')
const selectedAlgorithmKey = ref('')
const previewDisplayUrl = ref('')

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
      !uploadLoading.value &&
      !processing.value
  )
})

const uploadedImageSizeText = computed(() => {
  if (!uploadedImage.width || !uploadedImage.height) return '已上传'
  return `${uploadedImage.width} × ${uploadedImage.height}`
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
})

onMounted(() => {
  loadAlgorithms()
})

onBeforeUnmount(() => {
  revokeLocalPreviewUrl()
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
  const file = uploadFile.raw
  if (!file) return

  const checkResult = await validateImageFile(file)
  if (!checkResult.valid) {
    ElMessage.error(checkResult.message)
    return
  }

  uploadLoading.value = true

  try {
    const formData = new FormData()
    formData.append('file', file, file.name)

    const data = await uploadImageService(formData)

    if (!data?.success) {
      ElMessage.error(data?.message || '图片上传失败')
      return
    }

    const imagePath = data.image_path || data.image_id || data.filename
    if (!imagePath) {
      ElMessage.error('图片上传成功，但后端未返回 image_path')
      return
    }

    revokeLocalPreviewUrl()

    uploadedImage.id = imagePath
    uploadedImage.localUrl = URL.createObjectURL(file)
    uploadedImage.serverPreviewUrl = normalizePreviewUrl(data.preview_url)
    uploadedImage.name = data.original_filename || file.name
    uploadedImage.size = file.size
    uploadedImage.width = Number(data.width) || checkResult.width
    uploadedImage.height = Number(data.height) || checkResult.height

    previewDisplayUrl.value = uploadedImage.serverPreviewUrl || uploadedImage.localUrl

    await nextTick()
    resetResult()
    ElMessage.success('图片上传成功')
  } finally {
    uploadLoading.value = false
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

function clearUploadedImage() {
  revokeLocalPreviewUrl()

  uploadedImage.id = ''
  uploadedImage.localUrl = ''
  uploadedImage.serverPreviewUrl = ''
  uploadedImage.name = ''
  uploadedImage.size = 0
  uploadedImage.width = 0
  uploadedImage.height = 0
  previewDisplayUrl.value = ''

  resetResult()
  ElMessage.info('已移除当前图片')
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

  const endpoint = getRunEndpoint(selectedAlgorithm.value.module)
  const payload = {
    source_type: 'upload',
    image_path: uploadedImage.id,
    algorithm: selectedAlgorithm.value.name,
    algorithm_display_name: selectedAlgorithm.value.displayName,
    params: buildProcessParams(),
    return_steps: true
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

function revokeLocalPreviewUrl() {
  if (uploadedImage.localUrl) {
    URL.revokeObjectURL(uploadedImage.localUrl)
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

function getFileExtension(filename) {
  return filename.split('.').pop()?.toLowerCase() || ''
}

function isNumberType(type) {
  return ['int', 'float', 'odd_int'].includes(type)
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
  font-family: var(--font-stack);
  color: var(--c-ink);
}

/* 三栏布局：算法树 / 中栏(信息+上传+结果) / 参数面板 */
.workspace-shell {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr) 340px;
  gap: 24px;
  align-items: start;
}

.workspace-main {
  min-width: 0;
  display: grid;
  gap: 24px;
}

.middle-stack {
  display: grid;
  gap: 24px;
}

.params-column {
  align-self: start;
}

/* 1279–980：双栏（算法树 + 中栏），参数下移 */
@media (max-width: 1279px) {
  .workspace-shell {
    grid-template-columns: 240px minmax(0, 1fr);
  }

  .params-column {
    grid-column: 1 / -1;
  }
}

/* 980 以下：单列 */
@media (max-width: 980px) {
  .workspace-shell {
    grid-template-columns: 1fr;
  }
}
</style>
