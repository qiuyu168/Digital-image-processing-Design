<script setup>
import { useAuthStore } from '@/stores/authStore'
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { generateTestToken } from '@/utils/token'
import { chech_health } from '@/utils/check_health'

import LoginHero from '@/components/login/LoginHero.vue'
import LoginCard from '@/components/login/LoginCard.vue'

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

const cardRef = ref(null)

const register = async () => {
  await cardRef.value.validate()
  ElMessage.success('注册成功！')
  isRegister.value = false
}

const login = async () => {
  await cardRef.value.validate()
  const token = generateTestToken(formModel.value)
  userStore.setLoginInfo(token, {
    username: formModel.value.username
  })
  ElMessage.success('登录成功！')
  router.push('/')
}

onMounted(chech_health)
</script>

<template>
  <div class="login-page">
    <LoginHero />
    <LoginCard
      ref="cardRef"
      :is-register="isRegister"
      :form-model="formModel"
      :rules="rules"
      @login="login"
      @register="register"
      @toggle-register="isRegister = $event"
    />
  </div>
</template>

<style lang="scss" scoped>
.login-page {
  position: fixed;
  inset: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background:
    radial-gradient(circle at 8% 92%, rgba(217, 119, 6, 0.07), transparent 32%),
    radial-gradient(circle at 92% 8%, rgba(240, 217, 194, 0.22), transparent 34%),
    linear-gradient(180deg, var(--c-cream) 0%, var(--c-cream-2) 100%);
  color: var(--c-ink);
  font-family: var(--font-stack);
  overflow: auto;
}

@media (max-width: 1024px) {
  .login-page {
    grid-template-columns: 1fr;
  }
}
</style>
