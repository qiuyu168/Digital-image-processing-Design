<template>
  <div class="workspace-page">
    <section class="workspace-shell">
      <aside class="algorithm-sidebar">
        <div class="sidebar-header">
          <div>
            <h2>算法模块</h2>
          </div>

          <el-button
            class="refresh-btn"
            circle
            :loading="algorithmLoading"
            @click="loadAlgorithms"
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
            @select="handleSelectAlgorithm"
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

      <main class="workspace-main">
        <section class="panel-card algorithm-info-card">
          <div class="panel-title">
            <div class="title-left">
              <span class="title-icon">🪄</span>
              <div>
                <h3>{{ selectedAlgorithm?.displayName || '请选择算法' }}</h3>
                <p>
                  {{
                    selectedAlgorithm?.description ||
                    '请从左侧选择一个具体算法。'
                  }}
                </p>
              </div>
            </div>

            <el-tag v-if="selectedModule" class="soft-tag">
              {{ selectedModule.displayName }}
            </el-tag>
          </div>
        </section>

        <div class="right-grid">
          <div class="left-workflow">
            <section class="panel-card upload-card">
            <div class="panel-title">
              <div class="title-left">
                <span class="title-icon">📤</span>
                <div>
                  <h3>上传图片</h3>
                </div>
              </div>
            </div>

            <el-upload
              class="image-uploader"
              action="#"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleFileChange"
              :disabled="uploadLoading"
              accept=".jpg,.jpeg,.png,.bmp,.webp,.tif,.tiff"
            >
              <div class="upload-box" :class="{ 'has-image': previewDisplayUrl }">
                <template v-if="previewDisplayUrl">
                  <div class="image-frame upload-preview-frame">
                    <el-image
                      class="preview-image"
                      :src="previewDisplayUrl"
                      fit="contain"
                      :preview-src-list="[previewDisplayUrl]"
                      :preview-teleported="true"
                      :z-index="3000"
                      hide-on-click-modal
                      @error="handleImagePreviewError"
                    >
                      <template #error>
                        <div class="image-error">
                          <el-icon><Picture /></el-icon>
                          <span>图片预览失败</span>
                        </div>
                      </template>
                    </el-image>
                  </div>

                  <div class="image-mask">
                    <el-icon><UploadFilled /></el-icon>
                    <span>点击重新上传</span>
                  </div>
                </template>

                <template v-else>
                  <el-icon class="upload-icon"><UploadFilled /></el-icon>
                  <h4>选择本地图片</h4>
                  <p>支持 jpg、jpeg、png、bmp、webp、tif、tiff，大小 10KB - 5MB</p>
                </template>
              </div>
            </el-upload>

            <div v-if="uploadLoading" class="upload-loading">
              <el-icon class="is-loading"><Refresh /></el-icon>
              正在上传图片...
            </div>

            <div v-if="uploadedImage.id" class="image-meta">
              <div>
                <span>文件名</span>
                <strong>{{ uploadedImage.name }}</strong>
              </div>
              <div>
                <span>尺寸</span>
                <strong>{{ uploadedImageSizeText }}</strong>
              </div>
              <div>
                <span>大小</span>
                <strong>{{ formatFileSize(uploadedImage.size) }}</strong>
              </div>
              <div>
                <span>图片路径</span>
                <strong>{{ uploadedImage.id }}</strong>
              </div>
            </div>

            <div v-if="uploadedImage.id" class="upload-actions">
              <el-button plain class="ghost-btn" @click="clearUploadedImage">
                <el-icon><Delete /></el-icon>
                移除图片
              </el-button>
            </div>
          </section>

          <section class="panel-card params-card">
            <div class="panel-title">
              <div class="title-left">
                <span class="title-icon">🎚️</span>
                <div>
                  <h3>参数设置</h3>
                </div>
              </div>

              <el-button
                v-if="paramList.length > 0"
                class="reset-btn"
                plain
                @click="resetParamForm"
              >
                重置
              </el-button>
            </div>

            <el-empty
              v-if="!selectedAlgorithm"
              description="请先选择算法"
              :image-size="92"
            />

            <el-empty
              v-else-if="paramList.length === 0"
              description="该算法没有参数"
              :image-size="92"
            />

            <el-form v-else class="params-form" label-position="top">
              <el-form-item
                v-for="param in paramList"
                :key="param.key"
                class="param-item"
              >
                <template #label>
                  <div class="param-label">
                    <span>{{ param.label }}</span>
                    <em>{{ getParamTypeText(param.type) }}</em>
                  </div>
                </template>

                <el-slider
                  v-if="param.component === 'slider'"
                  v-model="paramForm[param.key]"
                  :min="param.min"
                  :max="param.max"
                  :step="param.step"
                  :precision="param.type === 'float' ? getPrecision(param.step) : 0"
                  show-input
                  @change="handleParamChange(param)"
                />

                <el-select
                  v-else-if="param.component === 'select'"
                  v-model="paramForm[param.key]"
                  class="full-control"
                  placeholder="请选择"
                >
                  <el-option
                    v-for="option in param.options"
                    :key="String(option.value)"
                    :label="option.label"
                    :value="option.value"
                  />
                </el-select>

                <el-switch
                  v-else-if="param.component === 'switch'"
                  v-model="paramForm[param.key]"
                  active-text="开启"
                  inactive-text="关闭"
                />

                <el-input-number
                  v-else-if="isNumberType(param.type)"
                  v-model="paramForm[param.key]"
                  class="full-control"
                  :min="param.min"
                  :max="param.max"
                  :step="param.step"
                  @change="handleParamChange(param)"
                />

                <el-input
                  v-else
                  v-model="paramForm[param.key]"
                  class="full-control"
                  placeholder="请输入参数值"
                />
              </el-form-item>
            </el-form>

            <div class="process-actions">
              <el-button
                class="process-btn"
                type="primary"
                :disabled="!canProcess"
                :loading="processing"
                @click="handleProcess"
              >
                <el-icon><MagicStick /></el-icon>
                开始处理
              </el-button>
            </div>
          </section>
          </div>

          <section class="panel-card result-card">
            <div class="panel-title">
              <div class="title-left">
                <span class="title-icon">🖼️</span>
                <div>
                  <h3>结果展示</h3>
                </div>
              </div>

              <el-tag
                v-if="resultInfo.status !== 'idle'"
                class="soft-tag"
                :type="getResultTagType(resultInfo.status)"
              >
                {{ getResultStatusText(resultInfo.status) }}
              </el-tag>
            </div>

            <div v-if="!previewDisplayUrl" class="result-empty">
              <el-icon><Picture /></el-icon>
              <p>上传图片后，将在这里显示原图与处理结果。</p>
            </div>

            <div v-else class="result-content">
              <div class="compare-box">
                <div class="compare-item">
                  <div class="compare-title">原图</div>
                  <div class="image-frame result-image-frame">
                    <el-image
                      class="compare-image"
                      :src="previewDisplayUrl"
                      fit="contain"
                      :preview-src-list="[previewDisplayUrl]"
                      :preview-teleported="true"
                      :z-index="3000"
                      hide-on-click-modal
                      @error="handleImagePreviewError"
                    >
                      <template #error>
                        <div class="image-error">
                          <el-icon><Picture /></el-icon>
                          <span>图片预览失败</span>
                        </div>
                      </template>
                    </el-image>
                  </div>
                </div>

                <div class="compare-item result-preview">
                  <div class="compare-title">处理结果</div>

                  <template v-if="resultInfo.status === 'done' && resultInfo.imageUrl">
                    <div class="image-frame result-image-frame">
                      <el-image
                        class="compare-image"
                        :src="resultInfo.imageUrl"
                        fit="contain"
                        :preview-src-list="[resultInfo.imageUrl]"
                        :preview-teleported="true"
                        :z-index="3000"
                        hide-on-click-modal
                      >
                        <template #error>
                          <div class="image-error">
                            <el-icon><Picture /></el-icon>
                            <span>图片预览失败</span>
                          </div>
                        </template>
                      </el-image>
                    </div>
                  </template>

                  <template v-else>
                    <div class="waiting-result">
                      <el-icon><View /></el-icon>
                      <p>点击“开始处理”后调用后端运行接口</p>
                    </div>
                  </template>
                </div>
              </div>

              <div class="result-message">
                <strong>说明：</strong>
                <span>
                  {{
                    resultInfo.message ||
                    '选择算法并上传图片后，点击“开始处理”即可调用后端算法运行接口。'
                  }}
                </span>
              </div>

              <div v-if="selectedAlgorithm" class="task-summary">
                <div>
                  <span>算法大类</span>
                  <strong>{{ selectedModule?.displayName }}</strong>
                </div>
                <div>
                  <span>选择算法</span>
                  <strong>{{ selectedAlgorithm.displayName }}</strong>
                </div>
                <div>
                  <span>运行接口</span>
                  <strong>{{ selectedRunEndpoint }}</strong>
                </div>
                <div>
                  <span>图像来源</span>
                  <strong>upload</strong>
                </div>
              </div>

              <div v-if="parameterSummary.length > 0" class="params-summary">
                <div
                  v-for="item in parameterSummary"
                  :key="item.key"
                  class="summary-item"
                >
                  <span>{{ item.label }}</span>
                  <strong>{{ item.value }}</strong>
                </div>
              </div>

              <div v-if="resultInfo.analysis" class="analysis-box">
                <div class="section-title">处理分析</div>
                <p>{{ resultInfo.analysis }}</p>
              </div>

              <div v-if="metricSummary.length > 0" class="metrics-summary">
                <div
                  v-for="metric in metricSummary"
                  :key="metric.key"
                  class="summary-item"
                >
                  <span>{{ metric.key }}</span>
                  <strong>{{ metric.value }}</strong>
                </div>
              </div>

              <div v-if="resultInfo.steps.length > 0" class="steps-block">
                <div class="section-title">处理步骤</div>
                <div class="steps-list">
                  <div
                    v-for="(step, index) in resultInfo.steps"
                    :key="`${step.name}_${index}`"
                    class="step-item"
                  >
                    <div class="compare-title">{{ index + 1 }}. {{ step.name }}</div>
                    <div v-if="step.image" class="image-frame step-image-frame">
                      <el-image
                        class="compare-image"
                        :src="step.image"
                        fit="contain"
                        :preview-src-list="[step.image]"
                        :preview-teleported="true"
                        :z-index="3000"
                        hide-on-click-modal
                      >
                        <template #error>
                          <div class="image-error">
                            <el-icon><Picture /></el-icon>
                            <span>步骤图片预览失败</span>
                          </div>
                        </template>
                      </el-image>
                    </div>
                    <div v-else-if="step.error" class="step-error">{{ step.error }}</div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
    </section>
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
const moduleIconList = ['🌗', '🎨', '📐', '🫧', '🌌', '⚡', '🌸', '✨']

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

function getModuleIcon(index) {
  return moduleIconList[index % moduleIconList.length]
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
.workspace-shell {
  display: grid;
  grid-template-columns: 290px 1fr;
  gap: 22px;
  align-items: start;
}

.algorithm-sidebar,
.panel-card {
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid rgba(255, 255, 255, 0.95);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.algorithm-sidebar {
  position: sticky;
  top: 96px;
  min-height: 680px;
  padding: 20px 14px;
  overflow: hidden;
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
  font-size: 22px;
  font-weight: 800;
}

.sidebar-header p,
.panel-title p {
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

.menu-scroll {
  height: 580px;
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
}

.module-icon {
  width: 30px;
  height: 30px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 107, 139, 0.1);
}

.module-name {
  flex: 1;
  font-weight: 700;
}

.module-count {
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

.algorithm-name {
  font-size: 14px;
}

:deep(.el-menu) {
  background: transparent;
}

:deep(.el-sub-menu__title) {
  height: 48px;
  padding: 0 12px !important;
  border-radius: 16px;
  color: #1a1a1a;
}

:deep(.el-sub-menu__title:hover) {
  background: rgba(255, 107, 139, 0.08);
}

:deep(.el-menu-item) {
  height: 42px;
  margin: 4px 0;
  padding-left: 44px !important;
  border-radius: 14px;
  color: #333;
}

:deep(.el-menu-item:hover),
:deep(.el-menu-item.is-active) {
  color: #ff5277;
  background: rgba(255, 107, 139, 0.1);
}

:deep(.el-menu-item.is-active) {
  font-weight: 700;
}

.workspace-main {
  min-width: 0;
}

.algorithm-info-card {
  margin-bottom: 22px;
}

.panel-card {
  padding: 22px;
}

.panel-title {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.title-left {
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
  font-size: 20px;
  font-weight: 800;
}

.soft-tag {
  border: none;
  color: #ff5277;
  background: rgba(255, 82, 119, 0.1);
}

.right-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(360px, 0.95fr);
  gap: 22px;
  align-items: start;
}

.left-workflow {
  min-width: 0;
  display: grid;
  gap: 22px;
  align-content: start;
}

.upload-card,
.params-card,
.result-card {
  min-width: 0;
}

.result-card {
  position: sticky;
  top: 96px;
  max-height: calc(100vh - 118px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.result-card > .panel-title {
  flex-shrink: 0;
}

.image-uploader {
  width: 100%;
}

.upload-box {
  position: relative;
  min-height: 300px;
  max-height: 430px;
  border-radius: 20px;
  border: 2px dashed rgba(255, 107, 139, 0.28);
  background: radial-gradient(circle at 20% 10%, rgba(255, 182, 193, 0.18), transparent 35%), rgba(255, 255, 255, 0.58);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-box:hover {
  border-color: rgba(255, 82, 119, 0.48);
  background: rgba(255, 255, 255, 0.72);
  transform: translateY(-2px);
}

.upload-box.has-image {
  border-style: solid;
  padding: 10px;
}

.image-frame {
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.72);
}

.upload-preview-frame {
  min-height: 220px;
  height: clamp(220px, 34vw, 360px);
  max-height: 360px;
}

.result-image-frame {
  min-height: 200px;
  height: clamp(200px, 28vw, 300px);
  max-height: 300px;
}

.preview-image,
.compare-image {
  width: 100%;
  height: 100%;
}

:deep(.preview-image .el-image__inner),
:deep(.compare-image .el-image__inner) {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.upload-icon {
  color: #ff6b8b;
  font-size: 54px;
}

.upload-box h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
}

.upload-box p {
  max-width: 360px;
  margin: 0;
  color: #666;
  font-size: 13px;
  line-height: 1.7;
  text-align: center;
}

.image-mask {
  position: absolute;
  inset: 10px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #fff;
  font-weight: 700;
  background: rgba(0, 0, 0, 0.35);
  opacity: 0;
  transition: opacity 0.25s;
}

.image-mask .el-icon {
  font-size: 34px;
}

.upload-box.has-image:hover .image-mask {
  opacity: 1;
}

.image-error {
  width: 100%;
  height: 100%;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #888;
  font-size: 14px;
}

.image-error .el-icon {
  color: #ff9aae;
  font-size: 42px;
}

.upload-loading {
  margin-top: 12px;
  color: #ff5277;
  font-size: 14px;
  font-weight: 700;
}

.image-meta,
.task-summary {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.image-meta div,
.task-summary div {
  min-width: 0;
  padding: 12px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.image-meta span,
.task-summary span {
  display: block;
  margin-bottom: 5px;
  color: #777;
  font-size: 12px;
}

.image-meta strong,
.task-summary strong {
  display: block;
  color: #1a1a1a;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upload-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.ghost-btn,
.reset-btn {
  color: #ff5277;
  border-color: rgba(255, 82, 119, 0.28);
  background: rgba(255, 255, 255, 0.72);
}

.ghost-btn:hover,
.reset-btn:hover {
  color: #fff;
  border-color: #ff6b8b;
  background: #ff6b8b;
}

.params-form {
  padding-top: 4px;
}

.param-item {
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.62);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.param-label {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.param-label span {
  font-weight: 700;
}

.param-label em {
  padding: 2px 9px;
  border-radius: 999px;
  color: #ff5277;
  font-style: normal;
  font-size: 12px;
  background: rgba(255, 82, 119, 0.1);
}

.full-control {
  width: 100%;
}

.process-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 4px;
}

.process-btn {
  min-width: 150px;
  height: 42px;
  border: none;
  border-radius: 999px;
  color: #fff;
  font-weight: 800;
  background: #ff6b8b;
  box-shadow: 0 6px 16px rgba(255, 107, 139, 0.35);
}

.process-btn:hover,
.process-btn:focus {
  color: #fff;
  background: #ff5277;
  box-shadow: 0 8px 20px rgba(255, 82, 119, 0.45);
}

.process-btn.is-disabled {
  background: #f3b8c4;
  box-shadow: none;
}

.result-empty {
  min-height: 520px;
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

.result-empty .el-icon {
  color: #ff9aae;
  font-size: 58px;
}

.result-empty p {
  margin: 0;
  font-size: 14px;
}

.result-content {
  min-height: 0;
  overflow-y: auto;
  display: grid;
  gap: 16px;
  padding-right: 6px;
}

.result-content::-webkit-scrollbar {
  width: 6px;
}

.result-content::-webkit-scrollbar-thumb {
  border-radius: 999px;
  background: rgba(255, 107, 139, 0.35);
}

.result-content::-webkit-scrollbar-track {
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.45);
}

.compare-box {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.compare-item {
  padding: 14px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.64);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.compare-title {
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: 800;
}

.waiting-result {
  min-height: 200px;
  height: clamp(200px, 28vw, 300px);
  max-height: 300px;
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #888;
  background: radial-gradient(circle at 30% 10%, rgba(255, 182, 193, 0.16), transparent 38%), rgba(255, 255, 255, 0.72);
}

.waiting-result .el-icon {
  color: #ff9aae;
  font-size: 42px;
}

.waiting-result p {
  margin: 0;
  font-size: 14px;
}

.result-message {
  padding: 14px 16px;
  border-radius: 16px;
  color: #444;
  font-size: 14px;
  line-height: 1.7;
  background: rgba(255, 107, 139, 0.08);
  border: 1px solid rgba(255, 107, 139, 0.12);
}

.result-message strong {
  color: #ff5277;
}

.params-summary,
.metrics-summary {
  display: grid;
  gap: 10px;
}

.analysis-box,
.steps-block {
  padding: 14px 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.66);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.section-title {
  margin-bottom: 10px;
  color: #ff5277;
  font-size: 14px;
  font-weight: 800;
}

.analysis-box p {
  margin: 0;
  color: #444;
  font-size: 14px;
  line-height: 1.8;
}

.steps-list {
  display: grid;
  gap: 14px;
}

.step-item {
  padding: 12px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.62);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.step-image-frame {
  min-height: 160px;
  height: clamp(160px, 24vw, 260px);
  max-height: 260px;
}

.step-error {
  color: #d84b65;
  font-size: 13px;
}

.summary-item {
  padding: 12px 14px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: rgba(255, 255, 255, 0.66);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.summary-item span {
  color: #666;
  font-size: 13px;
}

.summary-item strong {
  color: #1a1a1a;
  font-size: 14px;
}

:deep(.el-slider__bar) {
  background-color: #ff6b8b;
}

:deep(.el-slider__button) {
  border-color: #ff6b8b;
}

:deep(.el-input__wrapper),
:deep(.el-select__wrapper) {
  border-radius: 12px;
  box-shadow: 0 0 0 1px rgba(255, 107, 139, 0.15) inset;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px rgba(255, 82, 119, 0.45) inset;
}

:deep(.el-switch.is-checked .el-switch__core) {
  border-color: #ff6b8b;
  background-color: #ff6b8b;
}

:deep(.el-form-item__label) {
  width: 100%;
  padding-bottom: 8px;
}

@media (max-width: 1200px) {
  .workspace-shell {
    grid-template-columns: 1fr;
  }

  .algorithm-sidebar {
    position: relative;
    top: 0;
    min-height: auto;
  }

  .menu-scroll {
    height: 360px;
  }
}

@media (max-width: 980px) {
  .workspace-banner {
    padding: 36px 32px;
  }

  .banner-card {
    display: none;
  }

  .right-grid {
    grid-template-columns: 1fr;
  }

  .left-workflow {
    gap: 22px;
  }

  .upload-card,
  .params-card,
  .result-card {
    grid-column: auto;
    grid-row: auto;
  }

  .result-card {
    position: relative;
    top: auto;
    max-height: none;
    overflow: visible;
  }

  .result-content {
    overflow: visible;
    padding-right: 0;
  }
}

@media (max-width: 680px) {
  .workspace-banner {
    padding: 28px 22px;
  }

  .banner-content h1 {
    font-size: 28px;
  }

  .banner-content p {
    font-size: 14px;
  }

  .panel-card {
    padding: 18px;
  }

  .panel-title {
    flex-direction: column;
  }

  .image-meta,
  .task-summary {
    grid-template-columns: 1fr;
  }

  .process-actions {
    justify-content: stretch;
  }

  .process-btn {
    width: 100%;
  }
}
</style>
