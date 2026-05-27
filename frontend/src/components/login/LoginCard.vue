<script setup>
import { ref } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'

const props = defineProps({
  isRegister: Boolean,
  formModel: Object,
  rules: Object
})

const emit = defineEmits(['login', 'register', 'toggle-register'])

const form = ref(null)

defineExpose({
  validate: () => form.value?.validate()
})
</script>

<template>
  <main class="form-pane">
    <div class="form-card">
      <!-- Tab switch -->
      <div class="form-tabs">
        <button
          class="tab-btn"
          :class="{ active: !isRegister }"
          @click="emit('toggle-register', false)"
        >
          登录
        </button>
        <button
          class="tab-btn"
          :class="{ active: isRegister }"
          @click="emit('toggle-register', true)"
        >
          注册
        </button>
      </div>

      <!-- Login form -->
      <Transition name="form-fade" mode="out-in">
        <el-form
          v-if="!isRegister"
          key="login"
          ref="form"
          :model="formModel"
          :rules="rules"
          size="large"
          autocomplete="off"
          class="login-form"
          label-position="top"
        >
          <el-form-item>
            <h1>登录</h1>
          </el-form-item>

          <el-form-item prop="username" label="用户名">
            <el-input
              v-model="formModel.username"
              :prefix-icon="User"
              placeholder="请输入用户名"
            />
          </el-form-item>

          <el-form-item prop="password" label="密码">
            <el-input
              v-model="formModel.password"
              :prefix-icon="Lock"
              type="password"
              show-password
              placeholder="请输入密码"
            />
          </el-form-item>

          <el-form-item class="form-options">
            <div class="option-row">
              <el-checkbox>记住我</el-checkbox>
              <el-link underline="never">
                忘记密码？
              </el-link>
            </div>
          </el-form-item>

          <el-form-item>
            <el-button
              class="button"
              auto-insert-space
              @click="emit('login')"
            >
              登录
            </el-button>
          </el-form-item>

          <el-form-item class="bottom-link">
            <span>还没有账号？</span>
            <el-link underline="never" @click="emit('toggle-register', true)">
              注册
            </el-link>
          </el-form-item>
        </el-form>

        <!-- Register form -->
        <el-form
          v-else
          key="register"
          ref="form"
          :model="formModel"
          :rules="rules"
          size="large"
          autocomplete="off"
          class="login-form"
          label-position="top"
        >
          <el-form-item>
            <h1>注册</h1>
          </el-form-item>

          <el-form-item prop="username" label="用户名">
            <el-input
              v-model="formModel.username"
              :prefix-icon="User"
              placeholder="请输入用户名"
            />
          </el-form-item>

          <el-form-item prop="password" label="密码">
            <el-input
              v-model="formModel.password"
              :prefix-icon="Lock"
              type="password"
              show-password
              placeholder="请输入密码"
            />
          </el-form-item>

          <el-form-item prop="repassword" label="确认密码">
            <el-input
              v-model="formModel.repassword"
              :prefix-icon="Lock"
              type="password"
              show-password
              placeholder="请再次输入密码"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              class="button"
              auto-insert-space
              @click="emit('register')"
            >
              注册
            </el-button>
          </el-form-item>

          <el-form-item class="bottom-link">
            <span>已有账号？</span>
            <el-link underline="never" @click="emit('toggle-register', false)">
              返回登录
            </el-link>
          </el-form-item>
        </el-form>
      </Transition>
    </div>
  </main>
</template>

<style lang="scss" scoped>
.form-pane {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 56px;
}

.form-card {
  width: 100%;
  max-width: 420px;
  padding: 40px 36px 32px;
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-3);
}

/* ================ Tab switch ================ */
.form-tabs {
  display: flex;
  border-bottom: 1px solid var(--c-line);
  margin-bottom: 28px;
}

.tab-btn {
  flex: 1;
  padding: 10px 0 12px;
  background: none;
  border: none;
  font-size: 15px;
  font-weight: 600;
  color: var(--c-ink-2);
  cursor: pointer;
  position: relative;
  transition: color var(--dur-fast) var(--ease-standard);

  &::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 2px;
    background: transparent;
    border-radius: 1px;
    transition: background var(--dur-fast) var(--ease-standard);
  }

  &.active {
    color: var(--c-amber);

    &::after {
      background: var(--c-amber);
    }
  }

  &:hover:not(.active) {
    color: var(--c-ink);
  }
}

/* ================ Form fade transition ================ */
.form-fade-enter-active,
.form-fade-leave-active {
  transition: all 200ms var(--ease-standard);
}

.form-fade-enter-from {
  opacity: 0;
  transform: translateY(14px);
}

.form-fade-leave-to {
  opacity: 0;
  transform: translateY(-14px);
}

/* ================ Form ================ */
.login-form {
  width: 100%;
}

h1 {
  width: 100%;
  margin: 0 0 8px;
  color: var(--c-ink);
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

:deep(.el-form-item) {
  margin-bottom: 18px;
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
  transition: border-color 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.14);
  border-color: rgba(217, 119, 6, 0.4);
  background: #fff;
}

:deep(.el-input__inner) {
  color: var(--c-ink);
  height: 42px;
  font-size: 14px;
}

:deep(.el-input__inner::placeholder) {
  color: var(--c-ink-2);
  opacity: 0.6;
}

:deep(.el-input__prefix),
:deep(.el-input__suffix) {
  color: var(--c-ink-2);
  display: flex;
  align-items: center;
}

:deep(.el-input__prefix) {
  margin-right: 8px;
}

:deep(.el-input__suffix) {
  margin-left: 8px;
}

:deep(.el-input__prefix svg),
:deep(.el-input__suffix svg) {
  width: 16px;
  height: 16px;
}

:deep(.el-form-item__error) {
  color: var(--c-amber-2);
  padding-top: 4px;
  font-size: 12px;
}

.form-options {
  margin-bottom: 14px;
}

.option-row {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

:deep(.el-checkbox__label) {
  color: var(--c-ink-2);
  font-size: 13px;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--c-amber);
  border-color: var(--c-amber);
}

:deep(.el-link) {
  color: var(--c-amber);
  font-size: 13px;
  font-weight: 500;
}

:deep(.el-link:hover) {
  color: var(--c-amber-2);
}

.button {
  width: 100%;
  height: 42px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--c-amber);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
  transition: background 0.18s ease;
}

.button:hover,
.button:focus {
  background: var(--c-amber-2);
  color: #fff;
}

.bottom-link {
  margin-bottom: 0;
}

.bottom-link :deep(.el-form-item__content) {
  justify-content: center;
  color: var(--c-ink-2);
  font-size: 13px;
  gap: 6px;
}

/* ================ Responsive ================ */
@media (max-width: 1024px) {
  .form-pane {
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .form-card {
    padding: 32px 24px 24px;
  }

  h1 {
    font-size: 22px;
  }
}
</style>
