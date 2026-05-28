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

```js
import http from './http'

export const runAlgorithm = (moduleSlug, payload) => {
  const slug = String(moduleSlug || '').replaceAll('_', '-')
  return http.post('/api/algorithms/' + slug + '/run', payload)
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

- [ ] **Step 1: Add runAlgorithm and library API imports**

In `<script setup>`, change:

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

Delete lines 481-488 (the entire `const moduleRunEndpointMap = { ... }` block).

- [ ] **Step 3: Simplify getRunEndpoint**

Replace `getRunEndpoint` (lines 1005-1013) with:

```js
function getRunEndpoint(moduleName) {
  return '/api/algorithms/' + String(moduleName || '').replaceAll('_', '-') + '/run'
}
```

- [ ] **Step 4: Add second image reactive state**

Add after `const processing = ref(false)`:

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

Note: `computed` and `watch` are already imported from vue in the existing file.

- [ ] **Step 5: Add second image selector UI in template**

After the upload card closing `</section>` (after line 169), insert:

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

- [ ] **Step 6: Update handleProcess to use runAlgorithm**

In `handleProcess()`, change:

```js
    const data = await http.post(endpoint, payload)
```

To:

```js
    const data = await runAlgorithm(selectedAlgorithm.value.module, payload)
```

And add second_image_path to the payload (after `return_steps: true`):

```js
  if (secondImageEnabled.value && selectedSecondImagePath.value) {
    payload.second_image_path = selectedSecondImagePath.value
  }
```

- [ ] **Step 7: Add scoped style**

In `<style lang="scss" scoped>`, add after `.left-workflow` block:

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

Change `import { onMounted } from 'vue'` (line 174) to:

```js
import { ref, computed, onMounted } from 'vue'
```

Add after `import { useRouter } from 'vue-router'`:

```js
import { getAlgorithmService } from '@/api/algorithms'
```

- [ ] **Step 2: Add dynamic module state and fetch**

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
      tags: (Array.isArray(m.algorithms) ? m.algorithms.slice(0, 3) : []).map(function(a) { return a.display_name || a.name })
    }))
  } catch {
    dynamicModules.value = []
  } finally {
    modulesLoading.value = false
  }
}
```

Replace `onMounted(chech_health)` (line 177) with:

```js
onMounted(function() {
  chech_health()
  loadModules()
})
```

- [ ] **Step 3: Add displayModules computed**

After `loadModules()`, add:

```js
const displayModules = computed(function() {
  return dynamicModules.value.length > 0 ? dynamicModules.value : algorithmModules
})
```

- [ ] **Step 4: Update template**

Replace the algorithm modules section (lines 107-143) with:

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

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/HomeView.vue
git commit -m "feat: dynamic algorithm modules on homepage from backend API"
```
