<template>
  <el-form
    ref="passwordFormRef"
    :model="passwordForm"
    :rules="passwordRules"
    label-position="top"
    size="large"
  >
    <el-form-item label="旧密码" prop="oldPassword">
      <el-input
        v-model="passwordForm.oldPassword"
        type="password"
        show-password
        placeholder="请输入旧密码"
      />
    </el-form-item>

    <el-form-item label="新密码" prop="newPassword">
      <el-input
        v-model="passwordForm.newPassword"
        type="password"
        show-password
        placeholder="请输入新密码"
      />
    </el-form-item>

    <!-- Password strength indicator -->
    <div class="strength-bar" v-if="passwordForm.newPassword">
      <div class="strength-segments">
        <span class="seg" :class="{ fill: passwordForm.newPassword.length >= 1 }"></span>
        <span class="seg" :class="{ fill: passwordForm.newPassword.length >= 6 }"></span>
        <span class="seg" :class="{ fill: passwordForm.newPassword.length >= 10 }"></span>
      </div>
      <span class="strength-label">{{ strengthLabel }}</span>
    </div>

    <el-form-item label="确认新密码" prop="confirmPassword">
      <el-input
        v-model="passwordForm.confirmPassword"
        type="password"
        show-password
        placeholder="请再次输入新密码"
      />
    </el-form-item>

    <el-form-item>
      <el-button class="primary-btn" @click="$emit('change')">
        修改密码
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, computed } from 'vue'

defineProps({
  passwordForm: { type: Object, required: true },
  passwordRules: { type: Object, required: true }
})

defineEmits(['change'])

const passwordFormRef = ref(null)

function validate() {
  return passwordFormRef.value?.validate()
}

defineExpose({ validate })

const strengthLabel = computed(() => {
  const len = props.passwordForm.newPassword?.length || 0
  if (len >= 10) return '强'
  if (len >= 6) return '中'
  if (len >= 1) return '弱'
  return ''
})
</script>

<style scoped>
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

/* Strength bar */
.strength-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: -16px 0 24px;
}

.strength-segments {
  display: flex;
  gap: 4px;
}

.seg {
  display: block;
  width: 60px;
  height: 4px;
  border-radius: 2px;
  background: var(--c-line);
  transition: background var(--dur-fast) var(--ease-standard);
}

.seg.fill:nth-child(1) {
  background: var(--c-amber);
}

.seg.fill:nth-child(2) {
  background: var(--c-amber-2);
}

.seg.fill:nth-child(3) {
  background: #b45309;
}

.strength-label {
  font-size: 12px;
  color: var(--c-ink-2);
  font-weight: 500;
}
</style>
