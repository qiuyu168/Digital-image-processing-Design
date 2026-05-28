# Frontend-Backend Adaptation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adapt frontend to fully cover backend's 9 algorithm modules, fix bugs, and replace hardcoded content with dynamic API data.

**Architecture:** Four independent file changes. `check_health.js` and `run.js` can be done first (no deps). `WorkspaceView.vue` depends on `run.js`. `HomeView.vue` is independent throughout.

**Tech Stack:** Vue 3.5, Element Plus, Axios, Vite 8

---

### Task 1: Fix check_health.js missing ElMessage import

**Files:**
- Modify: `frontend/src/utils/check_health.js`

- [ ] **Step 1: Add ElMessage import**

```js
import { ElMessage } from 'element-plus'
import { checkHealthService } from "@/api/health"

export const chech_health = async () => {
    try {
        const data = await checkHealthService()
        if (data.success)
            ElMessage.success(data.message)
        else
            ElMessage.error('服务器异常！')
    } catch (e) {
        ElMessage.error('服务器异常！')
    }
    
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/utils/check_health.js
git commit -m "fix: add missing ElMessage import in check_health.js"
```

---

### Task 2: Implement api/run.js

**Files:**
- Modify: `frontend/src/api/run.js`

- [ ] **Step 1: Write runAlgorithm function**

Replace the empty file with:

```js
import http from './http'

export const runAlgorithm = (moduleSlug, payload) => {
  const slug = String(moduleSlug || '').replaceAll('_', '-')
  return http.post(`/api/algorithms/${slug}/run`, payload)
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/api/run.js
git commit -m "feat: implement runAlgorithm API function"
```

---

### Task 3: Update WorkspaceView.vue

**Files:**
- Modify: `frontend/src/views/WorkspaceView.vue`

Three sub-changes: (A) remove hardcoded endpoint map, (B) use imported runAlgorithm, (C) add second image selector from library.

- [ ] **Step 1: Add runAlgorithm and library API imports**

In the `<script setup>` block, change:

```js
import http from '@/api/http'
import { getAlgorithmService } from '@/api/algorithms'
import { uploadImageService } from '@/api/upload'
```

To:

```js
import { getAlgorithmService } from '@/api/algorithms'
import { uploadImageService } from '@/api/upload'
import { runAlgorithm } from '@/api/run'
import { getDetailImageService } from '@/api/library'
```

- [ ] **Step 2: Remove hardcoded moduleRunEndpointMap**

Delete lines 481-488:

```js
const moduleRunEndpointMap = {
  grayscale_image: '/api/algorithms/grayscale-image/run',
  color_image: '/api/algorithms/color-image/run',
  geometric_transform: '/api/algorithms/geometric-transform/run',
  spatial_filter: '/api/algorithms/spatial-filter/run',
  frequency_analysis: '/api/algorithms/frequency-analysis/run',
  frequency_filter: '/api/algorithms/frequency-filter/run'
}
```

- [ ] **Step 3: Replace getRunEndpoint to always use computed slug**

Replace the `getRunEndpoint` function (lines 1005-1013):

```js
function getRunEndpoint(moduleName) {
  const normalizedModuleName = String(moduleName || '')

  if (moduleRunEndpointMap[normalizedModuleName]) {
    return moduleRunEndpointMap[normalizedModuleName]
  }

  return `/api/algorithms/${normalizedModuleName.replaceAll('_', '-')}/run`
}
```

With:

```js
function getRunEndpoint(moduleName) {
  return `/api/algorithms/${String(moduleName || '').replaceAll('_', '-')}/run`
}
```

- [ ] **Step 4: Add second image reactive state and library images loader**

Add after `const processing = ref(false)` (around line 492):

```js
const secondImageEnabled = computed(() => {
  return selectedAlgorithm.value?.module === 'basic_operation'
})

const libraryImages = ref([])
const libraryImagesLoading = ref(false)
const selectedSecondImagePath = ref('')

async function loadLibraryImagesForSecond() {
  if (!secondImageEnabled.value) return
  libraryImagesLoading.value = true
  try {
    const data = await getDetailImageService({ params: { category: 'anime_character' } })
    libraryImages.value = Array.isArray(data?.images) ? data.images : []
  } catch {
    libraryImages.value = []
  } finally {
    libraryImagesLoading.value = false
  }
}

watch(secondImageEnabled, (enabled) => {
  if (enabled) {
    selectedSecondImagePath.value = ''
    loadLibraryImagesForSecond()
  }
})
```

- [ ] **Step 5: Add second image selector UI in template**

In `<template>`, after the upload card section (after line 169, right before `<!-- 参数设置 -->` section), add:

```html
            <section v-if="secondImageEnabled" class="panel-card second-image-card">
              <div class="panel-title">
                <div class="title-left">
                  <span class="title-icon">🖼️</span>
                  <div>
                    <h3>选择第二张图片</h3>
                    <p>该算法需要两张图片，从图像库中选择第二张</p>
                  </div>
                </div>
              </div>

              <el-select
                v-model="selectedSecondImagePath"
                class="full-control"
                placeholder="请选择第二张图片"
                :loading="libraryImagesLoading"
                clearable
              >
                <el-option
                  v-for="img in libraryImages"
                  :key="img.image_path"
                  :label="img.name || img.filename"
                  :value="img.image_path"
                />
              </el-select>
            </section>
```

- [ ] **Step 6: Update handleProcess to use runAlgorithm and include second_image_path**

Replace the `handleProcess` function (lines 921-976). Change the endpoint creation and the http.post call:

Old:
```js
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
```

New:
```js
  const moduleSlug = selectedAlgorithm.value.module
  const endpoint = getRunEndpoint(moduleSlug)
  const payload = {
    source_type: 'upload',
    image_path: uploadedImage.id,
    algorithm: selectedAlgorithm.value.name,
    algorithm_display_name: selectedAlgorithm.value.displayName,
    params: buildProcessParams(),
    return_steps: true
  }

  if (secondImageEnabled.value && selectedSecondImagePath.value) {
    payload.second_image_path = selectedSecondImagePath.value
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
    const data = await runAlgorithm(moduleSlug, payload)
```

- [ ] **Step 7: Add scoped style for second-image-card**

In the `<style lang="scss" scoped>` block, add at the end (before responsive media queries):

```scss
.second-image-card {
  margin-top: 0;
}

.second-image-card .full-control {
  margin-top: 8px;
}
```

- [ ] **Step 8: Commit**

```bash
git add frontend/src/views/WorkspaceView.vue
git commit -m "feat: adapt workspace to all 9 modules, use runAlgorithm, add second image selector"
```

---

### Task 4: Update HomeView.vue with dynamic algorithm data

**Files:**
- Modify: `frontend/src/views/HomeView.vue`

- [ ] **Step 1: Update imports**

In `<script setup>`, change the vue import on line 174 from:

```js
import { onMounted } from 'vue'
```

To:

```js
import { ref, computed, onMounted } from 'vue'
```

And add the API import after `import { useRouter } from 'vue-router'`:

```js
import { getAlgorithmService } from '@/api/algorithms'
```

- [ ] **Step 2: Add dynamic module data state and fetch logic**

After `const router = useRouter()`, add:

```js
const dynamicModules = ref([])
const modulesLoading = ref(false)

async function loadModules() {
  modulesLoading.value = true
  try {
    const data = await getAlgorithmService()
    const rawModules = Array.isArray(data?.modules) ? data.modules : []
    dynamicModules.value = rawModules.map((m) => ({
      icon: '🌸',
      title: m.display_name || m.module,
      desc: '共 ' + (Array.isArray(m.algorithms) ? m.algorithms.length : 0) + ' 个算法',
      tags: (Array.isArray(m.algorithms) ? m.algorithms.slice(0, 3) : []).map((a) => a.display_name || a.name)
    }))
  } catch {
    dynamicModules.value = []
  } finally {
    modulesLoading.value = false
  }
}

onMounted(() => {
  chech_health()
  loadModules()
})
```

Note: replace the existing `onMounted(chech_health)` call (line 177) with the `onMounted` block above that calls both `chech_health()` and `loadModules()`.

- [ ] **Step 3: Update template to use dynamic data with fallback**

In the algorithm modules section (lines 107-143), replace:

```html
    <section class="section-block">
      <div class="section-title">
        <span class="title-icon">🌸</span>
        <h2>算法模块</h2>
        <p>六大图像处理方向，覆盖数字图像处理核心算法</p>
      </div>

      <div class="module-grid">
        <div
          v-for="item in algorithmModules"
          :key="item.title"
          class="module-card"
          @click="goWorkspace"
        >
          <div class="module-icon">
            {{ item.icon }}
          </div>

          <div class="module-content">
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>

            <div class="module-tags">
              <span
                v-for="tag in item.tags"
                :key="tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <div class="module-more">
            进入处理
          </div>
        </div>
      </div>
    </section>
```

With:

```html
    <section class="section-block">
      <div class="section-title">
        <span class="title-icon">🌸</span>
        <h2>算法模块</h2>
        <p>{{ dynamicModules.length > 0 ? dynamicModules.length + '大图像处理方向，覆盖数字图像处理核心算法' : '六大图像处理方向，覆盖数字图像处理核心算法' }}</p>
      </div>

      <div v-if="modulesLoading" class="module-grid">
        <div v-for="n in 6" :key="n" class="module-card skeleton-card">
          <el-skeleton :rows="3" animated />
        </div>
      </div>

      <div v-else class="module-grid">
        <div
          v-for="item in displayModules"
          :key="item.title"
          class="module-card"
          @click="goWorkspace"
        >
          <div class="module-icon">
            {{ item.icon }}
          </div>

          <div class="module-content">
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>

            <div class="module-tags">
              <span
                v-for="tag in item.tags"
                :key="tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <div class="module-more">
            进入处理
          </div>
        </div>
      </div>
    </section>
```

- [ ] **Step 4: Add computed displayModules for fallback**

After `loadModules()` function and before `goWorkspace()`, add:

```js
const displayModules = computed(() => {
  return dynamicModules.value.length > 0 ? dynamicModules.value : algorithmModules
})
```

And update the `v-for` in the template to use `displayModules`:

```html
        <div
          v-for="item in displayModules"
          :key="item.title"
```

This keeps `algorithmModules` hardcoded data as fallback when the API is unavailable.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/HomeView.vue
git commit -m "feat: dynamic algorithm modules on homepage from backend API"
```
