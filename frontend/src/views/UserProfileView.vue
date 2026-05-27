<template>
  <div class="profile-page">
    <ProfileTabSidebar
      :active-tab="activeTab"
      :tabs="tabs"
      @update:active-tab="activeTab = $event"
    />
    <main class="tab-content">
      <div v-if="activeTab === 'info'" class="content-panel">
        <InfoForm
          :info-form="infoForm"
          :info-rules="infoRules"
          @save="handleSaveInfo"
        />
      </div>
      <div v-else-if="activeTab === 'avatar'" class="content-panel avatar-panel">
        <AvatarForm
          :avatar-url="avatarUrl"
          @upload="handleBeforeAvatarUpload"
          @remove="removeAvatar"
        />
      </div>
      <div v-else-if="activeTab === 'password'" class="content-panel">
        <PasswordForm
          :password-form="passwordForm"
          :password-rules="passwordRules"
          @change="handleChangePassword"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import ProfileTabSidebar from '@/components/profile/ProfileTabSidebar.vue'
import InfoForm from '@/components/profile/InfoForm.vue'
import AvatarForm from '@/components/profile/AvatarForm.vue'
import PasswordForm from '@/components/profile/PasswordForm.vue'

const tabs = [
  { key: 'info', label: '基本资料' },
  { key: 'avatar', label: '更换头像' },
  { key: 'password', label: '设置密码' }
]

const activeTab = ref('info')

const userStore = useAuthStore()
const router = useRouter()

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
  return false
}

function removeAvatar() {
  avatarUrl.value = ''
  ElMessage.info('头像已移除')
}

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
      userStore.clearLoginInfo()
      router.push('/login')
    } else {
      ElMessage.error('请检查输入')
    }
  })
}
</script>

<style lang="scss" scoped>
.profile-page {
  color: var(--c-ink);
  font-family: var(--font-stack);
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 32px;
  align-items: flex-start;
}

.tab-content {
  min-width: 0;
}

.content-panel {
  width: 100%;
  max-width: 640px;
  padding: 32px 32px;
  background: #fff;
  border: 1px solid var(--c-line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-2);
}

@media (max-width: 900px) {
  .profile-page {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

@media (max-width: 680px) {
  .content-panel {
    padding: 24px 20px;
  }
}
</style>
