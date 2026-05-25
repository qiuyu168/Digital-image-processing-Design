<script setup>
import { useAuthStore } from '@/stores/authStore'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

import bg1 from '@/assets/background/bg1.jpg'
import bg2 from '@/assets/background/bg2.jpg'
import bg3 from '@/assets/background/bg3.jpg'
import bg4 from '@/assets/background/bg4.jpg'

const images = [bg1, bg2, bg3, bg4]
const currentIndex = ref(0)
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % images.length
  }, 5000) // 5秒切换一次
})

onUnmounted(() => {
  clearInterval(timer)
})
// ------------------------------

const isRegister = ref(false)
const formModel = ref({
  username: '',
  password: '',
  repassword: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 5, max: 10, message: '用户名必须是5-10位的字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码必须是6-15位的非空字符',
      trigger: 'blur'
    }
  ],
  repassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码必须是6-15的非空字符',
      trigger: 'blur'
    },
    {
      validator: (rule, value, callback) => {
        if (value != formModel.value.password) {
          callback(new Error('两次输入密码不一致！'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const userStore = useAuthStore()
const router = useRouter()

watch(isRegister, () => {
  formModel.value = {
    username: '',
    password: '',
    repassword: ''
  }
})

const form = ref(null)

const register = async () => {
  await form.value.validate()
  ElMessage.success('注册成功！')
  isRegister.value = false
}

const login = async () => {
  await form.value.validate()
  ElMessage.success('登录成功！')
  router.push('/')
}
</script>

<template>
  <div class="login-page">
    <!-- 背景图片轮换层 -->
    <div class="bg-slider">
      <img
        v-for="(img, index) in images"
        :key="index"
        :src="img"
        :class="{ active: index === currentIndex }"
        class="bg-image"
      />
    </div>

    <!-- 表单卡片 -->
    <div class="form-card">
      <!-- 注册表单 -->
      <el-form
        v-if="isRegister"
        ref="form"
        :model="formModel"
        :rules="rules"
        size="large"
        autocomplete="off"
        class="login-form"
      >
        <el-form-item>
          <h1>注册</h1>
        </el-form-item>

        <el-form-item prop="username">
          <el-input
            v-model="formModel.username"
            :prefix-icon="User"
            placeholder="请输入用户名"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="formModel.password"
            :prefix-icon="Lock"
            type="password"
            show-password
            placeholder="请输入密码"
          />
        </el-form-item>

        <el-form-item prop="repassword">
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
            type="primary"
            auto-insert-space
            @click="register"
          >
            注册
          </el-button>
        </el-form-item>

        <el-form-item class="bottom-link">
          <span>已有账号？</span>
          <el-link type="info" underline="never" @click="isRegister = false">
            返回登录
          </el-link>
        </el-form-item>
      </el-form>

      <!-- 登录表单 -->
      <el-form
        v-else
        ref="form"
        :model="formModel"
        :rules="rules"
        size="large"
        autocomplete="off"
        class="login-form"
      >
        <el-form-item>
          <h1>登录</h1>
        </el-form-item>

        <el-form-item prop="username">
          <el-input
            v-model="formModel.username"
            :prefix-icon="User"
            placeholder="请输入用户名"
          />
        </el-form-item>

        <el-form-item prop="password">
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
            <el-link type="primary" underline="never">
              忘记密码？
            </el-link>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            class="button"
            type="primary"
            auto-insert-space
            @click="login"
          >
            登录
          </el-button>
        </el-form-item>

        <el-form-item class="bottom-link">
          <span>还没有账号？</span>
          <el-link type="info" underline="never" @click="isRegister = true">
            注册
          </el-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.login-page::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(4, 10, 22, 0.25);
  z-index: 0;
}

.bg-slider {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: #000;
}

.bg-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 1s ease-in-out;
}

.bg-image.active {
  opacity: 1;
}

.form-card {
  position: relative;
  z-index: 1;
  width: 430px;
  min-height: 500px;
  padding: 50px 38px 36px;
  border-radius: 4px;
  background: rgba(8, 18, 35, 0.48);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  display: flex;
  align-items: center;
}

.login-form {
  width: 100%;
}

h1 {
  width: 100%;
  margin: 0 0 18px;
  text-align: center;
  color: #ffffff;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 1px;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-input__wrapper) {
  background: transparent;
  box-shadow: none;
  border-radius: 0;
  padding: 0 14px;
  min-height: 44px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.75);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: none;
  border-bottom-color: #ffffff;
}

:deep(.el-input__inner) {
  color: #ffffff;
  height: 44px;
  font-size: 15px;
}

:deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.88);
}

:deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.9);
  margin-right: 12px;
  display: flex;
  align-items: center;
}

:deep(.el-input__suffix) {
  color: rgba(255, 255, 255, 0.9);
  margin-left: 12px;
  display: flex;
  align-items: center;
}

:deep(.el-input__prefix-inner),
:deep(.el-input__suffix-inner) {
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.el-input__prefix svg),
:deep(.el-input__suffix svg) {
  width: 18px;
  height: 18px;
}

:deep(.el-form-item__error) {
  color: #ffd2d2;
  padding-top: 5px;
}

.form-options {
  margin-bottom: 18px;
}

.option-row {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

:deep(.el-checkbox) {
  color: #ffffff;
}

:deep(.el-checkbox__label) {
  color: #ffffff;
}

:deep(.el-link) {
  color: #ffffff;
  font-size: 14px;
}

:deep(.el-link:hover) {
  color: #dbeafe;
}

.button {
  width: 100%;
  height: 42px;
  border: none;
  border-radius: 2px;
  background: #ffffff;
  color: #111827;
  font-size: 15px;
  font-weight: 500;
}

.button:hover,
.button:focus {
  background: #f3f4f6;
  color: #111827;
}

.bottom-link {
  margin-bottom: 0;
}

.bottom-link :deep(.el-form-item__content) {
  justify-content: center;
  color: #ffffff;
  font-size: 14px;
  gap: 6px;
}
</style>