<template>
  <div class="login-page">
    <div class="login-glow login-glow--pink"></div>
    <div class="login-glow login-glow--purple"></div>
    <div class="login-glow login-glow--blue"></div>

    <div class="login-card glass-card">
      <div class="login-logo">✦</div>
      <h1 class="login-title">动漫图像处理系统</h1>
      <p class="login-sub">Interactive Digital Image Processing</p>

      <div class="login-tabs">
        <button :class="{ active: isLogin }" @click="isLogin = true">登录</button>
        <button :class="{ active: !isLogin }" @click="isLogin = false">注册</button>
      </div>

      <form @submit.prevent="handleSubmit" class="login-form">
        <input v-model="username" class="glass-input" placeholder="用户名" autocomplete="username">
        <input v-model="password" type="password" class="glass-input" placeholder="密码" autocomplete="current-password">
        <input v-if="!isLogin" v-model="confirmPassword" type="password" class="glass-input" placeholder="确认密码">

        <button type="submit" class="btn-gradient login-submit">
          {{ isLogin ? '登 录' : '注 册' }}
        </button>
      </form>

      <p class="login-switch">
        {{ isLogin ? '没有账号？' : '已有账号？' }}
        <span @click="isLogin = !isLogin">{{ isLogin ? '立即注册' : '立即登录' }}</span>
      </p>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

import bg1 from '@/assets/background/bg1.jpg'
import bg2 from '@/assets/background/bg2.jpg'
import bg3 from '@/assets/background/bg3.jpg'
import bg4 from '@/assets/background/bg4.jpg'
import { generateTestToken } from '@/utils/token'
import http from '@/api/http'
import { chech_health } from '@/utils/check_health'

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
  const token = generateTestToken(formModel.value)
  userStore.setLoginInfo(token, {
    username: formModel.value.username
  })
  ElMessage.success('登录成功！')
  router.push('/')
}

onMounted(chech_health)
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.login-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.12;
  pointer-events: none;
  &--pink { width: 400px; height: 400px; background: var(--accent-pink); top: -100px; left: -100px; animation: glowMove 12s ease-in-out infinite; }
  &--purple { width: 350px; height: 350px; background: var(--accent-purple); bottom: -80px; right: -80px; animation: glowMove 12s ease-in-out infinite reverse; }
  &--blue { width: 250px; height: 250px; background: var(--accent-cyan); top: 50%; left: 50%; animation: glowMove 12s ease-in-out infinite 4s; }
}

.login-card {
  position: relative;
  z-index: 1;
  width: 380px;
  max-width: 90vw;
  padding: var(--space-2xl) var(--space-xl);
  text-align: center;
  animation: cardIn 500ms var(--ease-smooth) both;
}

.login-logo {
  font-size: 48px;
  width: 80px;
  height: 80px;
  margin: 0 auto var(--space-md);
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 32px rgba(255, 107, 157, 0.3);
}

.login-title {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 var(--space-xs);
}

.login-sub {
  font-size: 11px;
  color: var(--text-muted);
  margin: 0 0 var(--space-xl);
}

.login-tabs {
  display: flex;
  gap: var(--space-xs);
  margin-bottom: var(--space-lg);
  button {
    flex: 1;
    padding: 8px 0;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: var(--text-muted);
    font-size: 14px;
    font-family: var(--font-body);
    cursor: pointer;
    transition: all var(--dur-fast);

    &.active {
      background: rgba(255, 107, 157, 0.1);
      color: var(--accent-pink);
    }
  }
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.login-submit {
  width: 100%;
  padding: 12px 0;
  margin-top: var(--space-sm);
  font-size: 15px;
}

.login-switch {
  margin-top: var(--space-lg);
  font-size: 13px;
  color: var(--text-muted);
  span { color: var(--accent-cyan); cursor: pointer; }
}

@keyframes glowMove {
  0%, 100% { transform: translate(0, 0); }
  33% { transform: translate(30px, -20px); }
  66% { transform: translate(-20px, 10px); }
}

@keyframes cardIn {
  from { opacity: 0; transform: translateY(20px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
