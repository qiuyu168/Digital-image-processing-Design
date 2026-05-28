<template>
  <div class="profile-page page-enter">
    <aside class="profile-sidebar glass-card">
      <div class="profile-avatar">
        <div class="avatar-circle">{{ (authStore.userInfo?.username || 'U')[0].toUpperCase() }}</div>
      </div>
      <h2 class="profile-name">{{ authStore.userInfo?.username || '用户' }}</h2>
      <div class="profile-tabs">
        <button :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">基本资料</button>
        <button :class="{ active: activeTab === 'avatar' }" @click="activeTab = 'avatar'">更换头像</button>
        <button :class="{ active: activeTab === 'password' }" @click="activeTab = 'password'">设置密码</button>
      </div>
    </aside>

    <main class="profile-main">
      <div class="glass-card profile-form">
        <!-- 基本资料 -->
        <form v-if="activeTab === 'info'" @submit.prevent="saveInfo">
          <div class="form-field"><label>昵称</label><input v-model="nickname" class="glass-input"></div>
          <div class="form-field"><label>邮箱</label><input v-model="email" type="email" class="glass-input"></div>
          <button type="submit" class="btn-gradient">保存修改</button>
        </form>
        <!-- 更换头像 -->
        <div v-if="activeTab === 'avatar'" class="avatar-upload">
          <div class="avatar-preview-lg">{{ (authStore.userInfo?.username || 'U')[0].toUpperCase() }}</div>
          <input type="file" accept="image/*" @change="onAvatarChange" hidden ref="avatarInput">
          <button class="btn-glass" style="margin-top:12px;" @click="$refs.avatarInput.click()">选择图片</button>
        </div>
        <!-- 设置密码 -->
        <form v-if="activeTab === 'password'" @submit.prevent="savePassword">
          <div class="form-field"><label>旧密码</label><input v-model="oldPassword" type="password" class="glass-input"></div>
          <div class="form-field"><label>新密码</label><input v-model="newPassword" type="password" class="glass-input"></div>
          <div class="form-field"><label>确认密码</label><input v-model="confirmPwd" type="password" class="glass-input"></div>
          <div class="password-strength">
            <div class="strength-bar" :style="{ width: passwordStrength + '%', background: strengthColor }"></div>
          </div>
          <button type="submit" class="btn-gradient">更新密码</button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

// ---------- 三个标签页定义 ----------
const tabs = [
  { key: 'info', label: '基本资料' },
  { key: 'avatar', label: '更换头像' },
  { key: 'password', label: '设置密码' }
]

const activeTab = ref('info')

const userStore = useAuthStore()
const router = useRouter()

// ---------- 基本资料 ----------
const infoFormRef = ref(null)
const infoForm = reactive({
  username: userStore.userInfo?.username || '',
  nickname: userStore.userInfo?.nickname || '',
  email: userStore.userInfo?.email || ''
})
const infoRules = {
  nickname: [
    { max: 20, message: '昵称不能超过20个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
    { required: true, message: '邮箱不能为空' }
  ]
}

function handleSaveInfo() {
  infoFormRef.value?.validate((valid) => {
    if (valid) {
      ElMessage.success('个人信息已更新')
      userStore.setLoginInfo(userStore.token, {
        ...userStore.userInfo,
        username: infoForm.username,
        nickname: infoForm.nickname,
        email: infoForm.email
      })
    } else {
      ElMessage.error('请检查输入')
    }
  })
}

// ---------- 更换头像 ----------
const avatarUrl = ref('')

function handleBeforeAvatarUpload(file) {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    avatarUrl.value = e.target?.result
  }
  reader.readAsDataURL(file)

  ElMessage.success('头像已更新（本地预览）')
  // TODO: 实际上传头像 API
  return false
}

function removeAvatar() {
  avatarUrl.value = ''
  // TODO: 调用删除头像 API
  ElMessage.info('头像已移除')
}

// ---------- 设置密码 ----------
const passwordFormRef = ref(null)
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const checkOldSame = (rule, value, callback) => {
  if (value == passwordForm.value.oldPassword)
    callback(new Error('原密码和新密码不能一致！'))
  else
    callback()
}

const checkNewSame = (rule, value, callback) => {
  if (value != passwordForm.value.newPassword)
    callback(new Error('新密码和确认再次输入的新密码不一致!'))
  else
    callback()
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码长度必须是6-15位的非空字符串',
      trigger: 'blur'
    },
    { validator: checkOldSame, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次确认新密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码长度必须是6-15位的非空字符串',
      trigger: 'blur'
    },
    { validator: checkNewSame, trigger: 'blur' }
  ]
}

function handleChangePassword() {
  passwordFormRef.value?.validate((valid) => {
    if (valid) {
      ElMessage.success('密码已修改')
      // 清空表单
      userStore.clearLoginInfo()
      router.push('/login')
    } else {
      ElMessage.error('请检查输入')
    }
  })
}
</script>

<style lang="scss" scoped>
.profile-page { display: flex; gap: var(--space-md); padding: var(--space-md); max-width: 1000px; margin: 0 auto; min-height: calc(100vh - 64px - 80px); }

.profile-sidebar { width: 220px; padding: var(--space-xl) var(--space-md); text-align: center; display: flex; flex-direction: column; align-items: center; gap: var(--space-md); }

.avatar-circle {
  width: 72px; height: 72px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  border: 3px solid rgba(255,107,157,0.3);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-display);
  font-size: 28px; font-weight: 800; color: #fff;
}

.profile-name { font-family: var(--font-display); font-size: 16px; margin: 0; }

.profile-tabs { display: flex; flex-direction: column; gap: var(--space-xs); width: 100%;
  button { padding: 10px; border: none; border-radius: 8px; background: transparent; color: var(--text-secondary); cursor: pointer; font-size: 13px; transition: all var(--dur-fast); font-family: var(--font-body);
    &:hover { background: rgba(255,255,255,0.04); }
    &.active { background: rgba(255,107,157,0.1); color: var(--accent-pink); }
  }
}

.profile-main { flex: 1; }

.profile-form { padding: var(--space-xl); }

.form-field { margin-bottom: var(--space-md);
  label { display: block; font-size: 12px; color: var(--text-secondary); margin-bottom: var(--space-xs); font-family: var(--font-body); }
}

.avatar-upload { text-align: center; }
.avatar-preview-lg {
  width: 100px; height: 100px; border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-pink), var(--accent-purple));
  border: 3px solid rgba(255,107,157,0.3);
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-display);
  font-size: 36px; font-weight: 800; color: #fff;
  margin: 0 auto var(--space-md);
}

.password-strength { height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; margin: var(--space-sm) 0 var(--space-md); overflow: hidden; }
.strength-bar { height: 100%; border-radius: 2px; transition: width var(--dur-base) var(--ease-smooth); }
</style>