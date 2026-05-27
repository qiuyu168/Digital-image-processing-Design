<template>
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
              @error="$emit('preview-error')"
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
          <strong>{{ selectedModuleDisplayName }}</strong>
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
</template>

<script setup>
import { Picture, View } from '@element-plus/icons-vue'

defineProps({
  resultInfo: { type: Object, required: true },
  previewDisplayUrl: { type: String, default: '' },
  selectedAlgorithm: { type: Object, default: null },
  selectedModuleDisplayName: { type: String, default: '' },
  selectedRunEndpoint: { type: String, default: '' },
  parameterSummary: { type: Array, default: () => [] },
  metricSummary: { type: Array, default: () => [] }
})

defineEmits(['preview-error'])

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
</script>

<style lang="scss" scoped>
.panel-card {
  padding: 24px;
  border-radius: var(--radius-lg);
  background: #fff;
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
}

.result-card {
  animation: resultIn var(--dur-slow) var(--ease-decel) both;
}

@keyframes resultIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.panel-title {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.title-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.panel-title h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.2px;
}

.soft-tag {
  border: 1px solid var(--c-line);
  color: var(--c-amber);
  background: var(--c-peach);
  border-radius: var(--radius-sm);
  font-weight: 600;
}

.result-empty {
  min-height: 320px;
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--c-ink-2);
  background: var(--c-cream);
  border: 1.5px dashed var(--c-line);
}

.result-empty .el-icon {
  color: var(--c-amber);
  font-size: 48px;
  opacity: 0.6;
}

.result-empty p {
  margin: 0;
  font-size: 13px;
}

.result-content {
  display: grid;
  gap: 14px;
}

.compare-box {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.compare-item {
  padding: 12px;
  border-radius: var(--radius-md);
  background: var(--c-cream);
  border: 1px solid var(--c-line);
}

.compare-title {
  margin-bottom: 10px;
  font-size: 13px;
  font-weight: 700;
  color: var(--c-ink);
  letter-spacing: -0.1px;
}

.image-frame {
  width: 100%;
  border-radius: var(--radius-md);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--c-cream);
  border: 1px solid var(--c-line);
}

.result-image-frame {
  min-height: 200px;
  height: clamp(200px, 24vw, 280px);
  max-height: 280px;
}

.compare-image {
  width: 100%;
  height: 100%;
}

:deep(.compare-image .el-image__inner) {
  width: 100%;
  height: 100%;
  object-fit: contain;
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
  color: var(--c-ink-2);
  font-size: 13px;
}

.image-error .el-icon {
  color: var(--c-amber);
  font-size: 36px;
}

.waiting-result {
  min-height: 200px;
  height: clamp(200px, 24vw, 280px);
  max-height: 280px;
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--c-ink-2);
  background: #fff;
  border: 1px solid var(--c-line);
}

.waiting-result .el-icon {
  color: var(--c-amber);
  font-size: 32px;
  opacity: 0.6;
}

.waiting-result p {
  margin: 0;
  font-size: 13px;
}

.result-message {
  padding: 12px 14px;
  border-radius: var(--radius-md);
  color: var(--c-ink-2);
  font-size: 13px;
  line-height: 1.6;
  background: var(--c-cream-2);
  border: 1px solid var(--c-line);
}

.result-message strong {
  color: var(--c-amber);
}

.task-summary {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.task-summary div {
  min-width: 0;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  background: var(--c-cream);
  border: 1px solid var(--c-line);
}

.task-summary span {
  display: block;
  margin-bottom: 4px;
  color: var(--c-ink-2);
  font-size: 11px;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.task-summary strong {
  display: block;
  color: var(--c-ink);
  font-size: 13px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.params-summary,
.metrics-summary {
  display: grid;
  gap: 8px;
}

.analysis-box,
.steps-block {
  padding: 14px;
  border-radius: var(--radius-md);
  background: var(--c-cream);
  border: 1px solid var(--c-line);
}

.section-title {
  margin-bottom: 10px;
  color: var(--c-amber);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.analysis-box p {
  margin: 0;
  color: var(--c-ink-2);
  font-size: 13px;
  line-height: 1.7;
}

.steps-list {
  display: grid;
  gap: 12px;
}

.step-item {
  padding: 12px;
  border-radius: var(--radius-md);
  background: #fff;
  border: 1px solid var(--c-line);
}

.step-image-frame {
  min-height: 160px;
  height: clamp(160px, 24vw, 260px);
  max-height: 260px;
}

.step-error {
  color: #b91c1c;
  font-size: 13px;
}

.summary-item {
  padding: 10px 12px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: #fff;
  border: 1px solid var(--c-line);
}

.summary-item span {
  color: var(--c-ink-2);
  font-size: 12px;
}

.summary-item strong {
  color: var(--c-ink);
  font-size: 13px;
  font-weight: 600;
}

@media (max-width: 980px) {
  .compare-box {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 680px) {
  .panel-card {
    padding: 18px;
  }

  .panel-title {
    flex-direction: column;
  }

  .task-summary {
    grid-template-columns: 1fr;
  }
}
</style>
