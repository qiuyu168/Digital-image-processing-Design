<template>
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
        @click="$emit('reset')"
      >
        重置
      </el-button>
    </div>

    <div class="params-body">
      <el-empty
        v-if="!selectedAlgorithm"
        description="请先选择算法"
        :image-size="92"
      />

      <NoParamCard
        v-else-if="paramList.length === 0"
        :module-name="selectedAlgorithm.module"
      />

      <el-form v-else class="params-form" label-position="top">
        <el-form-item
          v-for="param in paramList"
          :key="param.key"
          class="param-item"
          :class="`module-tone-${selectedAlgorithm.module}`"
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
            @change="$emit('param-change', param)"
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
            @change="$emit('param-change', param)"
          />

          <el-input
            v-else
            v-model="paramForm[param.key]"
            class="full-control"
            placeholder="请输入参数值"
          />
        </el-form-item>
      </el-form>
    </div>

    <div class="process-actions">
      <el-button
        class="process-btn"
        type="primary"
        :disabled="!canProcess"
        :loading="processing"
        @click="$emit('process')"
      >
        <el-icon><MagicStick /></el-icon>
        开始处理
      </el-button>
    </div>
  </section>
</template>

<script setup>
import { MagicStick } from '@element-plus/icons-vue'
import NoParamCard from './NoParamCard.vue'

defineProps({
  selectedAlgorithm: { type: Object, default: null },
  paramList: { type: Array, default: () => [] },
  paramForm: { type: Object, required: true },
  canProcess: { type: Boolean, default: false },
  processing: { type: Boolean, default: false }
})

defineEmits(['param-change', 'process', 'reset'])

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
</script>

<style lang="scss" scoped>
.panel-card {
  padding: 24px;
  border-radius: var(--radius-lg);
  background: #fff;
  border: 1px solid var(--c-line);
  box-shadow: var(--shadow-1);
  display: flex;
  flex-direction: column;
}

.params-card {
  position: sticky;
  top: 88px;
  max-height: calc(100vh - 110px);
}

.panel-title {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
  flex-shrink: 0;
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

.params-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding-right: 4px;
}

.params-body::-webkit-scrollbar {
  width: 6px;
}

.params-body::-webkit-scrollbar-thumb {
  border-radius: 999px;
  background: rgba(43, 36, 25, 0.18);
}

.reset-btn {
  color: var(--c-ink);
  border: 1px solid var(--c-line);
  background: #fff;
  border-radius: var(--radius-sm);
  font-weight: 600;
  transition: color var(--dur-fast) var(--ease-standard),
              border-color var(--dur-fast) var(--ease-standard),
              background var(--dur-fast) var(--ease-standard);
}

.reset-btn:hover {
  color: var(--c-amber);
  border-color: rgba(217, 119, 6, 0.3);
  background: rgba(217, 119, 6, 0.06);
}

.params-form {
  padding-top: 4px;
}

.param-item {
  padding: 14px;
  margin-bottom: 12px;
  border-radius: var(--radius-md);
  background: var(--c-cream);
  border: 1px solid var(--c-line);
}

.param-label {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.param-label span {
  font-weight: 600;
  color: var(--c-ink);
  font-size: 13px;
}

.param-label em {
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  color: var(--c-amber);
  font-style: normal;
  font-size: 11px;
  font-weight: 600;
  background: var(--c-peach);
}

.full-control {
  width: 100%;
}

.process-actions {
  flex-shrink: 0;
  display: flex;
  justify-content: stretch;
  padding-top: 16px;
  margin-top: 12px;
  border-top: 1px solid var(--c-line);
}

.process-btn {
  width: 100%;
  height: 42px;
  border: none;
  border-radius: var(--radius-md);
  color: #fff;
  font-weight: 600;
  background: var(--c-amber);
  box-shadow: none;
  transition: background var(--dur-fast) var(--ease-standard);
}

.process-btn:hover,
.process-btn:focus {
  color: #fff;
  background: var(--c-amber-2);
}

.process-btn.is-disabled {
  background: rgba(217, 119, 6, 0.35);
}

.module-tone-grayscale_image,
.module-tone-color_image,
.module-tone-geometric_transform,
.module-tone-spatial_filter,
.module-tone-frequency_analysis,
.module-tone-frequency_filter {
  border-left: 3px solid var(--c-amber);
}

:deep(.el-slider__bar) {
  background-color: var(--c-amber);
}

:deep(.el-slider__button) {
  border-color: var(--c-amber);
}

:deep(.el-input__wrapper),
:deep(.el-select__wrapper) {
  border-radius: var(--radius-sm);
  box-shadow: 0 0 0 1px var(--c-line) inset;
  background: #fff;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px var(--c-amber) inset;
}

:deep(.el-switch.is-checked .el-switch__core) {
  border-color: var(--c-amber);
  background-color: var(--c-amber);
}

:deep(.el-form-item__label) {
  width: 100%;
  padding-bottom: 8px;
}

@media (max-width: 1279px) {
  .params-card {
    position: relative;
    top: auto;
    max-height: none;
  }

  .params-body {
    overflow: visible;
  }
}

@media (max-width: 680px) {
  .panel-card {
    padding: 18px;
  }

  .panel-title {
    flex-direction: column;
  }
}
</style>
