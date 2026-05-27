<template>
  <el-form
    ref="infoFormRef"
    :model="infoForm"
    :rules="infoRules"
    label-position="top"
    size="large"
    class="info-form"
  >
    <el-form-item label="账号" prop="username">
      <el-input v-model="infoForm.username" disabled />
    </el-form-item>

    <el-form-item label="昵称" prop="nickname">
      <el-input v-model="infoForm.nickname" placeholder="请输入昵称" />
    </el-form-item>

    <el-form-item label="邮箱" prop="email">
      <el-input v-model="infoForm.email" placeholder="请输入邮箱" />
    </el-form-item>

    <el-form-item>
      <el-button class="primary-btn" @click="$emit('save')">
        保存修改
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  infoForm: { type: Object, required: true },
  infoRules: { type: Object, required: true }
})

defineEmits(['save'])

const infoFormRef = ref(null)

function validate() {
  return infoFormRef.value?.validate()
}

defineExpose({ validate })
</script>

<style scoped>
.info-form {
  :deep(.el-form-item) {
    margin-bottom: 24px;
  }

  :deep(.el-form-item__label) {
    padding-bottom: 6px;
    color: var(--c-ink-2);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.2px;
  }
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-form-item__label) {
  padding-bottom: 6px;
  color: var(--c-ink-2);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.2px;
  line-height: 1.4;
}

:deep(.el-input__wrapper) {
  background: var(--c-cream-2);
  box-shadow: none;
  border-radius: var(--radius-sm);
  padding: 0 14px;
  min-height: 42px;
  border: 1px solid var(--c-line);
  transition: border-color var(--dur-fast) var(--ease-standard), background var(--dur-fast) var(--ease-standard);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: none;
  border-color: rgba(217, 119, 6, 0.4);
  background: #fff;
}

:deep(.el-input__inner) {
  color: var(--c-ink);
  height: 42px;
  font-size: 14px;
}

:deep(.el-form-item__error) {
  color: var(--c-amber-2);
  padding-top: 4px;
  font-size: 12px;
}

.primary-btn {
  height: 40px;
  padding: 0 22px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--c-amber);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: background var(--dur-fast) var(--ease-standard);

  &:hover, &:focus {
    background: var(--c-amber-2);
    color: #fff;
  }
}
</style>
